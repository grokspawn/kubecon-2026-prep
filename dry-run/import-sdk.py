#!/usr/bin/env python3
"""Import SDK slides 3–12 without rewriting their XML or media (stdlib only).

--self-check inspects only the source and writes an explicitly pending import
report. Normal operation verifies the written package before reporting success.
Absolute internal relationship targets, Strict OOXML, signatures, and shared
presentation-level table styles/embedded fonts are rejected rather than silently
changing the author's appearance. Relative package relationships stay unchanged.
"""

import argparse
import copy
import hashlib
import io
import json
import posixpath
import re
import sys
import zipfile
from pathlib import Path
from urllib.parse import unquote, urlsplit
import xml.etree.ElementTree as ET


P = "http://schemas.openxmlformats.org/presentationml/2006/main"
A = "http://schemas.openxmlformats.org/drawingml/2006/main"
R = "http://schemas.openxmlformats.org/officeDocument/2006/relationships"
REL = "http://schemas.openxmlformats.org/package/2006/relationships"
CT = "http://schemas.openxmlformats.org/package/2006/content-types"
PRES = "ppt/presentation.xml"
PRES_RELS = "ppt/_rels/presentation.xml.rels"
PREFIX = "sdk/"
CANVAS = (9144000, 5143500)
NUMBERS = tuple(range(3, 13))
BASE_SLIDES = 17
INSERT_AFTER = 15
TOTAL_SLIDES = BASE_SLIDES + len(NUMBERS)


def require(condition, message):
    if not condition:
        raise ValueError(message)


def digest(data):
    return hashlib.sha256(data).hexdigest()


def package(path):
    with zipfile.ZipFile(path) as archive:
        names = [i.filename for i in archive.infolist() if not i.is_dir()]
        require(len(names) == len(set(names)), "Duplicate ZIP members")
        require(all(not n.startswith("/") and ".." not in n.split("/")
                    for n in names), "Unsafe OPC part name")
        require(archive.testzip() is None, "ZIP CRC validation failed")
        return {n: archive.read(n) for n in names}


def xml(data):
    return ET.fromstring(data)


def serialize(root, original):
    """Retain namespace declarations needed by mc:Ignorable and QName values."""
    namespaces = dict(event for _, event in ET.iterparse(
        io.BytesIO(original), events=("start-ns",)))
    for prefix, uri in namespaces.items():
        if not re.fullmatch(r"ns\d+", prefix):
            ET.register_namespace(prefix, uri)
    data = ET.tostring(root, encoding="utf-8", xml_declaration=True)
    match = re.search(rb"<[^!?][^>]*", data)
    require(match is not None, "Missing XML root")
    start = match.group()
    extra = b""
    for prefix, uri in namespaces.items():
        attr = "xmlns" + (":" + prefix if prefix else "")
        if not re.search(rb"\s" + re.escape(attr.encode()) + rb"=", start):
            escaped = uri.replace("&", "&amp;").replace('"', "&quot;")
            extra += (' ' + attr + '="' + escaped + '"').encode()
    return data[:match.end()] + extra + data[match.end():]


def rels_name(part):
    parent, name = posixpath.split(part)
    return posixpath.join(parent, "_rels", name + ".rels")


def resolve(owner, target):
    parsed = urlsplit(target)
    require(not parsed.scheme and not parsed.netloc,
            "Internal relationship has a URI scheme: " + target)
    require(not parsed.path.startswith("/"),
            "Unsupported absolute OPC relationship target: " + target)
    path = unquote(parsed.path)
    require("\\" not in path, "Unsupported backslash relationship target")
    result = posixpath.normpath(posixpath.join(posixpath.dirname(owner), path))
    require(result != ".." and not result.startswith("../"),
            "Relationship escapes package: " + target)
    return result


def relationships(parts, part):
    name = rels_name(part)
    return list(xml(parts[name])) if name in parts else []


def displayed(parts):
    root = xml(parts[PRES])
    require(root.tag == "{" + P + "}presentation", "Strict OOXML is unsupported")
    ids = root.find("{" + P + "}sldIdLst")
    require(ids is not None, "Missing presentation slide list")
    rs = {r.get("Id"): r for r in relationships(parts, PRES)}
    slides = []
    for node in ids:
        rel = rs.get(node.get("{" + R + "}id"))
        require(rel is not None and rel.get("Type") == R + "/slide",
                "Unresolved presentation slide relationship")
        slides.append(resolve(PRES, rel.get("Target")))
    return slides


def canvas(parts):
    size = xml(parts[PRES]).find("{" + P + "}sldSz")
    require(size is not None, "Missing slide dimensions")
    return int(size.get("cx")), int(size.get("cy"))


def text(data):
    return [node.text or "" for node in xml(data).iter("{" + A + "}t")]


