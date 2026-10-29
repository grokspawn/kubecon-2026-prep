# The Next Era of Kubernetes Operator Lifecycle Management

This review package follows the 27-slide Google deck and the proposed
32-minute schedule. It is rebuilt from local source; it is not a byte-for-byte
export of Google Slides. Review markings remain on the generated OLM slides.

## Files

- [PowerPoint with speaker notes](kubecon-2026-dry-run.pptx)
- [PDF](kubecon-2026-dry-run.pdf)
- [Speaker notes](speaker-notes.md)
- Slide overviews: [1–10](contact-sheet-1.png), [11–20](contact-sheet-2.png),
  [21–27](contact-sheet-3.png)
- [SDK-themed copy without review markings](../final/README.md)

The builder generates 17 slides and imports Attila's original SDK source
slides 3–12 as slides 16–25. The 27 slides have a total proposed duration of
32 minutes, including questions. A/B/C speaker identities remain unassigned.

## Rebuild and validate

From this directory, run:

```sh
node build-deck.js --both
python3 validate-variants.py --variant both
```

Use `--final` for the themed copy alone; the default builds the review copy.
The build reads `slide-data.json`, `../current-visuals/`, and the unmodified
SDK source presentation at `~/Downloads/Copy of KubeCon2026.pptx`. To refresh
the slide data, first obtain a read-only Google deck snapshot as
`../current-deck-live.json`, check it against the run of show, then run
`python3 ../tools/sync-slide-data.py`.

Validation checks slide order, 32-minute timing, notes, visible copy, artwork,
source SDK slide and media bytes, page count, and generated-slide geometry.
The QR code was also decoded from both rendered slide 14 previews. Release
claims and upstream PR status still require date-appropriate verification.
