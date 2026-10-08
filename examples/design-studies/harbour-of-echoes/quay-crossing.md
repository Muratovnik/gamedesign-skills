# Quay crossing

An original deterministic paper encounter for one participant and one facilitator,
or a solo rule replay. Use three position cards, a tick marker, two stamina tokens,
a hazard schedule and one movement-command token. The aim is to reach Alcove
without a hit by the end of tick 32. There are no dice and no requirement to make
a physically fast response while reading the paper rules.

## Starting state and complete rules

At tick 22 the participant is at Start, finishing a winch action begun at 18.
That action cost two of four stamina at 18 and cannot be cancelled. Its useful
effect occurs at 24 and control returns at 27. Stamina does not regenerate
during this encounter. The crane schedule was not announced before the winch
commitment; at 22 a visible stripe first reveals the sweep's area and time.

At each integer tick, do these operations in order: update action availability;
accept a new permitted command; finish any arriving movement; resolve hazards.
An action of duration three started at 27 arrives at 30. The participant may
choose `move Alcove`, `move Upper Walk` or `wait`. Once moving, the route is fixed
until arrival. There are no jumps, immunity, attacks or other positions in this
small model. While in transit, the participant remains exposed to the Start
sweep. Once arrived, use the destination's exposure.

A movement press at 25 or 26 can be queued and starts at 27; the latest one
replaces the earlier one. Presses before 25 are discarded. A held button is not
a repeated press. A new press at or after 27 starts immediately if not already
moving. Wait chooses no movement. If no command is supplied, remain at Start.

The character is 0.8 m wide and requires 0.1 m clearance on both sides. Both
routes are 1.2 m wide in the ordinary versions. Travel speed is exactly 3 m per
model tick, with travel rounded up to complete ticks. These are tabletop metric
rules, not measurements from an engine or a person.

| Route | Original v1 | Altered v2 | Exposure on arrival |
| --- | --- | --- | --- |
| Start → Alcove | 12 m, four ticks | 9 m, three ticks after relocating the entrance | Safe from both hazards |
| Start → Upper Walk | 15 m, five ticks | Unchanged | Crane sweep and deck wash |

At tick 30 the crane hits Start and Upper Walk, including a participant still
travelling. Deck wash occupies Upper Walk from tick 28 through tick 32 inclusive.
The first hit ends that attempt. Surviving through 32 at Alcove succeeds; staying
alive elsewhere would not satisfy this version's goal. Reset restores tick 22,
Start, two remaining stamina and no queued movement. An external pause freezes
everything and resumes from the displayed tick without consuming game time.

## Play and compare

Show the hazard schedule at 22. The participant chooses commands while the
facilitator advances one tick at a time. Announce accepted, buffered or rejected
input and record the arrival/hit. At the end, compare v1 and v2 with the same
command: move to Alcove at 27. In v1, arrival at 31 is too late; in v2, arrival
at 30 occurs before the sweep. The altered geometry restores an answer while
the noncancellable action, stamina cost and warning are preserved.

V1 is a counterexample to a promised reactive escape from this particular
starting state. It does not establish that every unavoidable loss is bad: a
different version may show the whole hazard schedule before the player chooses
the winch at 18, making the commitment an informed risk. Preserve that legitimate
alternative instead of automatically adding cancellation.

## Additional discriminating states

| Variant, using v2 unless stated | Result under the complete rules |
| --- | --- |
| Return of control delayed to 28 | Alcove arrival 31; hit at 30 |
| Alcove passage narrowed to 0.9 m | Below the required 1.0 m; command rejected as unreachable |
| First available cue delayed to 29, no prior schedule information | Earliest cue-based move arrives 32; hit at 30 |
| Queued Alcove press at 25 | Starts at 27, arrives 30; succeeds |
| Press at 24 then hold, with no fresh command | Press discarded, no repeating edge; hit at Start |
| Move Upper Walk at 27 | Still in transit at 30; hit |

Recovery for the encounter begins at tick 33, after deck wash ends. Three clear
ticks are 33, 34 and 35; another threat may first begin at 36. Calling tick 30
“rest” would not remove the active wash.

See [actions and time](../../../skills/gameplay-design/references/actions-and-time.md)
and [space and situations](../../../skills/gameplay-design/references/space-and-situations.md)
for the construction. The [native Godot episode](../../godot-episode/README.md) has
its own actual input, movement, collision and persistence evidence; this paper
replay only establishes the declared model's outcomes.
