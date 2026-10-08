# Environment components: comparative evidence and change candidates

> Historical research-stage record, retained with its original scope and findings.
> Implementation and final dispositions are in [the integrated comparison](comparison.md);
> proposal wording in this record does not create an additional requirement.

Research date: 2026-10-08. Product baseline: `Muratovnik/gamedesign-skills` main `4fc654c2cb92989582c30bc048742f2cce7659ba`. Method source: Assay main `94c517b0aac9ba2575086bf9aead1cc828aadb0d`, 0.17.2. Product was read only in this research task. Public repositories and two optional npm dependencies were obtained only under this research directory; no client, engine, credentials, user installation, or live project was changed.

## Decision

**Connect two existing technical components through small optional artifact routes: inkjs for native Ink execution, and Khronos glTF-Validator for format validation.** Both ran on original synthetic artifacts here, including positive and defective controls. These routes extend the kinds of actual artifacts the package can operate on. They do not establish that the existing subject rules were missing, that another package has better design methods, or that model behavior improves after a skill change.

**Keep Unity and Blender execution bridges as conditional, project-owned connections requiring further qualification.** Their concrete source contains useful operations, but no Unity or Blender executable was available in this task's supplied environment. The existing Godot episode remains the stronger locally established native-engine route. Do not import another package's orchestration, installations, access discovery, universal budgets, model routes, or evaluation loop to gain an artifact operation.

The existing counterparts are already explicit:

