# KubeCon working-area instructions

- Generate all new content for this KubeCon project inside this directory or a subdirectory; do not scatter project output in the breadcrumbs root or temporary storage.
- Preserve original reference files in the parent directory, source decks and Google documents unless the user explicitly requests edits.
- Confirmed speakers: four total, three OLM plus Attila exclusively on Java Operator SDK.
- Catalog direction: flexible OLMv1 schemas first; OCI-native catalog storage/transport is deferred future work.
- Canonical OLM Helm content discriminator: `helm+v2`. Its version is a packaging/catalog representation, not a Helm CLI version claim.
- Describe availability and development activity accurately. Use “in active development” for evolving functionality and “controlled by feature-gate” for gated functionality. Keep review/planned/future work distinct from available behavior; avoid public technical maturity-stage labels. Preserve source evidence in notes and avoid unverified performance/adoption figures.
- Use the 2025 context to avoid repeating the same message; preserve the SDK handoff and no-live-demo default.
- Source-relative references to original inputs use `../`; references among generated documents remain local.

## Language and presentation preferences

- Confirmed talk title: **The Next Era of Kubernetes Operator Lifecycle Management**. Use it on the deck and in presentation metadata.
- Write direct technical prose. Avoid model-style antithetical slogans such as “Xs do not Y — they Z”, “do X — not Y”, and “X, not Y”. Avoid stock motivational phrases and repeated triadic slogans. State the technical point clearly.
- Apply this preference to slide text, illustration labels, captions, speaker notes and future generated material. Use technical restrictions where needed, with straightforward phrasing such as “Hooks are unsupported in the proposal.”
- Speaker assignments, handoffs and presentation-management details belong in speaker notes. Keep them out of slide titles, body copy, illustrations and footers.
- Preserve factual qualifications, support boundaries and maturity labels while editing style.
- Current dry-run uses availability/development wording instead of alpha/prototype/default-off labels. Preserve accurate feature-gate and in-review information.
- Attila's supplied SDK content is authored material. Preserve its wording and illustrations. Formatting changes and nonvisible assignment notes are allowed; obtain permission before content rewrites. This supersedes earlier SDK condensation proposals.
- Feature diagrams should illustrate historical choices, current work and future direction. Treat existing FBC capabilities as established foundations and identify specific newer schema/content/performance benefits.
- Cover is an intro with the operator-lifecycle illustration; progress discussion starts later. Slide 2 introduces Rashmi, Joe and Jordan, with pictures deferred. The old assumptions slide is summarized in the timeline Past bullet.
- Produce a review copy and a separate SDK-themed final copy when requested. The themed final copy reuses source fonts/colours/layout branding, retains availability labels and notes, and omits DRY RUN markings.
