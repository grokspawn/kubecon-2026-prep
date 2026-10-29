#!/usr/bin/env python3
"""Validate completed review/final decks; defaults to both, without rebuilding.

Only validation-report.json in each selected variant and the project root's
variant-comparison.json are written. Missing/in-progress outputs fail explicitly.
Uses the local import-sdk.py helpers, Python's standard library and local Poppler.
"""

import argparse
import hashlib
import importlib.util
import json
import math
from pathlib import Path
import re
import shutil
import subprocess
import sys
import xml.etree.ElementTree as ET
import zipfile

sys.dont_write_bytecode = True
ROOT = Path(__file__).resolve().parent
TITLE = "The Next Era of Kubernetes Operator Lifecycle Management"
SLIDES = 27
BASE_SLIDES = 17
SDK_FIRST = 16
SDK_LAST = 25
TOTAL_SECONDS = 1920
MARK = re.compile(r"\bdry[\s\-–—]*run\b|\balignment[\s\-–—]+draft\b", re.I)
OWNERSHIP = re.compile(
    r"\bAttila\b|\bOLM\s*[ABC](?:\b|/)|\bspeakers?\b|\bhand[ -]?offs?\b|"
    r"\bthree OLM\b|\b(?:Rashmi|Joe|Jordan)\b", re.I)
CONTRAST = re.compile(
    r",\s*not\b|(?:—|--)\s*(?:not|they)\b|"
    r"\b(?:do|does)\s+not\b[^.\n]{0,100}\bthey\b", re.I)
MATURITY = re.compile(
    r"\b(?:alpha|beta|prototype|experimental|tech(?:nical)?[ -]preview)\b|"
    r"disabled by default|default[ -]off", re.I)
NS = {"a": "http://schemas.openxmlformats.org/drawingml/2006/main",
      "p": "http://schemas.openxmlformats.org/presentationml/2006/main"}


def normalized(value):
    return " ".join(str(value).split())


def clock(seconds):
    return f"{seconds // 60:02d}:{seconds % 60:02d}"


def snapshot_text(slide):
    """Return snapshot copy as individually checkable lines, without furniture."""
    return [normalized(line.lstrip("• ")) for block in slide["text"]
            for line in block.splitlines() if line.strip()
            and not re.fullmatch(r"\s*\d+\s*/\s*27\s*", line)]


def embedded_images(parts, slide_part, sdk):
    """Return the bytes of images actually referenced by this displayed slide."""
    slide = ET.fromstring(parts[slide_part])
    rels = {r.get("Id"): r for r in sdk.relationships(parts, slide_part)}
    images = []
    for blip in slide.findall(".//p:pic//a:blip", NS):
        rel = rels.get(blip.get("{" + sdk.R + "}embed"))
        if rel is not None and rel.get("TargetMode") != "External":
            images.append(parts[sdk.resolve(slide_part, rel.get("Target"))])
    return images


def sha(data):
    return hashlib.sha256(data).hexdigest()


def load_json(path):
    return json.loads(path.read_text(encoding="utf-8"))


def tool(name):
    found = shutil.which(name)
    if found:
        return found
    for directory in ("/opt/homebrew/bin", "/usr/local/bin", "/usr/bin"):
        candidate = Path(directory) / name
        if candidate.is_file():
            return str(candidate)
    return None


def text_of(node):
    return normalized(" ".join(t.text or "" for t in node.findall(".//a:t", NS)))


def paragraphs(node):
    return [normalized("".join(t.text or "" for t in p.findall(".//a:t", NS)))
            for p in node.findall(".//a:p", NS)]


def public_content(slide, section):
    """Ignore only presentation furniture and the optionally hidden overline."""
    result = []
    for value in paragraphs(slide):
        if not value or value == normalized(section):
            continue
        if re.fullmatch(r"\d+\s*/\s*27(?:\s*\|\s*KUBECON NA 2026\s*\|\s*DRY[ -]?RUN)?",
                        value, re.I):
            continue
        result.append(value)
    return normalized(" ".join(result))


