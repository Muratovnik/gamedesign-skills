# The third bell

An original paper investigation and world vignette for one participant and one
facilitator. A solo reader can replay the rules with the truth visible, but that
does not reproduce discovering the mystery. Use a position token, a world-tick
marker, a blank docket, a notebook and the cards below. No random rolls are used.

The participant investigates a diverted water supply and decides what to place
on public record. The question of cause has a fixed answer. The choice about
reporting it has no designated morally correct option.

## Participant rules and initial state

Start at Quay just after bell 3, at world tick 3. Hold the blank docket. The
petition is open, no report is filed, and the practice drum's legend is available.
Choose an original or altered version before play:

| Version | Tower's shutter during bell 3 | Terrace water reserve |
| --- | --- | --- |
| `v1` | Open | None |
| `v2-shutter` | Closed | None |
| `v2-reservoir` | Open | Two batches |
| `v2-combined` | Closed | Two batches |

The true historical opening does not change between versions. Each version
changes an actual knowledge channel or material relationship, with the cards
and reactions below changing accordingly.

The pump can feed Terrace or Refuge. A damaged tide gate currently prevents
feeding both. Since bell 3 the pump feeds Refuge, where pressure holds a flood
door closed. Terrace's regular intake is dry. Repair is scheduled to restore
both supplies at world tick 6. These are invented rules, not real engineering.

The opening at bell 3 had exactly one cause: Mira manually turned the wheel,
Oren manually turned it, or an automatic pulse. Only Mira and Oren could have
operated it manually. The roster is complete for this bounded puzzle; hidden
operators, impersonation and unlisted routes are excluded. The participant may
choose one of those three hypotheses at any time. Merely selecting a tentative
hypothesis gives no correctness feedback.

| Footpath | Travel cost |
| --- | --- |
| Quay ↔ Pump | One world tick |
| Pump ↔ Terrace | One world tick |
| Terrace ↔ Quay | One world tick |
| Quay ↔ Tower | One world tick |
| Pump ↔ Refuge | One world tick |

On arrival the facilitator describes the place. Inspecting, talking, testing
the practice drum, local helping actions and writing notes use no world ticks.
Travel and an explicit wait each advance one. These ticks represent selected
scene transitions, not elapsed physical minutes. On first reaching tick 6, apply
the repair before describing the next place: both supplies now flow. Historical
records remain inspectable. A pause freezes position, time and pending choices;
return resumes the displayed state.

Available actions are travel on a listed footpath, inspect a local feature,
perform its listed action, ask its present speaker, wait, consult help, file at
Quay or end participation. There is no unlisted lockpicking, teleportation or
combat. All listed inspections succeed. The participant can end at any time;
an unfinished report remains unfiled.

## Encounter cards

The facilitator reads only material the participant encounters. Keep the
answer key at the end separate during play.

### Quay: the practice and public record

Read: “A public board lists Mira and Oren as the two manual operators. Beside an
unfinished petition is a small practice wheel. The real pump is down the path.”

The participant can test the practice wheel. Turning it places a labelled
`manual` stroke on its drum. Pressing its demonstration motor places a different
labelled `automatic` stroke. The legend remains in the notebook. This practice
does not affect the historical pump record. A participant who knows the notation
can skip it and inspect the real drum directly.

The participant can hand over the docket now or later. Doing so sets
`docket_returned=true` and `docket_owner=clerk`. Filing later depends on the past
return, so an early return does not remove eligibility. The clerk is present,
knows the repair schedule and receives only testimony actually submitted to her.
She does not know the operator's identity merely from the author's answer key.

### Pump: evidence P

Read: “The two labelled pipes run toward Terrace and Refuge. The drum preserves
the stroke made at bell 3. It is the same manual mark as on the practice legend.”

Give card P: **The bypass opened manually at bell 3.** The drum's classification
is reliable under the rules. The participant may follow either pipe, inspect its
label or compare the record with the legend. The emergency wheel has been
secured pending the scheduled repair; turning it now is not an available action
in this investigation.

After repair the pipe positions change, but the drum's historical stroke does
not. The facilitator must not replace past evidence with a current-state label.

### Terrace: evidence T and work

The rack starts lowered (`rack_raised=false`). Read: “The sole bridge out of the
harbour has a gate register. Cloth waits on a lowered rack beside the dye bowls.”
When `rack_raised=true`, use “Cloth waits on the raised rack beside the dye bowls”
for the second sentence, including on later visits.

Give card T: **Oren crossed outward at bell 2. The sole bridge remained shut
until bell 4, so he could not be at the pump at bell 3.** The gate record is
complete and reliable for that interval. No other crossing exists in this
puzzle. Reading it after reopening still establishes the earlier restriction.

Before repair, use the chosen material state:

- With no reserve: the bowls are dry; the worker says, “The wheel turned and
  our mixing stopped.” Mixing is unavailable.
- With a reserve: the intake is dry but two wet marks show stored water in a
  tank. The worker says, “We have two batches stored. That buys time, not a new
  supply.” Each `mix batch` consumes one reserve unit and produces one dyed cloth.
  After two batches, mixing is unavailable until repair.

After repair, fresh water supplies mixing. The worker describes the earlier
cost: “We had no stored water” or “The tank bought us time,” as appropriate.
Used reserve units remain used; the repair does not rewrite work history.
The participant can raise the cloth rack in every version, setting
`rack_raised=true`. Raising it again leaves the state and description unchanged.

