# KubeCon NA 2026 working area

All new generated project content belongs in this directory or its subdirectories. Original inputs remain outside it unless explicitly requested otherwise. Shared PAI workflow metadata/logs are system bookkeeping, not project deliverables.

## Current deck and confirmed direction

- The [working Google deck](https://docs.google.com/presentation/d/1yLWsXrp2GWjLyS_ztnbnmR40OGwm29QHI4qpxGHf7A8/edit) has 27 slides and a 32-minute target including questions. See the [current outline](kubecon-2026-outline.md#current-google-deck--2026-10-28) for order, proposed timing and evidence checks. The local builder follows this content and order; its PPTX/PDF outputs are regenerated presentations, not direct Google Slides exports.
- Four speakers: three OLM presenters; Attila exclusively Java Operator SDK.
- 32 minutes including questions; concise slides and online-only demos by default.
- Short-term catalog work prioritizes well-defined, flexible OLMv1 schemas. The October 2 direction is confirmed; OCI-native **catalog storage/transport** is future work.
- **`helm+v2` is canonical**, representing versioned Helm packaging in OLM-compatible catalog schemas. Do not confuse this with Helm CLI major version, standard chart OCI media types, or a requirement for a registry+v1 wrapper image.
- Schema/format decisions do not establish shipped support or measured performance.

## Working documents

- [Session handoff](SESSION-HANDOFF.md) — current scope, source files, demo branches, and resumption checklist.
- [SDK-themed presentation](final/README.md) — 27-slide PDF, editable PPTX and notes, without review markings.

- [Illustrated dry-run review package](dry-run/README.md) — 27-slide editable PPTX with notes, rendered PDF and visual overview.

- [Presentation and companion package outline](kubecon-2026-outline.md)
- [Current Google deck speaker notes](current-deck-speaker-notes.md) and [32-minute run of show](current-deck-run-of-show.json)
- [Resource assessment](kubecon-2026-resource-assessment.md) — dated October 9 source assessment, with later work tracked separately.
- [2025 prior-slide context and differentiation](kubecon-2025-slide-context.md)
- [Catalog, Helm and evolution planning context](kubecon-2026-feature-planning-context.md)

## Helpers and derived artifacts

- `tools/kubecon_text_extract.py`: standard-library local PPTX text/notes extraction; takes source PPTX and output directory arguments.
- `tools/read-prior-slides-mcp.mjs`: allowlisted, read-only temporary MCP adapter for the 2025 deck, reusing the existing installed Google integration's authentication. No credentials are stored here.
- `tools/parse-slide-export.py`: parses a PPTX byte stream into ordered slide text/notes for that adapter.
- `tools/update-current-deck.mjs` and `tools/position-inserted-visuals.mjs`: records of the one-time Google deck updates. Their expected original elements and text no longer match the updated deck; do not rerun them without review.
- `tools/sync-slide-data.py`: updates the 17 locally generated slide records from the checked Google snapshot and current run of show.
- `current-visuals/`: editable SVG illustrations, PNGs, the verified contribution-guide QR code, and previews of the updated slides. The visual PNGs also live in a private Drive folder for the presentation.
- `artifacts/kubecon2026-content/`: 80 XML/relationship files extracted from the proposed 2026 PPTX. This is an XML-only extraction, not a complete deck or visual rendering; media binaries were not extracted.

Helper scripts do not imply that runnable OLM demos have been built or validated. Do not publish credential stores or infer release availability from these artifacts.

## Original inputs — not moved

- [Breadcrumb resource list](../kubecon-2026.txt)
- [OLM evolution musings](../2026-olm-evolution-musings.md)
- `~/Downloads/Copy of KubeCon2026.pptx`
- Source Google Docs and Slides linked from the resource list.

The generated documents were relocated here from the breadcrumbs root; helpers/extractions were relocated from temporary storage. Keep future notes, outline revisions, illustrations, demo code, exports and review artifacts here.
