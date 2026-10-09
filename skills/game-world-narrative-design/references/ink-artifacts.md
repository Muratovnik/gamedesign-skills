# Optional Ink artifact route

Use this route when the requested result includes an executable Ink story,
its offered choices, a selected consequence, or a native save/resume handoff.
A written scene and its meaningful variants can already complete a writing
task. Choose the native route because a specific delivery or execution claim
needs it. The [conditional story method](conditional-story.md) still owns the
relationship, preparation, condition, reveal, refusal and surviving consequence.

The [adapter](../scripts/ink_artifact.cjs) delegates source parsing, compilation,
execution and state serialization to **inkjs 2.4.0**. It adds explicit file
selection, bounded caller actions, observations, identity checks and assessment
of caller predicates. It has no choice-selection strategy or model loop.

## Select the claim and its actual consumer

Write the scene first, then select the smallest trace that could disprove its
promised behavior. For example, an excerpt may become shareable only after its
imitation notice has been emitted. Inspect the offered choices before and after
the introduction, the emitted notice, the state effect, and the next choice after
a native save is reopened. Keep a legitimate departure or ending in the sample
where the scene permits one. A deliberately removed guard is a useful negative
control only if the resulting story still compiles and executes.

Emitted text does not establish that a person read, heard, understood or believed
it. The runtime also cannot establish dramatic effect, cultural accuracy, UI
readability, voice performance or a game engine's import behavior. Make those
claims through their actual consumer. This route observes only the supplied
action sequence; it does not enumerate all branches or prove global reachability.

## External dependency and operation boundary

The dependency is optional and remains outside the skill. The adjacent
[package manifest](../scripts/package.json) and [lock](../scripts/package-lock.json)
pin `inkjs@2.4.0`, including npm archive integrity. Install them in a new,
task-owned directory when a native run is needed; do not install into a live
game project, client configuration or the skill bundle.

```sh
skill_dir=/absolute/path/to/game-world-narrative-design
ink_deps=$(mktemp -d)
cp "$skill_dir/scripts/package.json" "$skill_dir/scripts/package-lock.json" "$ink_deps/"
npm ci --prefix "$ink_deps" --ignore-scripts --no-audit --no-fund
ink_work=$(mktemp -d)
```

Supply the installed package root explicitly as `--inkjs-root
"$ink_deps/node_modules/inkjs"`. The adapter verifies the package name, version
and SHA-256 of `dist/ink-full.js` before loading it. It does not discover a client
or game project. Node 24.19.0 and this exact package were exercised locally;
other Node releases and Ink runtime versions need their own compatibility check.
`assess` uses the recorded artifacts and does not load inkjs.

Supported inputs are a **single Ink source file**, compiled Ink JSON format 21,
an explicit scenario, and optionally a state envelope produced by this route.
All selected text files, including the dependency manifest, must contain valid
UTF-8. Malformed bytes return `invalid_utf8` with exit 2 before parsing or native
execution; they are never replaced with a different character. Valid Unicode,
including a literal U+FFFD replacement character, remains supported. JSON input
keeps its existing parser rules, including rejection of a leading byte-order mark.
The compiler has a denying file handler: an actual `INCLUDE` request is
unavailable, even when the file exists. The runtime supplies no external
function bindings and disables external fallbacks; a compiled story that calls
a host function is unavailable before the selected action sequence runs.
Unused external declarations alone do not provide a host capability. This is
not a claim of complete Ink language, integration or package-version coverage.

The adapter reads the explicitly selected artifacts, its own file and the
selected dependency's manifest/bundle. Ink receives no filesystem resolver,
network handler or external-code binding. A worker thread bounds native
execution and is terminated after a result or deadline; it is **not a security
sandbox for arbitrary JavaScript dependencies**. Only the pinned bundle is
loaded. All output paths are fixed filenames under a fresh output directory.

## Compile, run, save and resume

Commands require an existing parent for every new output directory. An existing
file, directory or symlink at `--out` is a collision; no artifact is overwritten.
If a run is interrupted or fails, use a different directory on the next attempt.

