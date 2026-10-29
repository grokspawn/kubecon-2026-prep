# The Next Era of Kubernetes Operator Lifecycle Management

## Speaker notes

OLM presenters: Rashmi, Joe and Jordan; A/B/C topic assignments remain to confirm. Attila presents original SDK source slides 3–12, preserved as authored. 27 displayed slides total 32:00 including questions and buffer.

## 1. The Next Era of Kubernetes Operator Lifecycle Management

**Speaker:** OLM A — context and installation; name to confirm  
**Start:** 00:00 · **Duration:** 00:45 · **Status:** 





Welcome the audience and introduce the talk, The Next Era of Kubernetes Operator Lifecycle Management, at KubeCon + CloudNativeCon North America 2026. Retain the operator-lifecycle illustration. Source: ../kubecon-2026-outline.md.

## 2. Presentation team

**Speaker:** OLM A — context and installation; name to confirm  
**Start:** 00:45 · **Duration:** 00:30 · **Status:** 





Introduce Rashmi, Joe and Jordan as the OLM presentation team. Introduce Attila as the fourth speaker, covering Java Operator SDK. The mapping from A/B/C to individual OLM presenters remains to be confirmed. Photos are deferred. The session uses prepared examples without live demos.

## 3. Compatibility and lifecycle foundations

**Speaker:** OLM A — context and installation; name to confirm  
**Start:** 01:15 · **Duration:** 01:30 · **Status:** FOUNDATIONAL WORK

OLM evolution builds on existing packages and operational experience.

- OLMv0 established lifecycle management
- Existing registry+v1 content shapes compatibility
- Operational experience informs OLMv1

Use OLMv0 evolution and compatibility with existing registry+v1 content as the historical basis. Explain how existing package formats, resource ownership and operational behavior shaped lifecycle implementation. Configuration and migration preparation build on that foundation. The bridge illustration is conceptual. This slide makes no measured availability, performance, adoption or elapsed-time claims. Sources: ../kubecon-2025-slide-context.md; ../kubecon-2026-resource-assessment.md; supplied evolution background.

## 4. OLM: past, current and future

**Speaker:** OLM A — context and installation; name to confirm  
**Start:** 02:45 · **Duration:** 01:15 · **Status:** EVOLUTION / PLANNED / FUTURE WORK

OLM feature evolution

- Past: OLMv0, flawed namespace-local CRD visibility assumptions, SQLite, FBC
- Current: OLMv1, ClusterExtension, pins, webhooks
- Ongoing: rollouts, config, install, migration

Enumerate the timeline: past work includes OLMv0, SQLite catalogs and established file-based catalogs (FBC). Summarize OLMv0's flawed assumptions about namespace-local CRD visibility, independently managed APIs and watch-aware dependencies. CRD definitions are cluster-scoped shared APIs; custom resource instances may be namespaced, and controller watch scope is configured separately. Shared CRDs can couple operator upgrades. The flawed assumptions belonged to OLMv0's lifecycle model; Kubernetes' cluster-scoped CRD design is the underlying API boundary. Keep the OperatorGroup recap brief and explain how these lessons informed OLMv1. Current OLMv1 capabilities include ClusterExtension, version pins and webhooks. Ongoing development includes resource rollouts, user configuration, direct bundle installation and migration. Direct installation remains an open proposal in PR #2907 at the supplied 2026-10-09 check. Planned work includes Helm content using helm+v2 and v2 catalog schemas. OCI-native catalog storage and transport remain future work. Release-specific availability and feature gates require the source-version qualifications on the detailed slides. The 2025 deck already listed delivered features. A continues with installation changes. Sources: ../kubecon-2025-slide-context.md slide 9; ../kubecon-2026-resource-assessment.md K-1/K-2/V0-2/V0-3; supplied feature-planning context.

## 5. Streamlined Installation

**Speaker:** OLM A — context and installation; name to confirm  
**Start:** 04:00 · **Duration:** 01:00 · **Status:** 

Standard channel since v1.11.0

