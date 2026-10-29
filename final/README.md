# The Next Era of Kubernetes Operator Lifecycle Management

This SDK-themed presentation follows the current 27-slide Google deck and the
proposed 32-minute schedule. It is rebuilt from local source, rather than
exported directly from Google Slides. Speaker notes and availability labels
are retained; the generated OLM slides have no review markings.

## Files

- [PDF](kubecon-2026-final.pdf)
- [PowerPoint with speaker notes](kubecon-2026-final.pptx)
- [Speaker notes](speaker-notes.md)
- Slide overviews: [1–10](contact-sheet-1.png), [11–20](contact-sheet-2.png),
  [21–27](contact-sheet-3.png)

The ten original Java Operator SDK technical slides are retained with their
authored text, slide XML, and media unchanged. The installation and namespace
illustrations appear on slides 5–6; slide 14 contains the contribution-guide
QR code. A/B/C assignments to the named OLM presenters remain to be confirmed.

To rebuild, run `node build-deck.js --final` from `../dry-run/`. Run
`python3 ../dry-run/validate-variants.py --variant final` to validate the
result. See the [session handoff](../SESSION-HANDOFF.md) for current scope
and source details.
