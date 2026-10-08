# Conditional story and dramatic consequence

Use for a scene, dialogue, quest, interruption, reveal, refusal or joined branch.
Conditions make a scene possible; composition makes its action and response
useful to the work. These are related but distinct tasks.

## Construct conditions and time

Recover the actual fragment and the states that can reach it. Separate a past
event, present ownership, actor knowledge, eligibility, selection, execution
progress and effects only where their combinations matter. For each needed
scene, write its entry condition, any priority against competing scenes, what
it presents, which actions it accepts, and when its effects commit. Specify
one-time events and the consequences of interruption before and after them.

Choose meaningful clocks: world time, player inputs, visits or real elapsed time
are not interchangeable. State which operations advance a deadline and what
pause or returning to a scene preserves. A simple stage number is sufficient
when all relevant states really are mutually exclusive; independent flags are
useful when returning an object, learning a fact and witnessing a reveal can
happen in different orders.

### Worked state: the petition at the quay

Original synthetic fragment. A tide repair is scheduled to complete at world
tick 6. Travel along one footpath and an explicit wait each advance the world
one tick. Inspecting a card, choosing dialogue and pausing do not. The council
accepts a petition before or after the repair; its acknowledgement changes with
the tide, so the deadline does not make the whole story inaccessible.

| State | Meaning and use |
| --- | --- |
| `docket_returned` | Past event: the blank docket was handed to the clerk; enables filing |
| `docket_owner` | Present object holder; may already be the clerk when the scene opens |
| `petition_closed` | A decision committed; prevents duplicate filing |
| `record_mode` | `unset`, `named`, `anonymous` or `unfiled`; carries the chosen public record into later material |
| `claim` | The submitted operator, if named; may be disputed rather than true |
| `reveal_delivered` | The participant actually received the scene's critical line; entering the scene does not set it |
| Actor records | [Entities](../../gameplay-design/references/entities.md#actor-knowledge) owns what each speaker knows and from which channel |

The petition is eligible when `docket_returned` and not `petition_closed`, while
at Quay. Returning the docket early is valid; the condition must not require
still carrying it. When both petition and repair acknowledgement are eligible,
present the acknowledgement first, then the petition. It changes no claim and
does not consume the petition's one-time state.

## Compose dramatic function

Write the preparation, action, response and consequence. Identify what the
participant is being invited to want and what the available action can actually
affect. Effects can live in local reaction, a future opportunity, world state,
knowledge, a relationship or expressed position; a different ending is not
required for every meaningful act.

For the harbour, the scene places responsibility for a diversion beside its
material cost. Before offering choices, the clerk says:

> The repair has already been arranged. You can decide what becomes public record.
> A name here is your accusation, not somebody else's confession.

At tick 6 or later use “The repair is complete” for the first sentence.
If Terrace was not visited, add the appropriate available context: before repair,
in the original version, “The dyers lost their working water”; with the new tank,
describe the reserve batches actually remaining. After repair, describe the
earlier lost work or use of the tank. This supplies
the relevant cost without assuming an optional earlier scene occurred.

At the point the clerk delivers the statement about the arranged or completed repair, set
`reveal_delivered=true`. An interruption before it leaves the flag false. An
interruption afterward preserves that delivered information but commits no
petition. On return, repeat the missing introduction if false; otherwise use
“You know the repair's status. What shall I record?”

| Participant action | Written response | Committed effect |
| --- | --- | --- |
| “Name Mira as the operator.” | “I will write that you name Mira. She will be allowed to answer.” | `record_mode=named`, `claim=Mira`; council receives this testimony, not automatic proof |
| “Describe the diversion without naming a person.” | “Then the damage and the work are public. An accusation is not.” | `record_mode=anonymous`; council learns the reported event but no operator identity from this act |
| “I will not file a statement.” | “The page stays blank.” | `record_mode=unfiled`; refusal is carried forward |

Each choice sets `petition_closed=true`. The first two produce one filing
receipt; refusal produces none. Subsequent visits permit discussion of the
record, not another receipt. A wrong named operator remains a disputed accusation
and does not silently rewrite world history. The claim-confirmation policy is
owned by [inference](../../game-information-design/references/inference.md).

### Carry the consequence through the merge

At tick 6 or later, the water returns in all three branches. Read:

> The repaired gate holds. Water moves through both pipes again.

Then select the record's visible carrier:

- `named`: the board names the participant's accusation and reserves space for
  the named person's response. Once Mira reads it, she can address that public
  act: “You made me answer in front of everyone.”
- `anonymous`: the board records damage and shared repair duties without an
  operator. Mira cannot thank the participant for withholding her name unless
  she learns who filed the account through another permitted channel.
- `unfiled`: the board records the repair with no participant testimony. A blank
  space remains where the docket would have been posted.

The common repair does not erase the difference in public accusation and
knowledge. It would be a false promise to label these options “save the refuge”
and “destroy the refuge” when all only change the record. Changing the wording
to the effect actually offered is one valid revision; changing the consequences
to honor a larger promise is another.

## Replay the states that change the scene

For this fragment, hand over at least the actual variant for an early-returned
docket, interruption before the reveal, interruption after it, a named report,
and a merged scene where Mira has not read the board. The important observations
are whether filing is still available, which introduction plays, whether a
receipt duplicates and whether a speaker has the information her line uses.
Do not infer those from a diagram's branch count.

**Counterexample and legitimate alternative.** A loader that sets
`reveal_delivered` merely because the scene was entered can make a later line
assume unheard information. Commit at the actual delivery point or write a
return that supplies it. A scene may deliberately continue while the participant
leaves, and a conversation may consume world time; those are valid policies if
their effects and the participant's later access are specified. NPC refusal,
linear structure and shared endings remain available dramatic choices.

Save, rollback or campaign changes use the canonical
[game state transfer](../../game-systems-design/references/game-state-transfer.md)
policy; inspect the resulting combination here for its story consequence.
For pause, skip or cancellation involving real participants, coordinate with
[access and return](../../game-participation-design/references/access-and-return.md).
For presentation whose effect depends on sound or duration, use the relevant
[actions and time](../../gameplay-design/references/actions-and-time.md) branch.

## Basis and transfer boundary

[inkle, Writing with ink, revision ff697147c10b](https://github.com/inkle/ink/blob/ff697147c10bf72a5d1339a1406d88f1dc59ab56/Documentation/WritingWithInk.md)
documents conditions, gathers, state and turn counters; those counters are not
automatically fictional-world clocks. [Emily Short, Storylets: You Want Them!,
2019](https://emshort.blog/2019/11/29/storylets-you-want-them/)
describes content, conditions and effects across different story structures.
These supply representational alternatives, not a requirement to adopt ink or
storylets for this procedure.

[Mateas and Stern, Structuring Content in the Façade Interactive Drama
Architecture, 2005, pp. 3–5](https://expressiveintelligence.github.io/papers/MateasSternAIIDE05.pdf)
describes interruption and coherence among dramatic units.
[Wardrip-Fruin and colleagues, Agency Reconsidered, 2009](https://dl.digra.org/index.php/dl/article/view/369)
provides a conceptual account relating desired and supported action. The
petition and its precise commit points are original transfers from these
distinctions. Their consistency does not establish a felt emotional outcome,
nor does a numeric dramatic-intensity label supply that evidence.
