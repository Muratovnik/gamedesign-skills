# Comparative change verification

This record concerns the changes derived from the
[external comparison](../../research/2026-10-08/comparison.md). It is separate
from the [historical own baseline](../2026-10-08/game-design-own-baseline.md).
The historical review is not independent approval of the new candidate.

**Work status:** runtime implementation, scoped operational reviews, all
twelve paired subjects and fresh product/behavior reviews are complete.
Authenticated native installed-client model behavior remains
blocked and is not qualified by the alternate comparison harness. The PR remains
a draft; this record does not claim full product acceptance.

## Source and experiment identity

- Initial researched main: `4fc654c2cb92989582c30bc048742f2cce7659ba`.
- Updated main used for implementation/comparison:
  `a0db5af71146586cf861881670c991ad94d87e2b`. The intervening release changes did
  not change runtime skills or game examples.
- Complete reviewed runtime candidate:
  `1873993a6491b52fe8288c19837600a012e18d4d`, tree
  `237e2892adefbf170c149ac644b0c4a18b31ba76`.
- Assay: 0.17.2, `94c517b0aac9ba2575086bf9aead1cc828aadb0d`, identical in the
  compared environments and separately obtained.
- Main has 48 runtime skill files; the frozen candidate has 59. Counts identify
  the compared sets, not their quality. Exact per-file identities are retained
  in the review and model records.

The candidate keeps the upstream 0.1.1 source version while additions are
unreleased. Same-version native replacement is deliberately checked by file
sets and hashes. A final evidence commit necessarily differs from the runtime
snapshot it records; file identities govern reuse of the runtime checks.

The [baseline byte comparison](baseline-reuse-identity.json) verifies the 151
historically recorded corrected files against the initially researched main,
including all 48 runtime files. The
[input identity record](input-document-identity.json) matches 11 supplied
historical inputs and excludes the normalized recovered plan and new discovery
report from that equality claim. The [runtime inventory](runtime-size-and-files.json)
records the source and size delta; none of these is a rerun of historical tests.

## Executed product checks

