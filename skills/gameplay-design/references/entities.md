# Actors: information, position and executable roles

Use for detection, searching, testimony, dialogue perspectives, task assignment
or behavior constrained by shared places and capabilities. This file is the
canonical owner of actor knowledge and role execution.

## Actor knowledge

Begin with a consequential decision or line. Determine what information would
justify it and how this actor could acquire that information. Separate the world
fact, the actor's available report or observation, its belief, and what it chooses
to express. A false statement can be a mistaken belief, an intentional lie or a
data error; those require different construction.

For each relevant proposition, create acquisition and revision rules. Decide
whether it comes from sight, sound, testimony, memory, prediction or an expressly
omniscient role. Set when the actor updates it, how conflicting reports are
resolved, how it becomes stale, and when it stops guiding behavior. Do this for
the information used by the decision; a complete psychology or belief database
is unnecessary. An object reference is not permission to read that object's
hidden current coordinates.

Use a compact knowledge record when timing or transmission matters:

| Data | Why it can change the behavior |
| --- | --- |
| Proposition and permitted precision | A sound can identify a location without identifying its maker |
| Source event and channel | Establishes how the actor gained access |
| Observation time and receipt time | Distinguishes old news arriving late from a fresh event |
| Belief/status and conflict rule | Distinguishes adopted, disputed, superseded and predicted information |
| Use/expiry rule | Determines when to search, ask, qualify a claim or stop acting on it |
| Motive and expressed version, for testimony | Explains deliberate omissions or lies without changing the underlying belief |

A squad may share records instantly, receive delayed reports, need an audible
call, or know only its members' independent observations. Choose this policy
before writing coordinated responses. Removing a channel must affect dependent
behavior and dialogue; it need not change world truth.

### Worked actor: the quay watchkeeper

Original synthetic example. At tick 5, Vale sees Mira at West Gate. At tick 6,
Vale loses sight behind the wall. The world moves Mira to Garden at tick 7, with
no available signal. At tick 8, a runner delivers an observation of Mira at Pump
from tick 2. Vale prioritizes the later event time of direct sight over this
older report. Its state remains “last seen West Gate at 5,” not “Mira is at West
Gate.” It approaches that last location, searches adjacent visible exits, and
after four search ticks returns to its post unless a new stimulus arrives.

| Situation | Allowed behavior or line | Remaining uncertainty |
| --- | --- | --- |
| No new evidence after loss of sight | Search West Gate; “I last saw Mira there before the bell.” | Current location |
| Noise from Pump, source unidentified | Inspect Pump as a new lead; “Something struck the wheel.” | Whether the sound was Mira |
| Fresh direct sight at Garden | Update location and begin the allowed pursuit | Routes hidden after the next loss of sight |
| No sight because the shutter was closed in the altered version | “The shutter hid the wheel; I heard the bell.” | Who operated it |

At the end of an investigation, Vale may learn the operator's identity from the
player's report. Mark that channel and its uncertain status; it does not become
eyewitness knowledge. If Vale deliberately protects Mira, write a motivated
line such as “I will describe the damage, but I will not give you her name,”
withholding an already known identity. That differs from inventing a witness
account to patch an otherwise impossible scene.

**Counterexample and alternative.** Change only Mira's hidden movement. If Vale
now turns toward Garden without a permitted prediction or signal, the behavior
uses unavailable information. A lucky prediction can be correct without a leak;
compare a case with the same observations and a different hidden destination.
An explicitly omniscient spirit, an intentionally unreliable witness or short
stylized memory can be appropriate. Their information policy should agree with
the fiction and actual behavior.

## Make the role executable

Describe what the actor contributes to the episode: displace, hold attention,
protect a passage, carry a load, observe a ritual or refuse assistance. List the
actions, targets and places it can actually use. Filter candidates for reachable
path, occupancy, orientation, capacity, resources and applicable knowledge;
then rank eligible candidates by the role's preferences. A high score cannot
make an unreachable place usable.

Define how a chosen role starts, continues, fails and relinquishes its place or
resource. Assign authority for competing claims, and decide what happens when a
path closes, the target disappears, the actor leaves or survival conflicts with
the instruction. Name the recovery behavior. “Try again” without a changed
condition can create a permanent useless loop. Waiting, retreating or acting
inefficiently for a social purpose can be the intended role.

### Worked role: two porters, one narrow bridge

The player needs a shelter door carried across a bridge. Porters Ada and Len can
each carry one end together on the wide path, or ferry separate smaller panels
across the narrow bridge. The intact door is too wide for the bridge. A single
porter may reserve the bridge for one crossing; earliest request wins, with
stable actor identifier breaking simultaneous ties. Reservations end on arrival,
failure or departure and expire if no progress occurs for two turns.

At turn 0 both request the narrow route with the intact door. The width filter
rejects it before distance scoring. They choose the wide path. At turn 1 that
path floods. They release its task assignment, set the door down at the near
bank and offer the player two actions: wait for the tide, or spend one work turn
separating the panels. After separation Ada reserves the bridge; Len waits with
his panel. Ada's arrival releases the bridge and Len can cross next turn. If Ada
leaves, her reservation ends and the group reassigns her panel before continuing.

The resulting artifact specifies a cooperative obstacle and a recovery decision,
not just an AI architecture. If the design instead values a procession with an
intact door, keep the wait and remove dismantling; the longer route is then the
point. Two actors repeatedly selecting the blocked shortest path would be a
defect under either version.

## Follow the consequences

[Space and situations](space-and-situations.md) owns the usable place and combined
demands. [Inference](../../game-information-design/references/inference.md) owns
what the participant may conclude from testimony. [World relations](../../game-world-narrative-design/references/world-relations.md)
owns the institution or ecology making the role meaningful, and
[conditional story](../../game-world-narrative-design/references/conditional-story.md)
owns which scenes become available after new knowledge or action. Actor records
crossing a campaign or save boundary use [game state transfer](../../game-systems-design/references/game-state-transfer.md).

## Basis and transfer boundary

[Epic's AI Perception documentation for UE 4.27](https://dev.epicgames.com/documentation/en-us/unreal-engine/ai-perception?application_version=4.27)
provides a historical representation of stimuli, their age and remembered versus
current perception. [Jeff Orkin, Three States and a Plan: The A.I. of F.E.A.R.,
2006, pp. 8–16](https://www.gamedevs.org/uploads/three-states-plan-ai-of-fear.pdf)
describes replanning, reserved positions and separate squad coordination; its
visible flanking did not require a dedicated complex flanking planner. These
are implementation accounts, not evidence that a particular architecture is
best or that observed behavior reveals its internal cause.

[Ryan, Summerville, Mateas and Wardrip-Fruin, Toward Characters Who Observe,
Tell, Misremember, and Lie, 2015](https://jamesryan.computer/papers/2015_ryan_toward_characters_who_observe_tell_misremember_and_lie.pdf)
provides a separate world/character representation in a developing prototype.
It does not supply a complete theory of human belief or mature motivated lying.
The knowledge procedure, watchkeeper and porters above are local constructions
transferred from these distinctions, not reproductions of those games.
