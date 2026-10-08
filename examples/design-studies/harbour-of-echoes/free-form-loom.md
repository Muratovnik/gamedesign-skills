# Sound-and-light loom

An original free-form tabletop score for one player and a facilitator, or for
one person moving controls and performing the output. There is no win, fail
score or required final state. Use two counters labelled `u` and `v`, each with
positions 0, 1 and 2, a circle on paper and a steady comfortable beat. A voice
or tapping supplies sound; exact pitch reproduction is optional for a paper
exploration of the mapping, and required only for judging that pitch composition.

## Controls and output

| Control | Position 0 | Position 1 | Position 2 |
| --- | --- | --- | --- |
| `u`: height | Hum C4; circle radius 1 unit | Hum E4; radius 2 | Hum G4; radius 3 |
| `v`: density | One sustained tone across the beat; one dot | Two equal pulses; two dots | Four equal pulses; four dots |

At each beat boundary the player may change either or both controls, hold,
rest, resume sound or return both controls to zero. Sound and picture use the
same current control positions. A rest silences the output but leaves the circle,
dots and controls visible. Holding rest does not reset anything. On a pause the
beat and controls freeze; resume starts a new complete beat with the retained
positions. The player may stop at any boundary and record the two positions to
return to the found configuration later.

This discrete version is deliberately easy to perform on paper. A continuous
adaptation would need its own interpolation and actual input/output timing;
those properties are not implied by these nine states.

## Two playable phrases of equal duration

Perform each row for its full indicated span, keeping a constant beat length
through the comparison. If one beat is chosen as one second, each phrase lasts
12 seconds; no particular tempo is a quality standard.

| Beats | Phrase A: rise and return | Phrase B: alternation and suspension |
| --- | --- | --- |
| 1–3 | `u=0,v=0` | `u=2,v=2` |
| 4–6 | `u=1,v=1` | `u=0,v=0` |
| 7–9 | `u=2,v=2` | `u=2,v=2` again |
| 10 | Rest, keep `2,2` | Rest, keep `2,2` |
| 11–12 | Sound on, return to `0,0` | Continue rest, retain `2,2` |

After the scored pass, repeat with free choice of controls. Try holding a sparse
high sound, returning to a dense low sound, or preserving a silence for several
beats. These are available actions rather than goals to maximize. The two scores
alter development, repetition and return while holding total duration constant.
Whether one is more convincing as music depends on its actual performance and
the intended work.

## Original mapping defect and altered mapping

The prototype computed pulse count as `min(4, 2**u * 2**v)`. At `u=2`, all three
positions of `v` make four pulses. That suppresses the promised independent
density control. The altered rule uses `2**v` for pulses, leaving pitch to `u`.
It offers one, two or four pulses at every pitch.

Keeping the coupling is a legitimate alternative if discovering saturation
becomes the intent. Rename and compose that relation honestly. The choice does
not need faster input, fewer pauses or a victory test. The published
[calculation output](calculation-output.json) checks the nine parameter pairs;
it is not a sound recording or a report of human perception.

## Optional rendered material

[loom-score.json](loom-score.json) records the same two phrases and every
`u/v/sound` state in the table. [render_loom.py](render_loom.py) consumes that
data using Python's standard library. From the package root, choose a new output
directory and run:

```sh
python3 examples/design-studies/harbour-of-echoes/render_loom.py --output-dir ../verification/loom
```

The renderer creates `phrase-a.wav`, `phrase-b.wav`, two visual-timeline CSVs
and `receipt.json`. An existing output directory is rejected before any writing.
Use another new directory for another run. No playback or external dependency
is required to generate and reopen these files.

This realization chooses one-second beats, mono PCM16 at 24 kHz, sine tones
at C4/E4/G4 using an A4=440 Hz pitch formula, and a peak amplitude of one quarter
of the positive PCM16 range. At `v=0`, each held section sounds continuously;
at `v=1/2`, each of the two/four equal pulse slots sounds for its first half.
Each sounding interval has a 5 ms linear attack and release. Those timbre and
articulation choices make a concrete rendition of the altered independent
mapping; they do not prescribe how a player must perform the paper score.

The renderer reopens each completed WAV and checks format, duration, sample
count, nonzero signal and silence in the declared rest sections. The receipt
binds these observations to the score, renderer and output hashes. The CSVs
record beat times, circle radii and dot counts, retaining the visual controls
during rest; they are data for presentation, not a rendered animation. The
[replay record](replay-notes.md#form-range-and-return) describes both
12-second files. No listening, perception, live input or device latency outcome
is inferred from those file checks.

Method: [free audiovisual form](../../../skills/gameplay-design/references/actions-and-time.md#free-audiovisual-form).
Story or emotional claims depending on the phrase use
[dramatic function](../../../skills/game-world-narrative-design/references/conditional-story.md#compose-dramatic-function)
with the actual performance material.
