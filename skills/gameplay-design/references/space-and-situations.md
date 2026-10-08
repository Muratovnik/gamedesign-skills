# Space and combined situations

Use when traversal, placement, visibility, cover or simultaneous demands change
what a participant can do. Build a particular place and
episode; “two flanks and some cover” is not yet a usable layout.

## Construct the space relative to an action

Recover the current controller, body/cursor dimensions, acceleration, jump or
reach, allowed poses, camera and acquisition of abilities. Establish coordinates
and units, then connect the intended destinations. Add enough geometry to express
the relevant constraint: width, height, approach distance, slope, turning room
or material clearance. An edge in a connectivity graph may require an ability
the participant does not yet have.

Place the participant and opposing observer or effect source. Represent motion
blocking, observation blocking and effect blocking separately, including their
directions and any change after destruction. Determine which route or threat
can be perceived before choosing. A top-down designer view alone cannot resolve
a camera question. For physical play, include reach, grip, body position and
component dimensions in the consumer's actual material test.

### Worked blockout: two routes through a drying shed

Original synthetic plan, in metres. The participant starts at `(0,0)` and needs
to reach `(8,0)`. A solid vat occupies `x=3..5, y=-1..1`. The lower passage has
usable width 0.7 m; the upper passage has usable width 1.2 m. The character's
body is 0.8 m wide and its game collision requires 0.1 m clearance on each side.
Therefore the lower passage is not traversable in the declared model: required
width is 1.0 m. A topology drawing showing both paths overstates the choices.

The new layout moves the lower wall 0.5 m outwards, making the lower passage
1.2 m wide. A shooter at `(8,3)` can cover the upper exit. A transparent screen
at the lower exit blocks projectiles from that direction but leaves observation
open. The vat blocks sight, movement and projectiles. A smoke vent at the upper
exit blocks sight only. These properties allow different decisions: the lower
route protects the crossing but reveals location; the upper conceals departure
without stopping a predicted shot.

The artifact to hand over is this scaled placement with those three material
properties and the controller clearance, plus the affected camera view. If the
camera hides the lower opening until after commitment, widen or move the reveal,
change the entry position, or choose intentional prior route learning. Geometry
alone establishes none of these perceptual outcomes.

**Counterexample and alternative.** Reusing a maximum jump distance for a gap
without the necessary run-up creates another false edge. A one-way drop, exposed
crossing, deliberate detour or disorientation can be appropriate; do not make
every direction equally safe or optimize away a pause the place is meant to hold.

## Compose the demands of the encounter

Give each role a concrete demand on the participant and a response it is meant
to invite. Use [entities](entities.md) for execution and knowledge, and
[actions and time](actions-and-time.md) for command and signal relationships.
Then combine demands on one initial state, placement and clock. Count remaining
responses under the combination, not the sum of enemy health or damage.

Construct how the situation begins, develops and ends. Specify what may appear
while earlier effects remain, what opens a recovery interval, how the participant
can leave and what persists on repeat. If selection varies, define the preserved
intent and constraints for the actual selector in
[repertoire](../../game-content-design/references/repertoire.md). A phase called
“rest” can still contain active hazards; decide which of those are allowed.

### Worked encounter: the crane and the deck wash

Use three abstract positions: Start, Alcove and Upper Walk. Travel from
Start to Alcove takes three ticks in the revised layout, and four in the original;
travel to Upper Walk takes five. Movement ends before hazard resolution on its
arrival tick. There are no other positions, attacks, jumps or damage immunities
in this small model; movement stays exposed to Start's sweep until arrival.
At tick 22, the visible crane stripe marks Start and Upper
Walk for a sweep at tick 30. Deck wash begins at tick 28 and affects Upper Walk
through tick 32. Alcove stays safe. The participant's existing noncancellable
action returns control at tick 27.

| State and action | Original layout | Revised layout |
| --- | --- | --- |
| Tick 27: choose Alcove immediately | Arrive 31, after the sweep; hit at 30 | Arrive 30 before the sweep; safe |
| Tick 27: choose Upper Walk | Arrive 32 into deck wash; also exposed at the sweep | Same unsuccessful answer |
| Remain at Start | Hit at 30 | Hit at 30 |
| Start the “rest” timer at tick 30 | Wash still active until after 32 | Wash still active until after 32 |

This revision restores one answer without erasing commitment. To create a
recovery interval, the encounter ends the crane effect at 30, ends deck wash
after 32, and begins three clear ticks of recovery at 33. In this model a new
threat can first begin at 36. The rule is “three ticks after the declared active
hazards end,” not simply “three ticks after the phase label changes.” A different
design may keep a low background threat during a lull; name that intended demand.

The small state space above supports a hand trace. It does not establish engine
collision, a physical controller's path, human recognition of the stripe or
whether the lull feels right. A loss of all responses can also be the intended
consequence of an earlier informed choice; trace that choice before diagnosing
the encounter as contradictory.

## Revise by the relationship that failed

If individual threats work but their combination fails, change schedule,
placement, composition, prior warning or available response. If the chosen role
cannot execute, fix its eligibility or the place. If a changed movement ability
alters clearance, revisit affected places rather than proving only one convenient
test room. Preserve the current scenario/version binding through the shared
[relations and context](../../game-design/references/relations-and-context.md).

## Basis and transfer boundary

[Devin Kelly-Sneed, Designing Raz's Jump, 2024](https://www.doublefine.com/news/devin-article-raz-jump)
describes phased movement, targeted jumps, camera-sensitive interaction and
different trajectory tools. [Epic, Multiplayer Map Theory for Gears of War](https://docs.unrealengine.com/udk/Three/GearsMultiplayerMapTheory.html)
connects geometry to that game's view, turning, lethality and cover. These are
primary production accounts; their dimensions and genre preferences do not set
standards for the synthetic shed.

[Michael Booth, Replayable Cooperative Game Design, 2009](https://cdn.fastly.steamstatic.com/apps/valve/2009/GDC2009_ReplayableCooperativeGameDesign_Left4Dead.pdf)
describes distinct enemy functions and placement constraints. His
[The AI Systems of Left 4 Dead, 2009](https://cdn.akamai.steamstatic.com/apps/valve/2009/ai_systems_of_l4d_mike_booth.pdf)
describes population and pacing phases. These related accounts are one project's
evidence, not independent experiments. The demand-combination and actual-hazard
construction above is a local transfer; its counters do not measure felt tension.
