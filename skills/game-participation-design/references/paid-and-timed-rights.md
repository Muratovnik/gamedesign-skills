# Paid and timed rights

Use this procedure for an offer, subscription, extra attempt, acceleration,
shared admission, expiry or schedule that changes a person's or group's game
plan. Work from actual current terms for a live product. Financial forecasting
and legal interpretation are separate tasks requiring their own evidence.

## Contents

- [Specify the acquired right](#specify-the-acquired-right)
- [Test the named shared plan](#test-the-named-shared-plan)
- [Worked offer: Lantern archive admission](#worked-offer-lantern-archive-admission)
- [Give each clock its own consequence](#give-each-clock-its-own-consequence)
- [Revise terms and promise together](#revise-terms-and-promise-together)
- [Source anchor](#source-anchor)

## Specify the acquired right

Read price and unit, entitlement holder, acquisition and activation, permitted
activity, capacity, expiry clock, transfer/delegation, absence, renewal,
cancellation, refund and already acquired stock. Separate a consumed item,
a right to choose later, a hosted group permission and personal ownership.
For a randomized purchase, use the distribution and presentation of its
terms; for a progression shortcut, use the unpaid route's actual conditions.

Construct a right by its effect, not by a label such as “premium”:

| Offer | Direct game change | Follow the dependency |
| --- | --- | --- |
| Content | Opens a place, encounter or story | Can a mixed-rights group play the promised common episode? |
| Capacity | Adds storage, characters or seats | Does another member rely on a holder to keep access? |
| New action | Changes a possible move or role | Which encounters or competitors are affected? |
| Acceleration | Shortens an existing acquisition route | Is the stated slower route still usable and meaningful? |
| Attempts or consumables | Adds opportunities that may be spent | What happens on failure, interruption or expiry? |
| Timed mode or hosted session | Admits an actor or group for a period | Which clock runs during pause and whose presence matters? |

These choices can be legitimate; their existence does not establish
acceptability, profitability or value. Explain who bears a consequence and
what alternative remains before judging it against the agreed project intent.

## Test the named shared plan

Choose an affected pair or group with different rights. Walk the actual
activity before purchase, after purchase, on refusal, after a missed scheduled
opportunity, after expiry and after the holder leaves when applicable. Check
who can invite, transmit a resource, see the clue, select the mission, perform
the required action and retain its result.

Historical ArenaNet rules for free Guild Wars 2 accounts distinguished entry
from communication, trading and guild-storage permissions. That primary
description is useful for this separation; it is not current account advice
or evidence that a free-to-play model is best. [GW]

A login path is insufficient evidence for “you can complete this campaign
together for free.” If a paid pass is necessary for its only restoration
mission, test that mission. Do not evaluate an unrelated free activity instead.

## Worked offer: Lantern archive admission

All prices and dates here are invented design data. No purchase or account
change is performed. The example offer reads:

> Archive pass: 6 demonstration credits. Holder: Ava. Activates immediately;
> expires on 15 October 2026 at 20:00 UTC. Ava may host Bo and Cy in an archive
> episode while she participates. A delegation must name a host and expiry
> before it takes effect. Leaving without such delegation suspends guest
> admission. Earned survey records remain. There is no automatic renewal.
> The demonstration refund rule returns all 6 credits if admission fails
> before the first episode starts; voluntary departure after starting does
> not refund the used pass.

The offer must be visible before commitment together with its affected shared
task. It specifies this game's terms; it does not claim legal adequacy.
Cancellation of a later fictional scene does not retroactively mean the
commercial episode never started.

At `2026-10-08T18:00:00Z`, Ava's pass is valid but Ava is absent and no
delegation exists. Bo has the winch; Cy has no paid right. The objective is to
repair the broken generator for 6 scrap, while the crew holds 4. Compare:

| Plan or event | Available to Bo and Cy? | Concrete consequence |
| --- | --- | --- |
| Enter archive using the absent host | No | The unexpired right exists, but its presence condition fails |
| Ava grants a permitted delegation to Bo before departure | Yes until the specified expiry | Bo can host the named episode within its capacity and time |
| Complete the free public survey | Yes under the revised rules | Earn 2 scrap, then choose whether to repair |
| Pass expires | No new archive admission | Previously earned records and personal winch remain |
| Decline the pass purchase | Public survey remains available | Archive content is unavailable; ordinary restoration still works |

This changes a concrete promise: free members can restore the harbor through
the public survey; the archive expedition is an optional paid route. If the
project instead promises free access to every archive scene, this construction
does not meet that promise. Change the entitlement or the authorized promise.

A nearby legitimate design makes the archive key crew-owned and transferable
with the elected office. Another gives each participant a permanent personal
copy. They have different departure and succession consequences even at the
same price. Use [game state transfer](../../game-systems-design/references/game-state-transfer.md)
for such changes; do not migrate the example's personal pass into a group
asset without an accepted policy.

## Give each clock its own consequence

Identify whether a duration measures wall time, simulated game time, active
session time, turn count or opportunities. State its origin, timezone where
needed, inclusive/exclusive end, pause behavior, and what survives expiry.
Capture source time for a live operation rather than pretending a supplied
test timestamp is the current clock.

For the example archive pass, admission is allowed only when `now < expiry`.
An archive episode takes 20 active minutes. Starting at 19:50 on expiry day
cannot finish by 20:00 under a rule that ejects everybody at expiry. Choose
and disclose one of these concrete policies:

| Policy | Start at 19:50 | At 20:00 | Cost or change |
| --- | --- | --- | --- |
| Finish required before expiry | Refuse this 20-minute episode; offer a shorter available activity | No interrupted episode | The final start time is earlier than entitlement expiry |
| Admission before expiry locks one episode | Admit and record its session right | Existing session may finish; no new entry | Access extends only for the admitted episode |
| Fixed ejection | Admit with explicit remaining time if partial play is the intended product | Stop and preserve the specified checkpoint | The product does not promise completion of this episode |

The second policy is the selected candidate here: a session admitted before
expiry gets up to 20 active minutes and ends no later than 30 wall minutes
after admission. A pause stops active-time consumption; the wall deadline
keeps running. At the deadline, close at the current checkpoint and preserve
earned records. Present both limits before starting. Guests share the
session's clock, not separate copies. This bounded extension is one local
choice; a long pause can still require a later admission or the free survey.

For a separate 30-active-minute ticket, define a pause to stop consumption.
After 8 minutes of play and 7 minutes of pause, 22 active minutes remain.
A 30-wall-minute ticket activated at 19:00 instead expires at 19:30; the same
15 minutes of elapsed time leave 15 minutes. Equal price does not make these
the same playable plan.

Use [access and return](access-and-return.md#worked-scene-pause-skip-and-cancel)
for an event-level example where pause freezes active time, skipping preserves
the committed cost, and cancellation restores a declared checkpoint. Keep
scene resources, entitlement time and monetary refund as separate fields.
Never infer that restoring a spent fuel token extends a wall-clock pass.

## Revise terms and promise together

If an expiring right blocks the claimed group activity, change capacity,
ownership, admission, continuation, schedule, unpaid path or the authorized
promise. Specify the future state and next action for somebody who declines,
misses or leaves. Preserving a missed opportunity's consequence may be an
intentional design; erasing every consequence is not required.

For acceleration, replay a concrete unpaid acquisition and application path
using [resources and development](../../game-systems-design/references/resources-and-development.md).
If it depends on a random drop, an average wait does not show readiness for
a fixed group date. If it is possible only through another payer's work,
name that dependency when stating the free path.

A rule table establishes specified eligibility. Executed entitlement and
balance operations need their actual outputs. Whether the offer is acceptable,
the schedule burdens people or the business earns revenue requires different
evidence. Preserve the material limit without blocking the completed game
design candidate.

## Source anchor

[GW] Mike O'Brien / ArenaNet, *Play For Free Today*, 2015-08-29,
“Free Accounts,” communication and economy restrictions.
[Primary announcement](https://www.guildwars2.com/en/news/play-for-free-today/).

The Lantern terms, clocks, group cases and policies are original synthetic
examples. They support construction and replay, not a current offer or an
empirical claim about spending, pressure or profit.