### Tower: evidence V or a limited account

Vale is present. The tower overlooks the pump wheel only when its shutter is
open. In v1 and v2-reservoir, give V: **Vale directly saw Mira turn the wheel at
bell 3.** The witness is reliable in these versions. Vale says, “I saw Mira's
hand on the wheel when the third bell sounded.”

In v2-shutter and v2-combined, read instead: “The shutter was closed. I heard the
third bell, but the wheel was hidden.” Vale supplies no operator identity. Do
not let later author knowledge turn that line into eyewitness testimony. If the
participant tells Vale a theory, record it as received testimony, not sight.

### Refuge: the material benefit

Read: “A taut brace holds the flood door. Households have laid sleeping mats above
the high-water line. A basket of bedding waits at the foot of the stairs.”

The participant can inspect the brace, read the household labels or carry the
bedding upstairs, setting `bedding_delivered=true`. Before repair, the caretaker
knows the diversion is keeping the door secure, but did not see the operator.
After repair, the new gate makes the temporary pressure arrangement unnecessary.
These details give reasons to discuss the diversion without giving a hidden
answer through a supposedly decorative speaker.

## Help that remains available

The notebook contains verbatim copies of encountered cards, their sources and
the practice legend, plus any personal notes. A facilitator may read it aloud
whenever requested. This permanent channel delegates recall and presentation.
It does not automatically add unvisited cards or connect their facts.

The participant may request either of these explicit changes in help:

- **Relationship hint:** “Compare the time of the manual stroke with the period
  when Oren could not reach the pump.” This supplies the central comparison;
  it is stronger than a search reminder.
- **Full solution:** “Mira operated it. P excludes an automatic pulse, and T
  excludes Oren.” This delegates the deduction. The participant still chooses
  what to report; the session is no longer evidence of independent deduction.

In the original shutter-open versions, Vale's testimony offers another route
to the answer. No particular number of visited cards is required.

## File, interrupt and return

At Quay, after the docket has been returned and while the petition remains open,
the facilitator presents the petition. Before the critical first line, the
participant may interrupt or leave. Do not set a delivered-information flag just
for opening the scene.

Read the first line and set `reveal_delivered=true` only after it is delivered:

> The repair has already been arranged. Your statement decides what enters the
> public record; it does not decide whether the refuge is repaired.

At tick 6 or later replace the first sentence with “The repair is complete.”
Then provide the relevant material cost: no stored supply, two stored batches,
or the resulting earlier work history. On returning after the first line,
acknowledge what was delivered and offer the remaining choice. No filing effect
occurs until an option is committed.

| Choice | Exact response and state change |
| --- | --- |
| Name Mira or Oren | “I will record your accusation and your name as its source. The person you name may answer.” Set `record_mode=named`, `claim` to that name; clerk gains the submitted testimony. |
| Attribute it to an automatic pulse | “I will record that account of the mechanism, under your name.” Set `record_mode=named`, `claim=automatic`; no person is accused. |
| Describe the diversion without assigning its cause | “The event and the repair are public. An accusation is not.” Set `record_mode=anonymous`, `claim=none`; clerk receives no operator identity from this act. |
| Decline to file | “Then the page stays blank.” Set `record_mode=unfiled`, `claim=none`. |

Every committed option sets `petition_closed=true`. Named and anonymous reports
produce one receipt; refusal produces none. A later visit discusses the existing
record and never creates another filing receipt. The participant can commit a
correct answer early or with alternative grounds. No “read every clue” gate is
used. Committed wrong claims remain wrong testimony and do not rewrite history.
There is no sequence of cost-free yes/no probes before commitment.

## Ending and visible consequences

After committing, choose to stay for the return of the water or leave. Advance
the authored aftermath to tick 6 if necessary. In every branch, read:

> The repaired gate holds. Water runs through both pipes again.

The public board then carries a different result:

- Named report: the board records the specific claim and the participant who
  submitted it, with space for a reply.
- Anonymous report: the board records the diversion, damage and shared repairs
  without a named cause.
- Unfiled: a blank docket space remains beside the repair notice.

Mira returns at tick 6 and reads the public board. She can then know a public
claim and its author. If the participant stayed, she responds to a named claim:
“You put that account in front of everyone. I will answer it in my own name.”
If no cause is named, she comments on the repair only. She does not thank the
participant for withholding her name without a channel establishing who did so.
A participant who left does not hear this line merely because it exists in the
facilitator's state.

The session ends after this material or the participant's departure. For a
world-only session, omit the mystery question and petition: visit places, perform
local acts and leave, preserving raised-rack/bedding/batch changes. This mode
is a usable non-simulated world vignette with no required plot.

## Facilitator answer key and author interpretation

Historical truth in every listed version: Mira manually diverted the supply at
bell 3 to protect Refuge. Oren was outside the harbour. The automatic system
did not cause the opening. Mira's act explains the facts; it does not choose the
participant's position on public responsibility.

After play, the facilitator may reveal this key for checking the puzzle. P and
T eliminate the automatic and Oren alternatives. V directly supports Mira only
in the shutter-open versions. A correct committed answer does not prove which
reasoning produced it. No human session was conducted to create the published
[author replay record](replay-notes.md).
