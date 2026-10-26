# KubeCon NA 2026 — presentation and companion package outline

Draft 3 · 2026-10-09 · Event: November 9–12, 2026. Generated working content lives in `~/devel/breadcrumbs/2026-kubecon-wip/`.

**Current dry-run revision:** see `dry-run/slide-data.json` for the reordered OLM material and `dry-run/deck-manifest.json` for the combined25-slide order. History opens the content section; direct bundle installation is included; original SDKtechnicalsource slides3–12 are retained unchanged as output14–23. The older twenty-beat/condensed-SDK treatment below is planning history and must not be reused as an approved SDK content rewrite.

## Confirmed title and session scope

**The Next Era of Kubernetes Operator Lifecycle Management**

The user confirmed this title for the 2026 talk. The regenerated dry-run copy in `dry-run/slide-data.json` follows the latest language preferences. Older proposed slide headlines below are planning history and require the same style review before reuse. Speaker ownership remains in notes.

**Audience takeaway:** understand why lifecycle progress required foundational and compatibility work, identify practical OLM/SDK improvements, and leave with a specific way to test content or contribute.

**Narrative:** the hard boundary we learned → the groundwork that followed → concrete lifecycle controls → broader content and shared logic → reliable controllers → your next contribution.

The 2025 talk explained why v1 was a reimagination. This year's talk must demonstrate progress against that intent, not repeat the pitch. Use **then → now → next contribution** where a topic was already on last year's roadmap.

### Draft assumptions

- One approximately 30-minute session; familiarity with Kubernetes assumed, deep OLM expertise not assumed. Adjust to accepted abstract/audience when supplied.
- **Four speakers confirmed:** three OLM presenters plus Attila. **A:** OLM context/host (Jordan suggested, not assigned). **B:** OLM lifecycle primitives (unassigned). **C:** OLM content/catalogs/contributions (unassigned). **D:** Attila, exclusively Java Operator SDK, final substantive segment. Do not assign him OLM exposition, roadmap or contribution ownership.
- Proposed allocation: **A 4 minutes + B 8 minutes + C 5 minutes + D 10 minutes + OLM-led close 1 minute + questions/buffer 2 minutes = 30 minutes.** Exact allocations and A/B/C identities require speaker agreement. Attila answers SDK questions only; A/B/C handle OLM questions.
- Twenty slide beats including title, a brief language-neutral handoff, shared closing slide and Q&A. Several can be combined during layout; this is not a mandate for twenty dense slides.
- No live demonstrations. Slides use illustrations or static captured outcomes; runnable examples live online. At most one optional 15–20-second recording, replacing—not extending—its slide's time.
- This draft creates no presentation/artwork/demo assets. It specifies the package to develop locally before manual deck integration.

## Status and evidence conventions

Use a small, consistent badge for **Released**, **Alpha / Prototype**, or **Planned** when status matters. “Released” requires a selected release and supporting evidence; appearance on the published docs site alone is insufficient. Until pinned, speaker notes say **release verification pending**.

Current evidence from the resource assessment:

- ClusterObjectSet runtime and DeploymentConfig: implemented **Alpha, disabled by default** at inspected local operator-controller `147a4c17`; draft documentation has status/example drift.
- library-olm migration: **Prototype** specification/workflow, not an independently tested supported migration product.
- Native Helm catalog content and revised catalog schemas: **Planned / design discussion**, now grounded in supplied August briefs and the catalog's October 2 update. This supplies canonical planning context, not implementation/release evidence. Successor/constraint/lifecycle semantics remain partly open.
- Current catalog direction is user-confirmed: short-term work focuses on well-defined, flexible schemas; OCI-native catalog storage/transport is future work. The October 2 removal of channels/legacy graphs and open lifecycle schema are the current direction, not provisional assumptions.
- Canonical Helm content representation is **`helm+v2`**, corresponding to versioned Helm packaging expressed through OLM-compatible catalog schemas. This is not a Helm CLI major-version claim; older `helm+v1` proposal examples are superseded. Schema/catalog representation does not itself introduce a registry+v1 wrapper-image requirement.
- SDK claims: verify against Attila's selected release. Virtual-thread material is currently WIP in his proposed deck; do not turn a proposed version into a release promise.

## Run of show

