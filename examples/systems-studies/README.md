# Systems and participation studies

This page contains one original synthetic paper study of resource ownership,
authority, migration, and recovery after a roster change. It needs only the
rules below, the linked JSON starting/result records, and paper or another way
to track quantities and turns. There is no executable consumer in this folder;
for digital state operations, follow the separately versioned
[analysis lab](../analysis-lab/README.md). These declared outcomes are not
observations of human play or evidence about a skill's effectiveness.

## Replay Lantern Crew

The crew wants to restore a harbor generator after a loss and roster change.
Ava is absent; Bo returns with a winch and one personal fuel; Cy joins with the
public survey map. The locker holds 4 crew scrap and repair costs 6. Ava still
owns an unexpired personal archive pass, but her absence suspends hosted entry.
The exercise asks you to preserve ownership, knowledge, and prior history while
finding a permitted route to repair or an agreed ending.

Begin with [x3-input.json](x3-input.json), the complete relevant paper-study
state. Read the boundary rule, then play the ridge branch under “Play the next
episode”; compare your final quantities and history with
[x3-ridge-result.json](x3-ridge-result.json). These JSON files encode this
paper contract. For executable state operations, use the analysis lab's own
fixtures through [state migration](../analysis-lab/README.md#state-migration)
and [observer-specific views](../analysis-lab/README.md#observer-specific-views).

Keep the two rule identities when comparing results. The paper contract
`lantern-crew-paper-2` gives 4 total scrap on a survey after repair and rejects
an already version-2 migration input. The technical build `lantern-crew-2`
gives 2 total scrap on that survey and returns an unchanged migrated state on
repeat. Both are specified alternatives; its execution verifies those technical
rules. Preserve the selected policy when adapting either encoding to a game.

This study fixes a wall-time snapshot of `2026-10-08T18:00:00Z`. Game turns
are discrete and have no wall-time conversion. The pass expires at
`2026-10-15T20:00:00Z`; admission requires a time strictly before that instant.
No live payment, migration or participant agreement is implied.

### Materials and authorities

Keep these views separate when assigning player roles. A facilitator may
inspect the full state to check the paper rules; that view is not player data.

| Holder | Supplied information and capability | Retained authority |
| --- | --- | --- |
| Ava, absent | Private archive code; personal pass; archive-reading unlock | Ownership remains; cannot currently host an archive episode |
| Bo, present | Winch procedure; equipped winch; 1 fuel | Approve personal fuel use; after the accepted election, authorize crew expense |
| Cy, present | Public survey map | Choose a route and propose a crew repair |
| Public crew record | Broken generator; locker 4; repair 6; prior message already delivered | Does not grant every member arbitrary spending rights |

The old state contains `elect-bo-01`, accepted by Ava, Bo and Cy before Ava
departed. It names Bo as successor for the crew treasury. Reading that record
is evidence of the synthetic game's supplied agreement; it is not evidence
that actual people accepted it.

### Apply the boundary rule

Use the canonical
[game state transfer procedure](../../skills/game-systems-design/references/game-state-transfer.md).
The paper migration accepts version 1 and produces version 2. An already
version-2 input is rejected as `already_migrated`; this is the selected repeat
contract for this paper operation, not a requirement for all migrations.

Apply these operations in order before starting the next episode:

1. Keep all participant IDs; record Ava as absent rather than delete her.
2. Carry 4 scrap with owner `crew:lantern-crew`; preserve personal fuel and
   each participant's unlock and knowledge sets.
3. Keep Ava's pass holder, expiry and lack of delegation. Archive admission
   remains unavailable to the present group.
4. Apply the accepted `elect-bo-01` decision: set treasurer to Bo and retain
   the authority record. Preserve prior event IDs, including delivered
   `archive-message-01`.
5. Keep the restoration objective, now with the permitted free survey path.

At this boundary the numerical stocks are unchanged. The office holder changes
through its accepted decision; the pass and private knowledge do not travel
with that office. A newly formatted save that combines all inventories or
copies Ava's code into Bo's view fails this preservation claim.

### Play the next episode

After the transfer, read the public map to Bo and Cy. This is a new observation
event for Bo:

> Ridge: three turns, no fuel, reveal stable landing. Canal: one turn,
> requires Bo's equipped winch and one fuel, reveal damaged pier. Completing
> either survey creates two crew scrap. A route abandoned before completion
> earns no marker or scrap.

Cy chooses a route. Canal requires Bo's confirmation before fuel is spent.
If Bo refuses, Cy may choose ridge or stop. There is no scrap-to-fuel exchange
in this episode. A completed survey adds 2 crew scrap. Bo may then approve
repair for 6, making the generator work. A generator that was already working
at a survey's completion adds another 2; this first repair has no retroactive
payout. The next public survey is also free to start.

For the supplied ridge choice, complete the three-turn survey, then let Bo
approve the repair. The expected paper result is:

| Step | Crew scrap | Bo fuel | Generator | Information and next action |
| --- | ---: | ---: | --- | --- |
| After version transfer | 4 | 1 | Broken | Bo is treasurer; archive remains unavailable |
| Present public map | 4 | 1 | Broken | Bo and Cy know the two routes |
| Cy chooses ridge; complete 3 turns | 6 | 1 | Broken | Both observe stable landing; propose repair or defer |
| Bo approves and pays 6 | 0 | 1 | Working | Both may start the next free survey |

The result file retains Ava's pass and code, Bo's winch and authority, Cy's
current route role, historical events and the newly observed landing. It does
not deliver the old archive message again. The next completed survey would
give 2 ordinary scrap plus 2 generator scrap, bringing the locker to 4.

### Replay the contrasts

Reset to the input for each branch; do not compose their results accidentally.

| Changed condition | Concrete replay and result |
| --- | --- |
| Bo accepts canal | Spend his 1 fuel, advance 1 turn, reveal damaged pier, earn 2, repair. Crew stock 0 and working generator match ridge; fuel 0 and route knowledge differ. |
| Bo refuses canal | No fuel is spent. Cy selects ridge or stops. An attempted charge of locker scrap cannot substitute for fuel. |
| `elect-bo-01` is missing | Preserve the inactive prior office holder and unresolved spending authority. The free survey can earn 2, but repair needs an accepted succession. Total scrap alone cannot settle it. |
| Ava explicitly delegates hosting to Bo while permitted | Archive entry becomes available under the named delegation's expiry; Bo still does not automatically know Ava's code. |
| Pass expires with no admitted session extension | No new archive entry; earned records and Bo's personal unlock remain. Public survey continues. |
| Restoration is an agreed finale instead | Decommission the base, return personal property, record the final landing and close the objective. Do not advertise another expedition. |

These contrasts distinguish source loss, right loss, authority, knowledge and
the choice to end. They do not require all games to preserve recovery or the
same distribution of control.

## Continue with the related complete studies

| Family | Material and replay | What the observation can establish |
| --- | --- | --- |
| Resources, exchange and development | [Ferry workshop arithmetic, random waiting, service mediation and winch use](../../skills/game-systems-design/references/resources-and-development.md) | Balances, permitted chains and action changes under stated rules |
| Continuing campaign and state transfer | Input/result files and replay above; [loss and continuation](../../skills/game-systems-design/references/loss-and-continuation.md) | A new concrete state with a reachable group plan or defined ending |
| Shared decisions and restricted population | [Refused expense, disputed office and missing-role queue](../../skills/game-participation-design/references/shared-play.md) | Formal dependencies and feasible compositions for the supplied schedule |
| Physical access, intensity and return | [Private route card, helper procedure and pause/skip/cancel accounting](../../skills/game-participation-design/references/access-and-return.md) | A usable candidate and paper transition; physical and social outcomes need their own evidence |
| Encountered content | [Five complete crossing cards, selection and four parcel worlds](../../skills/game-content-design/references/repertoire.md) | Specified content differences, selection omissions and coupled facts |
| Paid/time intersection | [Archive offer, mixed-rights group and distinct clock policies](../../skills/game-participation-design/references/paid-and-timed-rights.md) | Eligibility and timing implications of the invented terms |

For runtime, device and participant observations, apply the
[environment contracts](../../skills/game-design/references/environment-contracts.md).
The runtime skill bundle includes every reference and resource needed by its
methods; this example directory is a public teaching companion.
