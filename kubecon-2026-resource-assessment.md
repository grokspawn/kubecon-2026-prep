# KubeCon NA 2026 — resource assessment

Assessment date: 2026-10-09. Seed: `../kubecon-2026.txt` (not edited by this assessment). All generated work belongs in `~/devel/breadcrumbs/2026-kubecon-wip/` and its subdirectories.

**Event:** KubeCon North America, November 9–12, 2026 (user-confirmed). Updated after the second breadcrumb revision. The update below supersedes first-pass access gaps and unresolved implementation questions where stated; earlier reference tables remain useful background.

**Draft package outline:** [kubecon-2026-outline.md](kubecon-2026-outline.md) proposes the timed shared-session narrative, slide beats, illustration concepts, contribution paths and online companion deliverables. Its 17-minute OLM / 10-minute SDK allocation is proposed, not speaker-approved; no final slides or examples have been built.

## Latest correction and planning-source additions

- **Confirmed schema/format decisions:** short-term catalog work prioritizes well-defined, flexible schemas; OCI-native catalog storage approaches are future work. The October 2 direction is confirmed. **`helm+v2` is canonical** for versioned Helm packaging expressed through OLM-compatible catalog schemas; it is not a Helm CLI-version assertion.

- **Four speakers total, confirmed by the user:** three OLM presenters plus Attila **exclusively on Java Operator SDK**. This supersedes the original up-to-three interpretation. Proposed blocks are 4 minutes context, 8 lifecycle primitives, 5 catalogs/content/contributions, 10 SDK, 1 OLM-led close, 2 questions/buffer. OLM identities/timings remain provisional.
- **Planning sources now consumed:** both catalog/Helm Google Docs via authenticated MCP, plus the explicitly requested `../2026-olm-evolution-musings.md` original local note.
- **Durable assessment:** [kubecon-2026-feature-planning-context.md](kubecon-2026-feature-planning-context.md) records schema details, Helm compatibility limits, proposal inconsistencies, strategic hypotheses and contribution candidates. No linked-document crawl or release/benchmark validation.
- **Catalog takeaway:** package metadata once, first-class version/release, explicit content type, separate decorators. The later October 2 update defers storage/OCI-transport changes and removes channel/legacy-graph considerations; lifecycle schema remains open. Do not present the earlier transport appendix's selective fetches as current or measured performance.
- **Helm takeaway:** standard chart OCI identity without an operator-bundle wrapper, inline values and runtime rendering into OLM-managed manifests, not Helm release management. The proposed subset rejects hooks/keep/`crds/`, vendors dependencies and restricts changing templates. CRD deletion and release-object assumptions need deliberate validation.
- **Strategic takeaway:** lifecycle governance can complement packaging/GitOps. Musings about automatic dependency resolution and Argo/Flux delegation are hypotheses, not accepted commitments; delegation does not automatically expand CRD-safety/ownership coverage.
- **Remaining follow-through:** align outdated channel/transport/discriminator wording with confirmed schema-first direction and `helm+v2`; refine lifecycle/constraint schema and validate the implementation/test path. Do not ask again for resolved direction or representation. Planning targets are not launch promises.

## Confirmed session intent — speaker integration and contributions

User clarifications, including the later four-speaker correction:

- Attila's proposed Java Operator SDK content belongs to the **same approximately thirty-minute session**, typically as its final portion. There are four total speakers; he covers only Java SDK. Its early readiness is not a request to replace the OLM material or treat it only as a style reference.
- This is a **maintainer update**, combining accomplished work with a clearly distinguished planned backlog.
- Explain the rational basis for the long interval without new audience-visible features. Make architectural/compatibility investment understandable through concrete outcomes rather than an apology or a chronological inventory of internal work.
- Inspire collaborators and contributions. Give additional weight to demonstrable, approachable paths for developing content or helping the projects evolve.
- Exact segment durations, overall title/abstract, and target release/gate baseline remain unconfirmed.

### Narrative implications

Working arc: **what needed to change → what the investment enables now → where we are going and how to help → developer-runtime progress in Attila's closing segment**. Keep a short shared recap/contribution pointer after that segment if practical; do not count it as an extra presentation.

The long feature interval is context, not the protagonist. For each selected historical limitation, connect the design decision to an observable payoff and an honest boundary. Compatibility, migration and readiness work can explain investment, but validate chronology and team-count claims before quantifying them. Do not equate a quiet feature period with no maintenance, fixes, or engineering progress.

