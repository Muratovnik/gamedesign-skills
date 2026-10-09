# Harbour of Echoes: original design studies

These four original, synthetic tabletop games let you play through a design
relationship, change one condition, and compare the consequences. Start with
the written rules and supplied initial state; use paper, tokens, and a tick
marker where a study calls for them. The fictional people and events are game
content. Recorded replays and calculations describe the declared rules, not
human play or measured game feel.

## Choose a study

| Study | Start here | What to compare |
| --- | --- | --- |
| Committed action in a spatial encounter | [Quay crossing](quay-crossing.md) | A shorter route restores a dodge after commitment; a narrower gap still blocks it. |
| Free expressive play | [Sound-and-light loom](free-form-loom.md) | Independent pitch and density controls replace a mapping where high pitch saturates density. |
| World, perspective, and investigation | [The third bell gamebook](gamebook.md) | Closing a shutter removes a witness route; a reserve tank changes work, traces, and dialogue. |
| Learning, permanent help, and an external objective | [Lens workshop](lens-workshop.md) and the practice drum in the gamebook | Comparing proportions replaces an answer-highlighted badge; the readout remains available. |

For a complete path, read a study's starting state and rules, play or trace the
given scenario, then compare the altered condition in that same page. The
[replay record](replay-notes.md) gives worked paths for the longer studies.
The machine-readable [case inputs](cases.json) and
[published calculation output](calculation-output.json) show the bounded
symbolic relationships used in the paper replays; the output is already
provided, so no generation step is needed to follow them.

The loom also has an optional audio and visual-timeline renderer. From the
repository root, with Python 3.11+, run it into a new directory under ignored
`tmp/`:

```bash
mkdir -p tmp/reader-runs
python3 examples/design-studies/harbour-of-echoes/render_loom.py \
  --output-dir tmp/reader-runs/loom-run-1
```

The chosen output directory must not exist; use another unused name for another
render. The result contains `phrase-a.wav`, `phrase-b.wav`, two visual-timeline
CSVs, and `receipt.json`. The receipt reopens the WAVs and checks format,
duration, sample count, nonzero signal, and the declared silence sections. The
CSVs expose each beat's control positions. These checks establish the generated
files follow this score's declared mapping; they do not establish how the
rendition sounds to a person.
In PowerShell, use `py -3` (or your Python executable) in place of `python3` and
the equivalent backslash path.

## Connect the study to the executable examples

- **Lantern Quay:** the [native Godot episode](../../godot-episode/README.md)
  sends scheduled input through an actual controller and collision shapes.
  Quay Crossing is a separate paper model of cue, legal command, route, and
  combined threat timing; its result does not stand in for the native run.
- **Lantern Crew:** the [analysis lab](../../analysis-lab/README.md) migrates a
  digital save and makes actor-specific views for content selection. The third
  bell is authored as a paper gamebook; the two examples have different game
  identities and no shared implicit save format.

## Method owners

The studies draw on [actions and time](../../../skills/gameplay-design/references/actions-and-time.md),
[entities](../../../skills/gameplay-design/references/entities.md), and
[space and situations](../../../skills/gameplay-design/references/space-and-situations.md)
for action and expressive-play relationships;
[inference](../../../skills/game-information-design/references/inference.md)
and [learning and help](../../../skills/game-information-design/references/learning-and-help.md)
for reasoning and teaching; and [world relations](../../../skills/game-world-narrative-design/references/world-relations.md)
and [conditional story](../../../skills/game-world-narrative-design/references/conditional-story.md)
for the encountered world and persistent consequences. Each method reference
includes its source basis and transfer limits.
