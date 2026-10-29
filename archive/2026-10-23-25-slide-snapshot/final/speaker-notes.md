# The Next Era of Kubernetes Operator Lifecycle Management

## Speaker notes

OLM presenters: Rashmi, Joe and Jordan; A/B/C topic assignments remain to confirm. Attila presents original SDK source slides 3–12, preserved as authored. Twenty-five displayed slides total thirty proposed minutes including buffer.

## 1. The Next Era of Kubernetes Operator Lifecycle Management

**Speaker:** OLM A — context / host; name to confirm  
**Start:** 00:00 · **Duration:** 00:45 · **Status:** 





Welcome the audience and introduce the talk, The Next Era of Kubernetes Operator Lifecycle Management, at KubeCon + CloudNativeCon North America 2026. Retain the operator-lifecycle illustration. Source: ../kubecon-2026-outline.md.

## 2. Presentation team

**Speaker:** OLM A — team introduction; name to confirm  
**Start:** 00:45 · **Duration:** 00:30 · **Status:** 





OLM A introduces Rashmi, Joe and Jordan as the OLM presentation team; photos are deferred. Introduce Attila as the fourth presenter, covering Java Operator SDK exclusively. The mapping of Rashmi, Joe and Jordan to OLM roles A/B/C remains unconfirmed. A covers base slides 1–4, B covers 5–9, and C covers 10–13. The primary builder imports original SDK source slides 3–12 unchanged after the divider, allocating 60 seconds to each. These become final slides 14–23; the host closes on final slide 24 and topic owners answer questions on final slide 25. Adding this team slide and removing the standalone assumptions slide preserves 15 base records and 25 displayed slides. The base records total 1,200 seconds; the original SDK segment adds 600 seconds for a 30-minute session. Keep the no-live-demo plan. Sources: ../kubecon-2026-outline.md; ../kubecon-2025-slide-context.md.

## 3. Compatibility and lifecycle foundations

**Speaker:** OLM A — context / host; name to confirm  
**Start:** 01:15 · **Duration:** 01:30 · **Status:** FOUNDATIONAL WORK

OLM evolution builds on existing packages and operational experience.

- OLMv0 established lifecycle management
- Existing registry+v1 content shapes compatibility
- Operational experience informs OLMv1

Use OLMv0 evolution and compatibility with existing registry+v1 content as the historical basis. Explain how existing package formats, resource ownership and operational behavior shaped lifecycle implementation. Configuration and migration preparation build on that foundation. The bridge illustration is conceptual. This slide makes no measured availability, performance, adoption or elapsed-time claims. Sources: ../kubecon-2025-slide-context.md; ../kubecon-2026-resource-assessment.md; supplied evolution background.

## 4. OLM: past, current and future

**Speaker:** OLM A — context / host; name to confirm  
**Start:** 02:45 · **Duration:** 01:15 · **Status:** EVOLUTION / PLANNED / FUTURE WORK

OLM feature evolution

- Past: OLMv0, flawed namespace-local CRD visibility assumptions, SQLite, FBC
- Current: OLMv1, ClusterExtension, pins, webhooks
- Ongoing: rollouts, config, install, migration

Enumerate the timeline: past work includes OLMv0, SQLite catalogs and established file-based catalogs (FBC). Summarize OLMv0's flawed assumptions about namespace-local CRD visibility, independently managed APIs and watch-aware dependencies. CRD definitions are cluster-scoped shared APIs; custom resource instances may be namespaced, and controller watch scope is configured separately. Shared CRDs can couple operator upgrades. The flawed assumptions belonged to OLMv0's lifecycle model; Kubernetes' cluster-scoped CRD design is the underlying API boundary. Keep the OperatorGroup recap brief and explain how these lessons informed OLMv1. Current OLMv1 capabilities include ClusterExtension, version pins and webhooks. Ongoing development includes resource rollouts, user configuration, direct bundle installation and migration. Direct installation remains an open proposal in PR #2907 at the supplied 2026-10-09 check. Planned work includes Helm content using helm+v2 and v2 catalog schemas. OCI-native catalog storage and transport remain future work. Release-specific availability and feature gates require the source-version qualifications on the detailed slides. The 2025 deck already listed delivered features. A hands off to B after this overview at 04:00. Sources: ../kubecon-2025-slide-context.md slide 9; ../kubecon-2026-resource-assessment.md K-1/K-2/V0-2/V0-3; supplied feature-planning context.