def validate_relationships(parts):
    for name, data in parts.items():
        if not name.endswith(".rels"):
            continue
        if name == "_rels/.rels":
            owner = ""
        else:
            parent, basename = posixpath.split(name)
            require(posixpath.basename(parent) == "_rels", "Invalid relationship part")
            owner = posixpath.join(posixpath.dirname(parent), basename[:-5])
        seen = set()
        for rel in xml(data):
            require(rel.get("Id") not in seen, "Duplicate relationship ID: " + name)
            seen.add(rel.get("Id"))
            if rel.get("TargetMode") == "External":
                continue
            target = resolve(owner, rel.get("Target"))
            require(target in parts, "Dangling relationship: " + name + " -> " + target)


def notes_for(parts, slide):
    found = [resolve(slide, r.get("Target")) for r in relationships(parts, slide)
             if r.get("Type") == R + "/notesSlide"]
    require(len(found) == 1, "Expected one notes part for " + slide)
    return found[0]


def inspect_source(parts, path, start_seconds):
    slides = displayed(parts)
    require(len(slides) == 13, "SDK source must have 13 displayed slides")
    require(canvas(parts) == CANVAS, "SDK canvas must be 9144000 x 5143500")
    require(not any(n.startswith("_xmlsignatures/") for n in parts),
            "Signed OPC packages are unsupported")
    validate_relationships(parts)
    # Global table-style/font collections cannot be merged without changing
    # presentation semantics. Ordinary theme font references need no rewriting.
    pres = xml(parts[PRES])
    require(pres.find("{" + P + "}embeddedFontLst") is None,
            "Presentation-level embedded fonts are unsupported")
    for rel in relationships(parts, PRES):
        if rel.get("Type") == R + "/tableStyles":
            styles = xml(parts[resolve(PRES, rel.get("Target"))])
            require(not list(styles), "Nonempty presentation-level table styles unsupported")
    mapping = []
    for index, number in enumerate(NUMBERS):
        slide = slides[number - 1]
        require(slide == f"ppt/slides/slide{number}.xml",
                "Source display order differs from requested slide filenames")
        notes = notes_for(parts, slide)
        require(notes in parts, "Missing source notes: " + notes)
        start = start_seconds + index * 60
        end = start + 60
        mapping.append({
            "source_slide": number, "source_part": slide,
            "imported_part": PREFIX + slide, "speaker": "Attila",
            "section": "SDK", "duration_seconds": 60,
            "start": f"{start // 60:02d}:{start % 60:02d}",
            "end": f"{end // 60:02d}:{end % 60:02d}",
            "notes_part": PREFIX + notes,
            "source_slide_xml_sha256": digest(parts[slide]),
            "source_visible_text": text(parts[slide]),
            "source_visible_text_sha256": digest(json.dumps(
                text(parts[slide]), ensure_ascii=False).encode()),
        })
    return {
        "status": "source_checked_pending_base", "source": str(path),
        "source_sha256": digest(path.read_bytes()),
        "source_displayed_slides": len(slides), "canvas": list(CANVAS),
        "expected_displayed_slides": TOTAL_SLIDES, "displayed_slides": None,
        "source_mapping": mapping,
        "media": [{"source_part": n, "imported_part": PREFIX + n,
                   "source_sha256": digest(data)} for n, data in sorted(parts.items())
                  if n.startswith("ppt/media/")],
        "unsupported_opc_issues": [],
        "verification": {"source_package_relationships_valid": True,
                         "import_verified": False},
    }


def append_notes(data, entry):
    root = xml(data)
    body = None
    for shape in root.iter("{" + P + "}sp"):
        ph = shape.find("./{" + P + "}nvSpPr/{" + P + "}nvPr/{" + P + "}ph")
        if ph is not None and ph.get("type") == "body":
            body = shape.find("{" + P + "}txBody")
            break
    require(body is not None, "Source notes have no body placeholder")
    assignment = (f"[SDK import: speaker=Attila; section=SDK; "
                  f"sourceSlide{entry['source_slide']}; duration=60 seconds; "
                  f"start={entry['start']}; end={entry['end']}]")
    paragraph = ET.SubElement(body, "{" + A + "}p")
    run = ET.SubElement(paragraph, "{" + A + "}r")
    ET.SubElement(run, "{" + A + "}t").text = assignment
    result = serialize(root, data)
    require(text(result) == text(data) + [assignment], "Existing notes text changed")
    entry["notes_assignment"] = assignment
    entry["existing_notes_preserved"] = True
    return result


