# Demo development status

Started 2026-10-27. Demo material lives in
[~/devel/kubecon-2026-demos](https://github.com/grokspawn/kubecon-2026-demos)
(clone of `grokspawn/kubecon-2026-demos`); see its `README.md` and
`demo-plan.md` for the implementation inventory and per-demo plans.

## Source-control state

- `grokspawn/operator-controller`: fork `main` synced to upstream
  (75d8c16e, includes ObservedPhase enrichment #3044/#3045). Integration
  branch `kubecon-2026-demo` pushed off main. Feature sub-branch
  `kubecon-2026-demo-direct-bundle` carries PR
  [operator-framework#2907](https://github.com/operator-framework/operator-controller/pull/2907)
  (our fork's direct registry+v1 bundle installer, still OPEN upstream)
  rebased cleanly as three cherry-picks; `go build`/`go vet`/resolve tests
  pass. Sub-branches use hyphens because git refs cannot hold both
  `kubecon-2026-demo` and `kubecon-2026-demo/...`.
- `grokspawn/library-olm`: fork created; `kubecon-2026-demo` branch pushed
  off main (e0645d3). Migration CLIs (`migrate-catalogs-v0-to-v1`,
  `migrate-operators-v0-to-v1` with check/convert/rollback/cleanup/batch
  and structured output) are implemented upstream; no fork changes needed
  yet.
- Task clones: `~/devel/agent-playground/kubecon-oc-direct-bundle`,
  `~/devel/agent-playground/kubecon-library-olm` (plus
  `library-olm-inspect`, a read-only upstream clone used for inventory).
  Neighboring `~/devel/operator-framework/*` checkouts untouched.

## Findings affecting demo design

- catalogd is archived (Jan 2025); its function moved into
  operator-controller. No separate catalogd dependency.
- Direct bundle install exists only in PR #2907; it is not on upstream
  main and requires the `BoxcutterRuntime` gate (Alpha).
- ClusterObjectSets (phased rollout) and `DeploymentConfig` are on
  upstream main behind Alpha gates; demos 2–3 need builds only, no fork
  code. Upstream status model recently gained `ObservedPhase` status/
  completedAt/message/objectDetails — demo scripts should pin the commit.
- library-olm has no successor-resolution implementation; only migration.
- operator-registry main has no v2 catalog schema references; the
  catalog-v2 and Helm-content work remains design-stage upstream.
- Local envtest assets (`/usr/local/kubebuilder/bin/etcd`) are x86_64 on
  this arm64 host; controller envtest suites need arm64 assets before
  they can run.

## Current deck and demo updates

The current Google deck has 27 slides and a 32-minute rehearsal schedule.
Demo cross-references follow that order. Demo 1 now omits `spec.namespace`
to demonstrate a managed install namespace, shows its revision owner, and
waits for namespace and CRD cleanup. Its refreshed asciinema recording was
captured on the named disposable kind cluster after verifying the baseline;
the script checks the context and node provider IDs before deletion. Deleting
the managed namespace and CRD also deletes their contents.

## COD architecture tracking (2026-10-28)

Upstream merged #3058 ("Apply a ClusterObjectDeployment instead of
managing ClusterObjectSets") on 2026-10-28, one day after our demo
branches were cut: the operator-controller now applies one
ClusterObjectDeployment per ClusterExtension, and the COD controller owns
the revision lifecycle (cutting/archiving ClusterObjectSet revisions,
revisionHistoryLimit, progressDeadlineMinutes, impeded-rollout
Progressing reasons). ClusterObjectSets remain as immutable revision
objects; open PR #3078 removes the COS progression timeout, confirming
the migration of rollout semantics to the COD.

Response: fork branches rebased onto main 255a4026 (direct-bundle PR
#2907 commits rebased with one conflict in main.go from the #3048
CatalogResolver field renames; helm-direct stacked cleanly after
resolving getBundleAnnotations — upstream's new TODO there asks for
exactly the format-sniffing our change implements — plus
SimpleRevisionGenerator SystemNamespace and the #3058 test deletions).
All builds and tests pass; branches force-pushed; integration branch
updated. Demo pins updated (direct-bundle c8a7d3fe, helm-direct
5efa7495).

Demo 2 rewritten around the COD model (ownership chain, impeded-rollout
reasons, revision cut on config change, archival); demos 1/5 show the
COD alongside revisions. Re-recording against the rebuilt cluster.

Re-recording completed 2026-10-28: demos 1, 2, 3 and 5 re-cast on the
COD-era build (demos commit b73bb65). Demo 2's recording shows the COD
spec (template with bundle annotations, revisionHistoryLimit), the
blocked phase surfacing through COD Available=False/Progressing=True
plus the revision's Stabilizing detail, recovery, and a config change
cutting revision 2 with revision 1 Archived. Demo 4 is pinned to
released OLMv0/OLMv1 versions and was unaffected.

## Demo scope

Confirmed: 1 direct bundle install, 2 phased rollout, 3 deployment
config, 4 migration + structured output, 5 Helm chart direct install
(new demo-scope code stacked on the direct-bundle sub-branch; explicitly
the evolution path recorded in `../kubecon-2026.txt`).
Pending confirmation: catalog v2 offline schema demo, successor
resolution, optional OLMv0 shared-CRD historical failure.
User decisions 2026-10-27: secondary areas deferred (none for now);
demo 5 starts after demos 1–4 are recorded.

## Validation log (2026-10-27)

- Demos 1–3 executed end to end on the
  `operator-controller-experimental-e2e` kind cluster (built from
  `kubecon-2026-demo-direct-bundle`); asciinema casts captured in each
  demo's `recordings/`.
- Findings folded back into scripts: explicit `spec.namespace` must
  pre-exist (controller reports, does not create); ClusterExtension has
  no `Ready` condition — waits use `Available`; inline config
  validation rejects unknown fields at reconcile with an
  `InvalidConfiguration` condition, not at admission; the kubelet does
  not trust the demo registry CA, so operator images are `kind load`ed
  onto nodes under their in-cluster refs with
  `imagePullPolicy: IfNotPresent`.
- Host quirks: docker VM disk filled once (pruned dangling images/build
  cache; user's MCP containers untouched); skopeo needs
  `--insecure-policy` for localhost pushes because the host's
  containers/image policy rejects unlisted transports; skopeo cannot use
  the colima socket via DOCKER_HOST, so pushes go through
  docker-archive; this asciinema build (3.2.1) writes delta timestamps
  and cannot play back in a headless shell (no TTY).
- Demo 4 first setup attempt failed on a missing executable bit; fixed.
- Demo 4 additional findings: OLMv0 crds.yaml needs server-side apply
  (262KB annotation limit); two kind clusters exceed the 4CPU/8GiB
  colima VM (demos 1–3 cluster torn down after recording; migration
  cluster is single-node); the migration convert refuses when
  migration-created ClusterObjectSets linger, and a failed conversion
  can leave the operator's RBAC broken — run.sh now does a deterministic
  full-namespace reset before each run. Recorded cast shows check →
  catalog adoption → jsonl output → convert → verified handoff
  (ClusterExtension installed at the same version, Subscription removed,
  deployment never restarted).
- Demos 1–4 recorded and committed as of 2026-10-27. Demo 5 (Helm chart
  direct install, new code on kubecon-2026-demo-helm-direct) is next per
  the agreed sequencing.
- Demo 5 implementation complete on `kubecon-2026-demo-helm-direct`
  (commit 9973f48b, stacked on the direct-bundle branch): content
  sniffing for extracted charts and standard `helm push` tgz artifacts;
  HelmManifestProvider with inline values + values.schema.json
  validation, hook/keep annotation rejection, banned non-deterministic
  template functions, unvendored dependency rejection, .Release mapped
  to extension identity with proposed always-upgrade semantics;
  dispatching ManifestProvider wired in main.go. All touched-package
  unit tests pass; envtest suites now run locally after replacing the
  x86_64 kubebuilder assets with arm64 ones via setup-envtest
  (reinstalled natively; KUBEBUILDER_ASSETS must be absolute).
  Cluster validation and recording of demo 5 in progress.
- Demo 5 validated and recorded 2026-10-27/28: chart artifact pulled,
  sniffed, rendered with inline values (user replicaCount honored),
  CRD-in-templates managed through the lifecycle, bad chart rejected
  naming the template and function, full cleanup. Two upstream-relevant
  findings: containers/image refuses to unpack standard helm-push
  artifacts (cncf.helm config media type), so the demo assembles chart
  artifacts with OCI image configs; and the image cache unpacks the
  chart layer leaving the chart under its name directory, so sniffing
  recognizes three chart shapes. Final commits: fork branch
  kubecon-2026-demo-helm-direct; demos repo commit 007aca3. All five
  demos now have scripts, validated runs and asciinema recordings.