```sh
node "$skill_dir/scripts/ink_artifact.cjs" compile \
  --source /selected/scene.ink \
  --inkjs-root "$ink_deps/node_modules/inkjs" --out "$ink_work/compiled"

node "$skill_dir/scripts/ink_artifact.cjs" run \
  --compiled "$ink_work/compiled/story.json" --scenario /selected/inspect.json \
  --inkjs-root "$ink_deps/node_modules/inkjs" --out "$ink_work/inspected"

node "$skill_dir/scripts/ink_artifact.cjs" resume \
  --compiled "$ink_work/compiled/story.json" --state "$ink_work/inspected/state.json" \
  --scenario /selected/next-action.json \
  --inkjs-root "$ink_deps/node_modules/inkjs" --out "$ink_work/resumed"

node "$skill_dir/scripts/ink_artifact.cjs" assess \
  --compiled "$ink_work/compiled/story.json" --scenario /selected/next-action.json \
  --report "$ink_work/resumed/report.json" --out "$ink_work/assessment"
```

| Operation | Native operation | Artifacts and check |
| --- | --- | --- |
| `compile` | `Compiler.Compile()`, then `Story.ToJson()` | Copies `source.ink`, writes `story.json`, reopens it for its SHA-256, and writes `receipt.json` with diagnostics |
| `run` | Fresh `Story` from reopened compiled JSON; `Continue()` to a choice or ending; caller's `ChooseChoiceIndex()` | Copies `story.json` and `scenario.json`; writes observations/actions in `report.json` and native state in `state.json` |
| Save at completion of `run` or `resume` | `story.state.ToJson()` | `ink-state/1` envelope binds the native JSON digest, compiled story digest and exact dependency identity to the final checkpoint |
| `resume` | Fresh `Story`, `story.state.LoadJson()`; verify checkpoint; perform supplied next actions | Copies `input-state.json`; checks restored choices, selected variables and terminal state before advancing; emits another report and state |
| `assess` | No VM execution | Checks report coverage and selected artifact identities, then evaluates each supplied predicate; optional `assessment.json` |

Every successful run saves at its final observed pause or ending, including a
run with no supplied actions. Resuming does not replay earlier text. Its first
observation starts at the saved checkpoint and then follows its new scenario.
The state is tied to the exact compiled bytes and dependency. Edited stories,
another runtime version, an altered native-state checksum or a checkpoint that
the fresh runtime does not restore produce `unavailable`. Migration is a
separate task; a checksum is not a save-migration algorithm.

## Supply the choices and checks

A scenario is a JSON object with schema `ink-scenario/1`, an `id`, selected
`observe_variables`, an `actions` array and a `checks` array. Observation 0 is the
initial pause or ending after native continuation. Action 1 leads to observation
1, and so on. Each action contains exactly one selector: `{"choice": "Exact
label"}` or `{"index": 0}`. Text must match exactly one currently offered choice;
ambiguous labels require the current zero-based index. An unavailable choice,
invalid index or action after an ending fails as unavailable evidence. No
fallback action is selected.

```json
{
  "schema": "ink-scenario/1",
  "id": "disclosure-before-sharing",
  "observe_variables": ["disclosure_heard"],
  "actions": [{"choice": "Hear the introduction"}],
  "checks": [
    {"kind": "choice", "at": 0, "text": "Share the excerpt", "available": false},
    {"kind": "text", "at": 1, "includes": "The voice is an imitation"},
    {"kind": "variable", "at": 1, "name": "disclosure_heard", "equals": true},
    {"kind": "choice", "at": 1, "text": "Share the excerpt", "available": true},
    {"kind": "action_count", "at_least": 1}
  ]
}
```

| Predicate | Meaning |
| --- | --- |
| `choice`: `at`, `text`, `available` | Whether at least one current choice has the exact label; this does not resolve an ambiguous action selector |
| `variable`: `at`, `name`, `equals` | Exact equality for a selected declared global boolean, finite number or string |
| `text`: `at`, `includes` | Nonempty substring in the concatenated native text chunks emitted during that observation |
| `terminal`: `at`, `equals` | Whether native continuation has ended with no offered choice |
| `action_count`: `at_least` | Whether the completed transcript contains at least the positive number of explicit caller actions |

