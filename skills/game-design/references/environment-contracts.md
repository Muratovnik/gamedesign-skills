# Choose and complete an environment operation

Read this when a design claim depends on a file, calculation, episode, time,
geometry, observer, data or material operation. Select the relevant rows; a
small rule change does not require every environment. General verification is
owned by Assay `code-change` and `test-writing`; research design and interpretation
by `evidence-research`, reached through the [source contract](consumer-and-assay-contract.md).

## Carry the relation through the boundary

Before a dependent action establish the actual object and revision, the input
semantics, authority to act, available tool/version, required precision, output
destination and next consumer. These can be ordinary project files and task
context; no universal context JSON is required. Keep original inputs until the
consumer accepts the changed artifact. Reopen outputs and inspect the relation
that the change was intended to preserve or create.

For a result distinguish: the operation exists in documentation; its source was
inspected; it ran on these inputs; the resulting property was checked. A command
exit, valid schema or successful import cannot stand for all four. Missing access,
invalid evidence, refutation and a supported property need different outcomes.
Never pass an empty inspected or selected set as a clean result.

| Needed operation | Shipped route and actual consumer | What remains a different claim |
| --- | --- | --- |
| Read, edit and reopen a semantic artifact | JSON with versioned IDs; `scripts/validate_artifact.py` and skill-local `assets/*.schema.json`; original/candidate Godot fixtures and migration outputs are consumed again | Schema validity does not prove a playable or worthwhile relation; arbitrary game formats need their real importer |
| Calculate resources, waiting and reachable recovery | `examples/analysis-lab/lab.py`: resource witnesses, geometric waiting with a declared guarantee, save repair/survey; resulting save is read by `consumer.py` | A bounded witness is not exhaustive human strategy or a frequency distribution of play |
| Relate signal, input and clock | Godot fixed ticks/Input trace; `examples/design-studies/harbour-of-echoes/render_loom.py` consumes two control scores into WAV and timed radius/dot-count CSV, then reopens them | Native ticks and PCM samples do not measure perceptual onset, motor response, frame pacing, speaker output or device latency |
| Check geometry and observation | Real Godot bodies, collision query, point-ray and camera-frustum probes | A clear ray is not body clearance; in-frustum is not visually noticed; geometry is not material reachability |
| Enact an episode | Godot scene executes actual input and physics; `run` creates a report, `assess` accepts/refutes the named property; toy consumers enact later choices | A native action trace is not a human playtest, complete game or production-project edit |
| Save, reset and migrate state | Godot save/reload and analysis v1→v2 migration retain owners, rights, private knowledge, history and allowed next actions; idempotent operation IDs prevent repeated effects | Package update is not save rollback; every existing game's migration needs its own ownership and loss semantics |
| Represent different participant views | `consumer.py view` writes one actor's permitted information; `choose` consumes only that file and permitted content | Serialized redaction does not isolate a model that previously read both views; simultaneous social interaction needs actual separate participants/contexts |
| Analyze semantic event data | CSV sessions/events plus a versioned dictionary → SQLite query → build/cohort-specific denominator, unknown outcomes and result JSON | Synthetic rows show the pipeline, not player rates, causal explanations or live instrumentation |
| Import human or material observations | `scripts/observe_evidence.py` consumes documented CSV and manifest, retains recording/material references, assistance and missingness | The importer cannot authenticate consent, inspect a physical table, measure experience or turn invented rows into evidence |

Paths under `examples/` are public source examples, not mandatory runtime imports.
The full installed bundle contains the scripts and schemas needed by the runtime
contract. The game project owns its native engine and adapters. Use the actual
consumer's tools for another engine; these examples do not implement Unity,
Unreal, Blender or arbitrary UGC compatibility.

## Concrete command and handoff routes

For runtime validation, resolve paths from this skill's installed directory:

```bash
python3 scripts/validate_artifact.py --schema assets/episode.schema.json --input /absolute/game/candidate.json
```

Install the pinned requirements from `scripts/requirements.txt` into an isolated
environment only when using these Python operations. No install is performed by
loading a skill. Inputs and outputs below are placeholders for explicitly chosen
game-owned files; use the literal runnable commands in the shipped example READMEs.

For the Godot source example, from the source package root:

```bash
python3 examples/godot-episode/qualify.py run --godot /absolute/godot --fixture examples/godot-episode/fixtures/candidate.json --out /fresh/episode-run
python3 examples/godot-episode/qualify.py assess --fixture examples/godot-episode/fixtures/candidate.json --report /fresh/episode-run/report.json --claim escape
```

`assess` distinguishes supported (0), refuted (1), and missing, invalid, stale or
unavailable evidence (2). Verify the input digest, build and fixture identity,
executed events, relevant clock and actual output. A save/reload claim needs the
ordered operations and the state they preserved; an aggregate success flag is
not that evidence. The point-ray/body mismatch,
off-camera signal, unavailable input and blocked recovery controls show why a
single successful execution is insufficient.

For state work, migrate to a new path, inspect it, then build an actor view and
ask the consumer for the next legal choice. Compare owner, resource, right,
knowledge and history semantics as well as numbers. For telemetry, preserve the
session denominator, event definitions, build/cohort filter and missingness.
Check that the selected outcome is defined among that build's events before
counting outcomes; an invalid definition is not a failed attempt. A missing
completion event does not automatically mean failure.

## Human and material route

Choose the question first: noticing a signal, interpreting a clue, executing a
gesture, negotiating refusal, reaching a token, learning without a prompted
answer, or a cultural reading require different observations. Use the project's
existing consent and privacy rules, actual target materials/device and suitable
participants. Record task, artifact/build, conditions, assistance, attempted and
completed actions, participant report separately from interpretation, and an
inspectable recording or material note where authorized. Record unavailable
observations explicitly; do not fabricate participants to fill a table.

The import columns are `participant_id,object_id,build_id,task_id,attempted,completed,elapsed_s,assistance,report,missing_reason,recording_ref`.
Allowed attempt/outcome values are `yes`, `no`, `unknown`; assistance is `none`,
`facilitator`, `persistent-aid`, `unknown`. The observation schema records source
kind, question, game/build, limitations and whether the relevant relation was
available. Synthetic data must remain labeled synthetic after import.

```bash
python3 scripts/observe_evidence.py --csv /absolute/observations.csv --manifest /absolute/observation-manifest.json --output /fresh/observations.json
```

The importer retains rows and computes bounded descriptive counts. Its
`human_claim` remains `not_established`: the next researcher must inspect the
material, distinguish interpretation from cause, and decide whether a design
revision is supported. A successful import cannot settle readability, consent,
learning, social pressure or aesthetic experience.

## When the route is incomplete

Finish the useful authorized file or paper work, then leave the needed outcome
open with its missing tool, artifact, permission, participant or precision.
Do not substitute a different demonstration for an existing game's requested
change. A prepared capture route can satisfy preparation; it cannot satisfy a
claim that requires the missing observation. Work continuation belongs in the
[consumer contract](consumer-and-assay-contract.md); saving game state
belongs to [game state transfer](../../game-systems-design/references/game-state-transfer.md).

This contract connects design decisions to concrete operations and their
evidence boundaries.
Its technical components follow the [Godot Input contract](https://docs.godotengine.org/en/stable/classes/class_input.html),
[physics processing](https://docs.godotengine.org/en/stable/tutorials/scripting/idle_and_physics_processing.html),
and [JSON Schema 2020-12](https://json-schema.org/draft/2020-12).
Those specifications establish APIs and representation, not game quality.
