# Collect and interpret an observation of this episode

No people or physical materials were observed while constructing this example.
The shipped CSV and manifest are synthetic format demonstrations, not a
historical participant result. Use this route when a consumer supplies relevant
real recordings or arranges its own observation. The importer does not contact
participants, invent consent, or authenticate a source.

## Define the relation before collecting

Name the exact game/build, task, current state and question. For the gate episode,
one possible question is whether a first-time participant notices the quay cue
and can express a chosen dodge after commitment. That asks for a participant,
their real input device, a visible or otherwise accessible cue, and a recording
that covers input through resolution. A table of engine events alone cannot
answer it. A question about physical reach needs the actual geometry and material.

Specify whether persistent assistance is part of the intended path. Record its
presence and what work it performs. `persistent-aid` is not a defect label and
`none` is not automatically the preferred condition. Do not treat facilitator
instruction as independent discovery, or declined participation as a failed action.

Choose a recording method able to distinguish the needed order. Retain the
engine's world and run clocks separately, the capture clock, an identifiable
common anchor, dropped intervals and synchronization uncertainty. To inspect a
supplied audio/video file's timestamps, a consumer with FFprobe may run this
from the recording's directory, replacing the placeholder with its actual path:

```bash
ffprobe -v error -show_streams -show_frames -of json supplied-recording.mp4
```

This capture-dependent operation has not been run here because no recording was
supplied. Packet/frame timestamps do not measure end-to-end input latency without
a corresponding input observation. Source:
[FFprobe documentation](https://ffmpeg.org/ffprobe.html).

## Record the actual evidence

The CSV column order is part of this small import interface:

| Column | Meaning |
| --- | --- |
| `participant_id` | Consumer-assigned pseudonymous identity; do not infer population membership from it |
| `object_id`, `build_id`, `task_id` | Exact episode/object, revision and attempted task |
| `attempted` | `yes`, `no`, or `unknown` based on what was actually recorded |
| `completed` | `yes`, `no`, or `unknown`; a completion requires an observed attempt |
| `elapsed_s` | Finite non-negative seconds, blank if not measured |
| `assistance` | `none`, `facilitator`, `persistent-aid`, or `unknown` |
| `report` | What the participant or relevant observer said; distinguish it from observed action in interpretation |
| `missing_reason` | Required for unknown outcomes; retain interruption or missing capture as such |
| `recording_ref` | Inspectable recording/material reference; required for non-synthetic imports |

Copy the manifest structure and fill `record_kind` with `human-observation` or
`expert-material` only for an actual supplied source of that kind. Record the
collection method, available relation, conditions, precise question and known
limits. An expert interpretation of a scene differs from a novice performing it;
neither implies the other. The consuming project owns access, permissions and
retention of its recordings and personal information.

## Interpret after import

The importer needs Python 3.11+ and `jsonschema==4.26.0`. Follow the analysis
lab's [prerequisite setup](README.md#prerequisites-and-output-handling), then
run from the Game Design repository root with a new report path below ignored
`tmp/`. For example, in Bash:

```bash
mkdir -p tmp/reader-runs
RUN=$(mktemp -d tmp/reader-runs/observations-XXXXXX)
PYTHON=.venv/bin/python
"$PYTHON" skills/game-design/scripts/observe_evidence.py \
  --csv examples/analysis-lab/fixtures/observations.csv \
  --manifest examples/analysis-lab/fixtures/observation-manifest.json \
  --output "$RUN/observations.json"
```

On Windows PowerShell, create a unique directory and invoke the same operation
with the environment's Windows interpreter:

```powershell
$null = New-Item -ItemType Directory -Force tmp\reader-runs
$run = Join-Path (Resolve-Path tmp\reader-runs) ("observations-" + [guid]::NewGuid().ToString("N"))
New-Item -ItemType Directory $run | Out-Null
& .\.venv\Scripts\python.exe skills/game-design/scripts/observe_evidence.py --csv examples/analysis-lab/fixtures/observations.csv --manifest examples/analysis-lab/fixtures/observation-manifest.json --output (Join-Path $run observations.json)
```

The CSV and manifest above are synthetic examples. Their recognizable result
is `synthetic_format_demonstration` with `human_claim` set to
`not_established`.

For a supplied CSV and manifest, use the same three flags with their actual
paths and a fresh output filename. The importer validates metadata with JSON
Schema, parses CSV with Python's standard parser, rejects empty sets, preserves
unknown outcomes, and excludes declined attempts from completed-attempt counts.
It always leaves `human_claim` unresolved: format, filenames, and a provenance
label cannot establish authenticity or suitability.

Inspect the cited source and at least the material interval needed for the claim.
Separate action, self-report, expert interpretation and permission. Ask whether
the necessary cue, action, task and material were available; whether assistance
changed the task; whether the capture precision resolves the proposed explanation;
and which cases are absent. A missing cue, misunderstood rule and blocked body
call for different changes. When the source cannot distinguish them, preserve
the uncertainty instead of choosing the most convenient diagnosis.

Record a design revision tied to that distinction: a geometry change, timing
change, alternate signal, permanent aid, different participation path or a
revised promise. An observation can motivate such a local choice without claiming
an audience-wide causal effect. Learning transfer requires the corresponding
later task; a successful trained episode alone does not supply it.
