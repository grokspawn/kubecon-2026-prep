# KubeCon 2026 — catalog, Helm and evolution planning context

Assessed 2026-10-09. These sources establish **design intent and hypotheses**, not released support. Source documents remain unchanged; no proposal-linked repositories/documents were crawled and no implementation or performance tests were run.

**User-confirmed decisions:** October 2 schema-first direction is current; OCI-native catalog storage is future work. Canonical Helm packaging/catalog representation is **`helm+v2`**. This labels the versioned packaging represented by OLM-compatible schemas, not the Helm CLI version. Older brief examples remain recorded as source history, not live ambiguity.

## Sources and chronology

| Source | Read method / extent | Status and chronology |
|---|---|---|
| [Brief: v2 Catalog Schemas for OLMv1](https://docs.google.com/document/d/1J98HtTLvZC83XJawHqPJlrAxOlEWsR9UoftNc1Gfhck/) | Authenticated Google Docs MCP, full returned text, 14,237 characters | Jordan; August 7, 2026; expected 2026/Q4. Status/consensus fields blank. **Joe/Jordan October 2 update changes the direction relative to earlier transport/channel text.** |
| [Brief: First-Class Helm Chart Support for OLMv1](https://docs.google.com/document/d/1HTP4T14OBxxSJKfj8vgAJUSGS5hMNHEWjddqEJYcPXc/) | Authenticated Google Docs MCP, full returned text, 20,375 characters | Jordan; August 7, 2026; expected 2027/Q1. Status/consensus blank; proposed Alpha/default-off and future graduation gates. |
| `../2026-olm-evolution-musings.md` | Complete local read, 279 lines | August 5, 2026 discourse, explicitly progresses through corrections/conjectures. Strategic exploration, not an accepted roadmap or comparative product audit. |

Dates and quarters are **planning targets**, not presentation promises. Neither brief supplies verified merged-PR/release/benchmark evidence in the returned content. Public quotation/screenshots and canonical current wording should be confirmed before publication.

## Catalog v2: substantive proposal

### Problems the brief identifies

- Repeated package/descriptive metadata across bundles.
- Version identity embedded in properties instead of a first-class field.
- Lack of an explicit installable-content discriminator beyond registry+v1.
- Expensive retrieval/interpretation when identifying relevant catalog content and images for disconnected mirroring.

### Proposed schema responsibilities

| Schema | Intended responsibility |
|---|---|
| `olm.catalog` | Catalog-level provider, description, support and maturity metadata; replaces per-package channel maturity framing. Required fields use free text in the example. |
| `olm.package.v2` | Package-common provider/maintainer/description metadata stored once, rather than repeated per bundle. |
| `olm.package.decorators` | Optional presentation data such as icons, separated so consumers that do not render it can avoid it where transport permits. |
| `olm.bundle.v2` | Package, required top-level SemVer `version`, optional packaging `release`, explicit `mediaType`, digest-pinned content `image`, informational properties. |

Properties are proposed as forgiving/informational: unknown keys ignored. Prescriptive cluster-state constraints would fail closed on unknown keys, but their schema is **TBD**. The lifecycle schema is also still to be added. Do not show a finalized constraint/lifecycle contract that does not yet exist.

The main text orders versions by SemVer, excludes legacy graph representations, and drops explicit channels in favor of version pins/ranges. A registry+v1 entry still points to its existing operator bundle image. A Helm entry points to the chart's own OCI artifact, not an operator-bundle wrapper.

### Compatibility boundaries

- User frames these as **OLMv1-only** schemas: do not promise OLMv0 will consume new v2 schema semantics.
- The brief requires existing v1 FBC catalogs to remain unaffected and mixed v1/v2 documents to load in updated tooling. **Coexistence is not the same as v0 forward compatibility.**
- Proposed acceptance work spans operator-registry parsing/JSON Schema validation, catalogd serving, operator-controller resolution and disconnected mirroring.
- Schema adoption is proposed as author opt-in without a schema-level gate; new catalogd serving capabilities are separately proposed behind a default-disabled gate. Implementation/graduation remains unverified.

### Important chronological correction: transport is deferred

The earlier body/appendix describes OCI-native catalog/package indices and manifests, independent metadata/icon/bundle fetches, scoped catalogd endpoints and mirroring opportunities. This is useful longer-term architecture, **not the unqualified current deliverable**.

The **October 2 Joe/Jordan update** says:

1. Move storage-format changes to a future feature.
2. Eliminate `olm.channel` and upgrade-graph considerations completely.
3. Decide whether the new FBC I/O representation is monolithic or retains layered schemas.
4. Add a lifecycling schema.

The user confirms this later note as the current direction: prioritize well-defined, flexible schemas and defer OCI-native catalog storage. Do not advertise lazy/per-package OCI transport or specific `/api/v2` endpoints as implemented, committed immediate features. The appendix still depicts legacy channels and original schemas, and some PR-plan naming uses `olm.package.icon` rather than `olm.package.decorators`: those are document-reconciliation tasks, not new APIs to invent.

### Performance interpretation

Less duplicated data and clearer content identity provide a reasoned efficiency direction. Selective OCI fetches could offer further gains **if/when the deferred transport is implemented**. No before/after benchmark is supplied; describe a performance goal/design mechanism, not an achieved ratio, latency or memory improvement.

## Helm: first-class content with an explicit subset contract

### Proposed content path

```text
standard chart OCI artifact + v2 catalog metadata
                    + ClusterExtension inline values
                                      ↓
mediaType dispatch → Helm ManifestProvider
validate chart → merge/validate values → render → validate output
                                      ↓
existing OLM manifest application / phased ownership lifecycle
```

- Chart is pushed using normal `helm push`; chart config/tarball media types remain standard Helm OCI types.
- No registry+v1 CSV/bundle-image wrapper is required by the proposal.
- Runtime rendering reuses `ManifestProvider` and the existing ClusterExtension API; `spec.config.inline` supplies values. Defaults are merged using Helm mechanisms; `values.schema.json` is validated when present.
- Rendered manifests use OLM's application/reconciliation/ownership machinery. This is **not Helm CLI release management exposed through another API**.
- No new ClusterExtension CRD is proposed. The schema/content-specific render contract still needs implementation tests and matched API examples.

### Supported-subset restrictions in the brief

| Area | Proposed handling | User-facing consequence |
|---|---|---|
| CRDs | Reject `crds/`; require CRDs in `templates/` so they enter OLM's managed manifest lifecycle | Some existing charts require adaptation. This is not universal chart portability or a casual recommendation to relocate production CRDs without impact assessment. |
| Dependencies | Vendor subcharts into `charts/`; no runtime fetching/dependency installation | Self-contained/disconnected content, not automatic package dependency management. |
| Hooks | Reject `helm.sh/hook` | Hook-reliant charts need another approach; future sync-wave/hook-like work is explicitly deferred. |
| Retention | Reject `helm.sh/resource-policy: keep` | Chart-author retention expectations cannot silently override extension-owner cleanup. |
| Templates | Exclude random/UUID/time/environment/command-execution functions | Continuous rendering needs reproducible output for stable inputs; do not frame all ordinary Helm usage as inherently nondeterministic. |
| Values | Inline overrides; schema validation; ValuesFrom deferred | No promised ConfigMap/Secret-reference values support for the initial scope. |
| Release objects | Extension identity/namespace mapped into `.Release`; proposed always-upgrade semantics | Chart assumptions about Helm install/upgrade/revision behavior need deliberate compatibility testing. |

The proposal maps `.Release.IsUpgrade=true` and `.Release.IsInstall=false` even on initial installation, and says `.Release.Revision` increments on each render. These are **proposed semantics**, not harmless details: test charts using those objects and reconcile render-count changes with stable-reconciliation goals.

CRD safety checks remain bounded. The brief's managed deletion of CRDs on extension deletion has serious data implications: removing a CRD can remove its custom-resource instances. Shared CRD ownership and externally managed content need explicit treatment; do not present automatic cleanup as unconditionally safe.

### Gating and readiness evidence

The Helm brief proposes `V2CatalogServing`, `V2CatalogResolution` and `HelmChartSupport` gates, all Alpha/default off, with Helm rendering dependent on v2 resolution. **These are proposal gates**, unlike previously source-inspected existing runtime/configuration gates; their implementation was not checked here.

Validation targets include 50+ representative charts, disconnected operations, upgrade/security validation and under-ten-second typical render time. These are **graduation targets**, not observed results. A proposed two-quarter preview period and 2027/Q1 expectation are not a GA promise.

### Confirmed resolutions and remaining follow-through

1. **Discriminator resolved:** canonical **`helm+v2`**, as confirmed by the user. Older catalog/provider `helm+v1` examples are superseded. Standard Helm OCI media types, OLM packaging version and Helm CLI version are distinct concepts.
2. **Channels:** the confirmed October 2 direction removes channels/legacy graph considerations. Older Helm derived-channel wording needs alignment, not another decision about whether that direction applies.
3. **Transport dependency:** OCI-native **catalog storage** is confirmed as future work. Align old critical-path wording with the short-term schema focus; native **chart** OCI identity is a separate concept. Validate the actual implementation path later without promising immediate catalog transport changes.
4. **Output annotations:** the text describes an annotation allow-list, then specifically rejects hook/keep annotations. Clarify scope before claiming arbitrary non-Helm annotations remain compatible.
5. **Authoring:** the excluded `opm helm generate` item still refers to bundle images despite the no-wrapper direction. Separate any future authoring helper from runtime requirements.

## Evolution musings: what to carry into the talk

The useful strategic question is **“What value does OLM add in a mature Helm/GitOps ecosystem?”** A defensible direction is a catalog/installation/upgrade-governance contract that composes with content formats and existing controllers.

### Retain as framing or explicit exploration

- Separate content rendering from its lifecycle management: a provider yields Kubernetes objects; OLM manages a declared lifecycle boundary.
- Direct rendering (e.g. proposed Helm support) and delegation (e.g. hypothesized Argo CD Application/Flux HelmRelease output) are distinct designs.
- An external installation is not automatically a versioned, authoritative OLM package inventory entry. Adoption may conflict with its actual reconciler and becomes stale without a genuine ownership handoff.
- API/GVK presence does not prove controller health, compatible software version or future availability. Package-version requirements and loose API prerequisites are different concepts.

### Do not elevate these assertions to facts or roadmap commitments

- **“Only OLM provides safety/ownership” / “other tools blindly apply” / “OLM is not GitOps-native”:** broad, unverified comparative claims. Current docs describe declarative/GitOps-friendly OLM interfaces; Helm/GitOps tooling has its own ownership, policies and extensibility. Compare responsibility boundaries, not universal superiority.
- **Universal protection through delegation:** emitting an Application/HelmRelease CR does not automatically let OLM inspect or govern every descendant CRD managed by the external controller. Define the protection boundary before claiming it.
- **“Removing namespace scope makes dependency resolution solved”:** explicitly hypothetical AllNamespaces-only premise, not current compatibility reality. Global version conflicts, inventories, permissions, readiness, external ownership and administrator consent still matter; single-owner CRDs do not select all future providers or certify dependencies.
- **Return of auto-installing dependencies / two-tier package+GVK schemas:** strategic conjectures, not approved proposal/current behavior. The supplied catalog brief leaves constraints and lifecycle metadata TBD. Keep automatic dependency management out of the main committed roadmap.
- **Specific future media types** (`argocd+v1`, `flux+v1`, etc.): illustrative hypothesis names, not supported registered formats.

The stage-4 external-installation problem usefully qualifies stage-3 optimism. Prefer its honest trust-boundary insight over an “apt-get for Kubernetes” promise.

## Outline implications and grounded participation

- Three OLM speakers can tell **why the boundary matters → what current/prototype primitives do → how new content and metadata broaden the contract**; Attila then covers only Java SDK.
- Replace the generic Helm future beat with **“Your chart, OLM-managed lifecycle—not a Helm release”** and a small supported-subset checklist.
- Replace the generic catalog beat with **“Metadata once; versions explicit; content typed”**. Show package metadata and two differently typed content cards. Keep the deferred OCI hierarchy in the appendix.
- The post-2025 novelty is design precision and concrete work/test targets—not reannouncing “Helm charts” or promising achieved catalog speedups.
- Contribution candidates: representative chart/values fixture; CRD/hook/keep compatibility cases; pure-versus-changing-template tests; v1/v2 coexistence/validation fixture; package metadata/decorator split feedback; a bounded lifecycle/constraint question.
- Any “try it now” exercise still needs an implemented path, pinned versions, validation command, expected result and maintained issue destination. The briefs provide test ideas, not a ready authoring workflow.

## Remaining follow-up — confirmed decisions are not open questions

October 2 direction and canonical `helm+v2` are settled. Remaining work is to align old brief wording, define the lifecycle/constraint schema and validate actual implementation dependencies. When selecting runnable examples, pin implementation/gates and confirm intended CRD deletion/release-object behavior and vetted first tasks. No further broad ingestion is needed now.
