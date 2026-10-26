"""Extract local PPTX text and notes with Python's installed standard library."""
import posixpath
import sys
import zipfile
from pathlib import Path
from xml.etree import ElementTree as ET

source, destination = sys.argv[1:]
ns = {
    "a": "http://schemas.openxmlformats.org/drawingml/2006/main",
    "p": "http://schemas.openxmlformats.org/presentationml/2006/main",
    "r": "http://schemas.openxmlformats.org/officeDocument/2006/relationships",
}

def relationships(archive, part):
    relpart = posixpath.join(posixpath.dirname(part), "_rels", posixpath.basename(part) + ".rels")
    if relpart not in archive.namelist():
        return {}
    return {node.get("Id"): node for node in ET.fromstring(archive.read(relpart))}

def resolve(part, target):
    return posixpath.normpath(posixpath.join(posixpath.dirname(part), target))

def paragraphs(root):
    return ["".join(n.text or "" for n in p.findall(".//a:t", ns))
            for p in root.findall(".//a:p", ns)]

with zipfile.ZipFile(source) as archive:
    output = Path(destination)
    for name in archive.namelist():
        if name.endswith((".xml", ".rels")) and not name.startswith("/") and ".." not in Path(name).parts:
            path = output / name
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(archive.read(name))
    presentation = ET.fromstring(archive.read("ppt/presentation.xml"))
    rels = relationships(archive, "ppt/presentation.xml")
    slides = presentation.findall("p:sldIdLst/p:sldId", ns)
    print(f"SLIDE COUNT: {len(slides)}")
    for index, slide in enumerate(slides, 1):
        part = resolve("ppt/presentation.xml", rels[slide.get("{" + ns["r"] + "}id")].get("Target"))
        root = ET.fromstring(archive.read(part))
        print(f"\nSLIDE {index} ({part}) hidden={root.get('show') == '0'}")
        print("\n".join(text for text in paragraphs(root) if text.strip()) or "[No text]")
        print(f"[Embedded picture elements: {len(root.findall('.//p:pic', ns))}]")
        for rel in relationships(archive, part).values():
            if rel.get("Type", "").endswith("/notesSlide"):
                note_part = resolve(part, rel.get("Target"))
                notes = ET.fromstring(archive.read(note_part))
                substantive = []
                for shape in notes.findall(".//p:sp", ns):
                    placeholder = shape.find("p:nvSpPr/p:nvPr/p:ph", ns)
                    if placeholder is not None and placeholder.get("type") in {"sldNum", "hdr", "ftr", "dt"}:
                        continue
                    substantive.extend(text for text in paragraphs(shape) if text.strip())
                print(f"NOTES ({note_part}):")
                print("\n".join(substantive) or "[No substantive text]")