## 5. Install a bundle directly

**Speaker:** OLM B — lifecycle primitives; name to confirm  
**Start:** 04:00 · **Duration:** 01:30 · **Status:** IN ACTIVE DEVELOPMENT / CONTROLLED BY FEATURE-GATE

Select a registry+v1 bundle by its OCI image reference.

- Use sourceType: OCIImage
- Set source.ociImage.ref
- Bypass catalog resolution

PR #2907 is OPEN and unmerged as of the supplied check dated 2026-10-09. Present direct bundle installation as proposed behavior in active development. It supports registry+v1 bundles only and is controlled by the BoxcutterRuntime feature gate. The requested source uses sourceType: OCIImage and source.ociImage.ref. It bypasses catalog resolution. Describe CRD checks and other lifecycle safeguards according to the proposal's supported path; catalog bypass alone establishes no blanket removal of CRD safety. Pin the source revision and gate configuration before preparing an example. The session uses prepared examples without a live demo.

## 6. Inspect phased resource rollouts

**Speaker:** OLM B — lifecycle primitives; name to confirm  
**Start:** 05:30 · **Duration:** 02:00 · **Status:** IN ACTIVE DEVELOPMENT / CONTROLLED BY FEATURE-GATE

Ordered phases expose resource application and readiness progress.

- Apply resource groups in phase order
- Wait for applicable readiness checks
- Inspect revision content and ownership changes

Explain the evolution from ClusterExtensionRevision to ClusterObjectSets. The ascending stair-step illustration shows resource readiness progressing toward the installation goal. Objects within a phase have unspecified ordering. Readiness checks cover defined conditions; application correctness and transactional availability require additional validation. The rollout runtime is in active development and controlled by feature-gate. Pin the source version and gate settings for examples. Reconcile draft Succeeded wording with the inspected Ready/completedAt type before using status examples. Sources: supplied ClusterObjectSets draft and feature-planning context; ../kubecon-2026-resource-assessment.md; ../kubecon-2025-slide-context.md slides 7, 10 and 12.

## 7. User control of extension deployments

**Speaker:** OLM B — lifecycle primitives; name to confirm  
**Start:** 07:30 · **Duration:** 01:30 · **Status:** IN ACTIVE DEVELOPMENT / CONTROLLED BY FEATURE-GATE

Flexible user-defined deployment configuration.

- Environment variables and resource settings
- Placement, volumes and deployment metadata
- Operator-provided configuration and schemas

Describe the deployment as a configuration exchange between users and the operator team. Users express environment, resource, placement, volume and metadata requirements through the package's configuration interface. Operator authors define schema and validation behavior. OLM carries the selected configuration into the deployment. DeploymentConfig is in active development and controlled by feature-gate; values are expressed through ClusterExtension configuration. Explain field-specific merge, replace and append behavior and annotation precedence. Validate example input and inspect the resulting deployment against the pinned source version. Watch-namespace pass-through leaves CRDs shared and supplies no watch-aware dependency management. Sources: supplied customization draft; ../kubecon-2026-resource-assessment.md; ../kubecon-2025-slide-context.md slide 14.

## 8. OLMv0 → OLMv1 migration

**Speaker:** OLM B — lifecycle primitives; name to confirm  
**Start:** 09:00 · **Duration:** 02:00 · **Status:** IN ACTIVE DEVELOPMENT

Move operator management from OLMv0 to OLMv1.

- Prepare v1 catalogs from v0 CatalogSources
- Check and preview operator migrations
- Migration library with example binaries