Distinguish **released**, **alpha/prototype**, and **planned** work consistently. A planned capability may be an invitation to shape the design, not an action attendees can perform today. Preserve the distinction between language-neutral OLM packaging and Java-specific SDK runtime improvements at the speaker handoff.

### Candidate contribution paths — validate before promoting

| Attendee interest | Candidate next action | Evidence needed before calling it an easy on-ramp |
|---|---|---|
| Existing operator/content author | Try an appropriate compatibility or non-mutating migration eligibility check; report a concrete obstacle | Version-pinned commands, prerequisites, check scope, sample output and reporting destination. Migration eligibility is not universal portability certification. |
| Chart/content maintainer | Help validate a Helm-content example or supply representative packaging requirements | Current format/proposal, actual support tier, minimal example and feedback channel. Do not imply released native Helm support. |
| Platform practitioner | Exercise a documented rollout/customization example and report readiness/configuration edge cases | Reproducible online example, matched gates/controller revision, expected outcome and issue template. |
| First-time project contributor | Improve a focused example/documentation gap or add a small regression case | Maintainer-vetted issue, repository contribution guide, local test command and realistic scope. |
| Experienced contributor | Collaborate on catalog schemas, successor-resolution semantics or broader content designs | Canonical design document, bounded open question and active maintainer contact/discussion. |

Prefer a few verified invitations to a generic “contributions welcome” slide. Pair an accomplished or planned capability with **who can help, a first task, and where to start**. Put longer instructions and demos online; do not add live-demo time to sell the on-ramp. Contribution asks may appear alongside their topics so Attila's final segment does not displace the OLM invitation.

## Updated understanding — second pass

### Added 2025 deck: differentiation baseline

The user added the **2025 talk's Google Slides deck** to the previous-talk resources specifically to avoid repeating the same ground with the same message. This is separate from Attila's 2026 PowerPoint contribution.

- Source ID: `1_WK8mNw3pERO6U96ptlW3pKiQDvZdBpk12kRN5orIqk`; supplied link is in `../kubecon-2026.txt`.
- **Content successfully retrieved through MCP on 2026-10-09.** The installed integration lacks Slides/export operations, so a temporary read-only stdio MCP adapter reused its existing authentication module. Slides API returned 403 `accessNotConfigured`; authenticated Drive PPTX export succeeded. No server/config/authentication/scope changes or source-slide edits.
- **Durable source context:** [kubecon-2025-slide-context.md](kubecon-2025-slide-context.md), covering all 27 slides, speaker notes, historical claims and a 2026 differentiation matrix. Slide 5 is hidden and duplicates the visible v0/v1 comparison: 26 non-hidden slides.
- Drive title: “KubeCon NA 2025 - Operator Framework Maintainer Track”; opening title: “Package Management For Your Cluster, Reimagined.” Listed prior speakers: Rashmi Gottipati, Jordan Keister, Joe Lanford, Attila Mészáros. The user subsequently confirms four total speakers in 2026; prior names do not by themselves assign the three OLM roles.
- **Major overlap:** 2025 already presented v1 rationale, namespace-mode compatibility, webhook support, experimental immutable revisions/phases, a demo workflow, configuration/Helm/migration roadmap items, and contribution links. These need short recap or **then → now → next contribution** treatment, not first-time announcements.
- **SDK overlap:** 2025's closing segment already explained cache read-after-write problems, optimistic locking, comparable resource versions and self-update filtering benefits. Attila's proposed 2026 segment should emphasize concrete advances; observability/virtual threads are not explicit topics in extracted 2025 content.
- **Chronology caution:** the 2025 deck has an explicit “What's New Since v1.0” slide. Explain the long foundational/compatibility investment without claiming literally no features throughout that entire interval.
- **Extraction limits:** slide text, notes and image metadata assessed; no video transcript, rendered-image meaning, animations or actual demo delivery established. Do not turn a slide's historical product claim into current release evidence.

### What the additions resolve

- The event and year are explicit. The presentation remains approximately thirty minutes, now confirmed for four speakers (three OLM, Attila SDK only), with concise illustrations/humor and linked online demonstrations rather than live demos.
- Published OLMv1 docs and two selected **draft** pages are explicitly separate source tiers. Published location is not itself a release pin; draft is not automatically imaginary or absent from source.
- The local PowerPoint export closes the content-access gap for integration material. It does not provide transcripts of the three earlier talks.
- Four local upstream clones are available for narrow, version-recorded checks. No repository-wide ingestion or remote refresh was performed.
- Talk terminology is **ClusterObjectSets / phased installation**, not the internal BoxCutter implementation name.
- `library-olm` is intended to centralize reusable lifecycle concepts, notably migration and successor resolution. That is the user's project intent; inspected documentation below establishes prototype migration workflows, not successor-resolution API coverage.