- spec.serviceAccount is optional and ignored.
- The controller uses its own service account.
- Restrict ClusterExtension access with RBAC and admission policy.

As of operator-controller v1.11.0, the standard installation channel no longer requires spec.serviceAccount. The controller uses its own service account; the deprecated field is ignored. ClusterExtension write access is a high-privilege operation because the controller uses cluster-admin permissions. When delegating access, combine Kubernetes RBAC with appropriate admission policy, such as ValidatingAdmissionPolicy, to constrain allowed extensions. Source: https://github.com/operator-framework/operator-controller/pull/2770 and the v1.11.0 release notes.

## 6. Namespace Management

**Speaker:** OLM A — context and installation; name to confirm  
**Start:** 05:00 · **Duration:** 01:00 · **Status:** 

Experimental channel since v1.12.0
Controlled by feature gate

- Set spec.namespace: use an existing user-managed namespace.
- Omit it: OLM manages a derived namespace.
- Deletion removes that namespace and its contents.

Operator-controller v1.12.0 introduced optional spec.namespace in the experimental installation channel. With the feature-gated runtime, an explicitly supplied namespace remains user-managed. When the field is omitted, OLM derives and manages an install namespace using bundle metadata and defaults. Deleting the extension also deletes its managed namespace and all remaining objects in that namespace, including objects OLM did not install. Explain namespace-transition validation and verify the selected bundle and controller version before demonstrating. Sources: https://github.com/operator-framework/operator-controller/pull/2925, https://github.com/operator-framework/operator-controller/pull/2926, https://github.com/operator-framework/operator-controller/pull/2929.

## 7. Inspect phased resource rollouts

**Speaker:** OLM B — lifecycle primitives and migration; name to confirm  
**Start:** 06:00 · **Duration:** 02:00 · **Status:** IN ACTIVE DEVELOPMENT / CONTROLLED BY FEATURE-GATE

Ordered phases expose resource application and readiness progress.

- Apply resource groups in phase order
- Wait for applicable readiness checks
- Inspect ClusterObjectDeployment and revision status

Explain the ClusterExtension → ClusterObjectDeployment → ClusterObjectSet ownership model. ClusterObjectDeployment manages rollout and revision history; ClusterObjectSets hold immutable revisions with ordered phases. observedPhases and other status details help identify stalled objects. Objects within a phase have no defined ordering. The API and rollout behavior are in active development and controlled by feature-gate. Standalone ClusterObjectDeployment use is in active development. A namespace-scoped ObjectDeployment is under consideration, with no committed availability. Sources: https://github.com/operator-framework/operator-controller/pull/3058 and https://github.com/operator-framework/operator-controller/pull/3072.

## 8. User control of extension deployments

**Speaker:** OLM B — lifecycle primitives and migration; name to confirm  
**Start:** 08:00 · **Duration:** 01:30 · **Status:** IN ACTIVE DEVELOPMENT / CONTROLLED BY FEATURE-GATE

Flexible user-defined deployment configuration.

- Environment variables and resource settings
- Placement, volumes and deployment metadata
- Operator-provided configuration and schemas

Describe the deployment as a configuration exchange between users and the operator team. Users express environment, resource, placement, volume and metadata requirements through the package's configuration interface. Operator authors define schema and validation behavior. OLM carries the selected configuration into the deployment. DeploymentConfig is in active development and controlled by feature-gate; values are expressed through ClusterExtension configuration. Explain field-specific merge, replace and append behavior and annotation precedence. Validate example input and inspect the resulting deployment against the pinned source version. Watch-namespace pass-through leaves CRDs shared and supplies no watch-aware dependency management. Sources: supplied customization draft; ../kubecon-2026-resource-assessment.md; ../kubecon-2025-slide-context.md slide 14.

## 9. OLMv0 → OLMv1 migration

**Speaker:** OLM B — lifecycle primitives and migration; name to confirm  
**Start:** 09:30 · **Duration:** 02:00 · **Status:** IN ACTIVE DEVELOPMENT

Move operator management from OLMv0 to OLMv1.