- [`environment-contracts.md`](https://github.com/Muratovnik/gamedesign-skills/blob/4fc654c2cb92989582c30bc048742f2cce7659ba/skills/game-design/references/environment-contracts.md) distinguishes a documented operation, inspected source, actual execution, and checked property; requires re-opening outputs; excludes unsupported Unity/Blender/arbitrary UGC claims.
- [`conditional-story.md`](https://github.com/Muratovnik/gamedesign-skills/blob/4fc654c2cb92989582c30bc048742f2cce7659ba/skills/game-world-narrative-design/references/conditional-story.md) already teaches entry conditions, commit points, interruption, participant knowledge, refusal, and consequences through branch merges. The gap is an executable narrative consumer, not another statement of those rules.
- [`examples/godot-episode/README.md`](https://github.com/Muratovnik/gamedesign-skills/blob/4fc654c2cb92989582c30bc048742f2cce7659ba/examples/godot-episode/README.md) already carries original/candidate fixtures into actual input, physics, geometry, save/reset/reload, and an assessor with 0/1/2 outcomes. `examples/design-studies/harbour-of-echoes` and `examples/analysis-lab` explicitly exclude a general narrative VM.
- The uploaded project brief permits reusable game integrations in the public package while leaving private project context/access and game-specific adapters with the consumer. Operational requirements §4.2, OR-11 and OR-15 require actual operation, retained outputs, and acceptance by the requested property. OR-16 concerns continued agent work after restoring task context; the separate game-state and conditional-story references justify native save/resume checks. These justify execution components, not mandatory tools for every game.

## Scope and method

Read the product's `AGENTS.md`, compatibility, environment and consumer contracts, conditional-story reference, Godot episode README, relevant example inventory, and the supplied environment requirements. Read Assay `evidence-research/SKILL.md` plus search-and-coverage, evidence-and-claims, component-evidence, comparison-and-synthesis, and skill-evaluation's research-and-transfer reference.

Search families were: exact three attached Blender pointers; native and community Unity editor control/test/capture; Godot run/debug versus live observation/input; narrative compilation/choice/state; artifact format validation. Discovery used public source trees and primary documentation, with web queries on 2026-10-08 such as `Unity MCP editor run_tests capture screenshot`, `Godot MCP run_project get_debug_output screenshot`, `Unity CLI com.unity.pipeline MCP`, `inkle ink compiler tests JSON runtime license`, and `KhronosGroup glTF Validator JavaScript validateBytes`. Narrow official-domain queries resolved an initially failed fetch of Blender's own MCP page. Popularity was not a criterion. No exhaustive art-tool, AI generation service, game-engine, or scholarly playtesting survey was attempted.

Status terms in this note: **inspected** means the relevant source was read; **executed** means a recorded local operation ran; **author-reported** means the source asserts a result whose original execution was not reproduced here. A test file's presence is not a passing run. A repository branch is not automatically a stable release.

## Exact sources, terms, and reading scope

| ID | Source and exact revision | Terms read | Inspected implementation and limits |
|---|---|---|---|
| E01 | [scenario-labs/skills](https://github.com/scenario-labs/skills/tree/91caa011e13774a220aba7136309b49964104040), `91caa011e13774a220aba7136309b49964104040`, main, commit date 2026-10-04 | Root `LICENSE`: MIT, copyright 2026 Scenario. Blender/Unity READMEs explicitly credit ports from edemaistre expert-skills v0.1. | Blender family README; `scenario-blender-expert/SKILL.md`; `scripts/bx_audit.py` including metric and verdict/CLI code; hard-surface source/procedure references; Unity family README and lead skill, toolkit and pipeline inventory. Full domain suites were not executed. |
| E02 | [ra100/blender-claude-plugin](https://github.com/ra100/blender-claude-plugin/tree/78e9151fdc9e01ce37f1d16a9b677c3047411885), `78e9151fdc9e01ce37f1d16a9b677c3047411885`, master, 2026-04-29; plugin version 1.3.0 | `LICENSE`: MIT, copyright 2026 ra100; plugin metadata author `svarba`. | README, plugin manifest, setup reference, scene/rendering skill including inspect/mutate/verify, import/export recipes, inventory of all eight skills and references. Source is skill/reference text; no bridge implementation or runnable test files found in its tracked tree. Blender execution not run. |
| E03 | [elithril/blender-kiln](https://github.com/elithril/blender-kiln/tree/c415cb4ba8a3b9bbfe69b6edb76ad6f06dba9435), `c415cb4ba8a3b9bbfe69b6edb76ad6f06dba9435`, main, 2026-10-07; plugin version 2.2.0 | Root `LICENSE`: MIT, copyright 2026 Nicolas Dolphens. Referenced source photographs, marketplace models and generation services retain separate terms. | `plugin/SKILL.md`; export and validation references; `bench/measure.py`; benchmark methodology and limits; `plugin/tools/verify_blender.py`, `test_verify_docs.py`, `test_fidelity_check.py`; `.github/workflows/blender.yml`. Results branch and visual benchmark assets not independently checked. No model campaign or Blender run. |
| E04 | [Blender Lab MCP page](https://www.blender.org/lab/mcp-server/), primary page retrieved 2026-10-08 | No server-code terms established here. | Page documents Blender 5.1+, addon, separate server, client, and unrestricted generated Python execution. Direct open initially failed 402; official-domain search retrieved the page content. [Server source](https://projects.blender.org/lab/blender_mcp) was robots/403 blocked. No exact server source revision, API implementation, or license is claimed. |
| E05 | [CoplayDev/unity-mcp](https://github.com/CoplayDev/unity-mcp/tree/ef713afd7bbd1d5a1e0bdb5f62f13855f9da79bf), `ef713afd7bbd1d5a1e0bdb5f62f13855f9da79bf`, **beta**, 2026-10-07; package **10.3.1-beta.6** | Root `LICENSE`: MIT, copyright 2025 CoplayDev. | Unity package metadata; Python `Server/src/services/tools/run_tests.py` including start/poll schemas; C# `MCPForUnity/Editor/Tools/RunTests.cs`; `Runtime/Helpers/ScreenshotUtility.cs`; test/camera inventory; `Server/tests/integration/test_run_tests_async.py`. Inspected Python test uses mocked transport; no Unity execution established. |
| E06 | [Unity-Technologies/skills](https://github.com/Unity-Technologies/skills/tree/cb1dccb8f5adffcca43a5a26993fdeb8eae59433), `cb1dccb8f5adffcca43a5a26993fdeb8eae59433`, main, 2026-10-01 | `LICENSE.md`: **Unity Companion License for Unity-dependent projects**, copyright 2026 Unity Technologies. This is not an MIT package. | `skills/unity-cli/SKILL.md` and `references/playmode-verification-loop.md`; primary [Unity local-tools/CLI overview](https://docs.unity.com/en-us/unity-production-pipeline/local-tools-cli). This source is guidance, not the CLI or Pipeline implementation. No exact CLI/package runtime version was executed here. |
| E07 | [Coding-Solo/godot-mcp](https://github.com/Coding-Solo/godot-mcp/tree/1209744fad78f3998f98c7394fd0f6ef50da5281), `1209744fad78f3998f98c7394fd0f6ef50da5281`, main, 2026-04-16; package 0.1.1 | `LICENSE`: MIT, copyright 2025 Solomon Elias. | `package.json`, README, `src/index.ts` tool registry and run/debug handlers. MCP server identity string still says 0.1.0 while package says 0.1.1. No live screenshot/input tool in this inspected registry. No test command in package manifest. |
| E08 | [Erodenn/godot-mcp-runtime](https://github.com/Erodenn/godot-mcp-runtime/tree/04925002e227749048bd95274c5bdb0c929bb8c4), `04925002e227749048bd95274c5bdb0c929bb8c4`, main, 2026-09-29; package 3.8.1 | `LICENSE`: MIT, copyright 2025–2026 Owen Sterling. README credits Coding-Solo foundation. | Runtime tool schemas in `src/tools/runtime-tools.ts`, bridge lifecycle in `src/utils/bridge-manager.ts`, GDScript bridge inventory, `docs/tools.md`, unit-test inventory. No server or Godot runtime executed. |
| E09 | [y-lohse/inkjs npm 2.4.0 source](https://github.com/y-lohse/inkjs/tree/edccead8700e9f21be9825d87d8645d8c82a9936), **`edccead8700e9f21be9825d87d8645d8c82a9936`** from npm `gitHead`; discovered master was `6b1153410ab1c4bcfd9ef04eb2f0107f36be7778` (2026-09-01) | `LICENSE.md`: MIT, copyright 2017 inkle Ltd. and inkjs contributors; package author Yannick Lohse. | README, package metadata, `src/compiler/Compiler.ts`, `src/engine/Story.ts`, `StoryState.ts`, choices tests including save/reload, test README. Fetched published commit and compared these source paths/terms against master: no diff. **Executed actual published compiler and runtime**, not a rewritten interpreter. |
| E10 | [Khronos glTF-Validator npm 2.0.0-dev.3.10 source](https://github.com/KhronosGroup/glTF-Validator/tree/bcd52cc4ba5f333b2999a58f67cc05ddf28b4fb1), **`bcd52cc4ba5f333b2999a58f67cc05ddf28b4fb1`**, 2024-10-22; discovered main `602c54043ba66856b2e68c40fdf2bced975cdb8a` (2026-10-06) reports 2.0.0-dev.3.11 | Apache-2.0, Khronos Group, plus bundled `NOTICES`. | `node/index.js`, `module.mjs`, `node/README.md`, version and package metadata, `ISSUES.md`, test fixture/report inventory. Fetched npm commit and compared Node API/README/LICENSE/NOTICES against main: no diff. **Executed published 3.10 compiled Dart/JS validator**, not 3.11 main. |
| E11 | [YarnSpinnerTool/YarnSpinner](https://github.com/YarnSpinnerTool/YarnSpinner/tree/dd8d9b4f7b752364e3dce94961c00924e13f5d72), `dd8d9b4f7b752364e3dce94961c00924e13f5d72`, main, 2026-09-16 | `LICENSE.md`: MIT, Yarn Spinner Pty. Ltd., Secret Lab Pty. Ltd., contributors. | Core and compiler csproj files; `Compiler.Compile` result construction; `Dialogue`/`IVariableStorage` API; `DialogueTests` compilation/analysis; primary Dialogue/Continue/SetSelectedOption docs. Source csproj version is 0.0.0, so no release version is inferred. No .NET runtime/build executed. |

## Comparisons that change the decision

### Blender: separate tools and artifact checks from the expert workflow

**Scenario's reusable candidates are `bx_audit` metrics and `bx_review` contact sheets.** A chosen `.blend` object can become a topology/fidelity report; chosen objects can become controlled multi-view renders. That is a concrete improvement over merely giving a Blender prompt. The package's lead also enforces brief/stages, a build/measure/render/fix loop, mandatory visual review, persona chains, sibling installation, and machine/channel policy. Its family README says specialists import the lead's scripts and must be installed side by side. Calling it only technical knowledge with no workflow is inaccurate. [E01]

Its Blender README reports 13 skills and author-run Blender 5.2.1 tests; Unity reports 14 skills and 447 checks on Unity 6000.3.21f1/macOS Apple Silicon. Both explicitly explain that test paths inside the references identify the author's build project and are not included. The repository has tests for other subjects; therefore the correct finding is **the named Blender/Unity evidence suites are not shipped here**, not “Scenario has no tests.” The counts and quality comparisons remain attributed claims, not our replication. [E01]

`bx_audit.audit` calculates non-manifold/loose/degenerate elements, winding, symmetry, approximate self-intersection pairs, and optional distance to a high-poly object. It skips self-intersection computation above a face limit by returning `None`; `verdict` ignores that `None`. Its default `deforming=True` also introduces particular quad/ngon/pole preferences. Its CLI prints a problems array but does not set a failing exit status for a nonempty array. Thus reuse should adapt the metric/report boundary and explicitly handle omitted measurements and the intended mesh class, not promote an empty problem list or process exit into universal asset acceptance. A valid open surface, asymmetric prop, intentionally triangulated mesh, or non-deforming boolean model must not inherit a character-retopology judgment. [E01, `skills/dcc/blender/scenario-blender-expert/scripts/bx_audit.py`]

**ra100 is useful as an optional reference route, not a self-contained operation adapter.** Its eight skills offer many concrete bpy recipes and domain references, with MCP-first detection by tool names and Python-script fallback. Its README really does retarget to a Blender Lab server. Blender's own primary page confirms the server exists; the attached “official” phrase is not grounds to call it fabricated. Exact tool compatibility and deployment still require matching server source and a live check, which were unavailable here. No implementation or test claim about that server can be borrowed from a skill's tool-name table alone. [E02, E04]

**Kiln has the strongest inspected export-consumer pattern among the three Blender candidates.** `bench/measure.py` opens the exported GLB, reads its container metadata, imports the file into a clean Blender scene, excludes bone-display meshes, and measures geometry, dimensions, textures, rig structure, and deformation. Its own `EXT_meshopt_compression` branch records that re-import was skipped, prints a partial report, and exits zero. This is a useful example of why an adapter needs to carry `not inspected` evidence through the final outcome. `test_fidelity_check.py` constructs seeded geometry, known width differences and missing textures; `verify_blender.py` checks concrete API/export regressions. Those are meaningful tests in source, but Blender-dependent tests were not run here. [E03]

Kiln's benchmark page names one run per brief, a small reference set, lantern examples used while tuning, a contaminated run, and a cloud AI path that does not finish end to end under its own approval rule. Its separate results branch was not inspected. Therefore “full text/photo-to-production pipeline with proven quality” exceeds this evidence. Its self-contained pipeline also imports many decisions: interactive wizard, batch manifest, resource/generation routing, exact repeated inspection rules, all-stage file policy, mandatory interruption for some optimization, and a model-based benchmark runner. These are not needed for a GLB validator. [E03]

A concrete disagreement illustrates why local artifact checks matter: ra100's generic export recipe enables `export_apply=True`; Kiln prohibits that flag broadly but adds a geometry-node exception because unapplied evaluated geometry can disappear. The stable transferred question is **which evaluated geometry, instances, animation, and materials survive this export and target importer?** Neither flag is a universal rule for the public game-design method. Preserve an original, export the chosen representation, reopen it, and check the required relations. [E02 scene/rendering export recipe; E03 export-targets and skill rule 18; product environment contract]

**Decision:** adapt the export-and-reopen question; connect a precise metric/render tool later if a Blender task needs it; test further for native support; reject wholesale import of lead protocols, preference thresholds, benchmark conclusions, or paid/generation access routes. No external code or asset was copied into the product.

### Unity: real async tests and captures, but choose the project's actual bridge

Coplay's inspected beta has a concrete Python-to-C# path: `run_tests` validates/preflights, forwards the chosen test mode/filter to C# `TestJobManager`, and returns a `job_id` with `running`; `get_test_job` later returns progress and the terminal result, including total/passed/failed/skipped/duration/resultState and optional test records. Job start is not test success. The Python file includes focus-nudge machinery, instance routing, preflight, and transport policy. The package declares Unity 2021.3 minimum plus Unity modules, Newtonsoft JSON 3.0.2 and Unity Test Framework 1.1.31; the Python server has its own environment. This is an editor bridge, not a dependency-free skill. [E05]

Capture source is also material: the camera helper can render a specified camera into a temporary RenderTexture, while the ScreenCapture route sees the composited game output. The documented camera-specific path excludes screen-space overlay UI. A screenshot result from one route cannot silently stand for the user's complete game view. Even a correct view cannot establish that the game advanced through an action. [E05 `ScreenshotUtility.cs`; primary camera docs linked by repository]

Unity's own current CLI/Pipeline guidance provides a native alternative. It uses a local HTTP API to a running editor and requires the project's Pipeline package. The inspected verification reference distinguishes a play flag or screenshot from actual progression and asks for an observed `Time.frameCount` change; it warns that command names/parameters come from the connected package and must be discovered for that project. This observation is useful; the full skill also says always update to latest and gives automatic installation/configuration instructions. Neither that execution policy nor the Unity Companion licensed text should be copied into a neutral package. [E06]

Scenario's Unity family adds a third adapter surface (`ut_*` and C# AgentKit), but its own declared tested environment is a particular Mac/Unity build. Importing it would make the package own another environment/bridge maintenance surface without a locally demonstrated need. [E01]

**Decision:** connect/test further through the consumer's existing native CLI/Pipeline or vetted MCP bridge. A future qualifying project should provide exact editor + bridge + package versions, exact scene and test IDs, authorization, a disposable output destination, a known failing game condition and a lawful alternative. Path: scene/fixture -> controlled edit -> native run/test job -> actual frame/input/report artifact -> named predicate. No bridge installs or broad Unity support claim now.

### Godot: existing episode beats a weaker bridge; a live bridge is a separate candidate

Coding-Solo's source can create/edit scenes, start/stop projects and return captured debug text. Its inspected registry lacks the live screenshot/input observation used in some forks and unmerged proposals. The product already has actual controlled input/physics/state evidence in a pinned Godot episode, so replacing that with “run project + debug output” would weaken the demonstrated path. Package 0.1.1 and server identity 0.1.0 also need recording separately if this bridge is qualified. [E07]

Erodenn's 3.8.1 provides the materially different candidate: `run_project`/`attach_project`, screenshot, batched input, UI discovery, live GDScript, and profiler access. Its schemas and documentation preserve spawned-versus-attached differences: attached processes lack the captured stdout/stderr and some profiler state. Its input description waits for a frame after injection and reports effects. That can support an arbitrary project's observed interactions where the current fixed episode does not. [E08]

Its “zero footprint” label needs a precise reading. Source actually injects a `McpBridge` autoload into `project.godot`, creates its managed `.mcp` tree, augments `.gitignore`, tracks owners, and later cleans/restores managed state. Runtime control is therefore a temporary project mutation and local TCP service, not a purely read-only observation of an untouched project. Tests for owner collisions, bridge lifecycle, handler schemas and validation exist; this task did not run them or the engine. Node >=20 and an MCP SDK dependency are declared. [E08 `bridge-manager.ts`, runtime tools, package.json]

**Decision:** retain the current Godot episode; test Erodenn further only when runtime UI/input observation in a real target project is required. Treat temporary injection, cleanup and attached-mode evidence gaps as part of that project adapter. Do not import its policy scanner, approval mechanism, resource discovery or agent loop into game-design methods.

### Narrative VM: inkjs is the smallest executed route; Yarn remains a good environment-dependent alternative

Ink's existing role in the product is documented narrative semantics. The proposed addition calls its real runtime. Published inkjs 2.4.0 has no separately installed runtime npm dependencies and supplies `Compiler` via `inkjs/full`, `Compiler.Compile()`, `Story.ToJson()`, `new Story(compiledJSON)`, `canContinue`, `Continue()`, `currentChoices`, `ChooseChoiceIndex(index)`, `variablesState`, and `state.ToJson()/LoadJson()`. The source has compiler diagnostics and save-format checks. The package supports JSON format 21 in our execution. Source tests include conditional choices and save/reload of a choice thread. [E09]

Yarn's core is also engine-independent and concrete: `Compiler.Compile(CompilationJob)` produces a Program, string table, declarations, diagnostics, metadata and debug information. `Dialogue` loads the Program, exposes line/options handlers, continues execution and accepts a selected option ID; variable storage is an explicit host boundary. This is useful when the target project already uses Yarn and localization/line identity. Its inspected core targets netstandard2.1 and references Google.Protobuf; compiler additionally references Antlr4.Runtime.Standard, CsvHelper, System.Text.Json and file-system globbing. That is a different environment and larger initial integration than the already executable zero-runtime-npm-dependency Ink route here. No claim is made that Yarn is worse at narrative authoring or incapable of the same game relation. [E11]

**Decision:** connect inkjs now as the optional demonstrated runtime; retain Yarn as a project-dependent alternative, not a second mandatory interpreter. Store original game fragments and their dramatic/semantic assertions in examples or the consuming game. Runtime adapters should preserve artifact identity, diagnostics, actual choices/outputs/state and bounded execution, without deciding that every narrative needs branching, a victory, or a particular ending.

## Executed probes and concrete handoff

Workspace: `/workspace/scratch/e429285ef1e1/research/environment/probes`. Runtime: **Node v24.19.0**. Install used exact dependency versions, an isolated prefix/cache, and `--ignore-scripts`; no global install. `package-lock.json` contains only the two direct packages. These are feasibility probes with assertions, not finished product adapters or a behavioral evaluation of a skill.

### Ink probe

Run `node probe-ink.cjs` from the probe directory. Actual path:

`east-gate.ink` -> actual compiler -> saved compiled JSON -> reopen with actual Story -> observe and choose -> saved native state -> reopen native state with compiled digest -> observe and choose next legal action -> `ink-results/receipt.json`.

The original synthetic gate offers **Inspect the ledger** and **Leave freely** initially. Inspection sets a permit variable and replaces the initial option with **Enter the east gate**. After saving/reloading, both the variable and legal choices are preserved; selecting Enter reaches a terminal scene with `entered=true`. Starting afresh and leaving terminates without granting the permit or setting entered. This preserves a lawful departure, not only a successful gate traversal.

| Control | Observed result | Meaning |
|---|---|---|
| Conditional gate + inspect + save/reload + enter | Supported | Compiler/runtime actually executed the chosen relation and restored its next choice |
| Leave immediately | Supported legitimate alternative | Departure is not treated as a failed narrative because a gate was not crossed |
| Remove entry condition | Compiles, but contract refuted | Enter is incorrectly offered before the permit exists |
| Syntactically invalid source | Compiler rejects; unavailable execution evidence | Compiler failure is not a narrative-design failure observation |
| Empty `-> END` story | Executes with a blank output chunk; action relation refuted | Nonempty chunk array alone would be a bad acceptance test |
| Save envelope bound to other compiled JSON | Digest mismatch; unavailable | Prevents accidentally applying the receipt to a changed program; does not implement migration |

The first empty-story probe incorrectly expected zero output chunks; the actual VM returns an empty string chunk. The probe was corrected to examine the joined/trimmed content, then all controls passed. This is retained here as an observed API/acceptance correction.

Minimal runtime unit: optional `run_ink`/equivalent script, dependency declaration/lock, and a narrow artifact receipt contract. It should compile a selected source or load an explicitly supplied compatible compiled program, consume an explicit action plan, return emitted text/tags/choices and declared variable observations, support a save envelope tied to compiled identity, and report diagnostics/exhausted budgets distinctly. `INCLUDE`, external functions, random state, host time and UI delivery are explicit future/consumer boundaries; do not silently broaden file access or substitute a home-made parser. An assessor for a concrete petition/gate belongs with that game/example, not a universal “good story” test.

### glTF probe

Run `node probe-gltf.cjs`. Actual path:

original authored triangle GLTF/GLB -> write/reopen bytes -> actual `validateBytes` -> complete Khronos report + input SHA-256 -> explicitly selected mesh-delivery predicate -> `gltf-results/*.receipt.json` and summary.

| Control | Observed Khronos result | Probe outcome |
|---|---|---|
| Original embedded triangle GLTF | 0 errors; 1 triangle | Supported |
| Same original triangle GLB | 0 errors; 1 triangle | Supported |
| Accessor count exceeds buffer view | `ACCESSOR_TOO_LONG` error, plus a primitive-mode warning | Refuted |
| Legal empty GLTF | 0 errors; 0 triangles | Refuted **only for this mesh-delivery claim** |
| Referenced local buffer absent | `IO_ERROR` with tracked missing resource | Unavailable |
| External remote buffer URI | Policy declines network; `NON_RELATIVE_URI` and `IO_ERROR` | Unavailable |

Minimal runtime unit: optional wrapper around `validateBytes` or `validateString`, retaining the raw report, component version, input digest and any resource manifest. Do not rebuild the validator. It resolves the Promise when an asset has errors: a `.then()` callback means the operation finished, not that the asset conformed. `maxIssues: 0` avoids silently truncated evidence. A supplied external-resource reader must record and constrain what it actually read; the default omission leaves external resources unvalidated. Missing/disallowed bytes and malformed/stale receipts are distinct from an observed technical defect.

`UNSUPPORTED_EXTENSION` is informational by default in this component, so zero errors does not certify all extension content. Record the component's `supportedExtensions()` and bound the claim; unsupported required content may leave that dependent property unavailable. A nonempty total triangle count also does not prove the required named mesh is reachable in the default scene. Keep asset profile, scene identity, expected content and target-import assertions with the example/consumer. Camera-only or deliberately empty artifacts remain legal cases outside a mesh-delivery request.

Neither route establishes Blender/Unity/Godot import compatibility, visual fidelity, material transfer, perceptual readability, human narrative experience, all reachable branches, or improved agent quality. These are not disclaimers added in place of work: they identify the next specific consumer/observation required for the other claim.

## Dependency bytes and licensing handoff

Published packages were inspected and executed; tarballs were subsequently retained for exact provenance. Full local file checksums are in `probes/checksums.json`.

| Artifact | Exact SHA-256 | Bytes |
|---|---|---:|
| `probes/package.json` | `88dc675432072ba3c99e7845ef59142fcd14193f8144dbb4087c672696d71fc5` | 89 |
| `probes/package-lock.json` | `996544c1c9808fcaa8271adef353ac5ca022c4e66c9ae75a7f8b7f4d82b97b67` | 879 |
| `inkjs-2.4.0.tgz` | `100cf088ef2954927c2a107a42f2154e6b1c0dcea00faf7241b27542e5f88622` | 1,647,581 |
| `gltf-validator-2.0.0-dev.3.10.tgz` | `4e03dbdc3bc0d1342afd5d2d7ae341a7e3474502ccb872b02dbbaddaee0fdec6` | 110,015 |
| Executed `inkjs/dist/ink-full.js` | `23d707b76e9b759a25803c193da8e32e04f727dd13a54ed1df8a6a59dd909b9e` | 248,826 |
| Executed `gltf-validator/gltf_validator.dart.js` | `b73a7b2d455ac217567725138b46d826a13d7d1bb0c88c15f7c571bfb349298c` | 307,792 |
| glTF wrapper `index.js` | `78deff9ea85743e86461c2d14fae76e7fc3ca0432e652f62948066b55fa16f0d` | 2,829 |
| Ink MIT `LICENSE.md` | `040e957a77e3e19432e265cb549d5c3b4ca6f3551e24d22b81785ffd1bc2b67b` | 1,121 |
| glTF `LICENSE` | `3ddf9be5c28fe27dad143a5dc76eea25222ad1dd68934a047064e56ed2fa40c5` | 11,560 |
| glTF `NOTICES` | `933f161ca1e7b3ead5a6cf93ebb3bf6cb67f0e79b38e08d2046f8cdc41cb78a3` | 22,286 |

Registry integrities retained verbatim in the lock:

- inkjs: `sha512-EoPCYESIbMtfI8SqEDZCJwn+A5is0QozMLw250iic1ReJCgZpRKIezWj0VqgRUzAx0f3MmEbsUjY/ILe2815JQ==`.
- gltf-validator: `sha512-odJ4k0tRkGXiDGn78yDBg+fBbAIvBnXxh3RwAta0emSxGtyagFE8B4xELB1oYe3S5RD8Ci3uZAsZaascH2LAEQ==`.

Preferred operation is **calling installed packages through their API**, with original wrapper/example code and normal explicit dependency setup. This avoids vendoring approximately 7 MB of unpacked Ink distribution merely to supply a 249 KB full runtime bundle. If code or bundled binaries are redistributed, retain each package's original license/copyright and glTF's bundled notices; “no runtime npm dependencies” is not “no compiled third-party code.” If adapting another project's source bytes, record the exact source path, revision and most specific terms instead of relying on root MIT labels for adjacent textures/photos/models. No such external asset copying is needed for these probes.

The current glTF main version and npm version differ, and the npm package uses a `dev` version label. Record this accurately; neither older release age nor active main alone establishes security, abandonment, support, or migration urgency. The decision is bounded by the APIs and synthetic files actually checked.

## Change units and remaining acceptance

| Decision | Unit | Input -> operation -> artifact -> check | Cost/dependency boundary | Next check |
|---|---|---|---|---|
| Connect/adapt now | Optional Ink runtime adapter, original narrative example, routed environment reference | selected Ink -> real compiler/runtime -> compiled program, trace, native saved state -> named choice/state/reload predicates | Node, pinned inkjs; no model/API calls; explicit installation only | Product tests must exercise invalid/stale/missing evidence and lawful alternatives; no improvement claim without behavioral comparison |
| Connect/adapt now | Optional glTF validation adapter and original asset fixtures | chosen bytes/resources -> actual Khronos validator -> raw report and digest -> conformance plus explicit consumer profile | Node, pinned validator; no Blender/MCP/model required; bounded resource reads | Product checks for unsupported extensions, missing resources, malformed reports and artifact identity; native import remains separate |
| Retain | Current Godot episode and native report contract | fixture -> copied native project -> engine input/physics/save report -> current predicates | Existing qualified 4.7.2 route | No replacement justified by a launch/log bridge |
| Test further/connect conditionally | Existing Unity CLI/Pipeline or Coplay MCP project adapter | selected Unity project -> edit/play/test job/capture -> engine artifacts -> native relation and visual check | Editor/license, project package, bridge/host and render environment | Exact version receipt; live progress; failed and legitimate scenarios; cleanup/isolation |
| Test further/adapt narrowly | Blender audit/review/re-import helper | chosen source/export -> bpy operation -> actual exported file, measured report/render -> target profile | Matching Blender; render/GUI availability; asset terms | Run specified helper on actual controls; do not inherit unrun test claims or universal thresholds |
| Test further | Erodenn live Godot bridge | existing project -> temporary bridge + observed input -> frame/state/log artifacts -> target task predicate | Node/MCP SDK, Godot, temporary project writes/TCP, possible display | Ownership-safe cleanup, attached-mode limitations, genuine input/capture execution |
| Retain alternative | Yarn compiler/runtime | Yarn project -> compiler/Dialogue host -> program/string table/options -> project narrative relation | .NET + exact core/compiler dependencies | Use when the target game already needs Yarn; no migration just for package symmetry |
| Reject wholesale transfer | Lead/orchestrator skills, automatic installs, access scans, rigid model/budget protocols | Not required for the accepted artifact consumer | Duplicates Assay/general execution or introduces unrelated operating policy | No implementation warranted |

The next product step is implementation of the two accepted narrow routes, preserving the existing subjects and their separate evidence claims. The probes establish feasibility; their ad hoc receipts do not yet establish a published, validated, reusable runtime contract.
