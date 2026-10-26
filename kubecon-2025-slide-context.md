# KubeCon NA 2025 — prior-slide content and 2026 differentiation

Generated context is maintained in `~/devel/breadcrumbs/2026-kubecon-wip/`; original source references remain outside this work area.

## Provenance and scope

- Source: https://docs.google.com/presentation/d/1_WK8mNw3pERO6U96ptlW3pKiQDvZdBpk12kRN5orIqk/
- Drive title: **KubeCon NA 2025 - Operator Framework Maintainer Track**.
- Opening-slide title: **Package Management For Your Cluster, Reimagined**.
- Last modified: 2025-11-13T20:15:07.130Z. Retrieved: 2026-10-09.
- Retrieval: actual `tools/list` and `tools/call` over MCP stdio, using a temporary read-only `readPriorPresentation` adapter and the existing Google MCP authentication module. The installed server lacks Slides/export tools. Slides API returned 403 `accessNotConfigured`; authenticated Drive PPTX export succeeded. No API enablement, OAuth-scope change, source-deck mutation, or persistent server/config edit.
- Parsed the exported OOXML in presentation order: **27 slides; slide 5 hidden**, leaving 26 non-hidden slides. Notes and image metadata were extracted. This preserves slide content, not a transcript of delivery or proof that every planned demo occurred.
- This is distinct from Attila's proposed 2026 SDK contribution in `~/Downloads/Copy of KubeCon2026.pptx`.
- Historical product, adoption and roadmap assertions below are **claims in the 2025 deck**, not independently verified current facts. Notes often contain planning instructions.
- Images, rendered layout, animation and humor were not visually assessed. Image-only slides cannot be fully interpreted from text/notes alone.

## Executive assessment

2025 already told the **“OLMv1 is a reimagination, not a refactor”** story, explained v0 pain points, showed compatibility additions, introduced experimental revision/phased lifecycle management, included extension-workflow demo material, presented Helm/configuration/migration roadmap items, and invited contributions. The SDK closing segment explained read-after-write consistency and comparable resource versions.

2026 should therefore shift from **“why v1, and what we intend”** toward **“what the investment has delivered, what remains unresolved, and exactly how you can participate.”** Renaming ClusterExtensionRevision to ClusterObjectSet is not by itself a novel phased-rollout story. Migration, Helm content, configuration and contribution invitations also need evidence of progress beyond their 2025 announcement.

## Slide-by-slide context (1-based)

### 1. Package Management For Your Cluster, Reimagined

- Listed presenters: Rashmi Gottipati, Jordan Keister, Joe Lanford (Red Hat); Attila Mészáros (Apple).
- Note assigns Jordan as speaker.
- These are the prior speaker identities, not assignments for 2026. The user subsequently confirmed four total speakers in 2026, with Attila exclusively on Java SDK.

### 2. Speakers

- Joe: Senior Principal S/W Engineer, Red Hat.
- Attila: Senior S/W Engineer, Apple.
- Jordan: Principal S/W Engineer, Red Hat.
- Rashmi: Senior S/W Engineer, Red Hat.
- Note assigns Jordan; four portrait/screenshot images are present.

### 3. Quick Audience Poll

- Notes ask who has not installed an operator, who has heard of OLMv1, and who has tried OLMv1.
- Note: introduce the problem statement here. Assigned to Jordan.
- The slide includes an image; its content was not inspected.

### 4. Operator Lifecycle Manager (OLM)

- Simplified installation, upgrades and dependency management for Kubernetes operators; automated lifecycle experience.
- Historical ecosystem claims: 380+ operators on operatorhub.io; approximately 17.8 million v0 GitHub-release downloads, 41 thousand v1 downloads; 1.8K v0 / 166 v1 GitHub stars.
- Assigned to Jordan; image present.
- Do not reuse these figures as current adoption or v1 compatibility measurements.

### 5. OLMv1: Not Just a Refactor — A Reimagination [HIDDEN]

