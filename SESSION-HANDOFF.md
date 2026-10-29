# KubeCon 2026 session handoff

Updated October 28, 2026. Read this file, `AGENTS.md`, and the current outline
before continuing the presentation or demo work.

## Current presentation

- Title: **The Next Era of Kubernetes Operator Lifecycle Management**.
- Working master: [Google Slides](https://docs.google.com/presentation/d/1yLWsXrp2GWjLyS_ztnbnmR40OGwm29QHI4qpxGHf7A8/edit).
- The deck has 27 slides and a proposed 32-minute allocation, including two
  minutes for questions. The outline and schedule are in
  `kubecon-2026-outline.md` and `current-deck-run-of-show.json`; the notes are
  in `current-deck-speaker-notes.md`.
- Rashmi, Joe, and Jordan are the three OLM speakers. Roles A/B/C have not
  been mapped to individuals. A is allocated seven minutes including the
  close, B seven, and C six. Attila presents the ten Java Operator SDK slides
  exclusively. Keep his authored wording and illustrations unchanged.
- The Google deck contains the new installation and managed-namespace
  illustrations on slides 5–6, and a contribution-guide QR code on slide 14.
  Assets and slide previews are in `current-visuals/`. The QR code was
  decoded successfully from the rendered Google slide. The source PNGs also
  reside in a Drive folder with user-only permissions.
- Source data for the local builder is `dry-run/slide-data.json`. It has 17
  generated slide records; the builder inserts the ten original SDK slides
  after the divider. It reads the unchanged SDK source at
  `~/Downloads/Copy of KubeCon2026.pptx`. Do not edit that source file.
- The refreshed local [final PPTX](final/kubecon-2026-final.pptx) and
  [PDF](final/kubecon-2026-final.pdf), and the dry-run equivalents under
  `dry-run/`, follow the current content and order. They are locally rebuilt
  presentations, not direct exports of the Google deck. Both variants passed
  `python3 dry-run/validate-variants.py --variant both`; the QR decoded from
  each rendered slide 14 preview.
- The earlier 25-slide generated PPTX/PDF and notes were preserved under
  `archive/2026-10-23-25-slide-snapshot/`. Those are historical snapshots.

## Technical and editorial boundaries

- Use direct technical prose and the Google developer documentation style
  guidance. Keep speaker assignments and handoffs in notes, except for the
  explicit team-introduction slide.
- Standard-channel service-account deprecation: operator-controller v1.11.0.
  The field remains accepted but is optional and ignored. Treat
  ClusterExtension write access as highly privileged.
- Managed install namespaces: v1.12.0 experimental feature set, controlled
  by the runtime feature gate. Deleting a managed namespace removes all its
  contents, including unrelated objects; namespace changes on upgrade can
  also remove the previous namespace.
- Current rollout model: ClusterExtension → ClusterObjectDeployment →
  immutable ClusterObjectSet revisions. Pin the controller and gates in demos.
- Direct registry+v1 bundle installation is tracked in open upstream PR
  #2907 as last checked October 28. Recheck status before making release claims.
- Catalog work focuses on flexible OLMv1 schemas. OCI-native catalog storage
  and transport remain future work. `helm+v2` is the OLM content-format
  discriminator, not a Helm CLI version. Avoid unmeasured performance claims.
- Demo Helm support is a fork experiment, not a released capability. The
  recorded experiment uses an OCI image config as a workaround for pulling
  standard Helm OCI artifacts; do not describe it as standard chart support.

## Demo work and safety

- Repository: `github.com/grokspawn/kubecon-2026-demos`, local checkout
  `~/devel/kubecon-2026-demos`; demo 1 and slide references were updated in
  commit `929495f`. Demos are online companions, not live presentation steps.
- Feature branches in `grokspawn/operator-controller`: `kubecon-2026-demo`,
  `kubecon-2026-demo-direct-bundle`, and `kubecon-2026-demo-helm-direct`.
  Migration work uses `grokspawn/library-olm` branch `kubecon-2026-demo`.
  Feature code changes belong only in the approved grokspawn demo-branch
  scope; task-specific clones belong under `~/devel/agent-playground`.
- Demo 1 now omits `spec.namespace` and demonstrates a managed namespace.
  Its recording and script were validated on the named disposable kind
  cluster. Namespace and CRD deletion are destructive to their contents.
- A temporary kind kubeconfig was previously committed to the public demo
  repository. The affected cluster was deleted and reachable branch history
  was rewritten. Never add kubeconfigs, credentials, runtime files, or generated
  cluster state to a commit; inspect staged files before any push.
- Raw Slides API backups in this workspace can contain temporary image access
  URLs. They are ignored by `.gitignore`; do not publish or commit them.

## Resuming

1. Check the live Google deck before further editing; collaborators may have
   changed it since `current-deck-live.json` was captured.
2. Read the final build and validation reports before relying on local exports.
   Rebuild with `cd dry-run && node build-deck.js --both && python3
   validate-variants.py --variant both`.
3. Preserve the Google deck and original references unless the user requests
   changes. Do not rerun one-time Google update scripts without reviewing their
   preconditions and effects.
4. Confirm the individual speaker assignments and rehearsal timing with the
   presenters; treat release status and open PRs as date-sensitive.