| Slide | Start | Duration | Speaker | Working headline |
|---:|---:|---:|---|---|
| 1 | 00:00 | 00:45 | A | Operator lifecycle, beyond the install button |
| 2 | 00:45 | 00:45 | A | Last year: the direction. This year: the work you can use. |
| 3 | 01:30 | 01:15 | A | Different namespaces. Shared API definitions. |
| 4 | 02:45 | 01:15 | A | Rebuild the foundation without abandoning its users |
| 5 | 04:00 | 01:30 | B | State your intent; see the decisions |
| 6 | 05:30 | 02:00 | B | Rollouts you can inspect |
| 7 | 07:30 | 01:30 | B | Configure the deployment, not a fork |
| 8 | 09:00 | 02:00 | B | Migration should transfer management—not force a reinstall |
| 9 | 11:00 | 01:00 | B | Shared lifecycle logic, fewer divergent answers |
| 10 | 12:00 | 02:00 | C | Your chart, OLM-managed lifecycle—not a Helm release |
| 11 | 14:00 | 01:30 | C | Metadata once. Versions explicit. Content typed. |
| 12 | 15:30 | 01:00 | C | Bring us a package, an edge case, or a first PR |
| 13 | 16:30 | 00:30 | C → D | Any language. Two complementary lifecycle layers. |
| 14 | 17:00 | 00:45 | D | From last year's consistency problem to this year's improvements |
| 15 | 17:45 | 02:00 | D | Make updates visible; avoid unnecessary reconciliation |
| 16 | 19:45 | 02:30 | D | Share informers without sharing confusion |
| 17 | 22:15 | 02:15 | D | See what your controller is doing |
| 18 | 24:30 | 02:30 | D | Virtual threads: simpler execution, explicit limits |
| 19 | 27:00 | 01:00 | A / OLM team | Use it. Test it. Help shape it. |
| 20 | 28:00 | 02:00 | Topic owners | Questions / buffer |

Handoff at **17:00 is protected**. The SDK section is not whatever time remains after OLM. Questions/buffer includes applause, small transition overruns and brief Q&A; confirm conference expectations if longer questions are required.

## Slide-level treatment

### Act I — Why the investment was necessary (4 minutes)

**1. Operator lifecycle, beyond the install button**
- Message: this is a progress-and-participation update, not another first-install tutorial.
- Visual: one lifecycle line: **package → install → upgrade → operate**; OLM and SDK responsibilities sit on different layers, not opposing teams.
- Opening: “Last year we described the direction. Today: what that foundation lets you do—and where you can help.” Speaker names live here; no separate biography round.

**2. Last year: the direction. This year: the work you can use.**
- Message: turn selected 2025 roadmap items into a progress ledger: rollout revisions, deployment configuration, migration, broader content.
- Visual: three columns **2025 intention / present evidence / next task**. Fill with honest status badges, not a wall of checkmarks.
- Do not imply everything is released or claim literally no features appeared: 2025 explicitly had a “What's New” slide.
- Difference from 2025: outcomes/accountability replace the “reimagination” comparison table. No old download counts or compatibility percentages.

**3. Different namespaces. Shared API definitions.**
- Message: namespace-scoped custom-resource instances do not create separate CRD definitions; controller watch scope is a third concern. This bounds promises about tenant independence and dependency-driven upgrades.
- Visual: two namespace rooms with different resource instances, connected to one shared API-definition layer. Caption: **“Different rooms. Same plumbing.”** Do not draw a namespace as a guaranteed security wall.
- One example is enough. No complexity-class lecture or unsupported “NP-incomplete” phrase.
- Difference from 2025: one short mechanism illustration instead of retelling the whole install-mode history. Pre-CRD origin/forecasting detail belongs in notes only if historically verified.

**4. Rebuild the foundation without abandoning its users**
- Message: compatibility with existing registry+v1 content, API/ownership changes, operational behavior and migration preparation compete for engineering attention. Connect each selected investment to a user-visible payoff.
- Visual: existing content crossing a bridge while supports are replaced. Caption: **“Renovation with the tenants still inside.”** This is an analogy, not a guarantee of zero migration downtime.
- Speaker line: “The work wasn't just adding a new path. It was making that path useful to the people already depending on the old one.”
- Include measured catalog/cache progress only if a benchmark is supplied; otherwise omit performance numbers and keep the rationale qualitative. No unverified “hundreds of teams” or “vast majority compatible” claim.
- Handoff A → B: **“What does that investment buy an author or administrator?”**