def objects(slide):
    """Native text/picture/shape bounds, including nested group transforms."""
    found = []

    def visit(parent, sx=1.0, sy=1.0, tx=0.0, ty=0.0):
        for node in parent:
            kind = node.tag.rsplit("}", 1)[-1]
            if kind == "grpSp":
                xf = node.find("p:grpSpPr/a:xfrm", NS)
                if xf is None:
                    visit(node, sx, sy, tx, ty)
                    continue
                off, ext = xf.find("a:off", NS), xf.find("a:ext", NS)
                ch_off, ch_ext = xf.find("a:chOff", NS), xf.find("a:chExt", NS)
                if any(n is None for n in (off, ext, ch_off, ch_ext)):
                    raise ValueError("Incomplete native group transform")
                gx = int(ext.get("cx")) / int(ch_ext.get("cx"))
                gy = int(ext.get("cy")) / int(ch_ext.get("cy"))
                if int(xf.get("rot", "0")) or xf.get("flipH") == "1" or xf.get("flipV") == "1":
                    raise ValueError("Rotated/flipped generated group requires geometry support")
                visit(node, sx * gx, sy * gy,
                      tx + sx * (int(off.get("x")) - gx * int(ch_off.get("x"))),
                      ty + sy * (int(off.get("y")) - gy * int(ch_off.get("y"))))
            elif kind in ("sp", "pic", "graphicFrame"):
                text = text_of(node)
                xf = node.find("p:spPr/a:xfrm", NS)
                if xf is None:
                    xf = node.find("p:xfrm", NS)
                if xf is None:
                    if text:
                        raise ValueError("Generated text has no explicit geometry: " + text[:80])
                    continue
                off, ext = xf.find("a:off", NS), xf.find("a:ext", NS)
                if off is None or ext is None:
                    raise ValueError("Incomplete generated object transform")
                x, y = tx + sx * int(off.get("x")), ty + sy * int(off.get("y"))
                w, h = sx * int(ext.get("cx")), sy * int(ext.get("cy"))
                angle = math.radians(int(xf.get("rot", "0")) / 60000)
                rw = abs(w * math.cos(angle)) + abs(h * math.sin(angle))
                rh = abs(w * math.sin(angle)) + abs(h * math.cos(angle))
                found.append({"node": node, "text": text, "kind": kind,
                              "rect": (x + (w - rw) / 2, y + (h - rh) / 2, rw, rh)})

    tree = slide.find("p:cSld/p:spTree", NS)
    if tree is not None:
        visit(tree)
    return found


def intersection(a, b, tolerance=12700):
    x, y, w, h = a
    u, v, cw, ch = b
    return (min(x + w, u + cw) - max(x, u) > tolerance
            and min(y + h, v + ch) - max(y, v) > tolerance)


