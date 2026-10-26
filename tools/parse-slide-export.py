"""Extract ordered slide text/notes from a presentation export on stdin."""
import io
import json
import posixpath
import sys
import xml.etree.ElementTree as ET
import zipfile

NS = {
    "a": "http://schemas.openxmlformats.org/drawingml/2006/main",
    "p": "http://schemas.openxmlformats.org/presentationml/2006/main",
    "r": "http://schemas.openxmlformats.org/officeDocument/2006/relationships",
}

def paragraphs(root):
    return [value for paragraph in root.findall(".//a:p", NS)
            if (value := "".join(node.text or "" for node in paragraph.findall(".//a:t", NS)).strip())]

def relationships(archive, filename):
    path = posixpath.join(posixpath.dirname(filename), "_rels", posixpath.basename(filename) + ".rels")
    if path not in archive.namelist():
        return {}
    return {node.attrib["Id"]: node.attrib for node in ET.fromstring(archive.read(path))}

with zipfile.ZipFile(io.BytesIO(sys.stdin.buffer.read())) as archive:
    presentation = "ppt/presentation.xml"
    root = ET.fromstring(archive.read(presentation))
    refs = relationships(archive, presentation)
    slides = []
    for number, slide_ref in enumerate(root.findall("p:sldIdLst/p:sldId", NS), 1):
        relation = refs[slide_ref.attrib[f"{{{NS['r']}}}id"]]
        filename = posixpath.normpath(posixpath.join("ppt", relation["Target"]))
        slide = ET.fromstring(archive.read(filename))
        notes = []
        for note_ref in relationships(archive, filename).values():
            if note_ref.get("Type", "").endswith("/notesSlide"):
                notes_path = posixpath.normpath(posixpath.join(posixpath.dirname(filename), note_ref["Target"]))
                note_root = ET.fromstring(archive.read(notes_path))
                for shape in note_root.findall(".//p:sp", NS):
                    placeholder = shape.find("p:nvSpPr/p:nvPr/p:ph", NS)
                    if placeholder is not None and placeholder.get("type") in {"sldNum", "hdr", "ftr", "dt"}:
                        continue
                    notes.extend(paragraphs(shape))
        images = []
        for picture in slide.findall(".//p:pic", NS):
            props = picture.find("p:nvPicPr/p:cNvPr", NS)
            images.append({"title": props.get("title", "") if props is not None else "",
                           "description": props.get("descr", "") if props is not None else ""})
        slides.append({"number": number, "objectId": filename, "text": paragraphs(slide),
                       "notes": notes, "images": images, "skipped": slide.get("show") == "0"})
    print(json.dumps({"slideCount": len(slides), "slides": slides}, ensure_ascii=False))