### Act II — The payoff: concrete lifecycle primitives (8 minutes)

**5. State your intent; see the decisions**
- Message: package/version/channel intent, visible status, upgrade-path controls and CRD checks are more useful than hidden lifecycle decisions.
- Visual: a small intent card feeding a catalog selection/guardrail/status diagram; at most a few API fields, not a complete CR.
- Guardrails/escape hatch caption: **“Override is a decision—not a safety certificate.”** CRD checks are bounded, not complete application-upgrade verification.
- Difference from 2025: one practical decision flow replaces “Kubernetes-native” adjectives. Pin the target release before marking fields Released. Do not recycle the old delegated-installation-account security claim.

**6. Rollouts you can inspect**
- Message: show the evolution from last year's ClusterExtensionRevision story to ClusterObjectSets: ordered phases, readiness boundaries, inspectable revision content and ownership transitions.
- Visual: **API established → permissions present → controller ready → admission published**, with a paused gate and two revision cards. No thirteen-phase taxonomy.
- Status: **Alpha** at the inspected checkout. Explain what changed beyond the name; verify that specific delta before finalizing the slide.
- Do not promise automatic rollback, transactional upgrades or application-level availability. Old/new active revisions do not imply duplicate controllers.
- Online example pointer: deliberately block one readiness gate, inspect it, fix the cause, observe progress. Static before/after only in the room.

**7. Configure the deployment, not a fork**
- Message: express env/resources/scheduling intent through configuration; reuse familiar v0 concepts without editing generated deployments or forking package manifests.
- Visual: a tiny configuration card → generated deployment with one highlighted change.
- Status: **Alpha, DeploymentConfig gate**. Merge/replace/append behavior is field-specific; avoid broad “all overrides win” promises.
- Difference from 2025: roadmap intention becomes a concrete draft API/example. Namespace configuration pass-through does not restore namespace-private CRDs.
- Contribution seed: supply one realistic configuration fixture or a reproducible mismatch.

**8. Migration should transfer management—not force a reinstall**
- Message: prototype migration tooling assesses eligibility and transfers lifecycle management; it should not be framed as “delete the operator and hope.”
- Visual: running workload stays in place while a management badge moves from v0 to v1, with **check / preview / transfer / recover** milestones.
- Status: **Prototype**. Catalog migration first; eligibility checks and explicit blockers; namespace changes may require restarts/downtime. Rollback is a prototype workflow, not an unqualified guarantee.
- Difference from 2025: migration was a future bullet; now show a concrete workflow and captured eligibility output after validation.
- Online pointer: read-only check plus a documented interpretation of one blocker. Do not give an untested command a “run this now” instruction.

**9. Shared lifecycle logic, fewer divergent answers**
- Message: library-olm's intended role is to centralize migration and successor-resolution concepts rather than duplicate rules in controllers, CLIs and tooling.
- Visual: several consumers pointing at one contract/test-fixture set. Caption: **“One rule, fewer slightly different answers.”**
- Status: migration prototype is documented; successor-resolution API/implementation evidence is still needed. State the intent without claiming all consumers already share one implementation.
- Contribution seed: a representative upgrade graph or expected-result fixture for maintainer-reviewed semantics.
- Difference from 2025: turn legacy graph/self-service friction into a bounded shared-logic problem.
- Handoff B → C at 12:00: **“Those primitives give us the lifecycle boundary. What else should we be able to package inside it?”**

### Act III — Broader content and approachable contributions (5 minutes)