[GitHub Check run 37819498740](https://github.com/Muratovnik/gamedesign-skills/actions/runs/37819498740)
passed all four jobs on the runtime candidate. The actual server run/job/artifact
metadata is in [ci-runtime-provenance.json](ci-runtime-provenance.json).
The job logs identify GitHub's actual PR merge checkout as
`a06f5336e5805c0cd84c924ca3aefdc658dc8401`.
[Fetched Git data](ci-runtime-merge-identity.json) confirms that its complete
tree equals `237e2892adefbf170c149ac644b0c4a18b31ba76`, the candidate tree above.

| Suite or gate | Actual result | Scope |
| --- | --- | --- |
| Root Python suite | 26 passed on Linux and Windows | Packaging, distribution, binding and three native-verifier controls |
| Adaptation | 11 passed on Linux and Windows | Existing target-content consumer and legal/error controls |
| Analysis lab | 30 passed on Linux and Windows | Existing consumers plus saved observation-context regression |
| Godot receipt/runner unit suite | 13 passed on Linux and Windows | Python runner/assessor cases; this job does not execute Godot |
| Harbour/Loom executable tests | 2 passed on Linux and Windows | Existing score/content consumers |
| Strategy matrix | 18 passed on Linux | Actual SciPy 1.17.0/NumPy 2.3.5; includes corrupt-candidate refusal controls |
| glTF/GLB | 19 passed on Linux | Actual Khronos dependency, task-owned copied adapter/install |
| Native Ink | 8 passed on Linux | Actual inkjs 2.4.0, compilation, execution and fresh-process state |
| Static/projection/link/schema checks | Passed on Linux and Windows at runtime snapshot | Seven skills, local links, schemas and generated inventory |
| Release audit, archive build and smoke | Passed on Linux and Windows at runtime snapshot | Actual source archive and extracted package, not a public release |

This is **127 distinct suite tests**: 82 existing/root tests run on both OSes,
plus 45 optional-operation tests on Linux. Repeated local/reviewer runs are not
added to that total. Passing a script test does not establish model discovery,
human experience or arbitrary engine support.

Final review subsequently corrected a maintainer-only package receipt claim:
public evaluation records can be archived under `docs/reviews` while runtime
`evals` directories remain excluded. A new archive/reopen regression passed
with the complete **27-test root suite** locally. This raises the current
distinct suite inventory to **128**; it does not change the 127-test result of
the earlier runtime CI snapshot or any runtime file used by the model subjects.

An additional [fresh virtualenv first-use run](clean-matrix-first-use.json)
executed the documented unmodified requirements file, allowing its NumPy
requirement to resolve normally. It installed SciPy 1.17.0 and NumPy 2.5.3 under
Python 3.12.14; the actual Channel Signals CLI and all 18 matrix tests passed.
This qualifies that specific resolver outcome, not every version in SciPy's
declared NumPy range. It does not change the paired experiment's common NumPy
2.3.5. [Raw install/operation/test records](clean-matrix-first-use.zip),
[manifest](clean-matrix-first-use-manifest.json) and
[dependency terms/identity](clean-matrix-dependency-terms.json) are retained.

Actual job logs:
[Linux](ci-runtime-113456576647.log),
[Windows](ci-runtime-113456576901.log),
[optional operations](ci-runtime-113456576836.log),
[native clients](ci-runtime-113456576892.log).

## Fresh native client lifecycle

The native job ran on a fresh Linux x86_64 user with Python 3.12.15, Codex
0.159.2 and Claude Code 2.1.289 installed into task-owned runner storage. It
retained previous and candidate source directories and used each client's real
local marketplace manager. All 72 commands and 24 observations are preserved in
[native-lifecycle-qualified.json](native-lifecycle-qualified.json); the original
downloaded [artifact ZIP](native-lifecycle-qualified.zip) includes the exact
client package lock. Its SHA-256 is
`f78b01ed5ec0bab19c9a7a6b26e678aacbee6027b3d47c4d50f3fe058391a24f`.
The receipt SHA-256 is
`87d9d9c379cc6df24b79e5447fa83953937bef3fb55aa469ad2abe9a3973da24`.

Both clients installed main, disabled/reenabled it, replaced the registration
with the candidate, restored main and removed the target. Exact seven-skill
inventories and complete 48/59-file runtime sets were checked. Eight resource
actions executed the actual effective-source observation script and reopened
its report. Candidate reports carried all three corrected context fields.

Codex used namespaced native names and fresh app-server inventories. Disabling
removed its target from that inventory. Claude's native merged enable setting
changed while `details` still described the disabled package. Its actual source
was `readFromFolder`, not the separate cache. The verifier checked and executed
that source. These are registration, metadata and resource observations;
authenticated model selection/adherence is a separate boundary.

The local [Claude authentication status](claude-auth-status.json) additionally
records `loggedIn=false`, `authMethod=none`. No credential content is retained.
Thus an authenticated Claude model turn was unavailable through this installation;
native manager success does not fill that gap.

A sentinel plugin retained its full registration record through the target
lifecycle. Owned sentinel cleanup left both installed-plugin inventories empty.
This is evidence about registration interference, not arbitrary game saves or
plugin persistent data. Replacement used remove/add against retained sources;
automatic upgrade and save migration were not tested.

The first hosted attempt is preserved as
[native-lifecycle-first.json](native-lifecycle-first.json) and its
[original ZIP](native-lifecycle-first.zip). It correctly installed native
components but stopped because the verifier expected unqualified Codex names
and a failing disabled Claude `details`. Those expectations were wrong. The
corrected run reached the previously unexecuted replacement/rollback/removal
stages. The historical isolated bootstrap failure is also retained in the old
baseline; neither failure is relabeled as a package-quality failure.

## New independent review

Two reviewers who did not implement the subject inspected source and contracts,
executed actual dependencies and retained independent controls. Their verdicts
are bounded by file identities and reviewed responsibilities.

### Integration and evidence

[Integration review](integration-review.md) first found six actionable issues,
all corrected and rechecked:

1. A glTF report could create its own missing input through a directory alias.
2. Native verifier expectations rejected valid Codex names/disabled Claude details.
3. Claude source verification used the cache instead of the effective local source.
4. Substring inventory matching could accept a missing router skill.
5. Rollback comparison ignored surplus runtime files.
6. Timeout/protocol failures could lose the attempted command and partial evidence.

The review reran 19 glTF cases and three native-verifier tests; a disposable
observation mutant missing the context fields failed the new saved-output test.
It then independently checked the successful native receipt against both Git
revisions and all corrected scoped files: **144 receipt assertions passed**.
These are assertions about that receipt, not 144 additional game scenarios.
No in-scope defect remained. The review does not certify global docs, Ink/matrix
implementations or model behavior.

Full original supporting records and read-only verifier:
[integration-evidence.zip](integration-evidence.zip),
[manifest](integration-evidence-manifest.json).

### Numerical and narrative operations

[Numerical/narrative review](numeric-narrative-review.md) found no confirmed
in-scope defect in the frozen 21-file scope. It independently reran the 18 matrix
and eight Ink tests. Additional **19** actual matrix calculations used a
separate exact-Fraction two-row minimax oracle, including maximum-finite,
large-offset and subnormal utilities. The largest independently recomputed
normalized response gap was `1.376676550535194e-16`.

Additional **34** native Ink commands checked previously unobserved state after
resume, no repeated text, silent endings, lawful native functions/sticky choices,
host-work refusal, malformed reports, identity drift and exact output bounds.
One initial reviewer expectation about silent `END` text chunks was wrong; its
failure and corrected oracle are preserved. No product edit was needed for it.

Full original probe scripts, synthetic inputs, actual outputs and failed oracle:
[numeric-narrative-evidence.zip](numeric-narrative-evidence.zip),
[manifest](numeric-narrative-evidence-manifest.json).

These archives omit dependencies and duplicate source snapshots. Their manifests
preserve original evidence paths and SHA-256 values. Absolute paths in original
receipts describe the execution environment; they are not portable installation
instructions. Public example READMEs provide the reproducible supported routes.

### Product, global documentation and comparative evidence

The [fresh final product review](final-product-review.zip) and its
[manifest](final-product-review-manifest.json) retain a scoped **PASS after
correction**, with broader native-model acceptance explicitly **INCONCLUSIVE**.
It checked the complete runtime file set, current owner/routing contracts,
requirements and dependent plan, source/terms claims, installation documentation,
prior review identities and the materialized evidence assembly.

The review closed the package receipt's misleading evaluation-absence claim,
made the actual CI merge/tree identity explicit, and independently checked the
source-excerpt licenses. It ran 35 source/receipt/archive checks and the new
packaging regression. The seal covers 241 materialized files for identity;
direct reading and focused diff scopes are listed separately. This is not a
claim to have reread every line or rerun every historical test.

The [separate behavioral review](behavior-independent-review.zip) and its
[manifest](behavior-independent-review-manifest.json) independently examined all
six pairs and replayed numerical, Ink and glTF outcomes. It supports the
qualified diagnostic report, retaining main's localized observation prose
defect and the experiment's limitations. Its judgment is described in the
[model record](model-comparison.md#fresh-independent-review-of-this-comparison).

Both reviews precede adding their own receipts and the final publication
metadata. Those later evidence-only additions receive final archive/link and
scope-delta checks; they are not retroactively included in a prior review seal.

### Publication evidence and scanner boundaries

The separate [publication adjudication](publication-audit.md),
[original selected receipts](publication-audit-evidence.zip) and
[archive manifest](publication-audit-evidence-manifest.json) explain the actual
scanner findings and the narrow changes required to retain this public evidence.
An independent replay found 26 detections, all three independently recomputed
public content hashes. Three Betterleaks allowlist blocks require the exact rule,
digest and evidence path together; all eight neighboring boundary controls
passed. Default detection rules remain enabled.

The original review examined nine exact evidence-file exclusions. A subsequent
independent check reopened all 103 entries of its own publication-evidence ZIP,
matched all 102 selected payloads and the unchanged selection manifest, and
found no unsafe ZIP paths, symlinks, duplicate entries or CRC failures. Betterleaks
with the original configuration found no secrets in that ZIP. The only public
ReleaseKit finding was the captured home-path inventory, which justified a tenth
exact evidence-file exclusion. These exclusions omit suppressible built-in
path and semantic rules for those specific files; external scanning, archive
limits and declared non-excludable private/owner patterns remain enforced.
The archived review explains this boundary and why replacement bytes need a
new assessment. No parent-folder or wildcard exclusion was added.

The new outer publication manifest originally used filenames as JSON keys;
six hashes of scanner-control receipts were then classified as credentials.
Its generated representation now uses separate `path` and `sha256` fields.
The original selected receipts, internal selection manifest and ZIP bytes are
unchanged. This required no additional secret allowlist.

**Correction to the archived review's owner-gate wording:** its statement that
a final owner audit was unconditionally required was too broad for this draft
PR. Follow-up inspection of the pinned ReleaseKit implementation confirmed that
`[release].owner_audit` and `require_guard` apply to release procedures; the
ordinary audit enters owner mode only when requested. An installed owner
pre-push guard would also apply to ordinary pushes, but `protect check` confirmed
that this temporary checkout has no such guard. The existing
[publication instructions](../../../docs/releases.md) distinguish that owner
checkout from this public PR path. No private policy or guard was modified or
created, and neither owner-audit nor release readiness is claimed. This dated
correction leaves the independent review's original bytes intact.

The final branch's public audit, checks, build and smoke results belong to its
own GitHub Check run linked from the PR. The earlier runtime CI and the review
seals above retain their original, narrower identities.

## Comparative research execution

The research records distinguish source inspection, author-reported claims and
local execution. Domain probes include all 34 passing upstream matrix tests,
additional semantic counterexamples, the original observation-loss reproduction
and numerical feasibility. Native environment probes include actual Ink and
Khronos operations with positive/defective/neighboring controls.

- [Domain probe archive](domain-research-probes.zip) and [manifest](domain-research-probes-manifest.json).
- [Environment probe archive](environment-research-probes.zip) and [manifest](environment-research-probes-manifest.json).

The probe inputs and code are original; stdout records what the inspected tools
actually returned. No installed dependency bundle is included. Separately, raw
model evidence includes source reads with retained licenses and attribution,
as described in [NOTICE](../../../NOTICE.md). No Blender, Unity or new Godot
runtime run is claimed by these probes.

## Paired model tasks and remaining scope

Main and candidate task packets and rubrics were frozen before subject outputs,
with six families: utility matrix, observation-context handoff, Ink continuation,
glTF conformance, a sufficient paper-rule edit and expressive composition.
The same Assay, model/effort, external primitives and task requirements are used
on both sides. The intervention is the complete skill-plus-tool package; it is
not an instruction-only ablation.

The [completed model comparison](model-comparison.md) records all twelve
subjects, each task's outcome and preserved limitations. Both versions produce
correct matrix, Ink and glTF outcomes and complete the two paper controls.
Candidate preserves unspecified assistance more clearly in one observation
handoff and actually uses all four changed operations. No general superiority,
cost saving or causal effect of individual instructions is established.

The [original evidence archive](behavior-evidence.zip) and
[manifest](behavior-evidence-manifest.json) preserve the six pairs, task/rubric
freezes, source-read traces, artifacts, failed attempts, calibration history and
evaluator corrections. The additional [native model preflight](native-model-preflight.zip)
and [manifest](native-model-preflight-manifest.json) record the independent
explicit-prompt terminal timeout and redacted Claude authentication status.
Native metadata alone is not a model run, and the successful explicit-source
comparison does not qualify automatic client selection.

Existing Godot 4.7.2 receipts and paper studies are reused only for unchanged
files and their original limited claims. No human playtest, full Ink-language
coverage, glTF target-engine import, Unity/Blender pipeline or universal
model-performance result is established. Conditional research candidates do not
become mandatory changes merely because they appear in the comparison.
