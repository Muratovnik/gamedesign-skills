# Actions, signals and playable time

Use the branch matching the material being made. Action commitment, a shared
clock and free audiovisual composition are independent design problems; the last
does not need a threat, a score or a winning condition.

## Action commitment

Construct an action from the opportunity it should create: an early risky
commitment, a recoverable probe, a sustained manipulation or a precise sequence.
Recover legal source states, competing commands, resource rules, movement and
targeting capabilities, effect ownership and time units. Place the moments of
input acceptance, target/direction lock, resource debit, contact and return of
control on the same timeline. Animation can show these moments but does not
define them by itself.

Write transitions at the moments where a different command could change the
outcome. Include the priority of competing inputs, edge versus held input,
buffer replacement and expiry. For each allowed interruption, carry forward
already spent resources, contact, spawned objects and state changes. Choose the
representation the consumer can use: a timing table may be sufficient; editing
an existing game also requires the actual data or code governing these moments.

### Worked action: the latch strike

Original synthetic rule, measured in simulation ticks, with four starting stamina.
One accepted strike costs two. Its age is zero on acceptance. At each tick update
its phase, process permitted commands, then apply contact. A strike has one
contact per target; holding the button does not repeat it.

| Age | Phase and rule | Input relationship |
| --- | --- | --- |
| 0–3 | Windup; direction fixed on acceptance; no contact | Dodge cancels, refunds two, then costs one; if both commands arrive in idle, dodge wins and strike is discarded |
| 4–5 | Active; strike contacts its declared arc | Dodge is unavailable; the debit and any hit remain |
| 6–11 | Recovery; no new contact | No cancellation; a strike press at age 10 or 11 replaces the one-entry buffer |
| 12 | Ready | Execute the buffered strike if affordable; otherwise discard it; buffer expires after this tick |

Before the active phase, cancellation can be a feint. With four stamina, strike
at tick 0 and dodge at tick 3 leaves three stamina and no strike contact. In the
other trace, a dodge at tick 4 is rejected: the strike costs two and contacts if
its target is in the arc. A press at age 9 is discarded; at age 10 it can start
the next strike at age 12. A miss still costs two. This makes the rule usable
without assuming that a cancelled image reverses game effects.

**Counterexample and alternative.** Refunding at age 4 after contact creates
free damage under this contract. Repair the refund/cancellation boundary or
deliberately author that capability and account for its consequences. A
noncancellable version that commits at age 0 is equally legitimate when advance
commitment is the purpose; it needs no emergency cancel merely to satisfy this
method.

## Signal and available response

Work backward from the outcome. Identify the latest command that still changes
it, including command acceptance, execution duration, collision order and the
participant's current state. Then locate the earliest **distinguishing** cue in
the participant's actual view. A startup animation hidden behind the camera does
not provide that cue. Record which cue conveys direction, area, timing or type;
compare the depicted area with the effect area in the relevant pose and view.

Construct the response together with [space and situations](space-and-situations.md):
place a reachable destination, preserve the required corridor and identify
other active threats. Change the relation that fails. A blocked route needs a
route or different demand; extra sound alone cannot create one.

**Worked boundary.** A crane sweep resolves at tick 30. Movement resolves before
the sweep on that tick. Reaching the safe alcove takes four ticks, so tick 26 is
the latest useful command. The stripe appears at tick 22, but the participant's
prior noncancellable action returns control at tick 27. The nominal eight-tick
warning contains no available reactive answer. Moving the alcove entrance so
the trip takes three ticks makes a command at 27 sufficient. This is a geometry
revision with the commitment preserved. It establishes an answer in the stated
model; real visibility and movement still need the target representation.

A sweep may intentionally demand prediction. In that case place and identify
the earlier basis for choosing a safe position. Unavoidable damage after a
clearly signalled prior commitment is a legitimate consequence, not automatically
a defect. Do not assign a universal human reaction threshold to these tick values.

## Shared clock

Choose a time base and phase for every related action, signal and update. Place
the input window, buffer and moment of resolution on it. State the resolution
order when outcomes depend on events that appear simultaneous. Input tolerance
and time to read a newly displayed state are separate design choices.