**10. Your chart, OLM-managed lifecycle—not a Helm release**
- Message: proposed first-class Helm content uses the chart's standard OCI artifact, without a registry+v1 wrapper. Inline values feed a Helm-based manifest provider; rendered objects enter OLM's ownership/application lifecycle, not Helm CLI release management.
- Visual: **chart OCI artifact + inline values → rendered objects → OLM lifecycle**, with a small compatibility checklist. Caption: **“Bring the chart. Read the lifecycle contract.”**
- Status: **Planned proposal**, expected quarter is not a promised release. No implementation check was performed. Internal Helm use by OLM is not proof this content path has shipped.
- Make the supported subset explicit: embedded subcharts; no hooks or `keep`; no unstable rendering functions; proposed rejection of `crds/` in favor of CRDs in `templates/`. Do not imply any chart works unchanged or that moving CRDs is risk-free.
- Notes: chart release-object mappings and CRD deletion/data-loss implications need confirmation. Use canonical `helm+v2`; update older transport/channel dependency language to the confirmed schema-first direction. Do not reintroduce deferred OCI-native catalog storage as an immediate prerequisite without new evidence.
- Difference from 2025: a concrete artifact/rendering/compatibility contract replaces the old “Helm charts!” roadmap bullet.
- Contribution seed: a representative chart/values fixture or hook/CRD compatibility case. Link a maintainer-reviewed validation task, not an invented available publisher command.

**11. Metadata once. Versions explicit. Content typed.**
- Message: proposed v2 schemas separate catalog policy, package-common metadata, decorators and versioned content; version/release and content type become explicit. Existing v1 catalogs should remain unaffected; v0 forward compatibility is not promised.
- Visual: one package metadata card beside registry+v1 and Helm content cards with version/type labels. Optional icon card is visibly separate. Caption: **“A package biography should not be copied into every edition.”**
- Status: **Planned implementation**, with the catalog's later October 2 note now confirmed: channels/legacy graphs removed, storage changes deferred, lifecycle schema still open. Focus this slide on well-defined, flexible schemas. Do not promise complete author-defined lifecycle constraints before that schema exists.
- Efficiency rationale: less duplicate metadata and more direct identity. No achieved speedup claim; per-package OCI/lazy fetch benefits belong to the deferred transport appendix.
- Difference from 2025: legacy graph and self-service problems become concrete schema decisions and validation tasks.
- Musings bridge: OLM can aim to complement existing packaging/GitOps through a clear lifecycle contract. Argo/Flux delegation and return of automatic dependency installation remain hypotheses; emitting their CRs does not automatically govern descendant CRDs.
- Contribution seed: v1/v2 coexistence fixture, unknown-property/constraint behavior, or a bounded lifecycle-metadata question. LLM packaging remains outside the main narrative.

**12. Bring us a package, an edge case, or a first PR**
- Message: three entry points, not a generic “contributions welcome” invitation:
  1. **Content author:** provide one chart/values fixture and a specific compatibility obstacle, or an existing operator case.
  2. **Platform practitioner:** reproduce one rollout/configuration edge case with a minimal fixture.
  3. **Contributor:** improve one maintainer-vetted schema/coexistence fixture, template-determinism test or lifecycle-metadata question.
- Visual: three small task cards with prerequisites, expected result and destination. One short URL/QR to the resource hub, plus printed URL for accessibility.
- Do not invent issue IDs, guarantee ten-minute completion or imply all planned formats already have tooling. Resource hub must contain genuinely actionable tasks before publication.

**13. Any language. Two complementary lifecycle layers.**
- Message: OLM manages packaged cluster-extension lifecycle; an SDK helps authors implement continuous reconciliation. Bundle manifests/metadata and runnable controller images are distinct artifacts. Neither OLM nor the bundle format requires Java or Go.
- Visual: language-neutral controller/workload images above OLM packaging; zoom into one Java controller's runtime for Attila.
- Handoff C → D: **“That gets the extension onto the cluster. Now, what makes the controller dependable once it's running?”** Attila owns only the Java SDK portion from here.

### Act IV — Reliable controllers: Attila's segment (10 minutes)

This is a proposed condensation of his existing material, **subject to his agreement**, not an edit to his source deck. Preserve his concept/image pairings where they improve explanation; the five beats below may become more than five visually sparse slides while keeping ten minutes. Reuse one shared title/bio and one shared closing/Q&A rather than duplicating them.

**SDK novelty gate:** slides 14–15 must identify a verified post-2025 change or a genuinely new operational lesson, not merely state that the functionality shipped. If that evidence is absent, combine them into a 30-second recap and give the recovered **2:15** to informer pools/observability, by Attila's choice, within his protected ten minutes.