Prepare OLMv1 ClusterCatalogs from the existing OLMv0 CatalogSources first. Then evaluate each operator installation for eligibility and preview its migration before transferring management. The check and preview actions evaluate operators; catalog preparation is the earlier prerequisite. The migration specification describes check, convert, rollback and cleanup with ClusterObjectSets. Functionality is supplied as library-olm. The example binaries illustrate library use. The user confirms structured output that supports automated processing, including models; it has not been independently exercised in this editing task. Eligibility checks have defined coverage. Retaining the namespace can reduce disruption; namespace changes may restart workloads or cause downtime. Validate recovery boundaries and source/gate versions for the selected case. This area is in active development. Sources: library-olm README/spec; ../kubecon-2026-resource-assessment.md; user migration guidance.

## 9. Shared lifecycle logic in library-olm

**Speaker:** OLM B — lifecycle primitives; name to confirm  
**Start:** 11:00 · **Duration:** 01:00 · **Status:** IN ACTIVE DEVELOPMENT

Reuse lifecycle logic through a library with explicit contracts.

- Share migration checks and workflow logic
- Exercise current development examples
- Record expected results in reusable fixtures

Describe library reuse, the current migration development examples and fixtures that record inputs and expected results. The example binaries exercise library behavior and provide contribution starting points. Broader controller, CLI and UI consumption remains a design intent requiring implementation evidence and explicit contracts. Successor semantics need a defined contract. Fixtures can cover legacy input or version/release selection while respecting the proposed v2 schema direction. Pin source versions when documenting examples. B hands off to C after this slide at 12:00. Sources: library-olm README/spec; supplied feature-planning context; ../kubecon-2025-slide-context.md slide 13.

## 10. Planned Helm content support

**Speaker:** OLM C — content/catalogs/contributions; name to confirm  
**Start:** 12:00 · **Duration:** 02:00 · **Status:** PLANNED / helm+v2

The rendering contract targets deterministic chart behavior.

- Chart and values produce managed manifests
- Allow-listed features support reproducible rendering
- helm+v2 identifies the content representation

helm+v2 is the user-confirmed canonical discriminator for versioned OLM Helm packaging/catalog content. Standard chart OCI identity is used, with rendered manifests managed through OLM lifecycle behavior. User values are parsed and validated during rendering. Deterministic rendering is the design goal: features are allow-listed to exclude non-deterministic functionality, with compatibility fixtures required to validate the supported subset. Dependencies are vendored. Hooks and keep behavior are unsupported in the proposal. CRDs use templates/; crds/ is unsupported. Chart release-object mappings and restricted template functions require compatibility testing. Moving CRDs affects upgrade, deletion and data handling. Implementation of proposed gates remains independently unconfirmed. Native chart OCI identity and future OCI catalog storage are separate scopes. Sources: supplied Helm planning brief and feature-planning context.

## 11. Catalog performance and content types

**Speaker:** OLM C — content/catalogs/contributions; name to confirm  
**Start:** 14:00 · **Duration:** 01:30 · **Status:** PLANNED / FUTURE WORK

Design for lower catalog-processing cost and additional content types.

- Lower duplicated CSV metadata
- Direct version fields reduce property traversal
- Typed registry+v1 and helm+v2 content

Credit established FBC capabilities: plaintext editing, composition, extensibility, package-level metadata and version/release properties already exist. The v2 work refines the representation and consumers: less duplicated CSV metadata, version/release fields available directly rather than via property traversal, and explicit mediaType dispatch for installable formats including Helm. Arbitrary FBC schema extensibility alone does not supply end-to-end installation support for a new content type. Catalog processing efficiency is a design benefit to validate, with no measured speedup claimed. Show the practical resolution/metadata work the new representation is intended to reduce. The user-confirmed near-term focus is flexible OLMv1 schemas; OCI-native catalog storage, transport and selective fetching are future work. Channels and legacy graphs are excluded from v2; lifecycle/constraint metadata remains open. Sources: https://olm.operatorframework.io/docs/reference/file-based-catalogs/ ; supplied v2 catalog brief; feature-planning context.

