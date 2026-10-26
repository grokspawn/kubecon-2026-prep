# The Next Era of Kubernetes Operator Lifecycle Management

Dry-run slides for KubeCon NA 2026.

All generated build, asset, preview and output files for this draft stay in this directory. Source context is in the parent working area; original source presentations are not edited.

Speaker assignments are OLM A/B/C (names to confirm) and Attila (Java SDK only). Timings and SDK condensation are proposed. Speaker notes carry sources, qualifications and alignment questions.

The current revision uses direct technical language. Speaker assignments and timing stay in notes. Visible slide footers contain page numbers and event information. Language preferences are recorded in the parent `AGENTS.md`; build checks cover rejected contrast patterns, visible ownership and the confirmed title.

## Review files

Current revision: intro-only cover, Rashmi/Joe/Jordan team page, history on slide3, and the v0 namespace-visibility summary in the timeline on slide4. The standalone assumptions page is removed; the deck remains25slides. A separate [SDK-themed final copy](../final/README.md) uses the same content with source branding and no review markings.

- [Editable PowerPoint with embedded speaker notes](kubecon-2026-dry-run.pptx)
- [PDF slides rendered from the PowerPoint](kubecon-2026-dry-run.pdf)
- [Speaker notes and review questions](speaker-notes.md)
- [Slide overview, 1–10](contact-sheet-1.png)
- [Slide overview, 11–20](contact-sheet-2.png)

25 widescreen slides and 25 nonempty notes; proposed timing totals 30 minutes including questions/buffer. A owns 1–4 and24, B5–9, C10–13, Attila14–23, and25 has topic-scoped questions. The SDK section contains his original technical source slides3–12, with visible XML and media preserved byte-for-byte. Original title, biography and Q&A bookends are omitted because the combined session has shared bookends.

The OLM material uses availability/development language and explicit feature-gate/review information. Direct installation is based on open PR2907, checked2026-10-09. Catalog benefits build on established FBC and remain design goals pending measurement. Original SDK claims/wording are retained as authored. Detailed notes are in the PPTX and Markdown companion.

## Rebuild and validation

Sources: `slide-data.json`, `build-deck.js`, `make-assets.js`, and editable SVGs under `assets/`. `package-lock.json` records build dependencies. Browser/npm caches and LibreOffice profile are local and ignored by git.

From this directory: `node make-assets.js`, `python3 theme/prepare-theme.py`, `node build-deck.js --both`, then `python3 validate-deck.py`. Use `--final` for the themed copy alone; the default builds the review copy. Each build generates15base slides, imports10authoredSDKslides, and renders25pages. `theme/apply-theme.py` assigns source layout resources to generated final pages. `validate-variants.py` checks both variants and writes per-variant reports plus `../variant-comparison.json`. Some legacy assets are retained but unused in the current deck.

Rendered contact sheets were inspected for all twenty slides. The revised title page and deployment-configuration page were checked at full resolution. Validation reports zero off-canvas objects, overlapping text boxes, visible speaker assignments and rejected contrast-pattern matches. Feature behavior and release claims require separate evidence.