- Hidden comparison-slide variant, substantially duplicated by slide 6.
- v0 problems: unintended upgrades, automatic RBAC aggregation, challenging uninstallation, installation failures, lack of version pinning, opaque/non-Kubernetes-like resources, nine user APIs.
- v1 promises: isolated/deterministic installs and upgrades, explicit bundle-scoped permissions, deterministic complete cleanup, declarative GitOps-friendly model, desired-update-path control, Kubernetes-native resources, three user APIs.
- Notes assign Jordan and link a separate v0 pain-points Google Doc; that linked document was not fetched in this pass.

### 6. OLMv1: Not Just a Refactor — A Reimagination

- Visible version of the v0/v1 comparison above.
- Notes: redesigned from the ground up to solve problems faced by authors/customers.
- Notes list the nine v0 APIs: CatalogSource, OperatorGroup, Subscription, InstallPlan, ClusterServiceVersion, Operator, OLMConfig, OperatorConditions, PackageManifests.
- The slide says **three** v1 user APIs. Do not simply transfer that count to current documentation or assume the exact identities without context.
- Assigned to Jordan. The permission promise needs qualification against the current source-verified privilege model, rather than automatic reuse.

### 7. What's New in OLMv1 Since v1.0?

- Registry+v1 bundle webhook definitions.
- SingleNamespace and OwnNamespace install modes.
- Experimental ClusterExtensionRevision API.
- Built-in deployment availability monitoring.
- Experimental initial OLMv1 updates to the kubectl operator plugin.
- Assigned to Jordan. These were already presented as new work in 2025, so avoid a blanket “no features in two years” claim.

### 8. Webhook Support in Bundles

- Management of mutating, validating and conversion webhooks in registry+v1 bundles.
- Declarative installation through bundle manifests.
- Foundation for upgrades across breaking API changes.
- Integrations with cert-manager and OpenShift Service CA.
- Assigned to Rashmi. These are historical support claims, not a new 2026 headline without further advances.

### 9. SingleNamespace & OwnNamespace Installs

- v0's four modes: OwnNamespace, SingleNamespace, MultiNamespace, AllNamespaces.
- v0 multi-tenancy flexibility described as introducing footguns, including unexpected CRD downgrades.
- v1 initially AllNamespaces; minimal OwnNamespace/SingleNamespace restored for compatibility with registry+v1 content.
- Explicit message: no intention to return to multi-tenancy features.
- Assigned to Rashmi. The deck's broad “APIs/controllers are single-tenant by nature” phrasing should be narrowed to the shared API-definition problem when reused.

### 10. Revision-Based Lifecycle Management

- Replaces InstallPlan as the “unit of lifecycle.”
- Each extension change creates an immutable ClusterExtensionRevision containing installation state/configuration.
- Old revisions archived when a new revision rolls out and becomes available.
- Phased deployment; debugging/rollback comparison to ReplicaSets.
- Notes ask for phase sequence and point to historical controller/probe and phase implementation paths.
- Assigned to Rashmi. This is direct prior overlap with the planned ClusterObjectSets explanation; neither this slide nor its analogy proves automatic rollback guarantees.

### 11. OLMv1: Workflow

- Image-led workflow slide (`olmv1-workflow-2.png`), assigned to Rashmi.
- No textual workflow details were recoverable beyond the heading; inspect the image later if reusing its composition.

### 12. DEMO TIME: OLMv1 in Action!

- Visible invitation: “Do it yourself!” with https://github.com/joelanford/olm-kubecon-2025 .
- Assigned to Joe. Notes propose bundle preparation, ClusterCatalog creation, webhook-bearing bundle inspection, ClusterExtension installation, webhook verification, revision inspection, deletion/cleanup, and namespace-mode configuration.
- Notes discuss an upgrade with old revision archival, failed-revision/bad-image examples if available, and a watchNamespace/configuration incompatibility followed by repair.
- Notes explicitly say not to do live catalog-content discovery and suggest a prerecorded video/local asciicast.
- These are planned demo steps, not evidence of successful delivery. The linked repository is discovered from the deck, not newly inspected or tested here.
- For 2026, prefer linked reproducible examples showing a new outcome, not a replay of this entire installation/demo sequence.