## 12. Contribute to Operator Framework

**Speaker:** OLM C — content/catalogs/contributions; name to confirm  
**Start:** 15:30 · **Duration:** 01:00 · **Status:** PROJECT DEVELOPMENT

Help develop the project through documentation, code and test cases.

- Improve documentation and examples
- Contribute code and focused tests
- Add migration, chart and schema fixtures

Make an explicit project-development ask: contribute documentation, code, tests and fixtures to Operator Framework. Explain the distinction from submitting operator versions or upgrade graphs to a catalog; those submissions serve a separate publishing workflow. Useful development cases include rollout/configuration edge cases, migration eligibility, chart/values compatibility and schema behavior. Each contribution should identify the repository, issue or discussion, reproducible input and expected result. Maintainers still need to vet concrete task links and destinations. Companion examples are intended for online use; this session has no live demos. Sources: supplied feature-planning context; ../kubecon-2025-slide-context.md slide 15.

## 13. Operator Framework: Java Operator SDK

**Speaker:** OLM C — content/catalogs/contributions; name to confirm  
**Start:** 16:30 · **Duration:** 00:30 · **Status:** 





C hands off to Attila for Java Operator SDK. OLM packaging is language-neutral, and SDKs support controller implementation and reconciliation. Keep bundle metadata and the runnable controller image distinct in the spoken transition. The primary builder imports original SDK source slides 3–12 unchanged immediately after this divider. Each original SDK slide receives 60 seconds, for ten minutes total on final slides 14–23. Attila covers this segment exclusively.

## 14. SDK source slide 3

**Speaker:** Attila

**Start:** 17:00 · **Duration:** 01:00

Original authored slide XML and illustrations retained. SDK wording and release/version claims remain the author's source content. This import adds assignment/timing notes only.

Source: ~/Downloads/Copy of KubeCon2026.pptx, slide 3.

Read-Cache-After-Write Consistency since v5.3 API:   UpdateControl.patchStatus(resource) context. resourceOperations() .serverSideApply(resource); Additional cache brings complexity: Indexers Items store Comparable Resource Versions KEP Read-cache-after-write consistency blog 

## 15. SDK source slide 4

**Speaker:** Attila

**Start:** 18:00 · **Duration:** 01:00

Original authored slide XML and illustrations retained. SDK wording and release/version claims remain the author's source content. This import adds assignment/timing notes only.

Source: ~/Downloads/Copy of KubeCon2026.pptx, slide 4.

Read-Cache-After-Write Consistency

## 16. SDK source slide 5

**Speaker:** Attila

**Start:** 19:00 · **Duration:** 01:00

Original authored slide XML and illustrations retained. SDK wording and release/version claims remain the author's source content. This import adds assignment/timing notes only.

Source: ~/Downloads/Copy of KubeCon2026.pptx, slide 5.

Event Filtering - API & Challenges Filter out events for our own updates Challenges Informer lost event problem Our update did not change the resource but other actor did concurrently   context. resourceOperations() .serverSideApply(resource); 

## 17. SDK source slide 6

**Speaker:** Attila

**Start:** 20:00 · **Duration:** 01:00

Original authored slide XML and illustrations retained. SDK wording and release/version claims remain the author's source content. This import adds assignment/timing notes only.

Source: ~/Downloads/Copy of KubeCon2026.pptx, slide 6.

Event Filtering for Read-Cache-After-Write-Consistency

## 18. SDK source slide 7

**Speaker:** Attila

**Start:** 21:00 · **Duration:** 01:00

Original authored slide XML and illustrations retained. SDK wording and release/version claims remain the author's source content. This import adds assignment/timing notes only.

Source: ~/Downloads/Copy of KubeCon2026.pptx, slide 7.