- Prepare v1 catalogs from v0 CatalogSources
- Check and preview operator migrations
- Migration library with example binaries

Prepare OLMv1 ClusterCatalogs from the existing OLMv0 CatalogSources first. Then evaluate each operator installation for eligibility and preview its migration before transferring management. The check and preview actions evaluate operators; catalog preparation is the earlier prerequisite. The migration specification describes check, convert, rollback and cleanup with ClusterObjectSets. Functionality is supplied as library-olm. The example binaries illustrate library use. The example binaries produce structured output for automation and model consumers. The companion migration scenario exercises JSON Lines output. Eligibility checks have defined coverage. Retaining the namespace can reduce disruption; namespace changes may restart workloads or cause downtime. Validate recovery boundaries and source/gate versions for the selected case. This area is in active development. Sources: library-olm README/spec; ../kubecon-2026-resource-assessment.md; user migration guidance.

Note: Ask Todd to make a separate repo for the binaries (naming is hard :))

## 10. Install a bundle directly

**Speaker:** OLM B — lifecycle primitives and migration; name to confirm  
**Start:** 11:30 · **Duration:** 01:30 · **Status:** IN ACTIVE DEVELOPMENT / CONTROLLED BY FEATURE-GATE

Select a registry+v1 bundle by its OCI image reference.

- Use sourceType: OCIImage
- Set source.ociImage.ref
- Bypass catalog resolution

PR #2907 is OPEN and unmerged as of the 2026-10-28 check. Present direct bundle installation as proposed behavior in active development. It supports registry+v1 bundles only and is controlled by the BoxcutterRuntime feature gate. The requested source uses sourceType: OCIImage and source.ociImage.ref. It bypasses catalog resolution. Describe CRD checks and other lifecycle safeguards according to the proposal's supported path; catalog bypass alone establishes no blanket removal of CRD safety. Pin the source revision and gate configuration before preparing an example. The session uses prepared examples without a live demo.

## 11. Planned Helm content support

**Speaker:** OLM C — content, catalogs and contributions; name to confirm  
**Start:** 13:00 · **Duration:** 02:00 · **Status:** PLANNED / helm+v2

The rendering contract targets deterministic chart behavior.

- Chart and values produce managed manifests
- Allow-listed features support reproducible rendering
- helm+v2 identifies the content representation

helm+v2 is the user-confirmed canonical discriminator for versioned OLM Helm packaging/catalog content. Standard chart OCI identity is used, with rendered manifests managed through OLM lifecycle behavior. User values are parsed and validated during rendering. Deterministic rendering is the design goal: features are allow-listed to exclude non-deterministic functionality, with compatibility fixtures required to validate the supported subset. Dependencies are vendored. Hooks and keep behavior are unsupported in the proposal. CRDs use templates/; crds/ is unsupported. Chart release-object mappings and restricted template functions require compatibility testing. Moving CRDs affects upgrade, deletion and data handling. Implementation of proposed gates remains independently unconfirmed. Native chart OCI identity and future OCI catalog storage are separate scopes. Sources: supplied Helm planning brief and feature-planning context.

Transition: the direct-image source motivates future chart content support. The companion Helm experiment uses an OCI image config; standard Helm OCI config handling remains unverified.

## 12. Catalog performance and content types

**Speaker:** OLM C — content, catalogs and contributions; name to confirm  
**Start:** 15:00 · **Duration:** 01:30 · **Status:** PLANNED / FUTURE WORK

Design for lower catalog-processing cost and additional content types.

- Lower duplicated CSV metadata
- Direct version fields reduce property traversal
- Typed registry+v1 and helm+v2 content

Credit established FBC capabilities: plaintext editing, composition, extensibility, package-level metadata and version/release properties already exist. The v2 work refines the representation and consumers: less duplicated CSV metadata, version/release fields available directly rather than via property traversal, and explicit mediaType dispatch for installable formats including Helm. Arbitrary FBC schema extensibility alone does not supply end-to-end installation support for a new content type. Catalog processing efficiency is a design benefit to validate, with no measured speedup claimed. Show the practical resolution/metadata work the new representation is intended to reduce. The user-confirmed near-term focus is flexible OLMv1 schemas; OCI-native catalog storage, transport and selective fetching are future work. Channels and legacy graphs are excluded from v2; lifecycle/constraint metadata remains open. Sources: https://olm.operatorframework.io/docs/reference/file-based-catalogs/ ; supplied v2 catalog brief; feature-planning context.