### 13. Technical Challenges and Current Limitations

- Complete uninstall; orphaning/adoption logic still to come.
- Missing OperatorConditions support.
- Problems with legacy replaces/skips/skipRange graph mechanics for authors/users.
- Docs/tooling still needed for creator self-service.
- On-cluster catalog inspection tooling in progress.
- Notes assign Rashmi, with Jordan joining for the last three points.
- Useful basis for a “what changed / what still needs help” comparison, not a fresh limitations inventory.

### 14. OLMv1: The Road Ahead

- Improved registry+v1 configuration aligned with v0 Subscription.spec.config.
- Direct bundle installation without a catalog.
- New content types, explicitly **Helm charts**.
- Revision API used for broader policy approval, including catalog provenance/time-aware approvals beyond RBAC.
- Telemetry/insights.
- Migration from OLMv0 to OLMv1.
- Assigned to Joe. These are 2025 planned items; 2026 must show progress, a revised design or a concrete remaining task rather than reannounce the same backlog.

### 15. Let's Shape the Future of OLM Together!

- Visible operator-controller contribution-guide pointer.
- Notes list the operator-controller GitHub project, Kubernetes Slack `#olm-dev`, working-group agenda/meeting and YouTube channel, plus Java Operator SDK GitHub and Discord.
- Assigned to Joe; image present.
- Historical contribution destinations were recorded but not validated for current activity. The 2026 improvement is a small set of actionable first tasks, not just another community-links slide.

### 16. Java Operator SDK in 2025

- v5 released in January; characterized as a large release with relatively smooth transitions.
- v5.1 in May, stronger update guarantees; forthcoming v5.2 dependent-resource/expectations improvements; hoped-for v5.3 comparable-resource-version changes by year end.
- Expected only minor releases in 2026; milestones linked.
- Note explains a decision to focus on a confusing issue shared by Go/Java communities.
- This begins the prior SDK segment. Release expectations are historical claims, not today's SDK baseline.

### 17. Recap: resourceVersion as a String

- Equality-only string treatment versus a practically increasing integer, illustrated with a custom resource carrying resourceVersion and an external-resource ID in status.
- Record as the speaker's setup; numeric comparison must not become unqualified guidance for arbitrary Kubernetes versions/resource contexts.

### 18. Storing Allocated Values in Status

- Generated external resource IDs stored in status for future update/delete operations.
- Next reconciliation may not see the just-written status, risking repeated creation.
- Asks about cache read-after-write consistency. Image present.

### 19. Back to Basics: Informers

- Image-led slide.
- Notes discuss watches, eventual observation of the latest resource, and missing ordering guarantees.
- This establishes the previous consistency explanation; the note's watch-transport wording is not independently verified here.

### 20. Multiple Informers Triggering Reconciliation

- Image-led slide.
- Notes discuss synchronous cache polling, expectations, controller-runtime polling, and the SDK's temporary cache.

### 21. Solutions for Stronger Guarantees

- Poll the reconciler cache after updates.
- Expectations pattern.
- Additional cache over informers: TemporalResourceCache in JOSDK, optimizing throughput.

### 22. Temporal Cache on Top of Informers

- Image-led slide.
- Notes: cache the response resource; evict on the next event; “Problem solved? no.”

### 23. Temporal Cache + Caveat

- Image-led slide.
- Notes: another actor's concurrent updates; cannot tell before/after own update without resource-version comparison.

### 24. Solution: Optimistic Locking

- Historical argument: optimistic locking enables safe response-cache handling; failures retried with fresher resources; evict temporary cache on the next event without comparing its version.
- SDK support stated as v5.1; cites `PrimaryUpdateCacheUtils.ssaPatchStatusAndCacheResource(..)` and variants.
- This describes the talk's solution, not independently proven correctness of all implementations.

### 25. KEP-5504: Comparable Resource Versions

