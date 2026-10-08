# Access and return

Use this procedure when a participant cannot receive, choose, express, perform
or continue an intended action, or when a scene or absence changes how they
return. Identify the particular path and person; a difficulty setting or
general audience category does not identify the barrier.

## Contents

- [Locate the broken participation path](#locate-the-broken-participation-path)
- [Worked material: a private route choice](#worked-material-a-private-route-choice)
- [Construct interruption as a state transition](#construct-interruption-as-a-state-transition)
- [Worked scene: pause, skip and cancel](#worked-scene-pause-skip-and-cancel)
- [Build an actionable return](#build-an-actionable-return)
- [Source and evidence boundary](#source-and-evidence-boundary)

## Locate the broken participation path

Obtain the relevant instruction, signal, state, device or physical material,
table arrangement, available channels and the participant's stated needs.
Record the step at which the intended action becomes unavailable:

| Step | Construct an alternative when needed | Inspect its effect |
| --- | --- | --- |
| Receive information | Private audio, tactile mark, text, contrast, placement | Who else learns it and whether its timing changes |
| Compare and choose | Persistent view, agreed pacing or decision aid | Which reasoning or memory work is preserved or delegated |
| Express intention | Switch, speech, pointer, eye-gaze or partner signal | Whether the intention can be distinguished before execution |
| Execute | Reachable control, remapping, token assistant or shared control | Who chooses and who merely performs the chosen act |
| Learn the result | Accessible confirmation and changed-state display | Whether the player can correct a mistaken action |

Use [learning and help](../../game-information-design/references/learning-and-help.md)
when an aid changes inference, memory or learning. That procedure owns cognitive
help; this one owns its participation path. Use
[actor knowledge](../../gameplay-design/references/entities.md) when a new
channel affects hidden information.

Choose the relation to preserve or deliberately replace. Permanent help may be
the intended way to play. Shared control may be agreed. Lowering damage can
change punishment while leaving an unavailable warning completely unchanged.
Do not describe these changes as interchangeable ways to “make it easier.”

## Worked material: a private route choice

This is an original physical-game candidate, not a report about a tested
participant. The stated design case is: Dana wants to choose her own route,
needs the small print read privately, and cannot reach the center token rack.
She can express “one,” “two” or “stop” through her chosen available channel;
which channel works is to be established with Dana and the actual material.

Prepare the following player materials. Place the route card behind Dana's
screen and put two large, separated choice areas within her agreed reach.
If those areas are not usable, use the agreed speech or partner signal instead.

**Private route card, exact text to present:**

> One: North stairs. Arrive in three turns; keep your rope. The wind indicator
> says calm. Two: South ladder. Arrive in one turn; spend your rope. The ladder
> needs a repair after your crossing. You choose the route. You may stop before
> confirming.

**Public result card:**

> North chosen: move Dana's marker three spaces along North; rope remains.
> South chosen: move one space along South, return one rope token, and add a
> repair marker. Confirm the new position and remaining rope to Dana.

Use this execution rule: the assistant reads the private card only through
Dana's agreed private channel, without recommending a route. Dana indicates
one or two. The assistant repeats the selection through that channel; Dana
confirms or corrects it. Only after confirmation does the assistant move the
marker and announce the public result. The hidden wind information is not
announced unless Dana's own allowed communication reveals it.

Replay “two”: privately present both choices; Dana selects two; repeat “South
ladder, spend one rope”; Dana confirms; move the marker, remove one rope,
add repair, and confirm her state. If she corrects to one before confirmation,
no rope is spent. Stop before confirmation also leaves the state unchanged.
This is sufficient paper material to rehearse the channel and rule.

| Variation | What changes |
| --- | --- |
| Assistant reads privately and executes Dana's confirmed choice | Data and motor access change; Dana retains the choice |
| Assistant chooses the “best” route | Decision authority changes |
| Assistant reads the hidden card aloud to everyone | Information distribution changes |
| Dana explicitly requests shared choice with the assistant | A different, potentially legitimate participation form is established |

The candidate addresses access to a decision. It does not establish actual
legibility, hearing, reach, grip, reliable signaling or acceptable assistance
work. Rehearse with suitable materials and obtain the relevant participant's
observation before claiming those outcomes. A diagram or rendered screenshot
cannot supply body evidence.

## Construct interruption as a state transition

Choose a recognizable signal with an available channel. Specify who can
initiate it, when activity stops, which fictional events remain, what happens
to spent resources and clocks, and how the group agrees on the next action.
The person's reason need not be disclosed when the necessary limit and
continuation are already clear.

Separate three operations:

- **Pause:** halt further activity while retaining the committed state.
- **Skip depiction:** omit presentation while deciding which event and
  mechanical consequences remain.
- **Cancel or revise an event:** change the established event and its
  consequences, using an agreed checkpoint or explicit replacement.

Beau Jágr Sheldon's *Script Change* distinguishes analogous controls over
continued play and fictional content. It demonstrates a designed procedure,
not an assurance that every group can use a signal without pressure. [SC]
The concrete accounting below is an original extension for this example.

Use [conditional story](../../game-world-narrative-design/references/conditional-story.md)
for canon and downstream scene conditions, and
[game state transfer](../../game-systems-design/references/game-state-transfer.md)
for the resulting state transformation. A declared “skip” must not silently
become a rollback, and a declared cancellation must settle dependent costs.

## Worked scene: pause, skip and cancel

The synthetic lock scene begins at checkpoint C16: `fuel=3`, `gate=closed`,
`alarm=0`, `active_minutes_remaining=12`. Cy chooses “force lock.” Event E17
commits: spend 1 fuel and 2 active minutes; open gate; set alarm to 1. The
post-event state is `2, open, 1, 10`. An intense description is about to play.
The time package explicitly meters active game time and permits event
cancellation to restore charges; it is not a calendar expiry.

In this example any participant may signal “pause,” by speech or the agreed
text/card channel. Activity and active-time consumption stop immediately.
The facilitator offers the applicable operation and a minimal consequence
summary. No one must disclose a personal reason or agree to resume. The group
may choose a compatible continuation, a different role or an ending.

Reset to the post-event state for each branch:

| Operation | Fuel / paid active time | Canon and world | Concrete next action |
| --- | --- | --- | --- |
| Pause | 2 / 10 remain; neither decreases during pause | E17 remains; gate open; alarm 1 | On agreed resumption, choose enter or retreat |
| Skip description | 2 / 10 remain | E17 remains; accessible summary says gate open and alarm 1 | Choose enter or retreat without the omitted depiction |
| Cancel E17 | Restore 3 / 12 from C16 | E17 is revoked in history; gate closed; alarm 0 | Choose “ask for key,” taking 1 active minute and no fuel, or leave |

Cancellation keeps a revocation record rather than presenting E17 as both
completed and uncompleted. Any downstream trigger depending on E17 must use
the revised canon. Do not grant both the opened gate and refunded cost unless
that is the actual intended replacement. These rules do not require every
game's skip to have this accounting; they require a specified result.

Replay cancellation: signal; freeze; identify C16; mark E17 revoked; restore
the four fields; present “ask for key or leave”; choose ask; subtract one
active minute; show the keyholder's response defined by the next scene.
The resulting balance is 3 fuel and 11 active minutes. No lock-opening reward
or alarm event is active. The procedure reaches a next decision, not just a
named safety control.

For a wall-clock deadline the pause may not extend the entitlement. Route that
case to [paid and timed rights](paid-and-timed-rights.md), decide the promised
continuation explicitly, and show its real expiry before committing the episode.
Do not infer a monetary refund from this invented game's fuel refund.

## Build an actionable return

Obtain the returning participant's last known state, current role, relevant
world changes, outstanding commitments, newly available actions and what
decisions were assigned to others during absence. A complete history dump can
be less useful than the facts required for the current choice; preserve a
deliberate mystery through the knowledge owner.

For Lantern Crew, give returning Bo this current-state card:

> The generator is broken. The locker contains 4 scrap; repair costs 6. Ava is
> absent, so her pass cannot host archive entry. You retain the winch and one
> fuel. The earlier accepted election makes you treasurer. Cy chooses the
> survey route. You decide whether to spend your fuel and whether to authorize
> a crew repair. The public map is available now. You may decline this role.

Present the map as an observation, then let Bo choose accept, request a new
role or leave. On acceptance, replay Cy's route proposal and Bo's actual
expense decision. Do not give Bo Ava's private archive code or repeat the
already delivered archive message. A save can preserve Bo's unlock while
Bo still needs an explanation of its current use.

If Bo declines, apply the agreed authority procedure in
[shared play](shared-play.md#make-authority-and-dispute-executable) and choose
a route that does not depend on his fuel. If no permitted role or route remains,
name that limit and construct a revised episode or a conclusion. Returning
an avatar does not restore a decision irrevocably assigned to someone else.

## Source and evidence boundary

[SC] Beau Jágr Sheldon, *Script Change RPG Toolbox*, final version 2023,
“Pause,” “Fast-Forward,” “Rewind” and relevant mechanical-effect guidance.
[Author's primary resource](https://briebeau.com/thoughty/script-change/).
The resource's controls inform a distinction; the original cards, clock
accounting and state transitions here do not reproduce its toolkit.

Rules can establish an available signal and coherent aftermath. Runtime and
physical observations can establish particular channels and transitions.
Only relevant people can supply the missing evidence about their ability to
use the procedure and its social cost. Keep that distinction in the result.