### New source assessments

| Source | Evidence | Talk implication |
|---|---|---|
| [Draft ClusterObjectSets](https://operator-framework.github.io/operator-controller/draft/concepts/clusterobjectsets/) | Cluster-scoped immutable revision content, ordered phases, readiness gates, ownership transitions, archival, collision protection, inline/referenced objects. | Concrete basis for a phased-rollout illustration. Treat as draft/alpha-path behavior, not standard released support. |
| [Draft deployment customization](https://operator-framework.github.io/operator-controller/draft/howto/customize-operator-deployments/) | Explicit alpha `DeploymentConfig` feature gate; `ClusterExtension.spec.config.inline.deploymentConfig`; v0 SubscriptionConfig-style settings and merge/replace/append semantics. | Concrete example of configuration through APIs and reduced migration friction. Not arbitrary resource patching or control-plane tenant isolation. |
| [Migration specification overview](https://github.com/operator-framework/library-olm/blob/main/specs/20260821-migration-v0-to-v1/README.md) | Explicit upstream prototype: migrate catalogs first, then check/convert/rollback/cleanup operators; eligibility/conflict reporting, dry-run previews, management handoff via ClusterObjectSets. | More actionable than the root README. Supports a prototype readiness-check/demo story; no commands were run or downtime/rollback guarantees independently validated. |

Only these three additional public pages and a recheck of the library root README were fetched in this pass. No new general Kubernetes/Helm crawl.

#### ClusterObjectSets: explanation worth retaining

1. A ClusterExtension expresses installation intent; its managed ClusterObjectSet revisions represent phased resource rollout.
2. Resource groups apply in phase order; objects **inside a phase have no defined order**. Progress waits on applicable readiness probes.
3. operator-controller assigns a resource-kind-based order: namespaces/policies/identity/configuration/storage, then CRDs/RBAC, infrastructure/deployments, and publication/admission resources. This is the controller's policy, not a universal order enforced by the ClusterObjectSet API.
4. During an upgrade, old and new revisions remain active while objects transition ownership; the old revision is archived after completion. This does **not** imply duplicate running controllers or automatic rollback on failure.
5. Default readiness checks and experimental custom probes are distinct. A custom probe whose selector matches no objects passes; a passing probe is not proof of overall application correctness.
6. Collision controls govern resource adoption, not general upgrade correctness. Avoid framing adoption as risk-free takeover.

Use one small conceptual sequence such as **API established → permissions present → controller ready → admission published**, not all thirteen controller phases on a slide. Link fuller examples online. No need to expose implementation-brand terminology to the audience.

#### Deployment customization: explanation worth retaining

- The draft exposes env/envFrom, resource requests/limits, node selectors/tolerations/affinity, volumes/mounts, and annotations through a configuration object.
- It reuses v0 SubscriptionConfig concepts, while documenting that the unused `selector` field is excluded.
- Semantics are field-specific: resources/nodeSelector replace; tolerations/volumes append; env merges. Annotation conflicts are documented to favor bundle values. Do not promise all configuration always overrides package content.
- A `watchNamespace` configuration pass-through is not a promise of namespace-isolated CRD definitions, OLM-managed tenancy, or watch-aware automatic dependency resolution.
- Treat draft YAML as illustrative until matched against a target schema: examples omit `configType` required by the previously reviewed live API; one migration example uses singular `channel` while that API lists `channels`. No runnable demo has been validated from these examples.

### Local implementation provenance

All paths below are under `~/devel/operator-framework/`. Revisions are local observations, not proof of remote freshness or released support.

| Clone | Branch / short HEAD | Intended evidence role |
|---|---|---|
| `api` | `skip-range-upper-check` / `0387562` | Shared APIs, CSV/Subscription/bundle metadata contracts. Topic branch: record provenance before relying on changed behavior. |
| `operator-registry` | `skip-range-upper-check` / `eb319415` | Catalogs, packaging, registry+v1 handling. Same topic-branch caveat. |
| `operator-lifecycle-manager` | `master` / `580b74d64` | OLMv0 behavior; available, not newly ingested. |
| `operator-controller` | `main` / `147a4c17` | Focused v1 code/doc review; HEAD commit date October 5, 2026. |

Six selected operator-controller files had no staged/unstaged changes during inspection:

- `api/v1/clusterextension_types.go:89–97`: `serviceAccount` deprecated/ignored; comment explicitly identifies manager-owned cluster-admin credentials and ClusterExtension write access as delegated cluster-admin trust.
- `cmd/operator-controller/main.go:505–536,634–713`: runtime/configuration wiring; current ClusterObjectSet path selected by the runtime gate, otherwise Helm; manager credentials in both paths. Internal use of Helm does not establish native Helm-chart catalog-content support.
- `internal/operator-controller/features/features.go:54–67`: `BoxcutterRuntime` and `DeploymentConfig` **Alpha, default false** in this checkout. Use the gate name only in reproducibility notes.
- `api/v1/clusterobjectset_types.go:42–176,224–251,493–571`: actual cluster-scoped revision API, phase/probe semantics, and current status model.
- `docs/draft/concepts/clusterobjectsets.md:59–117,154–212`: draft rollouts/status/ClusterExtension relationship.
- `docs/draft/howto/customize-operator-deployments.md:5–40,94–224`: draft alpha configuration instructions/merge semantics; renderer semantics not independently traced in this pass.

**Security-model ambiguity narrowed:** live API text agrees with this checkout's API comments and runtime wiring. The older user-provided installation-service-account design is historical, not the current model evidenced here. Release history and downstream behavior remain unexamined; do not generalize to every OLMv1 release.

**Status-model drift found:** the draft ClusterObjectSets page describes `Progressing`, `Ready`, and terminal `Succeeded`; the migration overview waits for `Succeeded=True`. The inspected current Go type describes `Ready` and immutable `completedAt`. Match docs, migration tool, gates, and controller revision before producing runnable examples. This is a compatibility/documentation warning, not proof the migration implementation is broken; no migration code or tests were executed.

### Existing integration deck

Source: `~/Downloads/Copy of KubeCon2026.pptx`. Text/OOXML extracted without modifying the source; **13 slides, no substantive speaker notes**. Extraction used a temporary standard-library document-processing helper because markitdown and the unpack script's defusedxml dependency were unavailable. No dependency installation or embedded-link browsing.

Title: **“The Next Era of Kubernetes Operator Lifecycle Management.”** The deck lists **Attila Mészáros @ Apple** and includes “Not a contribution.” These are extracted words, not a confirmed overall title, lineup, or interpretation of the disclaimer.

| Slides (1-based) | Extracted topic |
|---|---|
| 1–2 | Title/disclaimer and Attila's bio. |
| 3–4 | Java Operator SDK read-cache-after-write consistency, v5.3 reference; paired image-led slide. |
| 5–6 | Event filtering, self-updates/informer event-loss/concurrent updates; paired image-led slide. |
| 7–8 | Shared informer pools and configuration/registration; paired image-led slide. |
| 9 | Logging/MDC, metrics, MicrometerMetricsV2, dashboards and observability examples. |
| 10–11 | Java virtual threads, explicitly WIP/planned v5.7.0, Java-version claims; paired image-led slide. |
| 12 | EventRecorder, ShardSelector, operations-documentation mentions. |
| 13 | Thank-you / Q&A. |

This is predominantly **controller-development/runtime material**, not OLM package migration or catalog policy. The user confirms it is Attila's segment in the same thirty-minute session, typically the final portion. Do not allocate the whole session to OLM; exact segment duration still needs agreement.

There is no extracted OLMv0/v1 migration content to duplicate directly. A potentially useful bridge is **developer tooling/runtime in any language ↔ packaged extension lifecycle on a cluster**. Keep that distinction explicit: SDK runtime language is not an OLM language requirement.

The concept/text → image-led explanation pattern may be reusable. Four image-led slides are present (4, 6, 8, 11), but image content, humor, layout quality, and animations were not visually assessed. Do not claim their illustrations were evaluated. The virtual-thread WIP/version claims require a fresh SDK baseline only if retained.

### Remaining questions, prioritized

1. **Time allocation and audience:** SDK material is confirmed as the usual final segment of the shared thirty-minute session. Exact allocation, audience/accepted abstract and final title remain open; no need to ask whether the SDK material belongs in the session again.
2. **Reproducible baseline:** maintainer-update framing with accomplished and planned work is confirmed. Select a release/commit and feature-gate combination for examples; clearly label alpha/prototype/planned capabilities. No need to ask whether forward-looking content is desired again.
3. **Design follow-through:** catalog/Helm planning docs and evolution musings are supplied/read; October 2 schema-first direction and `helm+v2` are confirmed. Align old wording and refine lifecycle/constraint schema; successor-library implementation evidence and validated migration/Helm examples remain open. Do not ask for already supplied links or repeat resolved decisions.

Lower priority unless needed for a chosen slide: video transcripts, a historical downgrade incident, a catalog performance artifact, a versioned OperatorHub compatibility dataset, permission for public internal-document quotations. No need to request the event date, another deck export, local clone paths, or the two draft URLs again.

## Bottom line

The seed supports a coherent story: **OLM learned to work with Kubernetes' actual scope and ownership model, then expose lifecycle primitives rather than hide administrator decisions.** This is a working thesis, not a finalized talk outline.

The evidence is sufficient to discuss the architectural trade-offs. It is NOT yet sufficient to assert release-specific feature availability, broad migration readiness, an OperatorHub compatibility percentage, or measured performance gains. Stop here for targeted documentation rather than a wider crawl.

### Presentation constraints retained

- Approximately 30 minutes; four speakers confirmed: three OLM presenters plus Attila exclusively on Java SDK.
- Concise slides, strong illustrations, accurate information, humor tied to concepts.
- Local development first; manually integrate later with the supplied PowerPoint/Google Slides material.
- Prefer linked online-only demos. No live demos by default; any essential in-talk demonstration must be brief.
- This assessment creates no slide deck, artwork, or demos yet.

## Supplied resource assessment

| Resource | Access / review | Value and caveats |
|---|---|---|
| `../kubecon-2026.txt` | Original reference, read completely | Strong thesis and topic inventory. Mixes history, capabilities, proposals, and measurement-dependent claims; label these separately before drafting slides. |
| Catalog v2 brief `1J98HtTLvZC83XJawHqPJlrAxOlEWsR9UoftNc1Gfhck` | Google Docs MCP, full 14,237-character return | Schema responsibilities are concrete; October 2 note defers transport and removes channels/graphs. Planning, not tested release/performance evidence. |
| Helm brief `1HTP4T14OBxxSJKfj8vgAJUSGS5hMNHEWjddqEJYcPXc` | Google Docs MCP, full 20,375-character return | Concrete restricted chart-rendering/ownership proposal, with discriminator and dependency inconsistencies. Planning targets, not GA availability. |
| `../2026-olm-evolution-musings.md` | Original reference, explicitly requested, 279 lines read | Strategic four-stage discourse. Retain compositional governance/trust-boundary framing; do not elevate comparative absolutes or dependency-return conjectures. |
| 2025 Google Slides deck `1_WK8mNw3pERO6U96ptlW3pKiQDvZdBpk12kRN5orIqk` | Retrieved via temporary read-only MCP adapter and authenticated Drive export; 27 slides plus notes, one hidden duplicate | Actual prior-message baseline now available in `kubecon-2025-slide-context.md`; no further access/export request needed. |
| Google Doc `1FGOpUev0V7uzkQMMEf3vp3rJ27gR29O2XSHWYOftOdA`, returned heading “OLM v1 Overview” | Read complete returned text, 34,654 characters | High value for design intent: global APIs, non-shared ownership, predictable administration, guardrails/escape hatches, dependency limits, and a smaller API surface. Low authority for current implementation: explicitly draft solution/roadmap, namespace-scoped `Extension`, Carvel/Rukpak plans, and future-tense features. Confirm permission before public quotation or screenshots. |
| Prior talk, YouTube ID `HrwHh5Yh6AM` | Not consumed | Transcript retrieval blocked: `fabric` is not installed. Seed URL starts at 26:59; clarify whether that passage or the whole talk is relevant. Request transcript or slides. |
| Prior talk, YouTube ID `XaIXWHKuzzI` | Not consumed | Same missing transcript-tool prerequisite; no additional extraction-service attempts. Request transcript or slides. |
| Prior talk, YouTube ID `941ywkgnmIw` | Not consumed | Same missing prerequisite. No title, speaker, argument, or humor inferred from the URL. Request transcript or slides. |
| Google Slides deck `12fq4rSg6uivQqy2bp9tsx0piG_3-3y2Jc1Lwg80rG1c` | First-pass web fetch returned HTTP 401; second-pass local PPTX content is now assessed above | Web failure did not test authenticated access. Supplied local export closes this content gap; no further export needed. |

Do not mistake the design document's old “4% of packages declare dependencies” estimate for a contemporary community compatibility statistic. Its example is a redhat-operators 4.14 catalog, not today's OperatorHub corpus; another table has a missing as-of date in the returned text.

## Bounded authoritative reference set

Fourteen distinct public pages were reviewed through successful web fetches. These are live documentation or a repository README, NOT release-pinned snapshots. No whole-site ingestion, OperatorHub enumeration, issue-history mining, or general ecosystem crawl was performed.

### OLMv0: mechanisms before historical interpretation

| ID / source | What it establishes | Assessment |
|---|---|---|
| V0-1 [Architecture](https://olm.operatorframework.io/docs/concepts/olm-architecture/) | Catalog Operator resolves content/dependencies and drives approved InstallPlans; OLM Operator checks CSV requirements and deploys the operator/RBAC. | Strong mechanism reference. A cache is described, but this is not a benchmark or evidence of distributed-cache cost. |
| V0-2 [Dependency resolution](https://olm.operatorframework.io/docs/concepts/olm-architecture/dependency-resolution/) | SAT-based solving of properties/constraints; catalog/channel/update-graph preferences; cluster-wide API coupling and cross-namespace update deadlock. | Best source for explaining complexity without unsupported complexity-class terminology. Does not prove an accidental downgrade incident. |
| V0-3 [OperatorGroup](https://olm.operatorframework.io/docs/concepts/crds/operatorgroup/) | Namespace targeting, install modes, generated RBAC, provided APIs, overlapping group conflicts; describes rudimentary multitenant configuration. | Explains what OLM scopes, not namespace-private CRD definitions or hard tenant isolation. |

Useful conceptual flow: requested package → resolution → approved InstallPlan → installed APIs/CSV → operator deployment. Keep package selection, API installation, controller execution, and operand reconciliation distinct.

### OLMv1: intent, documented APIs, and maturity conflicts

| ID / source | What it establishes | Assessment |
|---|---|---|
| V1-1 [Overview](https://operator-framework.github.io/operator-controller/) | Kubernetes extension lifecycle scope, simplified architecture, broad Helm/GitOps positioning. | Useful entry point; broad positioning is not proof of released native Helm-chart content support. |
| V1-2 [Design decisions](https://operator-framework.github.io/operator-controller/project/olmv1_design_decisions/) | Kubernetes-aligned ownership, opinionated defaults with administrator escape hatches, predictable lifecycle semantics, no first-class watch-namespace management or automatic dependency installation. | Strong rationale source; explicitly mixes implemented behavior and future plans. |
| V1-3 [Public API boundary](https://operator-framework.github.io/operator-controller/project/public-api/) | Kubernetes APIs and the catalogd web server are public surfaces; only documented public interfaces receive SemVer guarantees. | Distinguishes supported contracts from implementation details. |
| V1-4 [Limitations](https://operator-framework.github.io/operator-controller/project/olmv1_limitations/) | Current content described as OLMv0 `registry+v1`; dependency properties, CSV APIService definitions, and OperatorConditions restrictions. | Necessary counterweight to optimistic overview claims. Install-mode language needs clarification: AllNamespaces requirement alongside SingleNamespace/OwnNamespace backward compatibility. |
| V1-5 [API reference](https://operator-framework.github.io/operator-controller/api-reference/olmv1-api-reference/) | `olm.operatorframework.io/v1` ClusterCatalog/ClusterExtension, catalog/package/version/channel selection, status, documented overrides, fields labeled Standard/Experimental. | Best concrete API evidence, but especially important to pin to a release/channel. Contains major security-model drift relative to older design prose. |
| V1-6 [CRD upgrade safety](https://operator-framework.github.io/operator-controller/concepts/crd-upgrade-safety/) | Checks for unsafe schema/version/scope changes; a documented all-checks override. | Good bounded example of guardrails plus escape hatches; not a proof of overall application-upgrade correctness. |
| M-1 [library-olm README](https://github.com/operator-framework/library-olm) | Go libraries/CLIs and v0-to-v1 migration tooling. README calls the project personal and pre-release, with changing APIs. | Supports “tooling exists,” not production migration guarantees, portability coverage, or readiness percentages. |

Concrete examples supported by the live API reference:

- Package version pins/ranges, channel selection, and catalog selectors express installation/upgrade intent.
- `upgradeConstraintPolicy: CatalogProvided` respects package-author upgrade paths; `SelfCertified` bypasses them and permits upgrades/downgrades, with an explicit danger warning.
- `.spec.install.preflight.crdUpgradeSafety.enforcement` defaults to `Strict`; `None` skips the CRD checks. Bypass is administrator responsibility, not proof that an unsafe change becomes safe.
- The installation namespace field is not a promise of namespace-private APIs or watch scope.
- Some configuration, probe/revision, and deadline fields are explicitly Experimental. Their appearance in generated docs does not establish standard-channel release availability.

**First-pass source conflicts (second-pass resolutions noted):**

1. **Security:** old design promised user-provided installation accounts, unlike the live API's deprecated/ignored field and manager-owned cluster-admin model. Second-pass checkout evidence agrees with the live API; old design is historical. Still select the target release before making release-wide claims.
2. **Helm:** overview positioning versus limitations restricted to `registry+v1`. Distinguish an internal Helm-based installation mechanism from native Helm charts as supported catalog content.
3. **Migration:** overview says no concrete migration strategy; library README describes pre-release migration tooling. These can reflect different scope or publication age; obtain the intended migration workflow/release.
4. **Architecture:** old namespace-scoped `Extension`/Carvel roadmap is not the live ClusterExtension/ClusterCatalog contract. The seed's reason for dropping Carvel is maintainer context, not verified here.

### Kubernetes and Helm: avoid false comparisons

| ID / source | What it establishes | Assessment |
|---|---|---|
| K-1 [Custom resources](https://kubernetes.io/docs/concepts/extend-kubernetes/api-extension/custom-resources/) | API definitions versus instances; namespaced/cluster-scoped custom resources; controllers and the operator pattern. | Foundation for separating an API, its reconciler, and the application it manages. |
| K-2 [Multi-tenancy](https://kubernetes.io/docs/concepts/security/multi-tenancy/) | CRD definitions and other resources are cluster-scoped; namespace isolation needs RBAC/networking/security configuration; operators can act outside their deployment namespace. | Qualify “Kubernetes is not multi-tenant”: namespace-based tenancy exists, but independent per-tenant API definitions within one shared control plane are a different problem. |
| H-1 [Helm CRDs](https://helm.sh/docs/chart_best_practices/custom_resource_definitions/) | Standard `crds/` installation: non-templated, existing definitions skipped; no built-in upgrade/delete support through this mechanism; dry-run limitations. | Fair lifecycle comparison. Do not imply chart-authored jobs or external tooling cannot change CRDs. |
| H-2 [Helm hooks](https://helm.sh/docs/topics/charts_hooks/) | Lifecycle hooks, Job/Pod completion/failure behavior, readiness interaction, separate cleanup rules. | Helm has useful safeguards and extensibility; “Helm has no safety” is inaccurate. Hooks are not equivalent to continuous operator reconciliation. |

The fetched Helm pages identify version 4.3.0 and discuss behavior introduced in Helm 3. Match the presentation's Helm major/version before reproducing behavior or recommending flags.

Keep four layers separate: **package format/distribution, installation, upgrade policy/checks, and continuous application reconciliation.** Helm chart dependencies (subchart/package composition) are not interchangeable with OLMv0's installed package/API constraint solving. Detailed dependency comparison still needs version-matched Helm dependency docs.

## Seed claims: retain, qualify, or seek evidence

| Seed topic | Treatment now | Smallest useful next artifact |
|---|---|---|
| OLM began before CRDs; expected namespace-restricted APIs | Historical claim, not established by current docs | Dated original proposal/design discussion or maintainer-approved timeline; distinguish ThirdPartyResources from CRDs. |
| Namespace-based API visibility / tenancy is leaky | Retain precise distinction between cluster-scoped definitions, namespaced instances, discovery/authorization, and reconciliation scope | Existing K-1/K-2/V0-3 references suffice for mechanism; maintainer history for original intent. |
| “NP-incomplete” dependency solving | Remove that terminology pending a precise argument. Prefer “SAT-based constraint solving over coupled cluster state.” | Resolver design/technical analysis only if complexity theory is genuinely essential to the talk. SAT usage alone does not classify the entire product problem. |
| Unintended downgrades affecting other namespaces in the cluster | Documented coupling/deadlocks are supported; actual downgrade claim is not yet supported | One reproducible version-specific incident/issue showing before/after catalog graph and installed CRD/operator state. |
| Resource-intensive caching/catalog performance milestones | Qualitative hypothesis, not measured improvement | One before/after benchmark or profiler report, workload/catalog scale, component versions, and milestone PR. |
| Language neutrality | Keep, with clearer packaging terms | Bundle-format reference plus one non-Go example. A bundle image packages manifests/metadata; it is not necessarily the operator's runnable workload image. Tooling language must not be confused with runtime language. |
| Two years of work with hundreds of teams | Maintainer-reported effort, not a quantified public fact yet | Speaker-approved timeline and scoped adoption/readiness summary. |
| Vast majority of operators compatible | No numerical or “vast majority” conclusion yet | Versioned catalog snapshot and results of an agreed compatibility check. |
| ClusterObjectSets installation phases | Second pass establishes draft mechanics plus local alpha-gated implementation; omit internal runtime branding from talk | Select a release/gate baseline and validated representative example; avoid draft status-model drift. |
| Migration / test portability now | Prototype migration overview documents eligibility checks and management transfer; no execution validation | Confirm endorsed tool version, eligibility-check scope, matched controller status model, and known limitations. |
| Evolved catalog schemas, new packaging, Helm bundles | Canonical planning briefs read; schema-first direction and `helm+v2` now user-confirmed | Align older examples/dependency wording; actual implementation/release/performance evidence still needed for capability claims. |
| Arbitrary resources, Argo CD/Flux integration, LLM models | Inspiration, not demonstrated current capability | Include only after agreeing audience value and intended integration semantics. LLM-model packaging is especially likely to distract from the 30-minute thesis. |

### If an OperatorHub compatibility figure is desired later

Agree on **which catalog**, snapshot digest/date, OLM release/channel, and **what compatibility means** before downloading content. Package count, bundle count, and installable current channel heads give different denominators. A metadata portability check is not a successful install, upgrade, webhook operation, or operand test. Report those separately, classify failures, and publish numerator/denominator/method alongside any percentage. The old Red Hat dependency estimate cannot substitute for this.

## Targeted documentation queue — ask before ingesting

### Current priority

Use the revised questions above. Event dates, references, four-speaker SDK-only integration, maintainer-update goals, schema-first catalog direction and canonical `helm+v2` are confirmed/supplied. Release pinning, time allocation, audience/title, remaining schema/implementation work and vetted contribution destinations remain open.

### Nearby notes discovered, NOT read

Potentially high-value still-unread original sources in the parent directory: `../olmv1-helm-bundles.md`, `../olmv1-helm-pr-sequence.md`, `../operatorhub.io-fbc.md`, `../opm-v2-functional-gap-analysis.md`, and `../oci-native-v2-sketch.md`. `../2026-olm-evolution-musings.md` has been explicitly requested and read. Ask before expanding to the others; filenames do not establish conclusions or implementation status.

### Lower priority unless a specific slide requires them

- One historical downgrade incident and one catalog performance benchmark.
- FBC/registry+v1 specifications and only the proposed schema sections needed for the new-content comparison.
- Version-matched Helm chart dependencies, install/upgrade/rollback options.
- Argo CD Helm rendering/release-management and sync/hook/pruning semantics; Flux HelmRelease/helm-controller reconciliation, CRD policies and remediation. Select Argo CD, Flux, or both based on the intended example; do not survey every GitOps implementation.
- Kubernetes CRD versioning/conversion and ownership/garbage-collection references if needed for the chosen upgrade or migration example.

## Illustration and demo opportunities — not yet a deck plan

- **One API definition, multiple namespace rooms:** namespaced instances share the building's API plumbing. Humor should target the incorrect model, not users or past maintainers; do not draw namespaces as security-proof walls.
- **Guardrails and a clearly marked override:** two small API excerpts can show upgrade-path policy and CRD preflight bypass. Say the override changes responsibility, not the underlying risk.
- **Lifecycle layers:** show chart/bundle packaging, catalog policy, installer, operator, and operands as separate responsibilities. Helm and operators can compose rather than compete.
- **Linked reproducible examples:** a rejected unsafe CRD change, a version-range upgrade decision, and a portability assessment. Use captured results or an illustration in the room; put runnable instructions online with pinned versions.
- Four-speaker handoffs follow problems learned → present primitives → content/catalog/contributions → Attila's SDK-only material. Timings and OLM role identities remain proposed; avoid adding four separate biography sections.

## What these passes did not establish

Both the 2025 prior deck and the proposed 2026 PPTX textual content are now consumed; rendered visuals and earlier videos are not. No releases, migration checks, or demos were executed. No adoption counts, compatibility percentages, performance numbers, historical chronology, or released support claims were independently measured. Current-checkout security behavior is established by bounded source evidence; release/gate selection and draft status-model drift still need resolution for runnable examples. The 2025 roadmap and feature claims provide historical message context, not current capability verification.