**Worked four-beat rule.** Commands for beat `k` are accepted during
`(k - 0.25, k]`; the latest valid command replaces the earlier one. At `k`, expire
old effects, move the player, then resolve an enemy strike whose target was
locked on the previous beat. A player moving from A to B escapes a strike at A.
Reversing strike and movement causes a hit despite the same apparent beat.
Show the locked target before asking for that movement. No command means wait.

For this example, pause freezes the phase and queued command. Resume first shows
the pending command and gives one full beat of count-in during which it may be
replaced; that count-in does not advance the world. The remaining phase then
continues. This is a specified return, not a general requirement for count-ins.
If pause, device latency or synchronization is material, align captured input
and actual output clocks through the consumer's
[environment contract](../../game-design/references/environment-contracts.md).
These local rules do not supply a network rollback policy.

## Free audiovisual form

Start from what the participant can do to the material: stretch, layer, sustain,
interrupt, repeat, dissolve or return to a found configuration. Choose the
gesture-to-parameter mapping, ranges, interacting channels and state memory.
Compose actual transformations and transitions; adjectives such as “expressive”
or “calm” do not specify them. Decide whether repeatability, discontinuity or
irreversibility belongs to this particular form.

**Worked paper-and-voice loom.** Two controls have positions 0, 1 and 2. Moving
`u` chooses C4, E4 or G4 and a circle radius of 1, 2 or 3 units. Moving `v`
chooses one, two or four equal pulses within each beat and the same number of
dots on the circle. A facilitator may hum/tap and draw the result, or the
consumer may implement these mappings. A rest silences the output while keeping
the drawn circle and both control positions. There is no winning state.

| Beats | Phrase A | Phrase B, same eight-beat duration |
| --- | --- | --- |
| 1–2 | `u=0,v=0` | `u=2,v=2` |
| 3–4 | `u=1,v=1` | `u=0,v=0` |
| 5–6 | `u=2,v=2` | Repeat `u=2,v=2` |
| 7 | Rest; keep current positions | Rest; keep current positions |
| 8 | Return to `u=0,v=0` | Hold rest, retaining the dense state for later return |

A develops density and height, then returns. B alternates them and leaves a
suspended state. Their overall duration is identical; the compositional
difference is in the available transformations, repetition and ending. The
participant can hold a state, change either control, rest, resume or return to
the starting configuration at any time. A pause freezes the beat without
resetting the controls; resume may begin a new complete beat because this form
does not test timing accuracy.

**Counterexample and alternative.** If pulse count is implemented as
`min(4, 2**u * 2**v)`, all three values of `v` produce four pulses at `u=2`.
That defeats the stated independent density control. Change it to `2**v`, or
explicitly compose saturation as a discovered coupling. Unpredictability,
resistance, long holds and irreversible transformations remain available
choices. The paper score specifies a controllable composition; it is not a
recording or evidence that anybody heard or enjoyed it.

## Basis and transfer boundary

- [Rivals 2, Setting up an Attack](https://rivals2.com/workshop/knowledge-base/character-creation/setting-up-an-attack/), historical beta documentation, and [Maddy Thorson, Celeste & Forgiveness](https://www.maddymakesgames.com/articles/celeste_and_forgiveness/index.html) supply examples of distinct action windows and forms of tolerance. Their implementations do not establish ideal timings for another game.
- [Riot, Clarity in League, 2021](https://www.leagueoflegends.com/en-us/news/dev/clarity-in-league/) supplies the specific policy of matching presentation to competitive action, including a misleading area cue. The response-deadline construction above is a local transfer, not a measured universal clarity law.
- [Ryan Clark, Finding the beat in Crypt of the NecroDancer, 2014](https://www.gamedeveloper.com/audio/game-design-deep-dive-finding-the-beat-in-i-crypt-of-the-necrodancer-i-) describes choices about input tolerance and action order. [Fernando Ramallo and David Kanaga, Controlling space and sound in Panoramical, 2015](https://www.gamedeveloper.com/audio/game-design-deep-dive-controlling-space-and-sound-in-i-panoramical-i-) supplies a creator account of playable audiovisual dimensions. The beat rule, loom and phrases here are original synthetic constructions; neither account proves their artistic effect.