Informer Pools Sharing underlying informers between controller Matches the informer configuration Except list limit  Details in  InformerClassifier Supports dynamic Informer registration and de-registration

## 19. SDK source slide 8

**Speaker:** Attila

**Start:** 22:00 · **Duration:** 01:00

Original authored slide XML and illustrations retained. SDK wording and release/version claims remain the author's source content. This import adds assignment/timing notes only.

Source: ~/Downloads/Copy of KubeCon2026.pptx, slide 8.

Informer Pools

## 20. SDK source slide 9

**Speaker:** Attila

**Start:** 23:00 · **Duration:** 01:00

Original authored slide XML and illustrations retained. SDK wording and release/version claims remain the author's source content. This import adds assignment/timing notes only.

Source: ~/Downloads/Copy of KubeCon2026.pptx, slide 9.

Observability stack enhancements Facelift over  Observability stack Improved logging and Mapped Diagnostic Context (MDC) Putting event and primary resource to MDC if available Metrics API refined MicrometerMetricsV2 Generic Grafana Dashboard Sample with OTel + Prometheus + Grafana  

## 21. SDK source slide 10

**Speaker:** Attila

**Start:** 24:00 · **Duration:** 01:00

Original authored slide XML and illustrations retained. SDK wording and release/version claims remain the author's source content. This import adds assignment/timing notes only.

Source: ~/Downloads/Copy of KubeCon2026.pptx, slide 10.

Java Virtual Threads (WIP)  Planned for v5.7.0 We will officially support this for Java 25+ (but will work with Java 21+) Replacing ThreadPools with virtual threads  across  framework Virtually unlimited number of concurrent reconciliation The explicit limit applies though 

## 22. SDK source slide 11

**Speaker:** Attila

**Start:** 25:00 · **Duration:** 01:00

Original authored slide XML and illustrations retained. SDK wording and release/version claims remain the author's source content. This import adds assignment/timing notes only.

Source: ~/Downloads/Copy of KubeCon2026.pptx, slide 11.

Java Virtual Threads (WIP) 

## 23. SDK source slide 12

**Speaker:** Attila

**Start:** 26:00 · **Duration:** 01:00

Original authored slide XML and illustrations retained. SDK wording and release/version claims remain the author's source content. This import adds assignment/timing notes only.

Source: ~/Downloads/Copy of KubeCon2026.pptx, slide 12.

Some honorable mentions… EventRecorder API ShardSelector support Documentation improvements - operations section 

## 24. Resources and contribution steps

**Speaker:** OLM A — session host; name to confirm  
**Start:** 27:00 · **Duration:** 01:00 · **Status:** RESOURCE PACKAGE TO PREPARE

Use documented contracts and reproducible cases to guide contributions.

- Check content against a documented contract
- Share a reproducible case or fixture
- Select a maintainer-scoped contribution

The host closes on final slide 24, represented here by base record 14. Include verified resource routes for Operator Framework and Java Operator SDK in the final resource hub. Public URLs and QR codes need published destinations. Companion examples and vetted first-task links remain to be prepared. Give the audience a practical next-day contribution supported by the resource package. Speaker ownership stays in these notes. Sources: ../kubecon-2026-outline.md companion package; supplied feature-planning contribution candidates.

## 25. Questions?

**Speaker:** OLM A/B/C on OLM; Attila on Java SDK only  
**Start:** 28:00 · **Duration:** 02:00 · **Status:** 

Questions about lifecycle APIs, packaging or controller behavior?

- OLM configuration and migration
- Helm content and catalog schemas
- Java Operator SDK reconciliation

Final slide 25 is titled exactly Questions?. Base record 15 reserves two minutes for questions and transition overruns. A/B/C answer their OLM topics; Attila answers Java Operator SDK questions exclusively. The base segment totals 20 minutes, including this question allocation. Original SDK source slides 3–12 add ten minutes for a 30-minute session. Main slides occupy 28 minutes including the one-minute host close. Keep the no-live-demo plan. Source: ../kubecon-2026-outline.md run of show.