## 13. Shared lifecycle logic in library-olm

**Speaker:** OLM C — content, catalogs and contributions; name to confirm  
**Start:** 16:30 · **Duration:** 01:00 · **Status:** IN ACTIVE DEVELOPMENT

Reuse lifecycle logic through a library with explicit contracts.

- Share migration checks and workflow logic
- Exercise current development examples
- Record expected results in reusable fixtures

Describe library reuse, the current migration development examples and fixtures that record inputs and expected results. The example binaries exercise library behavior and provide contribution starting points. Broader controller, CLI and UI consumption remains a design intent requiring implementation evidence and explicit contracts. Successor semantics need a defined contract. Fixtures can cover legacy input or version/release selection while respecting the proposed v2 schema direction. Pin source versions when documenting examples. C connects catalog work with shared lifecycle logic. Sources: library-olm README/spec; supplied feature-planning context; ../kubecon-2025-slide-context.md slide 13.

## 14. Contribute to Operator Framework

**Speaker:** OLM C — content, catalogs and contributions; name to confirm  
**Start:** 17:30 · **Duration:** 01:00 · **Status:** PROJECT DEVELOPMENT

Contribute to Operator Framework development.

- Read the repository contribution guide
- Discuss an issue and propose a change
- Submit code, documentation or test fixtures

Invite contributions to the Operator Framework project: documentation, focused tests, code, and reproducible migration, chart, or schema fixtures. Start with the repository contribution guide: https://github.com/operator-framework/operator-controller/blob/main/CONTRIBUTING.md. Identify an issue or discussion, provide a reproducible case, and describe the expected result.

## 15. Operator Framework: Java Operator SDK

**Speaker:** OLM C — content, catalogs and contributions; name to confirm  
**Start:** 18:30 · **Duration:** 00:30 · **Status:** 





C hands off to Attila for the Java Operator SDK section. OLM packaging supports operators written in any language; SDKs support controller implementation. Attila presents the ten authored SDK slides, unchanged, in approximately ten minutes.

## 16. SDK source slide 3

**Speaker:** Attila

**Start:** 19:00 · **Duration:** 01:00

Original authored slide XML and illustrations retained. SDK wording and release/version claims remain the author's source content. This import adds assignment/timing notes only.

Source: ~/Downloads/Copy of KubeCon2026.pptx, slide 3.

Read-Cache-After-Write Consistency since v5.3 API:   UpdateControl.patchStatus(resource) context. resourceOperations() .serverSideApply(resource); Additional cache brings complexity: Indexers Items store Comparable Resource Versions KEP Read-cache-after-write consistency blog 

## 17. SDK source slide 4

**Speaker:** Attila

**Start:** 20:00 · **Duration:** 01:00

Original authored slide XML and illustrations retained. SDK wording and release/version claims remain the author's source content. This import adds assignment/timing notes only.

Source: ~/Downloads/Copy of KubeCon2026.pptx, slide 4.

Read-Cache-After-Write Consistency

## 18. SDK source slide 5

**Speaker:** Attila

**Start:** 21:00 · **Duration:** 01:00

Original authored slide XML and illustrations retained. SDK wording and release/version claims remain the author's source content. This import adds assignment/timing notes only.

Source: ~/Downloads/Copy of KubeCon2026.pptx, slide 5.

Event Filtering - API & Challenges Filter out events for our own updates Challenges Informer lost event problem Our update did not change the resource but other actor did concurrently   context. resourceOperations() .serverSideApply(resource); 

## 19. SDK source slide 6

**Speaker:** Attila

**Start:** 22:00 · **Duration:** 01:00