- References the comparable-resource-version KEP.
- Claims official support in the next Kubernetes version, integer comparison permitted, and no underlying implementation change.
- These were time-sensitive 2025 statements. Check supported Kubernetes versions and comparison scope before turning them into 2026 guidance.

### 26. Comparable Resource Versions in JOSDK

- Existing partial feature-flag support, initially off by default; full support planned for v5.3.
- Per-informer opt-out; generalized beyond primary resources.
- Claimed benefits: response caching without optimistic locking, filtering own-update events, overlapping informers, further improvements.
- Significant overlap with the proposed 2026 cache-consistency and event-filtering material. The useful 2026 distinction is delivered behavior/new edge cases and shared-informer-pool implementation, not repeating the whole motivation.

### 27. Q&A / Thank You / Feedback

- Notes assign Joe; feedback image present.

## Differentiation matrix for the 2026 session

| Proposed topic | 2025 baseline | Recommended 2026 treatment |
|---|---|---|
| Why v1 / v0 pain points | Slides 4–6, 9 | Brief recap only. Connect selected limitations to outcomes; avoid the same comparison-table sales pitch. |
| Namespace tenancy/compatibility | Slide 9 | Clarify actual boundaries and compatibility progress. A fresh illustration can help, but the message itself is not new. |
| Webhooks and installation workflow | Slides 7–8, 11–12 | Mention only where needed to explain readiness or a new example. Do not present old compatibility additions as new features. |
| ClusterObjectSets / phases | Slides 7, 10, 12 already introduced revisions/phases | Explain the evolution from ClusterExtensionRevision: what became more usable, inspectable or general-purpose; show evidence of a new capability, not only a rename. |
| Deployment customization | Roadmap slide 14 | Demonstrate the concrete alpha configuration contract and compatibility payoff; label gates and limitations. |
| Migration / library-olm | Roadmap slide 14; orphan/adoption gap in slide 13 | Show concrete prototype workflow, eligibility reporting/shared logic and remaining tasks. Validate matched versions before “try it now.” |
| Catalog evolution / successor resolution | Graph/self-service/catalog-inspection gaps in slide 13 | Explain which old author/admin friction is being addressed and give collaborators one bounded design/test problem. Implementation still needs canonical evidence. |
| Native Helm content / broader resources | Helm/new-content roadmap already on slide 14 | Show progress/design precision or representative content-author participation. Not a new announcement and not released support without evidence. |
| Contributions | Slide 15 already invited participation | Verified first tasks, expected result, prerequisites and maintained destination; embed asks alongside outcomes. |
| SDK consistency / event filtering | Slides 17–26, especially 18 and 26 | Coordinate with Attila: shortened recap, then concrete advances since the prior explanation. |
| SDK informer pools | Multiple/overlapping informers discussed in slides 20/26 | Shared-pool configuration/lifecycle details may add new value; do not label the broader multiple-informer concept new. |
| SDK observability / virtual threads | Not explicit topics in extracted 2025 text/notes | Candidate fresh closing-segment material, subject to SDK baseline and time budget; this does not prove prior oral remarks lacked them. |

## Implications for the rationale and contribution story

- Avoid claiming literally no features across a period that includes the 2025 “What's New” slide. Distinguish the long foundational/compatibility investment from the next wave of user-visible features; confirm exact chronology with maintainers.
- Instead of another “we are reimagining packaging” opener, a working 2026 question is: **“What can you do with the foundation now, and what can you help unlock next?”**
- Use the 2025 backlog as accountability/context, not a list of overdue promises: show **then → now → next contribution** for a few selected items.
- Treat API-count, permissions, isolation, complete-cleanup and rollback claims as version-specific. In particular, the old permission phrasing must not obscure the source-verified current privileged installation model.
- Reserve Attila's final segment in the shared thirty-minute session. Its 2025 overlap is now known; coordinate depth with him rather than cut or rewrite his proposed content unilaterally.
- No additional linked documents/repos were ingested in this deck-only pass. The prior demo repository and separate v0 pain-points document are targeted follow-up candidates only if needed.
