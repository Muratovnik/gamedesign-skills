# Game state transfer

This is the canonical procedure for changing game state at an attempt, roster,
season, mode or rule-version boundary, including a specified save migration.
The agent's task notes and continuation are a separate object owned by the
general work method.

## Contents

- [Define the boundary and preservation claim](#define-the-boundary-and-preservation-claim)
- [Construct the transformation](#construct-the-transformation)
- [Worked migration: Lantern Crew](#worked-migration-lantern-crew)
- [Check the new playable state](#check-the-new-playable-state)
- [Source anchors](#source-anchors)

## Define the boundary and preservation claim

Obtain both rule versions, original states, stable identities, mode exceptions,
the triggering outcome, roster changes and the accepted meaning of preservation.
Read the consumer of the new state, not only the serializer. Bind authorized
operations on real data through the shared
[environment contract](../../game-design/references/environment-contracts.md).

Write `next = transfer(previous, outcome, roster, rules)` for the relevant
parts; do not impose a universal save schema. A balance, character, account,
group, office and world can have different lifetimes. Preserve an event as
history when it no longer grants an action.

| Field family | Possible operation | Dependent question |
| --- | --- | --- |
| Stock in one unit | Keep, sum, scale, convert, reset | Who owns the result and can spend it now? |
| Nonlinear progress | Convert from earned base quantity | Does adding levels overstate earned experience? |
| Unlock set | Union, filter by mode, retire | Are duplicates one ability or multiple charges? |
| Capability or item | Preserve, replace, change prerequisites | Is the target action implemented and reachable? |
| History and one-time events | Retain IDs, archive or deliberately rewrite | Can a completed event award or trigger again? |
| Authority or obligation | Continue, elect, delegate, settle, terminate | What accepted decision authorizes the new holder? |
| Knowledge and observation | Preserve or reveal under the knowledge rule | Does a new actor receive facts never learned? |
| Paid or timed right | Retain owner/expiry or apply agreed replacement | Does a valid path to the named activity remain? |

Game knowledge follows
[the actor-knowledge procedure](../../gameplay-design/references/entities.md).
Story history follows
[conditional story](../../game-world-narrative-design/references/conditional-story.md).
This procedure specifies their boundary transformation without redefining who
may know a fact or what makes an event canonical.

## Construct the transformation

Map each material old field to its new field, operation, condition and
exception. Use an explicit retired or archived destination for a meaningful
removed field. Explain an intentional reset at the action it changes. Equal
new rules do not by themselves preserve different prior investments; prior
investment also does not prohibit every change.

For a nonlinear example, total experience required for level `L` is
`100 * L**2`. Records with 400 and 900 experience represent levels 2 and 3.
Combining experience gives 1300 and level 3, because level 4 requires 1600.
Adding levels gives 5, which would require 2500. Union of unlock sets
`{winch, chart}` and `{winch}` gives two abilities, not three. Addition fits
only if the field means additive charges.

Specify repeated invocation when it belongs to the operation's contract.
A migration may reject an already migrated input, or return the new-version
state unchanged. A seasonal transfer may run once per distinct season.
Do not impose idempotence on an accumulating operation without a repeat
contract. Define partial completion if several stores must change.

## Worked migration: Lantern Crew

This synthetic version change preserves a continuing crew after Ava departs.
`ava`, `bo` and `cy` are stable IDs. Current time is `2026-10-08T18:00:00Z`.
Ava's personal archive pass expires at `2026-10-15T20:00:00Z`; it hosts an
archive episode only while she participates unless a recorded delegation
exists. None exists here.

The old state is complete for this paper operation:

| Old field | Value |
| --- | --- |
| Rule version / crew | `1` / `lantern-crew` |
| Roster / presence | `{ava, bo, cy}` / `{bo, cy}` |
| Crew locker / generator | `4 scrap` / `broken` |
| Personal fuel | `bo: 1`, `ava: 0`, `cy: 0` |
| Unlocks | `ava: {archive-reading}`, `bo: {winch}`, `cy: {}` |
| Equipped tools | `bo: {winch}`, others none |
| Knowledge | `ava: {archive-code}`, `bo: {winch-procedure}`, `cy: {public-survey-map}` |
| Archive right | Holder `ava`; expiry above; no delegation |
| Treasurer | `ava` |
| Accepted decision | `elect-bo-01`: all three accepted Bo before departure |
| Public history | `generator-lost-01`; `archive-message-01` already delivered |
| Open objective | `restore-light`: repair generator for 6 crew scrap |

Version 2 makes owners explicit and retains inactive member records. It also
admits the free public survey described in
[loss and continuation](loss-and-continuation.md#worked-episode-a-darkened-harbor).
Apply the following operations:

| Transformation | Result |
| --- | --- |
| Carry locker with its holder | `owner=crew:lantern-crew, amount=4, unit=scrap` |
| Preserve people and presence separately | Ava's record remains with `present=false`; Bo/Cy are present |
| Preserve personal fuel, unlocks and equipment | Bo retains 1 fuel and his equipped winch; Cy gains neither by joining |
| Preserve knowledge by ID | Three original knowledge sets; no archive code copied to Bo |
| Preserve personal right | Ava retains unexpired pass; hosted archive entry is unavailable now |
| Apply accepted succession | Treasurer becomes Bo, citing `elect-bo-01` |
| Retain history and event IDs | Both prior events remain; `archive-message-01` cannot re-award |
| Keep objective with a reachable route | `restore-light` still needs 6; the present crew can start survey |

Bo can authorize locker expenditure and operate his winch. Cy can choose the
route from the public map. Bo does not learn the archive code by becoming
treasurer. Presenting the public map to Bo is a separate observation event;
it may then add that fact to his knowledge. The existing pass was not
destroyed, but its absent host makes current archive entry unavailable.

Replay: present the public map to Bo and Cy; Cy chooses ridge; complete three
turns; add 2 scrap; Bo authorizes repair and pays 6. The result has `scrap=0`,
`generator=working`, the new public landing marker and unchanged archive
ownership. No prior message is delivered again. This is a continuing plan
without transferring a personal purchase by fiat.

Vary one condition: remove `elect-bo-01`. The transformation cannot invent
acceptance. Retain Ava's authority as inactive and leave crew spending
unresolved until an authorized succession occurs. A survey with no upfront
expense may still be possible. The same total scrap can coexist with a
different action set.

Another accepted design may transfer a group-owned pass with an office,
complete the campaign or reset every unlock. These are legitimate when
ownership and participation terms authorize them. A preserved sum does not
establish those terms.

## Check the new playable state

Compare owner IDs, units, predicates, mode exceptions, historical events and
affected actors' actions. Follow an objective into the new state, including
the consumer view. Inspect an absent owner, duplicate unlock, completed event
and boundary time when applicable. State the inspected population; an empty
eligible-save set cannot establish migration success.

For implemented transfer, retain source/result identity, execute the authorized
operation and load its result through the new consumer. Inspect whether
restoration or presentation pooled inventories or revealed diagnostic truth.
Use existing parsers and migration tools; a generic migration engine is not
required for a small rule.

Distinguish rejected input, partial migration, unresolved policy and refuted
preservation. A parser success confirms format acceptance. Round-trip equality
confirms only compared fields. Neither establishes that the next quest has
its required action or that a returning person understands the situation.
Use [access and return](../../game-participation-design/references/access-and-return.md)
for participation and [paid and timed rights](../../game-participation-design/references/paid-and-timed-rights.md)
for entitlement semantics.

## Source anchors

Blizzard's historical *Season 10 Ending Soon* describes field-specific
rollover: experience rather than level addition, recipe union, artisan maximum,
mode separation, item handling and retained leaderboard history. This is an
example, not current service guidance. [Primary rollover notice](https://news.blizzard.com/en-us/article/20845156/season-10-ending-soon),
“The Season Rollover” and “Season 10 Leaderboards.”

The procedure, nonlinear example and Lantern Crew are original local
constructions. They make preservation inspectable; they do not establish a
real account migration or an informed human return.
