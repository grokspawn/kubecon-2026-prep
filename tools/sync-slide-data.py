"""Refresh the local slide data from a verified Google Slides text snapshot.

The Google presentation is the working master. This updates only the 17
generated slides; Attila's ten authored slides continue to be imported from
the source presentation by the builder.
"""
import json
import re
from pathlib import Path

root = Path(__file__).resolve().parent.parent
path = root / "dry-run/slide-data.json"
existing = json.loads(path.read_text())
deck = json.loads((root / "current-deck-live.json").read_text())
run = json.loads((root / "current-deck-run-of-show.json").read_text())
assert len(deck["slides"]) == len(run["records"]) == 27
for slide, scheduled in zip(deck["slides"], run["records"], strict=True):
    assert slide["number"] == scheduled["number"]
    assert slide["text"] and slide["text"][0].strip() == scheduled["title"].strip(), (
        f"Slide {slide['number']} differs from the run of show; review before syncing"
    )
old = {entry["title"]: entry for entry in existing}
selected = list(range(1, 16)) + [26, 27]


def seconds(value):
    minutes, secs = map(int, value.split(":"))
    return minutes * 60 + secs


records = []
for number in selected:
    slide = deck["slides"][number - 1]
    schedule = run["records"][number - 1]
    assert slide["number"] == schedule["number"] == number
    assert slide["text"][0] == schedule["title"]
    title = slide["text"][0]
    if number in (5, 6):
        paragraphs = [s.strip() for s in slide["text"][1].split("\n\n") if s.strip()]
        entry = {
            "title": title,
            "section": "02 / INSTALLATION",
            "status": "",
            "imagePath": f"current-visuals/{'streamlined-installation' if number == 5 else 'namespace-management'}.png",
            "lead": paragraphs[0],
            "bullets": [s.removeprefix("• ") for s in paragraphs[1:]],
            "caption": "",
        }
    else:
        assert title in old, f"No earlier source record for {title}"
        entry = dict(old[title])
        visible = slide["text"]
        if number in (3, 4, 7, 8, 9, 10, 11, 12, 13, 14, 26):
            assert len(visible) == 6, (number, visible)
            entry["status"], entry["lead"] = visible[1:3]
            entry["bullets"] = visible[3].split("\n")
            entry["caption"] = visible[4]
        elif number == 27:
            assert len(visible) == 5
            entry["lead"] = visible[1]
            entry["bullets"] = visible[2].split("\n")
            entry["caption"] = visible[3]
        if number == 14:
            entry["imagePath"] = "current-visuals/contributing-qr.png"
            entry["visualKind"] = "qr"
            entry["captionUrl"] = "https://github.com/operator-framework/operator-controller/blob/main/CONTRIBUTING.md"
    notes = "\n".join(slide["notes"])
    marker = "TALK TRACK / SOURCES / CAVEATS:"
    assert marker in notes, f"Missing talk track for slide {number}"
    for expected in (f"SPEAKER: {schedule['speaker']}",
                     f"START: {schedule['start']}",
                     f"DURATION: {schedule['duration']}"):
        assert expected in notes, f"Slide {number} notes differ from the run of show: {expected}"
    entry["speaker"] = schedule["speaker"]
    entry["duration"] = seconds(schedule["duration"])
    entry["notes"] = notes.split(marker, 1)[1].strip()
    assert not re.search(r"<upstreamRelease>|QR code remains deferred", entry["notes"])
    records.append(entry)

assert len(records) == 17
assert sum(entry["duration"] for entry in records) == 1320
path.write_text(json.dumps(records, ensure_ascii=False, indent=2) + "\n")
print("Synchronized 17 generated slides and 22 minutes of notes from the current deck.")
