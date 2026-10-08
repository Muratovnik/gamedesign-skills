# Ink episode: the listening room

This original synthetic scene exercises a native narrative artifact boundary.
The participant can hear a recording's introduction, share an excerpt after
the introduction, or leave. The introduction says that the voice is an
imitation. Sharing carries that notice into the final text. Departure remains a
valid ending and does not require sharing.

The scene applies the existing
[conditional story method](../../skills/game-world-narrative-design/references/conditional-story.md).
The optional [Ink artifact route](../../skills/game-world-narrative-design/references/ink-artifacts.md)
adds actual compiler, runtime and save/reload observations. It does not replace
the story method or establish that a person understood the introduction.
`disclosure_heard` is an authored variable whose tested meaning here is that the
native trace emitted the introduction before sharing became available.

## Run the selected paths

Run from the repository root. Install the optional dependency in fresh scratch;
the skill and live game project do not need an installation.

```sh
ink_deps=$(mktemp -d)
cp skills/game-world-narrative-design/scripts/package.json \
  skills/game-world-narrative-design/scripts/package-lock.json "$ink_deps/"
npm ci --prefix "$ink_deps" --ignore-scripts --no-audit --no-fund
ink_work=$(mktemp -d)
ink_adapter=skills/game-world-narrative-design/scripts/ink_artifact.cjs
ink_fixtures=examples/ink-episode/fixtures

node "$ink_adapter" compile --source "$ink_fixtures/listening-room.ink" \
  --inkjs-root "$ink_deps/node_modules/inkjs" --out "$ink_work/compiled"

node "$ink_adapter" run --compiled "$ink_work/compiled/story.json" \
  --scenario "$ink_fixtures/inspect.json" \
  --inkjs-root "$ink_deps/node_modules/inkjs" --out "$ink_work/inspected"
node "$ink_adapter" assess --compiled "$ink_work/compiled/story.json" \
  --scenario "$ink_fixtures/inspect.json" --report "$ink_work/inspected/report.json" \
  --out "$ink_work/inspect-assessment"

node "$ink_adapter" resume --compiled "$ink_work/compiled/story.json" \
  --state "$ink_work/inspected/state.json" --scenario "$ink_fixtures/resume-share.json" \
  --inkjs-root "$ink_deps/node_modules/inkjs" --out "$ink_work/shared"
node "$ink_adapter" assess --compiled "$ink_work/compiled/story.json" \
  --scenario "$ink_fixtures/resume-share.json" --report "$ink_work/shared/report.json" \
  --out "$ink_work/share-assessment"

node "$ink_adapter" run --compiled "$ink_work/compiled/story.json" \
  --scenario "$ink_fixtures/leave.json" \
  --inkjs-root "$ink_deps/node_modules/inkjs" --out "$ink_work/left"
node "$ink_adapter" assess --compiled "$ink_work/compiled/story.json" \
  --scenario "$ink_fixtures/leave.json" --report "$ink_work/left/report.json" \
  --out "$ink_work/leave-assessment"
```

Each process reopens its selected file. `compile` saves the real compiler's JSON.
`run` saves the real runtime's native state, plus an envelope binding the compiled
story SHA-256 and inkjs version/bundle digest. `resume` creates a fresh `Story`,
loads that native state, verifies the saved checkpoint and performs the next
explicit choice. The observation after resuming starts at the checkpoint; it
does not replay the introduction's earlier output.

Every output directory must be new. Keep the source copy, compiled JSON,
scenarios, reports, native-state envelope and assessments together when handing
off evidence. The report records the exact adapter, compiled story and scenario
digests. Hashes identify selected bytes; they are not an attestation of execution.

| Selected path | Expected native observation | Assessment |
| --- | --- | --- |
| Initial room → introduction | Share absent before the introduction; notice emitted; share and leave offered afterward | `inspect.json`: supported |
| Saved informed state → fresh runtime → share | Informed state restored; share accepted; excerpt and notice carried to the ending | `resume-share.json`: supported |
| Fresh room → leave | Terminal scene with both variables false | `leave.json`: supported |
| Closed room with no supplied action | Closing text and legal terminal state | `terminal.json`: supported; a required-action predicate would be refuted |
| Same room with only the sharing guard removed | Native compilation and execution still succeed; share is already offered initially | The unchanged `inspect.json` refutes its first predicate |

For the terminal scene, compile `fixtures/closed-room.ink` into another fresh
directory and run `fixtures/terminal.json`. It supplies no action and checks an
accepted ending. The adapter also permits an entirely silent native ending; an
empty list of checks cannot yield a supported assessment.

## Focused tests and controls

```sh
INKJS_ROOT="$ink_deps/node_modules/inkjs" \
  node --test examples/ink-episode/test_ink_artifact.cjs
```

The built-in Node test runner launches the actual adapter and selected inkjs
bundle. It does not mock the compiler, interpreter or native state format.
`INKJS_ROOT` is required: an absent runtime is a setup failure, not a skipped or
passing integration test. Fixtures and temporary artifacts are task-owned; the
suite removes only its own temporary directories.

The checks protect these distinctions:

- The original scene supports the guard, emitted notice and surviving sharing
  consequence through a real saved-file handoff and a fresh process/runtime.
- Removing only the sharing guard produces a runnable defect. The same
  assessment refutes exactly the initial-availability predicate; a compiler
  crash cannot substitute for that negative result.
- Leave remains available and executable before and after the introduction.
  JSON member reordering in the state envelope does not change its meaning.
- A terminal scene with no action supports its text/ending predicates, refutes a
  required-action predicate, and leaves an empty check set unavailable.
- A different compiled story, dependency identity, altered native-state checksum
  or false saved checkpoint cannot silently resume.
- Duplicate choice labels need a current index. An absent, negative or
  fractional index cannot select a fallback or continue after an ending.
- Invalid Ink syntax retains compiler diagnostics. `INCLUDE` cannot load an
  existing sentinel file, and a host-function call receives no binding.
  Native `RANDOM(3, 1)` reports a runtime error; `RANDOM(3, 3)` supplies a nearby
  valid control. The source of that error expectation is the pinned runtime's
  [random-range validation](https://github.com/y-lohse/inkjs/blob/edccead8700e9f21be9825d87d8645d8c82a9936/src/engine/Story.ts).
- A continuing text loop exhausts its continuation budget; a silent native loop
  reaches the worker deadline. Neither leaves a completed save. Existing output
  directories are preserved, and stale or incomplete reports are unavailable.

During development, an initial negative fixture assumed a scene without an
explicit `END` was invalid. The actual runtime accepted it as a terminal scene.
That mistaken oracle was replaced by the native random-range control above;
the adapter was not changed to reject the lawful ending.

## Scope and provenance

The original fixture, scenarios, adapter and tests are this repository's MIT
material. The optional external `inkjs@2.4.0` package is MIT, credits inkle Ltd.
and inkjs contributors, and has no runtime npm dependencies. The
[runtime reference](../../skills/game-world-narrative-design/references/ink-artifacts.md#component-provenance-and-terms)
records its exact source commit, artifact hashes and terms. The lock's
integrity and the adapter's bundle hash are both checked on the installation/run
path. No external source, sample scene or orchestration loop is vendored here.

The local compatibility observation is Node 24.19.0 with the exact pinned npm
package and format-21 compiled JSON. This example exercises selected Ink text,
conditions, choices, scalar globals, native state and the documented failures.
It does not establish all Ink language features, every branch, save migration,
Yarn compatibility, Unity/Godot integration, audio or UI behavior, human
comprehension, cultural accuracy or dramatic quality.