def merge_types(base, source):
    root = xml(base)
    defaults = {n.get("Extension").lower(): n.get("ContentType")
                for n in root if n.tag == "{" + CT + "}Default"}
    for node in xml(source):
        node = copy.deepcopy(node)
        if node.tag == "{" + CT + "}Default":
            ext = node.get("Extension").lower()
            require(ext not in defaults or defaults[ext] == node.get("ContentType"),
                    "Content-type Default conflict: " + ext)
            if ext in defaults:
                continue
            defaults[ext] = node.get("ContentType")
        elif node.tag == "{" + CT + "}Override":
            node.set("PartName", "/" + PREFIX + node.get("PartName").lstrip("/"))
        else:
            raise ValueError("Unsupported content-type element")
        root.append(node)
    return serialize(root, base)


def merge(base, source, report, insert_after):
    slides = displayed(base)
    require(len(slides) == BASE_SLIDES, f"Base must have {BASE_SLIDES} displayed slides")
    require(insert_after == INSERT_AFTER, f"This SDK import requires --insert-after {INSERT_AFTER}")
    require(canvas(base) == CANVAS, "Base/source canvas mismatch")
    require(not any(n.startswith(PREFIX) for n in base), "Base already contains sdk/ parts")
    validate_relationships(base)
    output = dict(base)
    for name, data in source.items():
        if name != "[Content_Types].xml":
            output[PREFIX + name] = data
    for entry in report["source_mapping"]:
        source_notes = entry["notes_part"][len(PREFIX):]
        output[entry["notes_part"]] = append_notes(source[source_notes], entry)
    output["[Content_Types].xml"] = merge_types(
        base["[Content_Types].xml"], source["[Content_Types].xml"])
    pres = xml(base[PRES])
    rels = xml(base[PRES_RELS])
    used = {r.get("Id") for r in rels}

    def add_rel(kind, target):
        count = 1
        while f"rIdSDK{count}" in used:
            count += 1
        rid = f"rIdSDK{count}"
        used.add(rid)
        ET.SubElement(rels, "{" + REL + "}Relationship", {
            "Id": rid, "Type": R + "/" + kind, "Target": "../" + PREFIX + target})
        return rid

    masters = pres.find("{" + P + "}sldMasterIdLst")
    if masters is None:
        masters = ET.Element("{" + P + "}sldMasterIdLst")
        pres.insert(0, masters)
    master_id = max([2147483647] + [int(n.get("id")) for n in masters]) + 1
    report["registered_sdk_masters"] = []
    for rel in relationships(source, PRES):
        if rel.get("Type") != R + "/slideMaster":
            continue
        target = resolve(PRES, rel.get("Target"))
        require(master_id <= 4294967295, "Slide master ID overflow")
        rid = add_rel("slideMaster", target)
        ET.SubElement(masters, "{" + P + "}sldMasterId", {
            "id": str(master_id), "{" + R + "}id": rid})
        master_id += 1
        report["registered_sdk_masters"].append(PREFIX + target)
    ids = pres.find("{" + P + "}sldIdLst")
    slide_id = max([255] + [int(n.get("id")) for n in ids]) + 1
    for index, entry in enumerate(report["source_mapping"]):
        require(slide_id < 2147483648, "Slide ID overflow")
        rid = add_rel("slide", entry["source_part"])
        ids.insert(insert_after + index, ET.Element("{" + P + "}sldId", {
            "id": str(slide_id), "{" + R + "}id": rid}))
        slide_id += 1
        entry["output_slide"] = insert_after + index + 1
    output[PRES] = serialize(pres, base[PRES])
    output[PRES_RELS] = serialize(rels, base[PRES_RELS])
    if "docProps/app.xml" in output:
        app = xml(output["docProps/app.xml"])
        for node in app:
            if node.tag.endswith("}Slides"):
                node.text = str(TOTAL_SLIDES)
        output["docProps/app.xml"] = serialize(app, base["docProps/app.xml"])
    return output