def validate(variant, directory, data, source_path, source, sdk, profile, snapshot, show):
    result = {"variant": variant, "status": "failed", "errors": [],
              "offCanvasObjects": [], "overlappingTextBoxes": [],
              "brandingObstructions": [], "sdkUnchanged": False}

    def check(condition, message):
        if not condition:
            result["errors"].append(message)
        return bool(condition)

    logical = []
    try:
        stem = "kubecon-2026-final" if variant == "final" else "kubecon-2026-dry-run"
        required = [directory / (stem + ext) for ext in (".pptx", ".pdf")]
        required += [directory / name for name in
                     ("deck-manifest.json", "import-report.json", "speaker-notes.md")]
        missing = [str(p) for p in required if not p.is_file()]
        if missing:
            raise ValueError("Outputs not ready; missing: " + ", ".join(missing))
        parts = sdk.package(required[0])
        manifest = load_json(directory / "deck-manifest.json")
        imported = load_json(directory / "import-report.json")
        notes_document = normalized((directory / "speaker-notes.md").read_text())
        order = sdk.displayed(parts)
        check(len(order) == len(manifest) == SLIDES, "Expected 27 displayed slides and manifest records")
        check(sdk.canvas(parts) == sdk.CANVAS, "Unexpected slide canvas")
        check(sum(i["duration"] for i in manifest) == TOTAL_SECONDS, "Manifest duration must total 1920 seconds")
        check(imported.get("verification", {}).get("import_verified"), "SDK import report is not verified")
        check(imported["source_sha256"] == sha(source_path.read_bytes()), "SDK source hash changed")
        for name, content in parts.items():
            if name.endswith((".xml", ".rels")):
                ET.fromstring(content)
        sdk.validate_relationships(parts)
        core = ET.fromstring(parts["docProps/core.xml"])
        check(core.findtext("{http://purl.org/dc/elements/1.1/}title") == TITLE,
              "Core metadata title differs from confirmed title")
        if "docProps/app.xml" in parts:
            app = ET.fromstring(parts["docProps/app.xml"])
            slides_metadata = next((node.text for node in app if node.tag.endswith("}Slides")), None)
            check(slides_metadata == str(SLIDES), "Presentation slide-count metadata must be 27")
        # Independently compare the complete imported source resources, not report flags.
        changed_notes = {sdk.notes_for(source, f"ppt/slides/slide{n}.xml") for n in range(3, 13)}
        protected = {n: b for n, b in source.items()
                     if n != "[Content_Types].xml" and n not in changed_notes}
        for name, content in protected.items():
            check(parts.get("sdk/" + name) == content, "Source resource bytes changed: " + name)
        result["sdkSlideXmlUnchanged"] = all(
            parts.get(f"sdk/ppt/slides/slide{n}.xml") == source[f"ppt/slides/slide{n}.xml"]
            for n in range(3, 13))
        result["sdkResourcesUnchanged"] = all(parts.get("sdk/" + n) == b for n, b in protected.items())
        result["sdkSourceFileUnchanged"] = imported["source_sha256"] == sha(source_path.read_bytes())
        media = [n for n in source if n.startswith("ppt/media/")]
        check(len(media) == 11, "Expected all 11 source media resources")
        check({e["source_part"] for e in imported["media"]} == set(media), "Import media inventory differs")
        check([e["source_slide"] for e in imported["source_mapping"]] == list(range(3, 13)),
              "Import SDK mapping differs from source 3–12")
        elapsed, generated, sdk_count = 0, 0, 0
        for number, slide_part in enumerate(order, 1):
            item = manifest[number - 1]
            slide = ET.fromstring(parts[slide_part])
            visible = text_of(slide)
            notes_part = sdk.notes_for(parts, slide_part)
            notes = normalized(" ".join(sdk.text(parts[notes_part])))
            reference = show["records"][number - 1]
            reference_slide = snapshot["slides"][number - 1]
            check(bool(notes), f"Slide {number}: missing notes")
            check(item["number"] == number and item["start"] == elapsed,
                  f"Slide {number}: manifest position/start mismatch")
            check(reference["number"] == number and reference_slide["number"] == number,
                  f"Slide {number}: reference position mismatch")
            check(item["title"] == reference["title"] and clock(item["start"]) == reference["start"]
                  and clock(item["duration"]) == reference["duration"],
                  f"Slide {number}: title/start/duration differs from run-of-show")
            elapsed += item["duration"]
            check(normalized(item["title"]) in notes_document,
                  f"Slide {number}: title absent from speaker-notes.md")
            # Authored SDK material is exempt from style/geometry, never review-mark checks.
            if variant == "final":
                check(not MARK.search(visible), f"Slide {number}: final contains a review mark")
                for rel in sdk.relationships(parts, slide_part):
                    if rel.get("Type") == sdk.R + "/slideLayout":
                        layout = sdk.resolve(slide_part, rel.get("Target"))
                        check(not MARK.search(text_of(ET.fromstring(parts[layout]))),
                              f"Slide {number}: inherited layout contains a review mark")
                        for master_rel in sdk.relationships(parts, layout):
                            if master_rel.get("Type") == sdk.R + "/slideMaster":
                                master = sdk.resolve(layout, master_rel.get("Target"))
                                check(not MARK.search(text_of(ET.fromstring(parts[master]))),
                                      f"Slide {number}: inherited master contains a review mark")
            if SDK_FIRST <= number <= SDK_LAST:
                sdk_count += 1
                source_number = number - SDK_FIRST + 3
                original = f"ppt/slides/slide{source_number}.xml"
                check(item["kind"] == "authored-sdk" and item["sourceSlide"] == source_number,
                      f"Slide {number}: SDK source assignment mismatch")
                check(parts[slide_part] == source[original], f"Slide {number}: SDK XML bytes changed")
                check(sdk.text(parts[slide_part]) == sdk.text(source[original]),
                      f"Slide {number}: SDK visible text changed")
                entry = imported["source_mapping"][number - SDK_FIRST]
                check(entry.get("output_slide") == number and entry["imported_part"] == slide_part,
                      f"Slide {number}: import report mapping mismatch")
                check(entry.get("speaker") == "Attila" and entry.get("duration_seconds") == 60
                      and entry.get("start") == reference["start"]
                      and entry.get("end") == clock(item["start"] + item["duration"]),
                      f"Slide {number}: SDK import report timing/assignment mismatch")
                expected_notes = sdk.append_notes(source[sdk.notes_for(source, original)], dict(entry))
                check(sdk.text(parts[notes_part]) == sdk.text(expected_notes),
                      f"Slide {number}: authored notes/assignment changed")
                check(item["duration"] == 60 and item.get("speaker") == "Attila",
                      f"Slide {number}: SDK timing/speaker mismatch")
                logical.append({"title": normalized(item["title"]), "content": visible,
                                "sdkXmlSha256": sha(parts[slide_part])})
                continue
            generated += 1
            index = number - 1 if number < SDK_FIRST else number - 11
            original = data[index]
            check(item["kind"] == "generated" and item["baseIndex"] == index,
                  f"Slide {number}: generated base assignment mismatch")
            check(item["title"] == original["title"] and item["duration"] == original["duration"],
                  f"Slide {number}: logical title/duration differs from source JSON")
            for value in snapshot_text(reference_slide):
                check(value in visible, f"Slide {number}: snapshot public copy missing: {value}")
            for value in [original["title"], original.get("status", ""), original.get("lead", ""),
                          *original.get("bullets", []), original.get("caption", ""), *original.get("team", [])]:
                check(not value or normalized(value) in visible,
                      f"Slide {number}: missing public copy: {value}")
            speaker = original.get("speaker")
            check(speaker == reference["speaker"] and item.get("speaker") == reference["speaker"]
                  and f"SPEAKER: {reference['speaker']}" in notes,
                  f"Slide {number}: missing source speaker assignment (source speaker={speaker!r})")
            check(f"SLIDE {number}: {reference['title']}" in notes,
                  f"Slide {number}: notes slide number/title mismatch")
            check(normalized(original["notes"]) in notes, f"Slide {number}: source notes not preserved")
            talk_track = reference["notes"].partition("TALK TRACK / SOURCES / CAVEATS:")[2].strip()
            check(bool(talk_track) and normalized(talk_track) in notes,
                  f"Slide {number}: run-of-show talk track/caveats not preserved")
            check(f"DURATION: {item['duration'] // 60:02d}:{item['duration'] % 60:02d}" in notes,
                  f"Slide {number}: notes duration differs")
            check(f"START: {item['start'] // 60:02d}:{item['start'] % 60:02d}" in notes,
                  f"Slide {number}: notes start differs")
            check(not CONTRAST.search(visible) and not CONTRAST.search(original["notes"]),
                  f"Slide {number}: generated contrast-copy guard failed")
            guarded = visible
            if original.get("team"):
                for name in ("Rashmi", "Joe", "Jordan"):
                    guarded = re.sub(r"\b" + name + r"\b", "", guarded)
            check(not OWNERSHIP.search(guarded), f"Slide {number}: visible ownership/assignment")
            allowed_maturity = {m.group().lower() for value in snapshot_text(reference_slide)
                                for m in MATURITY.finditer(value)}
            check(all(m.group().lower() in allowed_maturity for m in MATURITY.finditer(visible)),
                  f"Slide {number}: unreferenced technical maturity label")
            native = objects(slide)
            text_boxes = [o for o in native if o["text"]]
            for first_index, obj in enumerate(text_boxes):
                x, y, w, h = obj["rect"]
                if w <= 0 or h <= 0 or x < -1000 or y < -1000 or x + w > sdk.CANVAS[0] + 1000 or y + h > sdk.CANVAS[1] + 1000:
                    result["offCanvasObjects"].append({"slide": number, "text": obj["text"], "rect": obj["rect"]})
                for second in text_boxes[first_index + 1:]:
                    if intersection(obj["rect"], second["rect"]):
                        result["overlappingTextBoxes"].append(
                            {"slide": number, "texts": [obj["text"], second["text"]]})
            if number == 1:
                check(not re.search(r"\bprogress\b", visible, re.I), "Cover contains visible 'progress'")
                asset_dir = ROOT / "theme" / "assets" if variant == "final" else ROOT / "assets"
                asset = asset_dir / original["image"]
                check(asset.is_file() and asset.read_bytes() in embedded_images(parts, slide_part, sdk),
                       "Cover must embed the real s01 operator-lifecycle asset")
            if number in (5, 6, 14):
                asset = ROOT.parent / original["imagePath"]
                pictures = embedded_images(parts, slide_part, sdk)
                check(asset.is_file() and asset.read_bytes() in pictures,
                      f"Slide {number}: required {asset.name} is not embedded")
                if number == 14:
                    check("https://github.com/operator-framework/operator-controller/blob/main/CONTRIBUTING.md" in notes,
                          "Slide 14: contribution guide destination missing from notes")
                    check(any(r.get("TargetMode") == "External" and r.get("Target") == original.get("captionUrl")
                              for r in sdk.relationships(parts, slide_part)),
                          "Slide 14: contribution guide hyperlink missing")
            for image in reference_slide.get("images", []):
                description = image.get("description", "")
                if description.lower().endswith(".png"):
                    name = Path(description).name
                    asset_dir = ROOT / "theme" / "assets" if variant == "final" else ROOT / "assets"
                    asset = asset_dir / name
                    check(asset.is_file() and asset.read_bytes() in embedded_images(parts, slide_part, sdk),
                          f"Slide {number}: snapshot illustration {name} is not embedded")
            if number == 2:
                check(original.get("team") == ["Rashmi", "Joe", "Jordan"], "Unexpected team names")
                check(not slide.findall(".//p:pic", NS), "Team slide contains invented portraits/images")
                check(all(any(o["text"] == name for o in text_boxes) for name in original["team"]),
                      "Team names must be native text cards")
            if number == 4:
                past = re.search(r"\bPast:.*?(?=\bCurrent:|$)", visible, re.I)
                check(bool(past) and all(re.search(word, past.group(), re.I) for word in
                      (r"\bCRD\b", "namespace", "assum", "flaw", "SQLite", r"\bFBC\b")),
                      "Timeline Past must retain flawed CRD namespace assumptions, SQLite and FBC")
            check(not re.search(r"assumptions", original["title"], re.I), "Standalone assumptions slide remains")
            if variant == "final":
                layouts = [sdk.resolve(slide_part, r.get("Target")) for r in sdk.relationships(parts, slide_part)
                           if r.get("Type") == sdk.R + "/slideLayout"]
                check(layouts == ["sdk/ppt/slideLayouts/slideLayout5.xml"],
                      f"Slide {number}: final layout must resolve to SDK layout5")
                check(slide.get("showMasterSp", "1") not in ("0", "false"),
                      f"Slide {number}: inherited branding hidden")
                for brand in profile["brandingBoundsPt"]:
                    rect = tuple(brand[k] * 12700 for k in ("x", "y", "width", "height"))
                    for obj in native:
                        if intersection(obj["rect"], rect):
                            result["brandingObstructions"].append(
                                {"slide": number, "text": obj["text"], "kind": obj["kind"]})
            logical.append({"title": normalized(item["title"]),
                            "content": public_content(slide, original.get("section", ""))})
        check(generated == BASE_SLIDES and sdk_count == 10 and elapsed == TOTAL_SECONDS, "Slide kinds/timing mismatch")
        check(manifest[-1]["title"] == "Questions?", "Last slide must be Questions?")
        check(not result["offCanvasObjects"], "Generated native text extends off canvas")
        check(not result["overlappingTextBoxes"], "Generated native text boxes overlap")
        check(not result["brandingObstructions"], "Generated objects obstruct reserved source branding")
        if variant == "final":
            check(not MARK.search(" ".join(core.itertext())), "Final core metadata contains review marks")
            check(profile["sourceSha256"] == sha(source_path.read_bytes()), "Theme source hash mismatch")
            check(profile["sourceLayoutPart"] == "ppt/slideLayouts/slideLayout5.xml",
                  "Source theme profile uses an unexpected layout")
            applied = load_json(directory / "applytheme-report.json")
            check(applied.get("status") == "verified" and len(applied.get("generatedSlides", [])) == BASE_SLIDES,
                  "Theme application report must verify all 17 generated slides")
            check(applied.get("outputSha256") == sha(required[0].read_bytes()), "Stale theme application report")
        pdfinfo = tool("pdfinfo")
        check(bool(pdfinfo), "pdfinfo is required for independent PDF page count")
        if pdfinfo:
            info = subprocess.check_output([pdfinfo, str(required[1])], text=True, timeout=30)
            match = re.search(r"^Pages:\s+(\d+)\s*$", info, re.M)
            check(bool(match) and int(match.group(1)) == SLIDES, "PDF must contain 27 pages")
            result["pdfPages"] = int(match.group(1)) if match else None
        pdftotext = tool("pdftotext")
        result["pdfReviewMarkCheck"] = "not installed" if not pdftotext else "not applicable"
        if variant == "final" and pdftotext:
            pdf_text = subprocess.check_output([pdftotext, "-layout", str(required[1]), "-"],
                                               text=True, timeout=30)
            check(not MARK.search(pdf_text), "Final PDF contains a review mark")
            result["pdfReviewMarkCheck"] = "checked"
        result.update({"slides": len(order), "notes": len(order), "seconds": elapsed,
                       "generatedSlides": generated, "sdkOriginalSlides": list(range(3, 13)),
                       "sdkOutputSlides": list(range(SDK_FIRST, SDK_LAST + 1)), "sourceMediaCount": len(media),
                       "sdkSourceSha256": sha(source_path.read_bytes()),
                       "pptxSha256": sha(required[0].read_bytes()), "logicalSlides": logical})
    except (OSError, ValueError, KeyError, IndexError, TypeError, ZeroDivisionError,
            ET.ParseError, zipfile.BadZipFile, subprocess.SubprocessError) as error:
        result["errors"].append(f"{type(error).__name__}: {error}")
    result["status"] = "passed" if not result["errors"] else "failed"
    result["sdkUnchanged"] = all(result.get(key, False) for key in
                                  ("sdkSlideXmlUnchanged", "sdkResourcesUnchanged", "sdkSourceFileUnchanged"))
    if directory.is_dir():
        (directory / "validation-report.json").write_text(json.dumps(result, indent=2) + "\n")
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--variant", choices=("both", "review", "final"), default="both")
    parser.add_argument("--review-dir", type=Path, default=ROOT)
    parser.add_argument("--final-dir", type=Path, default=ROOT.parent / "final")
    parser.add_argument("--source", type=Path, default=Path("/Users/jordan/Downloads/Copy of KubeCon2026.pptx"))
    args = parser.parse_args()
    spec = importlib.util.spec_from_file_location("sdk_import", ROOT / "import-sdk.py")
    sdk = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(sdk)
    data = load_json(ROOT / "slide-data.json")
    snapshot = load_json(ROOT.parent / "current-deck-after.json")
    show = load_json(ROOT.parent / "current-deck-run-of-show.json")
    if len(data) != BASE_SLIDES or sum(i["duration"] for i in data) != 1320:
        parser.error("Source JSON must contain 17 base slides totalling 1320 seconds")
    if (snapshot.get("slideCount") != SLIDES or len(snapshot.get("slides", [])) != SLIDES
            or show.get("totalSeconds") != TOTAL_SECONDS or len(show.get("records", [])) != SLIDES):
        parser.error("Reference snapshot/run-of-show must contain 27 slides totalling 1920 seconds")
    source = sdk.package(args.source)
    profile = load_json(ROOT / "theme" / "theme.json") if args.variant != "review" else None
    selected = [("review", args.review_dir), ("final", args.final_dir)]
    reports = {name: validate(name, directory, data, args.source, source, sdk, profile, snapshot, show)
               for name, directory in selected if args.variant in ("both", name)}
    comparison = {"status": "not compared", "variants": {n: r["status"] for n, r in reports.items()}}
    if args.variant == "both":
        review, final = reports["review"], reports["final"]
        a, b = review.get("logicalSlides", []), final.get("logicalSlides", [])
        comparison.update({"sameLogicalTitles": len(a) == len(b) == SLIDES and
                           [s["title"] for s in a] == [s["title"] for s in b],
                           "samePublicMainContent": len(a) == len(b) == SLIDES and
                           [s["content"] for s in a] == [s["content"] for s in b],
                           "sdkUnchangedBoth": all(r["sdkUnchanged"] for r in reports.values()),
                           "differences": [i + 1 for i, (x, y) in enumerate(zip(a, b)) if x != y]})
        comparison["status"] = "passed" if all(r["status"] == "passed" for r in reports.values()) and all(
            comparison[k] for k in ("sameLogicalTitles", "samePublicMainContent", "sdkUnchangedBoth")) else "failed"
    if args.review_dir.parent.is_dir():
        (args.review_dir.parent / "variant-comparison.json").write_text(json.dumps(comparison, indent=2) + "\n")
    print(json.dumps({"variants": {n: {"status": r["status"], "errors": r["errors"]}
                                  for n, r in reports.items()}, "comparison": comparison}, indent=2))
    return 0 if all(r["status"] == "passed" for r in reports.values()) and comparison["status"] != "failed" else 1


if __name__ == "__main__":
    try:
        sys.exit(main())
    except (OSError, ValueError, KeyError, ET.ParseError, zipfile.BadZipFile) as error:
        print("validate-variants: " + str(error), file=sys.stderr)
        sys.exit(1)