The VM retains its own state representations. This route does not flatten Ink
lists, divert targets or other complex values into invented scalar observations;
selecting such a variable is unavailable. Actions and checks contain no code or
expressions. Unknown fields and unsupported predicates are rejected.

An empty action list is legal. A terminal text scene can support its text and
ending predicates without offering a choice. It cannot support
`{"kind":"action_count","at_least":1}`. An empty check list may be useful for
capturing a run, but assessment returns unavailable because no property was
selected. A positive result always names the predicates actually inspected.

## Limits and result interpretation

Native commands use a 5,000 ms worker deadline by default; `--timeout-ms` accepts
1–30,000 ms. Each run allows at most 1,000 `Continue()` calls and 100,000 emitted
text/tag characters by default. Optional scenario `limits` may set
`max_continue` from 1 to 100,000 and `max_output_chars` from 1 to 1,000,000.
Scenarios allow at most 1,000 actions, 1,000 checks and 100 scalar variable names.
The observation transcript is limited to 2 MiB; each selected file and written
artifact is limited to 8 MiB. A loop, oversized artifact, unavailable variable or
native error cannot produce a completed save.
Compiler/runtime diagnostics are retained; warnings alone do not establish a
failed story property. Deadlines and infrastructure failures can leave only an
unavailable receipt, without a partial transcript.

| Command result | Exit code | What it establishes |
| --- | --- | --- |
| `compile`: `compiled`; `run` / `resume`: `executed` | 0 | The named native operation completed within the bounds; this is not a design assessment |
| `assess`: `supported` | 0 | Every supplied predicate holds in the selected completed transcript |
| `assess`: `refuted` | 1 | At least one predicate is false in otherwise usable evidence |
| `unavailable` | 2 | Input, identity, native execution or report coverage could not support assessment |

Reports bind the exact compiled JSON, scenario bytes, adapter bytes and
dependency identity. Changing any of those inputs requires a new run. Hashes
detect stale or mismatched artifacts; they do not authenticate who ran the
program or prevent someone from fabricating a report. Preserve the actual
command outputs and state files for review, and reopen them through their
consumer when the delivery claim depends on doing so.

## Component provenance and terms

The selected npm artifact is
[`inkjs@2.4.0`](https://www.npmjs.com/package/inkjs/v/2.4.0), with npm `gitHead`
[`edccead8700e9f21be9825d87d8645d8c82a9936`](https://github.com/y-lohse/inkjs/tree/edccead8700e9f21be9825d87d8645d8c82a9936).
The inspected implementation includes
[Compiler](https://github.com/y-lohse/inkjs/blob/edccead8700e9f21be9825d87d8645d8c82a9936/src/compiler/Compiler.ts),
[Story](https://github.com/y-lohse/inkjs/blob/edccead8700e9f21be9825d87d8645d8c82a9936/src/engine/Story.ts),
[StoryState](https://github.com/y-lohse/inkjs/blob/edccead8700e9f21be9825d87d8645d8c82a9936/src/engine/StoryState.ts)
and [choice tests](https://github.com/y-lohse/inkjs/blob/edccead8700e9f21be9825d87d8645d8c82a9936/src/tests/specs/ink/Choices.spec.ts).

It has no runtime npm dependencies. Its
[MIT license](https://github.com/y-lohse/inkjs/blob/edccead8700e9f21be9825d87d8645d8c82a9936/LICENSE.md)
credits inkle Ltd. and the inkjs contributors (2017). The package is an external
compiler/runtime dependency; this skill does not vendor its source or bundle,
copy its examples, or import its repository's orchestration. Preserve its
copyright and permission notice if redistributing it. Its development toolchain
is outside this installation and local claim.

- npm archive SHA-256: `100cf088ef2954927c2a107a42f2154e6b1c0dcea00faf7241b27542e5f88622`.
- Executed `dist/ink-full.js` SHA-256: `23d707b76e9b759a25803c193da8e32e04f727dd13a54ed1df8a6a59dd909b9e`.
- npm archive SHA-512 integrity is recorded in the lockfile and checked by `npm ci`.