def verify(output, base, source, report, insert_after):
    order = displayed(output)
    expected = displayed(base)[:insert_after] + [e["imported_part"] for e in report["source_mapping"]]
    expected += displayed(base)[insert_after:]
    require(order == expected and len(order) == TOTAL_SLIDES, "Displayed slide order/count mismatch")
    validate_relationships(output)
    changed_notes = {e["notes_part"] for e in report["source_mapping"]}
    for name, data in source.items():
        if name == "[Content_Types].xml" or PREFIX + name in changed_notes:
            continue
        require(output[PREFIX + name] == data, "Copied source bytes changed: " + name)
    for entry in report["source_mapping"]:
        data = output[entry["imported_part"]]
        entry["output_slide_xml_sha256"] = digest(data)
        entry["slide_xml_byte_identical"] = data == source[entry["source_part"]]
        entry["visible_text_identical"] = text(data) == entry["source_visible_text"]
        require(entry["slide_xml_byte_identical"] and entry["visible_text_identical"],
                "Source slide preservation failed")
    for entry in report["media"]:
        data = output[entry["imported_part"]]
        entry["output_sha256"] = digest(data)
        entry["byte_identical"] = data == source[entry["source_part"]]
        require(entry["byte_identical"], "Media preservation failed")
    report["displayed_slides"] = len(order)
    report["verification"].update({
        "import_verified": True, "displayed_order_correct": True,
        "slide_xml_byte_identical": True, "source_visible_text_identical": True,
        "media_byte_identical": True, "copied_non_notes_parts_byte_identical": True,
        "package_relationships_valid": True, "source_file_unchanged": True,
    })


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--base", type=Path, help="17-slide base (required for import)")
    parser.add_argument("--source", type=Path, required=True)
    parser.add_argument("--out", type=Path, help="Merged 27-slide PPTX (required for import)")
    parser.add_argument("--insert-after", type=int, default=INSERT_AFTER)
    parser.add_argument("--start-seconds", type=int, help="SDK segment start in seconds (required for import)")
    parser.add_argument("--self-check", action="store_true", help="Check source without a base")
    parser.add_argument("--report", type=Path,
                        default=Path(__file__).resolve().with_name("import-report.json"))
    args = parser.parse_args()
    if not args.self_check and (args.base is None or args.out is None):
        parser.error("--base and --out are required unless --self-check is used")
    if not args.self_check and args.start_seconds is None:
        parser.error("--start-seconds is required for import")
    if args.start_seconds is not None and args.start_seconds < 0:
        parser.error("--start-seconds must be nonnegative")
    protected = {args.source.resolve(), Path(__file__).resolve()}
    if args.base:
        protected.add(args.base.resolve())
    require(args.report.resolve() not in protected, "Report would overwrite an input/helper")
    require(args.report.parent.is_dir(), "Report parent directory does not exist")
    source = package(args.source)
    report = inspect_source(source, args.source, args.start_seconds or 0)
    for index, entry in enumerate(report["source_mapping"]):
        entry["planned_output_slide"] = args.insert_after + index + 1
        # Exercise notes editing in memory during the source-only check too.
        append_notes(source[entry["notes_part"][len(PREFIX):]], entry)
    if args.self_check:
        # Exercise the complete merge/ZIP round trip without a real base or
        # creating another file. This fixture is explicitly synthetic.
        fixture = dict(source)
        root = xml(source[PRES])
        ids = root.find("{" + P + "}sldIdLst")
        next_id = max(int(node.get("id")) for node in ids) + 1
        for index in range(BASE_SLIDES - len(ids)):
            node = copy.deepcopy(ids[index])
            node.set("id", str(next_id + index))
            ids.append(node)
        fixture[PRES] = serialize(root, source[PRES])
        trial_report = copy.deepcopy(report)
        trial = merge(fixture, source, trial_report, args.insert_after)
        buffer = io.BytesIO()
        with zipfile.ZipFile(buffer, "w", compression=zipfile.ZIP_DEFLATED) as archive:
            for name, data in trial.items():
                archive.writestr(name, data)
        buffer.seek(0)
        with zipfile.ZipFile(buffer) as archive:
            verify({n: archive.read(n) for n in archive.namelist()},
                   fixture, source, trial_report, args.insert_after)
        report["synthetic_merge_check"] = {
            "passed": True, "displayed_slides": TOTAL_SLIDES,
            "slide_xml_byte_identical": True, "media_byte_identical": True,
            "package_relationships_valid": True,
            "registered_sdk_masters": trial_report["registered_sdk_masters"],
            "real_base_used": False,
        }
    if not args.self_check:
        require(args.out.resolve() not in protected and args.out.resolve() != args.report.resolve(),
                "Output would overwrite an input/helper/report")
        require(args.out.parent.is_dir(), "Output parent directory does not exist")
        base = package(args.base)
        output = merge(base, source, report, args.insert_after)
        verify(output, base, source, report, args.insert_after)
        with zipfile.ZipFile(args.out, "w", compression=zipfile.ZIP_DEFLATED) as archive:
            for name, data in output.items():
                archive.writestr(name, data)
        verify(package(args.out), base, source, report, args.insert_after)
        require(digest(args.source.read_bytes()) == report["source_sha256"],
                "Source file changed during import")
        report.update({"status": "import_verified", "base": str(args.base),
                       "output": str(args.out), "output_sha256": digest(args.out.read_bytes())})
    require(digest(args.source.read_bytes()) == report["source_sha256"],
            "Source file changed during checking")
    report["verification"]["source_file_unchanged"] = True
    args.report.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"status": report["status"], "displayed_slides": report["displayed_slides"],
                       "expected_displayed_slides": TOTAL_SLIDES, "report": str(args.report)}))


if __name__ == "__main__":
    try:
        main()
    except (ValueError, OSError, KeyError, ET.ParseError, zipfile.BadZipFile) as error:
        print("import-sdk: " + str(error), file=sys.stderr)
        sys.exit(1)
