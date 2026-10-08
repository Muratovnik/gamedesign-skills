# Lantern Crew: an existing controller, a changed recovery boundary

This original, synthetic Godot episode demonstrates a bounded change to an
existing scene and controller. `fixtures/baseline.json` is build
`gate-episode-1`. `fixtures/candidate.json` is build `gate-episode-2`: recovery
changes from 36 to 12 physics ticks. The scene, body, input pipeline, threats,
camera and no-cancellation rule stay shared. A change to the JSON reaches the
same native consumer; it is not a Python model of Godot physics.

**Task:** after a committed attack, make a later dodge available through the
gap while retaining the commitment. Bo must avoid the quay pulse and crane
sweep, preserve the archive-message history and personal right owners through
save/reset/load, and obtain Ivo's response from Ivo's restored local knowledge.
These diagnostic timings are chosen to make the cases easy to distinguish,
not as recommended combat timings for people.

## Prerequisites and commands

Use a supplied **Godot 4.7.2 Linux x86_64 standard editor binary** and Python
3.11+ with `jsonschema==4.26.0`. The recorded host used Python 3.12.14. Obtain
Godot from its [official archive](https://godotengine.org/download/archive/4.7.2-stable/)
into a disposable directory. The package does not install an engine or modify
client settings. The binary is not redistributed in this example.

From the Game Design repository root, choose an isolated environment. If one
does not already exist:

```bash
python3 -m venv .venv
.venv/bin/python -m pip install -r examples/godot-episode/requirements.txt
```

Set `PYTHON` to that environment's executable and `GODOT` to your actual
binary path. All remaining commands run from the repository root. `RUN` is a
new disposable output root; each `--out` below must be a nonexistent directory.

```bash
PYTHON=.venv/bin/python
GODOT=/absolute/path/to/Godot_v4.7.2-stable_linux.x86_64
RUN=$(mktemp -d)
"$PYTHON" examples/godot-episode/qualify.py run \
  --godot "$GODOT" \
  --fixture examples/godot-episode/fixtures/candidate.json \
  --out "$RUN/candidate"
"$PYTHON" examples/godot-episode/qualify.py assess \
  --fixture examples/godot-episode/fixtures/candidate.json \
  --report "$RUN/candidate/report.json" --claim escape
```

The first command validates the fixture using the installed JSON Schema
library, copies the exact native inputs to a disposable project, runs native
import, then executes the scene. Godot configuration, data and cache directories
are redirected into that output directory. It stores the input fixture, source
copy, process stdout/stderr, `receipt.json`, `report.json`, and the native saved
state `report.json.save.json`. It never replaces an existing output directory.

The second command tests the specified game property against the current
fixture and native source hashes. It reads the actual input events, positions,
collisions, threat resolutions and post-load NPC response. It returns **0** for
supported, **1** for a refuted property and **2** for missing, malformed or stale
evidence. A `run` exit of zero means the consumer executed, not that Bo escaped.
The report is ordinary inspectable evidence, not a signed authenticity service.

The report has its own `episode-report.schema.json` contract, separate from the
input fixture schema. The assessor checks the root, event/detail records,
state, integer counters, boolean observations and two-coordinate vectors before
evaluating a game property. The shared standard-library JSON boundary rejects
NaN, Infinity and numeric overflow. A list in `hit`, the string `"false"` in a
camera flag, or a malformed position therefore returns structured invalid
evidence with exit 2. Actual boolean observations can still refute a property
with exit 1. Extra root diagnostic metadata is allowed; it is not evidence for
the property. Empty observed populations remain unavailable with exit 2.

Run the complete public control set with:

```bash
"$PYTHON" examples/godot-episode/qualify.py suite \
  --godot "$GODOT" --out "$RUN/control-suite"
```

The suite expects some property checks to return 1 or 2. It succeeds only when
those distinctions match the stated contracts. A launch/import timeout returns
2, retains that attempt, and leaves dependent claims unavailable. The 30-second
per-process bound is an operational limit of this small qualification command.
Do not interpret an import timeout as a collision or game-design defect.

## What the native consumer does

`episode.tscn` loads `episode.gd` and the separate existing `player.gd`
controller. `Input.parse_input_event()` feeds `InputEventAction` objects into
Godot. `Node._input()` receives and queues them; the controller accepts or
rejects them during physics. A committed action cannot be cancelled. Movement
uses `CharacterBody2D.move_and_slide()` against native `StaticBody2D` shapes.
The harness does not write a successful position in place of an input.

The harness explicitly flushes the engine input buffer at its declared tick.
This removes render-loop scheduling from this synthetic delivery contract; it
does not measure hardware latency. The
[Input API](https://docs.godotengine.org/en/stable/classes/class_input.html#class-input-method-parse-input-event)
documents both delivery to `_input` and the separate
[`flush_buffered_events` operation](https://docs.godotengine.org/en/stable/classes/class_input.html#class-input-method-flush-buffered-events).

| Shared relation | Input and observation |
| --- | --- |
| Identity | Game `lantern-crew`; actor `bo`; scene/fixture hashes in each report; Ivo is local NPC `keeper-ivo` |
| Body and gap | Bo starts at `[40,90]` px, radius 8 px; barrier centered at x=120 px, thickness 16 px; normal gap 28 px |
| Camera | Fixed 240×180 px viewport, center `[120,90]`; cue positions transformed through Godot's canvas transform |
| Attack | Input at run tick 2; baseline recovery ends at world tick 38, candidate at 14; neither is cancellable |
| Dodge | Input at run tick 16; when admitted, 12 ticks of rightward motion at 600 px/s |
| Threats | Quay pulse warns at 10, resolves at 26; crane sweep warns at 12, resolves at 34; each has its own affected x-range |
| Knowledge | Ivo acquires `gate-crossed` only after the crossing and an unoccluded native physics ray to Bo |
| State | Save at run tick 40, reset at 42, load at 44; interaction at 48 consumes restored Ivo knowledge |

`run_tick` is the non-resetting harness clock. `world_tick` is the saveable game
clock. Every event records both, the engine physics frame and a monotonic host
timestamp. The simulation step is 1/60 s. Restoring game time intentionally
does not reset the harness schedule or host clock. Input, action acceptance,
warning and resolution are therefore inspectable without confusing a restored
world clock with elapsed recording time.

## Distinguishing cases and actual observations

Qualification used `4.7.2.stable.official.ed1daf0bf` on Linux x86_64.
The native files compiled/imported and six scenarios reached the controller.
Current source assessments matched all twelve expected checks across the named
runs and a focused follow-up; this was not a claim that every initial attempt
passed.

| Fixture | What differs | Observed native result | Relevant assessment |
| --- | --- | --- | --- |
| `baseline.json` | Recovery 36 ticks | Dodge rejected during commitment; x=40 px; health=0 | `escape`: 1; `recovery-blocked`: 0 |
| `candidate.json` | Recovery 12 ticks | Dodge accepted; x=160 px; health=2; save/load relations match; Ivo answers from crossing knowledge | `escape`: 0; `camera-signals`: 0 |
| `recovery-locked.json` | Warning wording becomes more explicit; recovery stays 36 | The same committed-recovery rejection and damage | `escape`: 1; `recovery-blocked`: 0 |
| `narrow-gap.json` | Candidate recovery; gap 12 px | Center ray is clear, but the actual body collides and stops near x=106.66 px; health=0 | `escape`: 1; `body-blocked`: 0 |
| `off-camera.json` | First source moves outside the camera rectangle | Bo still escapes under the prerecorded schedule; first cue is outside the viewport | `escape`: 0; `camera-signals`: 1 |
| `no-input.json` | Valid candidate import, empty input schedule | Native execution completes with no action and no crossing | `escape`: 1 |
| Baseline report supplied as candidate | Stale fixture identity | Rejected before game-property acceptance | `escape`: 2 |

The first control run exposed delayed delivery of buffered input. The explicit
flush was added, and the narrow-gap case then exercised its intended native
collision. A later no-input import timed out before execution; the original
attempt was retained. A fresh focused run completed and its no-action result
refuted escape as intended. Operational startup reliability is bounded by those
observations, not claimed from one successful repeat.

An intentional non-cancellable attack is a legitimate rule. `recovery-blocked`
supports that rule even though `escape` is refuted for this schedule. A designer
may instead change geometry, threat composition or the promise of an available
escape; the example does not require shortening every commitment.

## Evidence limits and further use

The collision witness concerns one body, trajectory, collision mask and geometry.
An unobstructed ray is not volumetric clearance, camera readability, audibility
or proof that every route was searched. The ray query runs in physics as
required by the [native physics API](https://docs.godotengine.org/en/stable/tutorials/physics/ray-casting.html).
The off-camera check concerns a coordinate within the viewport rectangle;
headless execution does not inspect rendered contrast or attention.

The source also draws simple diagnostic shapes and accepts Space (attack), D
(dodge), E (interact), F5 (save), R (reset) and F9 (load). An optional graphical
run may pass `--interactive` after the engine's `--` separator. That disables
the prerecorded schedule and automatic exit. Graphical play, audio, device
comfort, human interpretation and input latency have **not** been qualified.
The default path uses headless mode and Dummy audio, as documented in the
[Godot CLI](https://docs.godotengine.org/en/stable/tutorials/editor/command_line_tutorial.html).

Save/load uses native `FileAccess` and JSON parsing, with explicit conversion
of vector coordinates into numeric arrays. The owning scene preserves actor
identity, time, health, commitment, owners, history, knowledge and resolved
threat flags. Its [native save primitives](https://docs.godotengine.org/en/stable/tutorials/io/saving_games.html)
do not automatically define a game's migration policy. The companion
[analysis lab](../analysis-lab/README.md#state-migration) supplies a separate
campaign migration, resource and observer example.

To adapt this example to another game, keep entity IDs, permissions, units,
rules and private data with that consumer. Use its existing controller and save
format. Preserve an old fixture and create a candidate with the proposed change;
then execute and interpret the relevant property. These original files are a
public teaching example and cannot serve as secret final model-evaluation data.

## Report contract regressions

```bash
"$PYTHON" -m unittest discover -s examples/godot-episode -p test_report_contract.py -v
```

Five public tests exercise the assessor and a separate CLI rejection. They use
the byte-preserved native candidate report at
`fixtures/test_recorded_candidate_report.json`, then alter only selected fields
to distinguish malformed evidence from a typed negative observation. That file
is a historical test fixture, not a new engine run or a game input. Its `test_`
name identifies it as test data. The tests also retain valid
extra diagnostic metadata, empty-observation and stale-fixture controls.