**14. From last year's consistency problem to this year's improvements** (00:45)
- One-image recap of the stale-cache/concurrent-update problem; do not repeat the 2025 resourceVersion/optimistic-locking tutorial.
- Establish which improvements are delivered in the selected SDK/Kubernetes baseline.

**15. Make updates visible; avoid unnecessary reconciliation** (02:00)
- Combine read-cache-after-write guarantees with self-update filtering; show one before/after event sequence and a concurrent-actor caveat.
- Reuse proposed source slides 3–6 selectively. Difference from 2025: concrete delivered behavior and a new edge case, not just the old motivation.
- Visual caption option: **“I changed it. I saw it. I don't need to argue with myself.”** Label whose writes/events are involved; don't imply all events may be ignored.

**16. Share informers without sharing confusion** (02:30)
- Explain the resource motivation, matching-configuration contract, and dynamic registration/deregistration with a shared-pool diagram.
- Proposed source slides 7–8. Shared pools add specificity to last year's overlapping-informer discussion.
- No performance ratios without measured data. The diagram should show that not all configurations share the same informer.

**17. See what your controller is doing** (02:15)
- Show one concrete logging/event/metrics workflow and a readable dashboard excerpt; avoid inventorying every API name.
- Proposed source slide 9. An optional example screenshot can link to the OTel/Prometheus/Grafana walkthrough online.
- Contribution seed: reproduce one missing diagnostic or improve a focused observability example.

**18. Virtual threads: simpler execution, explicit limits** (02:30)
- Preserve the distinction between execution mechanism and bounded concurrency/backpressure; avoid “unlimited reconciliation.”
- Proposed source slides 10–11; **Planned/WIP unless Attila confirms release status** and supported Java versions.
- If not ready or deprioritized, Attila may replace this beat with a stronger delivered SDK example using source slide 12 or deeper observability. Do not silently delete the section or steal its time for OLM.

### OLM-led session close (1 minute) and topic-owned questions/buffer (2 minutes)

**19. Use it. Test it. Help shape it.**
- Three audience actions: **test your content / share a real edge case / take one scoped contribution**.
- Single resource-hub URL/QR linking both OLM and SDK tracks; distinguish immediately usable examples from design feedback opportunities.
- Closing line: **“You don't need to rewrite your operator to help. Bring the package, the case, or the question.”** Avoid implying every operator is already portable.

**20. Questions / buffer**
- Keep resource URL visible. No new roadmap material or surprise live demo.
- A/B/C handle OLM questions; Attila handles Java SDK questions only. The host delivers the overall resource pointer; no OLM closing material is assigned to Attila.

## Companion package: what we should develop alongside the deck

| Deliverable | Purpose | Scope / acceptance gate |
|---|---|---|
| Main slide deck + PDF | Concise session visuals and later distribution | One claim per slide, accessible contrast, alt text where practical, status labels; speaker-approved handoffs. |
| Speaker notes / claim ledger | Context, caveats, citations and rehearsal guidance | Every material support/performance/adoption claim has a source/version or is marked unverified; source notes don't become slide walls of text. |
| Public resource hub | One stable printed URL and QR, avoiding link overload | Routes for content authors, practitioners and contributors; distinguishes usable examples, alpha/prototype exercises and planned-design feedback. No placeholder links in final slides. |
| Example 1: readiness-gated rollout | Demonstrate a blocked phase, inspection, remediation and progress | Disposable cluster, pinned controller/gates/bundle digests, expected outcomes, cleanup; account for draft status-model drift. Online-only by default. |
| Example 2: configuration / eligibility | Show one configuration change and/or non-mutating migration check | Separate directories/workflows: do not conflate configuration with migration or migration eligibility with general portability. Pin tool versions and explain blockers. Prioritize one if time/resources are tight. |
| Example 3: authoring/contribution starter | Language-neutral minimal content example and a maintainer-vetted first task | Choose a currently supported bundle path. Helm starter remains a design example until actual format/tooling is verified. Include validation/test commands and expected result. |
| SDK links / selected recording | Support Attila's event/informer/observability explanation | Speaker-approved versions and examples; no additional SDK research or asset edits assumed in this outline. |
| Appendix / follow-up notes | Detail that is useful but too expensive in the room | Full phase map, migration blockers, release matrix, catalog/graph semantics, security/ownership caveats and measured performance only when verified. |

