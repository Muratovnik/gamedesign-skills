# External comparison and implemented decisions

Research and implementation date: **2026-10-08**.

The comparison supports four changes: preserve observation context in the
existing importer; add an optional certified zero-sum calculation; execute and
resume native Ink artifacts; and validate glTF/GLB with the Khronos consumer.
It does **not** support installing a second game-design framework, importing a
general agent workflow, or requiring these tools for every game.

This report owns the comparative rationale. The [requirements and plan
addendum](requirements-and-plan.md) owns this change's acceptance delta. Runtime
instructions remain with the existing skill owners; general methodology remains
with [Assay](https://github.com/Muratovnik/assay/tree/94c517b0aac9ba2575086bf9aead1cc828aadb0d).
The [verification record](../../reviews/2026-10-08-comparison/README.md) separates
technical execution, native discovery, model behavior and independent review.

## Baseline, questions and search scope

The supplied review was a discovery pointer, not evidence of a repository's
contents, license, compatibility or performance. We resolved exact repositories,
read selected implementations and their references, inspected tests and terms,
and ran discriminating probes where an executable environment was available.
Repository names, star counts, file counts and matching skill names did not decide
acceptance. The detailed research records retain the inspected paths,
unread portions, counterexamples, provenance and reconsideration conditions:

- [Domain methods and tools](domain-landscape.md).
- [Environment components and native consumers](environment-components.md).
- [Computational game and multi-agent environments](simulation-environments.md).

The initial product revision was
[`4fc654c2cb92989582c30bc048742f2cce7659ba`](https://github.com/Muratovnik/gamedesign-skills/commit/4fc654c2cb92989582c30bc048742f2cce7659ba).
The independently reconstructed corrected baseline matched all **151** retained
files, including **48** runtime files; **11** currently supplied historical source
inputs matched their recorded identities. The recovered normalized plan and the
new discovery report are outside that input-equality claim. This was a file comparison, not a fresh
execution of the historical checks. The earlier correction commit was not
available in the shallow checkout, so no unavailable Git comparison is implied.

During this work, main advanced to
[`a0db5af71146586cf861881670c991ad94d87e2b`](https://github.com/Muratovnik/gamedesign-skills/commit/a0db5af71146586cf861881670c991ad94d87e2b).
Those intervening commits changed release identity, projections and publication
documentation; the runtime skills and game examples used for comparison were
unchanged. We retained the upstream 0.1.1 release work and used this newer main as
the implementation and paired-comparison base. A version label does not identify
the candidate: its first complete runtime snapshot is
[`1873993a6491b52fe8288c19837600a012e18d4d`](https://github.com/Muratovnik/gamedesign-skills/commit/1873993a6491b52fe8288c19837600a012e18d4d),
tree `237e2892adefbf170c149ac644b0c4a18b31ba76`. Later evidence and documentation
must be read with their own source identities.

Questions were derived from the common product, rather than the external
packages' taxonomies: construct a game relation; revise an existing artifact;
preserve information, assistance, rights and lawful endings; calculate a stated
model; consume native narrative and asset formats; retain observations; and make
installation, discovery, operation and evidence distinguishable.

Search covered six subject-method repositories, Blender/Unity/Godot operation
families, narrative runtimes, numerical optimization and asset conformance.
It expanded beyond the supplied list to official Unity and Blender routes,
live Godot observation, Ink/Yarn, Khronos validation, SciPy/Nashpy and
OpenSpiel/PettingZoo game-environment representations. This is a
task-driven comparison of meaningful components, not an exhaustive survey of
every engine, art service or game-design publication. Unread or unexecuted
branches are explicitly bounded in the research records and cannot justify a
transfer by themselves.

## What changes, and what was already present

| Decision | Intended result and existing counterpart | Exact transferred unit | Cost and acceptance |
| --- | --- | --- | --- |
| **M1 — adapt an operation idea and connect SciPy** | GDE-02 already required meaningful utilities, reproducible calculations and sensitivity. Systems design and the analysis lab covered resources, access and state, but supplied no executable matrix solver. | Original `solve_zero_sum.py`, optional dependency declaration, conditional systems reference and original examples. SciPy/HiGHS performs optimization; the adapter verifies the reported mixtures independently. No apetrov source is copied. | Optional SciPy/NumPy environment; a deliberately limited model/input contract; numerical and dependency maintenance. Accept mathematical consequences only after probability, value and best-response checks. |
| **M2 — repair an existing requirement** | GDE-09 and GDR-10/11 already required the conditions of observation and the work done by assistance. The input schema required this context, but the importer discarded it. | Preserve `conditions`, `collection_method` and `units` in the saved observation report. Extend its existing test and environment description. No new playtest protocol or report template. | Three fields carried through the same data path; a saved-output regression test. Equal counts with different assistance remain distinguishable after reopening. |
| **I1 — connect a native narrative consumer** | Conditional story already distinguished state, knowledge, commit points, interruption, refusal and meaningful common endings. The missing operation was actual Ink compilation, choices and state restoration. | Original `ink_artifact.cjs`, exact inkjs dependency/lock, conditional narrative reference and original episode/scenarios. inkjs owns the language and runtime. | Optional Node/package environment; explicit action/observation contract; artifact identity and execution bounds. No new narrative VM, automatic player or mandatory branching structure. |
| **G1 — connect a format validator** | The shared environment contract already required reading the actual artifact, retaining identity and reopening through a consumer. No shipped glTF/GLB operation established format conformance. | Original `validate_gltf.cjs`, exact Khronos dependency/lock, conditional environment reference and original fixtures. The real Khronos library parses and validates. | Optional Node/package environment; bounded local-resource resolution and preserved raw report. Format validity leaves game geometry, rendered fidelity and import behavior unevaluated. |

The permanent-help, expressive/no-victory, purposeful-repetition, common-ending
and narrow-local-edit cases remain legitimate. A new script is not evidence that
the old model could not solve the task; comparative behavior is assessed
separately. An installed dependency is not proof that the agent discovers or
uses the operation well.

The transfer has a concrete maintenance cost. The frozen runtime grows from
48 files / 285,580 bytes to 59 files / 378,443 bytes: **92,863 additional source
bytes**. The three adapters are 305, 522 and 247 lines respectively; the native
qualifier is another 366 maintainer-only lines. These figures are recorded in
[the size/file comparison](../../reviews/2026-10-08-comparison/runtime-size-and-files.json),
not used as quality scores. Conditional references keep that entire source out
of an ordinary task's required reading. Forty-five operation tests plus the
observation regression and three verifier tests expand maintenance obligations;
optional dependency and exact-client CI jobs also add installation/runtime cost.
No per-task token or speed improvement is inferred from file counts.

## M1: compute the stated model, preserve its meaning

The comparative trigger was apetrov's
[`game-analysis/scripts/matrix_analysis.py`](https://github.com/apetrovCode/game-design-skills/blob/b8bc2c4d99ccd6e8b2fb3a5fed63fec66dfce35c/game-analysis/scripts/matrix_analysis.py)
and the associated interaction-structure and analysis workflow. They offer real
executable analysis of ordinal outcomes, counter graphs, dominance, cycles,
unbeaten sets and a damped eigenvector heuristic. The skill warns that the
heuristic is not equilibrium or player frequency; another reference describes
it more strongly as underlying viability. These meanings cannot be silently
interchanged with expected utility.

All **34** supplied matrix tests ran successfully. Additional actual probes
accepted nonfinite input, produced a vacuous singleton “2-Paradox” result, and
classified `a > b`, `b > c`, `a ~ c` as transitive. Those observations narrow the
tool's usable claims; they do not establish that the entire package is useless.
Its universal redesign pressure and mandatory audit/three-proposal workflow do
not fit this product's intentional hierarchies and sufficient local edits.

The accepted component is an explicit calculation, independently implemented
against [SciPy 1.17.0 `linprog(method="highs")`](https://docs.scipy.org/doc/scipy-1.17.0/reference/optimize.linprog-highs.html).
Inputs declare two-player zero-sum utility, named row/column actions, state,
availability, horizon, units and costs. The row maximizes expected utility; the
column receives its negative. Rectangular models, negative utility, one legal
action and intended dominance are valid. General-sum utility is unavailable for
this operation; a damage multiplier or counter graph is not silently converted
into a preference model.

The adapter solves both primal roles with unrestricted value variables, scales
finite utilities, then checks the actual returned probabilities and best-response
bounds independently. Output includes identity, versions, normalization,
tolerances and the certificate. A successful optimizer flag alone is insufficient.
The report makes no claim about fun, equilibrium behavior in a repeated game,
human action frequency or the adequacy of the chosen utility model.

SciPy owns the LP implementation and bundled HiGHS. Direct SciPy avoids an extra
dependency for this narrow contract; inspected Nashpy 0.0.43 minimax documentation
remains a useful alternative if a later task actually needs broader bimatrix
methods. Extending this adapter into a general game solver is not approved by
this comparison. See the [runtime contract](../../../skills/game-systems-design/references/zero-sum-analysis.md)
and [executable examples](../../../examples/strategy-matrix/README.md).

## M2: observation context is part of the result

Donchitos' playtest report preserves build, platform, input and session context;
edhahn's tabletop guidance preserves rules/material version, seats, experience
and the relation between an observation and its interpretation. Both are useful
representations. Their presence also contradicts the supplied review's narrow
claim about the availability of playtest-oriented methods.

Our existing schema already required `conditions`, `collection_method` and
`units`, yet `import_observations` returned neither field. The exact original
source reproduced this loss. Keeping only a manifest digest identifies a missing
document; it does not carry its meaning to a recipient of the report.

The correction preserves these fields through the existing command and a real
write/reopen cycle. The new test uses equal event counts but different assistance
conditions. Read-aloud help and a displayed answer can have the same numeric
success record while delegating different work. Both forms of help may be
appropriate; neither count by itself proves learning. Existing unknown outcomes,
synthetic provenance and `human_claim: not_established` remain in force.

This is a defect in satisfying an existing subject requirement, with a dependent
output/test correction. It is not a reason to add a second universal research
reference, recruit imaginary players, or make every edit wait for a playtest.

## I1: actual Ink state and the next legal action

The implementation calls the published
[inkjs 2.4.0 compiler and runtime](https://github.com/y-lohse/inkjs/tree/edccead8700e9f21be9825d87d8645d8c82a9936):
`Compiler.Compile`, `Story.ToJson`, `Continue`, `currentChoices`,
`ChooseChoiceIndex`, `variablesState`, and `state.ToJson/LoadJson`. It saves and
reopens compiled JSON and restores native state in a fresh process before the
next caller-selected action. The save envelope binds compiled bytes, dependency
identity, state and observed checkpoint. It is not a JSON imitation of Ink state.

The original Listening Room example separates acquiring knowledge, committing a
reveal and leaving. A missing guard still compiles but the same assessment
refutes its initial action availability. A legitimate ending executes without
an invented victory or return obligation. Silent `END` is a valid program; it
cannot satisfy a separately required action merely because a text-chunk array
exists. Native runtime errors and absent evidence yield unavailable, not a claim
that the author designed a bad scene.

The implemented contract is intentionally narrower than the entire Ink language
and every host integration: one source, compiled format 21, no include-file
resolver or host external-function fallback, explicit scalar observations and
action selection, new output directories and bounded worker execution. The
worker is not a JavaScript security sandbox. A native Ink save does not contain
the rest of an engine's world, inventory, rights or presentation state. Migration,
localization, rendered UI, full branch exploration and engine-host bindings need
their own consumer evidence.

[Yarn Spinner's inspected compiler and Dialogue/variable-storage APIs](https://github.com/YarnSpinnerTool/YarnSpinner/tree/dd8d9b4f7b752364e3dce94961c00924e13f5d72)
are substantive alternatives, especially for an existing Yarn/.NET project.
The inspected source did not establish a release version or a local .NET run.
It would be wasteful to install a second mandatory narrative engine merely to
cover another name. Use the owning project's native consumer when it already
provides the required relation. See [Ink operation](../../../skills/game-world-narrative-design/references/ink-artifacts.md).

## G1: conformance, resource availability and game predicates

The exact published
[Khronos glTF-Validator 2.0.0-dev.3.10](https://github.com/KhronosGroup/glTF-Validator/tree/bcd52cc4ba5f333b2999a58f67cc05ddf28b4fb1)
is called through `validateBytes`. The discovered upstream main had already
advanced to 3.11; the report does not rename our executed 3.10 dependency as
latest. The returned Promise can resolve with format errors, so process success
is not acceptance. The adapter preserves the complete native report and counts
actual errors, resource failures and unsupported coverage separately.

An empty glTF and a camera-only scene can be conformant. They are accepted for
that property. A caller's mesh, collider, visible-signal, texture-fidelity or
target-engine-import predicate remains `not_evaluated`. An unsupported extension
or unavailable external buffer cannot silently certify the omitted portion.
Local resource reads require an explicit root and remain within lexical and
resolved containment; remote resources are unavailable. These path checks assume
a stable filesystem and do not provide process isolation against hostile races.

The original fixtures exercise embedded glTF, GLB and external local buffers;
bad accessor ranges; malformed/unknown formats; absent and remote resources;
unsupported extensions; empty and camera-only assets; and output/path aliases.
The output-alias defect found by independent review was fixed before acceptance:
a report cannot create its own missing input through a symlinked parent.

The Blender comparison supplies a useful next-consumer question. Kiln actually
reimports GLB into a clean Blender scene and measures selected geometry/fidelity;
Scenario has concrete topology metrics and contact-sheet tools. Neither a raw
metric nor a clean validator report replaces that target reopen. We adopt the
question and keep native Blender qualification conditional; no Blender code,
thresholds or generated assets are imported. See [glTF operation](../../../skills/game-design/references/gltf-artifacts.md).

## Other findings and dispositions

| Finding | What is useful | Decision, reason and what would change it |
| --- | --- | --- |
| baxatron vision, narrative and prototype methods | Explicit design intent, scope and playtest questions | **Adapt only when a concrete example needs it.** Its incomplete attached license and missing topology reference prevent treating it as an immediately reusable complete package. Universal market-fit/persona, disposable-prototype and intervention-failure rules do not transfer. |
| Donchitos creative phases and system maps | Real concept construction, dependency/order/handoff representation, context-rich playtest reporting | **Use M2's insight; retain other components as alternatives.** Its GDD checker explicitly checks headings, not design completeness; test specifications are not run receipts. Mandatory concept counts and human-selection stops remain outside this package. |
| abagames concept exploration and refinement | Causal variation, a concept record, and stopping when further iteration lacks sufficient expected value | **Additional example requires further evidence.** This refutes the supplied claim that substantive concept search is absent. Our existing concept method already varies a mechanism against an intended relation. Fixed 18/6/4 populations, duplicate thresholds and compact-game assumptions are not universal subject requirements. General stopping/evaluation belongs to Assay. |
| ncdlek state and quest graphs | Stored versus derived state; explicit prerequisites; some static defect detection | **Do not copy its validator.** Actual probes found an optional global-NPC rule unenforced, a top-level-array crash, and condition values unexamined. Connectivity and AND-prerequisite assumptions cannot establish mutable-state reachability. Add a consumer-specific graph operation only when its precise semantics are needed. |
| Scenario Blender metrics and renders | Concrete measurement and controlled visual evidence | **Conditional component candidate.** Above-threshold self-intersection checks can be skipped and disappear from verdicts; default deforming-mesh preferences are not universal. Named Blender/Unity test suites are author-reported and not shipped in the inspected repository. Do not inherit the lead's orchestration and family dependency. |
| ra100 Blender recipes and Blender Lab MCP | Real bpy operations and a documented official bridge route | **Test further.** The official server exists, contrary to a possible name-based suspicion; exact source/license retrieval was blocked and no live Blender was available. A skill's tool-name list does not qualify a bridge. |
| Kiln reimport and fidelity checks | Original-versus-exported geometry/texture/rig comparisons and seeded tests | **Adapt the consumer-check idea; defer native integration.** The inspected benchmark discloses one run per brief, a small reference set, tuning contamination and an incomplete cloud path. It does not establish general quality superiority. Its meshopt partial path exits zero; preserve omitted coverage. |
| Coplay Unity MCP beta | Real asynchronous test start/poll and capture code | **Connect only for a qualified target project.** A `job_id` is not a passing test. Camera RenderTexture does not include all overlay UI. Exact editor/bridge/package versions, project access and terminal test evidence are required. |
| Unity's own CLI/Pipeline guidance | An available native alternative; actual frame progression distinguished from a play flag | **Conditional alternative.** Unity Companion License is not MIT. Do not copy its text, always-update policy or automatic installation flow. Inspect the connected project's actual command schema. |
| Coding-Solo Godot MCP | Project start/stop and debug output | **Do not replace the stronger existing episode.** Inspected registry lacks live screenshot/input; package and server version strings differ. A weaker bridge does not improve the demonstrated input/physics/save path. |
| Erodenn Godot runtime bridge | Live input, screenshot, UI and profiler operations for real projects | **Test further when needed.** Its temporary autoload, `.mcp` tree, project/settings changes and TCP lifecycle are real mutations despite “zero footprint” wording. Attached and spawned modes provide different evidence. Keep the bridge under its project owner. |
| Yarn and broader game-theory packages | Native alternatives for another existing format/model class | **Retain as alternatives, not extra mandatory dependencies.** A concrete unsupported consumer or utility model would justify the next integration. |
| OpenSpiel game/state/algorithm interfaces | Executable information states, legal actions, simultaneous play and real LP/dominance implementations | **Conditional project-owned model.** The inspected CVXPY/pyspiel LP route and tests are substantive but unexecuted here. A multi-step/imperfect-information requirement could justify the larger model/dependency surface; M1's narrow certified matrix operation does not need it. |
| PettingZoo AEC/parallel environments and API tests | Explicit per-agent observations/actions, episode lifecycle and interface conformance | **Conditional simulation integration.** AEC-to-parallel conversion has cycle semantics; the test's no-revival rule is an episode-identity constraint, not a game-design prohibition on returning players. No RL loop, reward metric or orchestration is imported. |

Coinciding skill names do not establish a conflict. An actual conflict concerns
two rules governing the same action, incompatible representations or settings,
two managed owners, duplicate activation, or an unavailable required reference.
A foreign system can be unsuitable as a whole and still supply a useful local
representation or operation.

## Terms, provenance and responsibility

No third-party game-design skill, framework, template, test fixture, art asset or
solver implementation is copied into the runtime. The new scripts and examples
are original. Comparative ideas are attributed here and in the detailed notes;
external APIs are declared as optional dependencies and obtained separately.

| Actual reuse | Qualified identity and terms | Distribution consequence |
| --- | --- | --- |
| SciPy API, bundled HiGHS; NumPy prerequisite | SciPy 1.17.0, commit `8c75ae75176236f233824e9a0483c26a69e6dfec`, BSD-3-Clause; HiGHS submodule `222cce79a2bca866dbfbcd91b55da11336ae88f4`, MIT; tested NumPy 2.3.5 `c3d60fc8393f3ca3306b8ce8b6453d43737e3d90`, BSD-3-Clause | The repository ships a requirement and original adapter, no wheel or solver source. A future redistributor must retain the packages' license and bundled notices. |
| inkjs compiler/runtime | npm 2.4.0, published gitHead `edccead8700e9f21be9825d87d8645d8c82a9936`, MIT, 2017 inkle Ltd. and contributors | Exact lock/integrity; no vendored bundle. Keep its notice if redistributed. Its npm package has no runtime npm dependencies. |
| Khronos validator | npm 2.0.0-dev.3.10, published gitHead `bcd52cc4ba5f333b2999a58f67cc05ddf28b4fb1`, Apache-2.0 plus bundled `NOTICES` | Exact lock/integrity; no vendored compiled Dart/JS. Zero npm dependencies does not mean zero bundled third-party obligations. Preserve license/notices on redistribution. |
| Native qualification clients | Codex CLI 0.159.2, Apache-2.0 package; Claude Code 2.1.289, Anthropic terms referenced by its package | CI obtains exact external clients. Their binaries are not included in Game Design; Claude is not relicensed as MIT. |

The [NOTICE](../../../NOTICE.md) records the resulting distribution boundary.
The later documented first-use recipe additionally resolved NumPy 2.5.3
(`dd88c0c19b54ad9ed3533224221285bf0873249a`) and passed the actual operation and
18-test suite. Its compound installed license expression and bundled-license
identities are retained with that separate receipt; this does not change the
NumPy 2.3.5 vector used for the paired model tasks.
MIT statements in agent repositories were checked against their actual license
files; baxatron's missing full terms and the provenance of apetrov's externally
derived theory text are recorded, rather than silently repaired by a root label.
Unity Companion licensed guidance is not an MIT borrowing. Referenced images,
games and generation services keep their own terms.

Game Design owns the meaning of a utility, action, choice, observation or game
predicate. A dependency owns its parser, optimizer or runtime. The consuming
project owns host state, engine bindings, access and private assets. Assay owns
general research, implementation, verification, audit, evaluation, planning and
stopping methods. No agent orchestration, model routing, permission discovery,
memory service, installer or mandatory review cycle was imported with the useful
subject content. The new maintainer qualifier exercises native client managers;
it is not a replacement installer or runtime rule.

## Evidence and outstanding boundaries

The accepted operations have actual dependent-consumer tests, valid neighboring
cases and distinct unavailable/refuted outcomes. New independent review found
and closed six integration/verifier findings; the numerical/narrative review
used additional independent mathematical and native-state probes. The first
hosted native attempt exposed two incorrect verifier expectations; both the
failed and corrected receipts are preserved.

GitHub Actions run
[37819498740](https://github.com/Muratovnik/gamedesign-skills/actions/runs/37819498740)
qualified the local-source lifecycle at the runtime snapshot above: Linux and
Windows package gates, Linux optional artifact operations, and fresh-user Linux
Codex/Claude native managers. Client metadata, source-byte verification and a
verifier-executed installed resource are different observations; this run did
not conduct authenticated model conversations.

Comparable model tasks and their actual results are reported in the
[verification record](../../reviews/2026-10-08-comparison/README.md). They cannot
be inferred from passing script tests, dependency installation, source inspection
or this report. Existing Godot and paper evidence is reused only for unchanged
files and claims; it is not a fresh independent review of the whole candidate.
No human study, Unity/Blender execution, arbitrary engine import or universal
model-performance improvement is established.
