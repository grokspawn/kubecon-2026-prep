"""Validate displayed slide order, authored SDK preservation and generated copy."""
import hashlib
import importlib.util
import json
import re
import subprocess
import xml.etree.ElementTree as ET
from pathlib import Path

root = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location("sdk_import", root / "import-sdk.py")
sdk = importlib.util.module_from_spec(spec)
spec.loader.exec_module(sdk)
data = json.loads((root / "slide-data.json").read_text())
manifest = json.loads((root / "deck-manifest.json").read_text())
report = json.loads((root / "import-report.json").read_text())
parts = sdk.package(root / "kubecon-2026-dry-run.pptx")
order = sdk.displayed(parts)
source_path = Path("/Users/jordan/Downloads/Copy of KubeCon2026.pptx")
source = sdk.package(source_path)
assert len(order) == len(manifest) == 25
assert sdk.canvas(parts) == (9144000, 5143500)
assert report["verification"]["import_verified"]
assert hashlib.sha256(source_path.read_bytes()).hexdigest() == report["source_sha256"]
assert sum(item["duration"] for item in manifest) == 1800
for name, content in parts.items():
    if name.endswith((".xml", ".rels")):
        ET.fromstring(content)
sdk.validate_relationships(parts)
ns = {"a": sdk.A, "p": sdk.P}
title = "The Next Era of Kubernetes Operator Lifecycle Management"
core = ET.fromstring(parts["docProps/core.xml"])
assert core.find("{http://purl.org/dc/elements/1.1/}title").text == title
ownership = re.compile(r"\bAttila\b|\bOLM\s+[ABC]\b|\bspeaker\b|\bhandoff\b", re.I)
contrast = re.compile(r",\s*not\b|(?:—|--)\s*(?:not|they)\b|\b(?:do|does)\s+not\b[^.\n]{0,100}\bthey\b", re.I)
technical_stage = re.compile(r"\balpha\b|\bprototype\b|disabled by default|default off", re.I)
off_canvas, overlaps = [], []
notes_count, pictures = 0, 0
for number, slide_part in enumerate(order, 1):
    item = manifest[number - 1]
    slide = ET.fromstring(parts[slide_part])
    visible = " ".join(sdk.text(parts[slide_part]))
    note_part = sdk.notes_for(parts, slide_part)
    notes = " ".join(sdk.text(parts[note_part]))
    assert notes.strip()
    notes_count += 1
    pictures += bool(slide.findall(".//p:pic", ns))
    if item["kind"] == "authored-sdk":
        original = f"ppt/slides/slide{item['sourceSlide']}.xml"
        assert parts[slide_part] == source[original]
        assert "speaker=Attila" in notes
        continue
    original = data[item["baseIndex"]]
    assert original["title"] in visible
    assert original["speaker"] in notes and "SPEAKER:" in notes
    assert not ownership.search(visible)
    assert not contrast.search(visible)
    assert not technical_stage.search(visible)
    boxes = []
    for shape in slide.findall(".//p:sp", ns):
        text = " ".join(node.text or "" for node in shape.findall(".//a:t", ns)).strip()
        transform = shape.find("p:spPr/a:xfrm", ns)
        if text and transform is not None:
            offset, extent = transform.find("a:off", ns), transform.find("a:ext", ns)
            if offset is not None and extent is not None:
                boxes.append((text, int(offset.get("x")), int(offset.get("y")), int(extent.get("cx")), int(extent.get("cy"))))
    for i, first in enumerate(boxes):
        _, x, y, w, h = first
        if x < -1000 or y < -1000 or x + w > 9145000 or y + h > 5144500:
            off_canvas.append({"slide": number, "text": first[0][:60]})
        for second in boxes[i + 1:]:
            _, x2, y2, w2, h2 = second
            if min(x + w, x2 + w2) - max(x, x2) > 12700 and min(y + h, y2 + h2) - max(y, y2) > 12700:
                overlaps.append({"slide": number, "texts": [first[0][:50], second[0][:50]]})
for entry in report["media"]:
    assert parts[entry["imported_part"]] == source[entry["source_part"]]
assert manifest[13]["kind"] == "authored-sdk" and manifest[22]["kind"] == "authored-sdk"
assert manifest[-1]["title"] == "Questions?"
pdf_info = subprocess.check_output(["/opt/homebrew/bin/pdfinfo", str(root / "kubecon-2026-dry-run.pdf")], text=True)
assert re.search(r"Pages:\s+25\b", pdf_info)
result = {"slides": 25, "notes": notes_count, "illustratedSlides": pictures, "pdfPages": 25,
          "seconds": 1800, "sdkOriginalSlides": list(range(3, 13)), "sdkOutputSlides": list(range(14, 24)),
          "sdkSlideXmlUnchanged": True, "sdkMediaUnchanged": True, "sdkSourceFileUnchanged": True,
          "offCanvasObjects": off_canvas, "overlappingTextBoxes": overlaps,
          "visibleGeneratedSpeakerAssignments": 0, "generatedTechnicalMaturityLabels": 0}
(root / "validation-report.json").write_text(json.dumps(result, indent=2))
print(json.dumps(result, indent=2))
assert not off_canvas and not overlaps