Recordings are optional companion assets, not required main-session playback. Start with **two tested examples and one verified contribution path**, then expand if justified. Nothing in this table has been built or tested yet.

## Evidence gates before final slide drafting

1. **Speaker/pacing approval:** four speakers confirmed; agree on A/B/C OLM identities, 4/8/5 split and Attila's ten-minute SDK-only budget/condensation; confirm audience/accepted title and Q&A expectations.
2. **Release matrix:** choose controller/API/channel/gate versions, migration-tool version, SDK release, Kubernetes version and Java support. Resolve source/doc drift before using YAML or status screenshots.
3. **Novelty evidence:** identify the actual post-2025 rollout delta; verify customization/migration outcomes. Apply the same test to SDK consistency/filtering: establish a post-2025 change or new operational lesson. If no delta is established, shorten that beat to context and shift emphasis to better-evidenced advances within the same speaker's allocation.
4. **Proposal follow-through:** October 2 schema-first direction and `helm+v2` are confirmed. Align old proposal examples/transport/channel references with those decisions; refine lifecycle schema and actual implementation prerequisites. Validate CRD ownership/deletion and release-object behavior before public examples. Successor-library implementation evidence is still separate from these schema proposals.
5. **Rationale evidence:** maintainer-approved chronology and public wording for the foundational/compatibility investment. No generalized two-year no-feature claim, unsupported downgrade incident, security improvement, team count, OperatorHub percentage or performance figure.
6. **Online exercise readiness:** test pinned examples on disposable environments, document failure paths and cleanup, vet contribution destinations, verify short URL and QR. A prototype link alone is not an easy on-ramp.

## Cut plan: preserve the handoff and main takeaways

Use cuts from **remaining material** at each checkpoint; do not expect an already-delivered introduction to recover time.

- **At the 04:00 checkpoint, one minute behind:** shorten the forthcoming slide 9 library detail by 30 seconds and slide 10 content-contract explanation by 30 seconds; keep references online.
- **At the 12:00 checkpoint, two minutes behind:** collapse the forthcoming slides 10–11 (normally 3:30) into one 2:00 design slide and reduce slide 12 from 1:00 to 0:30. This recovers two minutes without touching Attila's allocation.
- **At the 15:30 checkpoint, one minute behind:** deliver slide 12 as a 15-second resource-hub pointer and slide 13 as a 15-second handoff, saving one minute.
- **Hard wall at actual 16:30:** whichever OLM slide is active, finish the current point and use the next thirty seconds for the language-neutral handoff. Move any remaining OLM detail online; Attila begins at 17:00.
- **Unverified roadmap item:** replace its specifics with one bounded design question; do not fill the time with speculative demos or dates.
- **Longer required Q&A:** agree in advance on a 16-minute OLM + 9-minute SDK + 1-minute close + 4-minute Q&A variant. Do not improvise a smaller Attila budget at the handoff.
- **SDK preferences differ:** Attila chooses the best ten-minute sequence. The outline provides integration boundaries, not a requirement to discard his proposed content.
- Keep detailed pre-CRD chronology, caching topology, broad GitOps comparisons, LLM packaging and catalogue-sized compatibility analysis in the appendix or future work unless they directly earn their main-session time.

## Source/context anchors

- `../kubecon-2026.txt`: original seed topics and supplied references; unchanged.
- `kubecon-2026-resource-assessment.md`: published/draft distinction, local revision provenance, feature gates and evidence gaps.
- `kubecon-2025-slide-context.md`: prior-message baseline, particularly slides 6–15 and SDK slides 17–26.
- `kubecon-2026-feature-planning-context.md`: both MCP-read planning briefs, later catalog decision and evolution musings; separates proposals, hypotheses, trade-offs and contribution tasks.
- `../2026-olm-evolution-musings.md`: original August strategic exploration, not a release/roadmap commitment.
- `~/Downloads/Copy of KubeCon2026.pptx`: Attila's proposed segment; no source-deck edits.

This revision incorporates only the two supplied Google Docs and the requested local musings. No implementation/release/benchmark validation or broader ecosystem crawl was performed. This is a proposal for narrative, timing, illustrations and deliverables—not a declaration that the backlog or examples are already released/ready.
