# Author replay record

All inputs and fictional events are original and synthetic. Arithmetic/set
outputs are produced by [calculate.py](calculate.py) from [cases.json](cases.json).
The story paths below are author walkthroughs of the written rules, not runs of
a narrative interpreter and not sessions with participants.

## Reproduce the calculation

With Python 3 available, from the package root run:

```sh
python3 examples/design-studies/harbour-of-echoes/calculate.py
```

The command writes `calculation-output.json` beside the script and prints the
counts and main outcomes. It uses only the Python standard library. It reads
these selected case inputs and has no access to a real game, a human learner or
a model-evaluation service. The output records its input and script identity.
Those identify the calculation inputs, not every sentence of the gamebook.
The executed set contained 9 crossing cases, 6 evidence sets, 9 loom parameter
pairs, 4 proportion rounds and 3 reserve requests. An empty family stops the
calculator; an inspected evidence case with zero observations is explicitly
reported as `no-evidence`.

## Response in the declared paper model

| Case | Observed calculation |
| --- | --- |
| Original 12 m route, press/control at 27 | Arrival 31; hit at 30 |
| Altered 9 m route, press/control at 27 | Arrival 30; safe through 32 |
| Control delayed to 28 | Arrival 31; hit at 30 |
| Gap width 0.9 m, required width 1.0 m | Unreachable; hit at Start |
| Cue first available at 29 | Arrival 32; hit at 30 |
| Press queued at 25 | Starts 27, arrives 30; safe through 32 |
| Press 24 followed by hold | Discarded before buffer; hit at Start |
| Upper Walk | Arrival 32; already hit during transit at 30 |
| No command | Hit at Start |

Both viable crossings preserve the two-stamina commitment and lack of cancel.
First clear recovery tick is 33; after three clear ticks the next threat can
begin at 36. These results establish only the collision/order abstractions
declared by the paper rules. The [native Godot episode](../../godot-episode/README.md) has its own
execution record.

## Form, range and return

At high pitch (`u=2`), the prototype mapping produces four pulses for every
`v`. The altered mapping produces 1, 2 and 4. All nine pairs were calculated.
The two public phrases each contain 12 beats. In Phrase A, the final two beats
sound the starting configuration; in Phrase B they preserve silence and the
dense high configuration. These are distinct written transformations with
equal total duration.

The optional audio route was then actually executed from the package root:

```sh
python3 examples/design-studies/harbour-of-echoes/render_loom.py --output-dir ../verification/loom
```

It writes separate WAVs, timed circle/dot CSVs and a receipt in a new directory.
Its input is [loom-score.json](loom-score.json),
the machine-readable version of the two published phrases. The concrete sine,
pulse-duty and envelope choices are described in
[the score's rendering section](free-form-loom.md#optional-rendered-material).
The script reopened both WAVs as mono PCM16 at 24 kHz and inspected the samples:

| Material | Reopened frames/samples | Duration | Nonzero samples | Declared rests observed as zero |
| --- | --- | --- | --- | --- |
| Phrase A | 288,000 | 12 s | 191,957 | Seconds 9–10; sound returns at 10 |
| Phrase B | 288,000 | 12 s | 143,948 | Seconds 9–12 |

Both files are 576,044 bytes and have a peak absolute sample value of 8,192.
Every declared sounding section contains nonzero samples. Each CSV has 12 beat
rows and preserves the retained control positions during the written rests.
The receipt records the generated materials and rendering choices. The
generated audio can be reopened as data. It supplies no listening, musical preference, perceived
visual relation, live-control, device-playback or latency evidence. The CSVs
remain visual-state data, and a phrase does not become a better composition
because its WAV passes these checks.

## World, evidence and story paths

### Altered combined version, independent evidence route

The author walked this path against [the gamebook](gamebook.md):

1. At Quay, tick 3: return the docket early. Its owner becomes the clerk while
   `docket_returned=true` persists. Test the practice drum; retain its legend.
2. Travel to Terrace, tick 4: receive T. Mix two batches locally, leaving reserve
   zero and two dyed cloths. A third batch is unavailable before repair. The
   world clock stays at 4 during these local scene actions.
3. Travel to Pump, tick 5: receive P. Under the public three-cause roster, T
   excludes Oren and P excludes automatic opening. Their intersection is Mira.
   The calculator reports that exact unique set. Tower was never required.
4. Return to Quay, tick 6: repair occurs. The prior return still enables filing
   despite the docket no longer being in the participant's inventory. The clerk
   describes the repair as complete and stored water as earlier work history.
5. File without assigning a cause: one receipt is created and the petition
   closes. The council learns the reported event without acquiring an operator
   identity from this act. The public board has no named cause.
6. Mira reads that board: her later dialogue concerns the repair; it cannot
   thank the participant for withholding her name without another channel.

This path uses the altered material and knowledge policies in one episode. It
does not require that the participant visit the unavailable witness route.

### Original version, direct witness route and merged consequence

At tick 3 return the docket, travel Quay → Tower at 4, obtain V, return at 5 and
name Mira. The current rule accepts the early sufficient answer without P or T.
At the ending's tick 6, the water returns and the board retains the accusation
and its author. Mira's reading of that public board is an explicit channel for
responding to the public act. A shared repair ending has not erased this effect.

### Removed channel and unsupported shortcut

In a shutter-closed version, the V card leaves all three causes possible. P alone
leaves Mira/Oren; T alone leaves Mira/automatic. The current calculator marks
each as underdetermined and zero evidence separately as no-evidence. Retaining
the original eyewitness line after closing the shutter would be an information
leak. Requiring every visited-card flag would be another defect: it would reject
the valid P+T route. Neither counterexample is present in the delivered rulebook.

### Interruption, clocks and one-time effects

Open the petition at tick 3 and interrupt before its critical line: no information
or filing flag changes. On return, deliver the critical line, then pause:
`reveal_delivered=true`, `petition_closed=false`, receipts zero. Resuming does not
advance the world. Commit a named or anonymous report: petition closed, receipts
one. Returning for another conversation does not file again. This is a manual
state walkthrough; the [technical actor-view consumer](../../analysis-lab/README.md#observer-specific-views)
does not execute these prose scenes.

### World without the investigation

Omit the mystery and petition, travel to Terrace, raise the rack and mix the two
stored batches before the repair. Revisiting exposes the raised rack, used tank
and produced cloth. Visit Refuge and deliver bedding; the returned description
includes it upstairs. Leave. These small authored state changes make a playable
world fragment without a required plot or autonomous simulation.

## Learning and the external objective

The calculated lower-fraction choices are Right, Left, Right, and Either/Equal.
The smaller-count shortcut fails both the introduction and new-application
numerical comparison, while it works in the same-size round. The original
highlighted introduction can nevertheless award success without comparison,
because its prompt supplies the selected answer. The altered new case removes
that selecting highlight and changes the correct side; it keeps the definition
and spoken readout.

This supplies a task/decision/feedback relation and a concrete misconception
contrast. It does not prove that all successful strategies use proportions,
that someone learned them, or that they transfer outside the exercise. No
participants were recruited or simulated to create that missing evidence.

## Limits of this record

The source package supplies formal paper outcomes, actual small calculations
and usable authored material. Native collision, controller feel, audible
composition, perceived clue clarity, cultural interpretation, learner outcomes
and comparative skill benefit are separate claims. The relevant native example
or actual human material must support them. This record is not an independent
review or a paid/behavioral model run.