Original authored slide XML and illustrations retained. SDK wording and release/version claims remain the author's source content. This import adds assignment/timing notes only.

Source: ~/Downloads/Copy of KubeCon2026.pptx, slide 6.

Event Filtering for Read-Cache-After-Write-Consistency

## 20. SDK source slide 7

**Speaker:** Attila

**Start:** 23:00 · **Duration:** 01:00

Original authored slide XML and illustrations retained. SDK wording and release/version claims remain the author's source content. This import adds assignment/timing notes only.

Source: ~/Downloads/Copy of KubeCon2026.pptx, slide 7.

Informer Pools Sharing underlying informers between controller Matches the informer configuration Except list limit  Details in  InformerClassifier Supports dynamic Informer registration and de-registration

## 21. SDK source slide 8

**Speaker:** Attila

**Start:** 24:00 · **Duration:** 01:00

Original authored slide XML and illustrations retained. SDK wording and release/version claims remain the author's source content. This import adds assignment/timing notes only.

Source: ~/Downloads/Copy of KubeCon2026.pptx, slide 8.

Informer Pools

## 22. SDK source slide 9

**Speaker:** Attila

**Start:** 25:00 · **Duration:** 01:00

Original authored slide XML and illustrations retained. SDK wording and release/version claims remain the author's source content. This import adds assignment/timing notes only.

Source: ~/Downloads/Copy of KubeCon2026.pptx, slide 9.

Observability stack enhancements Facelift over  Observability stack Improved logging and Mapped Diagnostic Context (MDC) Putting event and primary resource to MDC if available Metrics API refined MicrometerMetricsV2 Generic Grafana Dashboard Sample with OTel + Prometheus + Grafana  

## 23. SDK source slide 10

**Speaker:** Attila

**Start:** 26:00 · **Duration:** 01:00

Original authored slide XML and illustrations retained. SDK wording and release/version claims remain the author's source content. This import adds assignment/timing notes only.

Source: ~/Downloads/Copy of KubeCon2026.pptx, slide 10.

Java Virtual Threads (WIP)  Planned for v5.7.0 We will officially support this for Java 25+ (but will work with Java 21+) Replacing ThreadPools with virtual threads  across  framework Virtually unlimited number of concurrent reconciliation The explicit limit applies though 

## 24. SDK source slide 11

**Speaker:** Attila

**Start:** 27:00 · **Duration:** 01:00

Original authored slide XML and illustrations retained. SDK wording and release/version claims remain the author's source content. This import adds assignment/timing notes only.

Source: ~/Downloads/Copy of KubeCon2026.pptx, slide 11.

Java Virtual Threads (WIP) 

## 25. SDK source slide 12

**Speaker:** Attila

**Start:** 28:00 · **Duration:** 01:00

Original authored slide XML and illustrations retained. SDK wording and release/version claims remain the author's source content. This import adds assignment/timing notes only.

Source: ~/Downloads/Copy of KubeCon2026.pptx, slide 12.

Some honorable mentions… EventRecorder API ShardSelector support Documentation improvements - operations section 

## 26. Resources and contribution steps

**Speaker:** OLM A — session host; name to confirm  
**Start:** 29:00 · **Duration:** 01:00 · **Status:** RESOURCE PACKAGE TO PREPARE

Use documented contracts and reproducible cases to guide contributions.

- Check content against a documented contract
- Share a reproducible case or fixture
- Select a maintainer-scoped contribution

Close with the Operator Framework contribution guide, the OLM documentation, and the Java Operator SDK project. Companion demos are intended for online use; no live demo is planned. Confirm resource links before publication.

## 27. Questions?

**Speaker:** OLM A/B/C and Attila — questions  
**Start:** 30:00 · **Duration:** 02:00 · **Status:** 

Questions about lifecycle APIs, packaging or controller behavior?

- OLM configuration and migration
- Helm content and catalog schemas
- Java Operator SDK reconciliation

Reserve two minutes for questions and transition overruns. A/B/C answer OLM questions; Attila answers Java Operator SDK questions. The proposed total duration is 32 minutes.

