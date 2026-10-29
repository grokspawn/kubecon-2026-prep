"""Sync the local run-of-show notes from the read-only Google Slides export."""
import json
from pathlib import Path

root = Path(__file__).resolve().parent.parent
deck = json.loads((root / "current-deck-after.json").read_text())
run = json.loads((root / "current-deck-run-of-show.json").read_text())
assert len(deck["slides"]) == len(run["records"]) == 27
for slide, record in zip(deck["slides"], run["records"], strict=True):
    assert slide["number"] == record["number"]
    record["notes"] = "\n".join(slide["notes"]).strip()
    assert record["start"] in record["notes"]
(root / "current-deck-run-of-show.json").write_text(json.dumps(run, indent=2, ensure_ascii=False) + "\n")
text = "# Current Google Slides: speaker notes\n\n32 minutes total. A/B/C assignments to named OLM speakers remain open.\n\n"
text += "\n".join(f"## {r['number']}. {r['title']}\n\n{r['notes']}\n" for r in run["records"])
(root / "current-deck-speaker-notes.md").write_text(text)
print("Synced notes for 27 slides.")
