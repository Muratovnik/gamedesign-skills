# Repertoire construction

Use this procedure for an authored catalog, generated content, improvised
selection or a mixture. The useful unit is a playable difference in context,
including the cases where repeating the same relation is intended.

## Contents

- [Define the repertoire's job](#define-the-repertoires-job)
- [Worked set: harbor crossings](#worked-set-harbor-crossings)
- [Follow selection into play](#follow-selection-into-play)
- [Generate dependent facts together](#generate-dependent-facts-together)
- [Worked generation: the parcel at the quay](#worked-generation-the-parcel-at-the-quay)
- [Revise the stage that lost the relation](#revise-the-stage-that-lost-the-relation)
- [Source anchors](#source-anchors)

## Define the repertoire's job

Obtain concrete members, their purpose, prerequisite states, combination
rules, frequency, ordering, presentation and the cost of repetition. For a
generator also obtain its representation, constraints, selection inputs,
manual overrides and how to reproduce an output. Use native IDs and state
fields; a catalog exported without its selection rules is incomplete evidence
for the encountered set.

Select differences that change this game's work. Useful axes might be route
commitment, evidence available, reversible versus lasting cost, coordination,
timing, application of an unlock or a return to a changed place. A new name,
biome or statistic can matter, but explain its actual effect before counting
it as another decision family.

Build at least the members needed for the opened task. A broad redesign may
need contrasting relations; a precise repair may need one changed member and
its existing neighbors. Do not impose a quota of types or an obligation to
maximize variety. Remove a cosmetic duplicate only if its repeated form has
no intended function here.

## Worked set: harbor crossings

These original cards share a paper rule: deliver one parcel from the near
bank to the far bank. Start each independent card with one fuel, one rope,
an intact parcel and no outstanding debt. Advance turns only when an action
says so. The intact parcel awards 2 marks; a damaged parcel awards 1. A
participant may stop before committing an action and receive no mark.

| ID / card | Complete action rule | Meaningful relation |
| --- | --- | --- |
| A / Ferry | Spend 1 fuel to cross in 1 turn, or carry the parcel along the ridge in 3 turns for no fuel. Deliver intact. | Present resource versus time |
| B / Painted ferry | Spend 1 fuel to cross in 1 turn, or use the blue ridge in 3 turns for no fuel. Deliver intact. | Same rule as A; appearance alone adds no new relation |
| C / Tide steps | Tide starts high. Cross now in 1 turn and damage the parcel, or wait 1 turn for low tide then cross in 1 turn intact. | Read a changing condition and choose speed versus damage |
| D / Keeper's bargain | Accept a recorded obligation to make one future delivery for the keeper and cross intact in 1 turn, or refuse and take the 3-turn ridge without debt. The future keeper delivery takes 2 turns and earns no marks. | Present advantage versus a future obligation |
| E / Shared hoist | Requires Bo's winch. Cy proposes a lift; Bo independently approves 1 personal fuel. If approved, cross intact in 1 turn and spend it; otherwise Cy can take the 3-turn ridge without fuel. | Joint decision with a retained refusal |

The [ready-to-copy catalog](../assets/harbor-repertoire.json) contains these
rules and the selection schedules below. Reading E's implementation of a
refusal requires [shared play](../../game-participation-design/references/shared-play.md).
An actual timed action or visibility claim uses
[actions and time](../../gameplay-design/references/actions-and-time.md).

Remove the names: A and B still coincide in available actions, cost, duration
and resulting state. C changes a state-dependent timing decision, D leaves
an obligation after the current card, and E distributes authority. These are
model-level distinctions; they do not establish how different the encounters
feel to people.

Develop the set: keep A; remove B from this selection; keep C/D/E. Repeat A
once before C so the group can reuse an established fuel-versus-time choice.
That repetition is intentional familiarization. A subsequent play observation
could show whether the repeat helps or whether its cost outweighs its purpose.
The method does not require disguising A as a new room to justify its return.

Replay the authored outputs: on A choose ridge, spend 3 turns, retain fuel,
receive 2 marks. On C wait then cross, spend 2 turns, receive 2. On D take
the bargain, spend 1 turn, receive 2 and retain the keeper obligation; later
perform its 2-turn delivery for no marks. On E let Bo decline; Cy chooses
ridge, retains Bo's fuel and receives 2 after 3 turns. These are complete
paper episodes, not a list of future content ideas.

## Follow selection into play

Keep possible, generated, valid, eligible, selected, presented and entered
sets distinguishable where those stages exist. A human curator may combine
several stages; preserve the decision rather than requiring separate software
components. “Presented” in a record does not mean a person noticed it.

For the example, Bo's winch is available and all five cards are eligible.
An initial selector assigns A and B score 3, C and D score 2 and E score 0;
it always chooses the highest score, breaking ties alphabetically, with no
history adjustment. Its five-episode result is A/A/A/A/A. E is valid and
eligible yet never selected. Adding hundreds of E variants with score 0
does not change that result.

Replace this policy with the authored sequence A/A/C/D/E, keeping the deliberate
repeat and scheduling the missing relations. Select each next card only after
the previous episode finishes. If E is ineligible because Bo lacks the winch,
present the explicitly selected fallback A and record that reason; the result
must no longer claim that this sequence included coordination.

| Synthetic selection record | Selected | Inspected outputs | Consequence |
| --- | ---: | ---: | --- |
| A/A/A/A/A, complete cards available | 5 | 5 | Only resource/time relation appears in the inspected selection |
| A/A/C/D/E, all five displayed | 5 | 5 | Four specified relations, with a purposeful repeat |
| A/A/C/D/E, E selected but its view failed | 5 | 4 | Selector includes coordination; presentation of it remains unverified |
| No recorded episodes | 0 | 0 | No evidence about an encountered set |

For the third row, do not repair the generator: inspect the failed view. For
the last row, do not report zero defects as a clean sample. If no encounter
is supposed to follow an agreed finale, an empty result may be the correct
game state; it still supplies no evidence about the quality of encountered
content. If logs omit a class, distinguish true nonselection from missing data.

Reproduce the authored schedule using Python 3's existing JSON parser, from
this skill directory:

```python
import json
from pathlib import Path

data = json.loads(Path("assets/harbor-repertoire.json").read_text())
cards = {card["id"]: card for card in data["cards"]}
for name, sequence in data["schedules"].items():
    kinds = sorted({cards[card_id]["relation"] for card_id in sequence})
    print(name, len(sequence), kinds)
```

The original schedule prints 5 selections with `resource_time`; the revised
one prints 5 with `coordination`, `future_obligation`, `resource_time` and
`timing_state`. These labels are authored explanations of inspected rules,
not an automatic measure of experiential variety.

## Generate dependent facts together

Choose a representation that retains the relation the player can encounter.
Bind together event participants, dates, routes, evidence, actor knowledge and
scene predicates. Generate from a shared event, solve constraints jointly,
or construct a world backward from an intended clue; then materialize all
dependent outputs. A syntax-valid JSON record can still contain a witness
who was absent at the claimed time.

For space-dependent tasks, keep logical prerequisites and physical routes
separate enough to check their interaction. Dormans's level-generation paper
distinguishes mission dependencies from geometry and describes preventing
new connections from short-circuiting a mission. This is a useful relation
to transfer, not a universal prohibition on shortcuts. [D10]

Preserve reproduction data appropriate to the operation: source state,
generator/grammar revision, seed or enumerated choices, accepted exclusions
and a concrete output. A curated final choice can be sufficient for an
authored episode; claiming a distribution needs the eligible population and
selection mechanism too.

## Worked generation: the parcel at the quay

This original finite generator has four worlds: choose `day` from `{4, 5}`
and `courier` from `{Nia, Oren}`. The goal is to retrieve a parcel at the quay
and identify who delivered it. The following rules define all dependent data:

1. At 18:00 on the chosen day, the chosen courier delivers the parcel at Quay.
   The other courier is at Hill at 18:00. Travel between Hill and Quay takes
   one hour, and this episode supplies no teleport or alternate traversal.
2. Mira is at Quay from 17:40 through 18:10 that day. She observes the courier
   and can tell the player the witnessed delivery. Chen leaves Quay at 17:30;
   he knows the office schedule and cannot claim to have seen that delivery.
3. Derive the physical receipt from that same event: date, 18:00, courier name,
   Quay and parcel ID `Q-day-courier`. Never randomize its date independently.
4. Put the receipt in the public office; its accessible copy gives the same
   game information. Mira's player-facing line uses only her observation.
   Chen's line is “I left at 17:30. I did not see the delivery.”
5. The player may read the receipt, ask either witness, collect the office
   key and enter Quay. The locked gate requires the key. “Retrieve parcel”
   at Quay finishes retrieval; an early spoken guess alone does not do so.

Actor knowledge and how observations authorize dialogue use
[entities](../../gameplay-design/references/entities.md). Building the full
deductive challenge uses [inference](../../game-information-design/references/inference.md);
this small example demonstrates generation consistency and presentation.

Two concrete generated outputs are:

| Output | World event and locations | Receipt text | Mira's line |
| --- | --- | --- | --- |
| `Q-4-Nia` | Day 4, Nia at Quay 18:00; Oren at Hill 18:00 | “Day 4, 18:00. Nia delivered parcel Q-4-Nia at Quay.” | “On day 4 at 18:00 I saw Nia leave that parcel at Quay.” |
| `Q-5-Oren` | Day 5, Oren at Quay 18:00; Nia at Hill 18:00 | “Day 5, 18:00. Oren delivered parcel Q-5-Oren at Quay.” | “On day 5 at 18:00 I saw Oren leave that parcel at Quay.” |

All four outputs are in the
[finite world data](../assets/parcel-worlds.json). Replay `Q-4-Nia`: read its
receipt at Office; take key; ask Mira; open gate; enter Quay; perform retrieve.
The final state includes that parcel and identified courier Nia. Chen's
line remains limited to his own absence. Reset and replay `Q-5-Oren`: the
route remains valid, but the receipt, witness statement and identification
all change together.

Vary the coupled rule and inspect the resulting action:

| Change | Consequence | Legitimate neighboring choice |
| --- | --- | --- |
| Randomize receipt day to 3 without changing event | Receipt no longer supports the assigned delivery | An intentional forged receipt with a discoverable contradiction may be valid |
| Give Chen the delivery line from world truth | The absent actor reports an unsupported observation | A recorded message from Mira could give Chen attributed secondhand knowledge |
| Add Office-to-Quay bridge bypassing the lock | Retrieval is reachable without the key | Accept the bridge if multiple entry routes are intended; update the key's purpose |
| End on a partial spoken guess from Office | Required retrieval can be skipped in the actual interaction | Allow remote identification if retrieval is no longer the objective |

The authority for deciding these cases is the desired game relationship.
Do not tune a formal solver to demand the planned answer when the actual
interaction permits another complete, accepted plan.

## Revise the stage that lost the relation

When a member is invalid, revise its representation or dependent production
rule. When valid members never appear, change selection or eligibility. When
selection succeeds but presentation fails, fix the delivery path. When people
encounter the set but find its distinctions unhelpful, revisit the chosen
differences, order and cost of repetition using their actual evidence.

Reinspect a related combination affected by the change: a new movement can
bypass a lock, a transferred right can alter selection, and a changed language
can erase a clue. Read the canonical subject procedure instead of duplicating
its whole method here. Keep rejected, missing, uninspected and deliberately
excluded outputs separate. A sample can refute a universal constraint; a
successful sample cannot prove every possible output is valid.

## Source anchors

[D10] Joris Dormans, *Adventures in level design: generating missions and
spaces for action adventure games*, PCGames 2010, §2 “Missions and Spaces”
and §6 “Generating Space from Mission,” DOI 10.1145/1814256.1814257.
[Primary paper](https://pcgworkshop.com/archive/dormans2010adventures.pdf).

The paper supports the distinction and a concrete generation implementation.
The cards, selection records and parcel generator above are original local
constructions; they do not establish human enjoyment or a superior production
method.
