# Shared play

Use this procedure to construct a cooperative or competitive episode, an
authority rule or a policy that assembles people for an actual joint task.
Keep formal capability, situational leadership and accepted authority distinct.

## Contents

- [Construct a dependency worth playing](#construct-a-dependency-worth-playing)
- [Worked episode: two routes and a refused expense](#worked-episode-two-routes-and-a-refused-expense)
- [Make authority and dispute executable](#make-authority-and-dispute-executable)
- [Construct a feasible composition policy](#construct-a-feasible-composition-policy)
- [Worked queue: the absent signal keeper](#worked-queue-the-absent-signal-keeper)
- [Observe the appropriate outcome](#observe-the-appropriate-outcome)
- [Source anchors](#source-anchors)

## Construct a dependency worth playing

Obtain the joint objective, individual objectives, available observations,
action order, private and common resources, permissions, communication channels
and roster. Include supporting labor when it matters: who explains the rule,
maintains the record or makes another person's action possible?

Choose the relation the episode should create. One actor may improve another's
attempt, prepare a condition, absorb a consequence, commit jointly, negotiate
a trade, or compete for a shared opportunity. Blades's teamwork rules supply
published examples of several such relations; the existence of those mechanics
does not establish their effect on actual conversational dominance. [TW]

Create actions whose dependencies express the chosen relation. A common score
from independent solo tasks may fit a cooperative theme, but it does not by
itself require mutual decisions. Conversely, an asymmetrical leader with
deliberately delegated decisions can be the agreed form of play.

For each affected action write: who knows enough to propose it, who decides,
who may refuse, who executes, who bears its cost and who recognizes the outcome.
Follow actor knowledge through the canonical
[entities procedure](../../gameplay-design/references/entities.md). Keep role
cards and observer outputs separate from facilitator truth during a replay.

## Worked episode: two routes and a refused expense

This original Lantern Crew episode has Bo and Cy present. Bo has 1 personal
fuel, the equipped winch and knowledge of its operation. Cy has the public
survey map and chooses the route. The crew locker has 4 scrap. Survey completion
produces 2 scrap; repair costs 6. This is the complete player material:

| Card | Information supplied to its holder | Choice it retains |
| --- | --- | --- |
| Cy: route | Ridge takes 3 turns and no fuel; canal takes 1 turn with a winch and 1 fuel. Ridge reveals stable landing; canal reveals damaged pier. | Propose either route or stop the survey |
| Bo: equipment | Winch is equipped; its single use costs Bo's 1 fuel. Bo may explain the procedure but fuel use requires his confirmation. | Accept or refuse his expenditure |
| Public crew ledger | Locker 4; survey payout 2; repair price 6; Bo is authorized treasurer by an earlier accepted election. | Bo authorizes a specific crew purchase after hearing Cy's proposal |

Use this complete resolution rule: Cy proposes a route. If it needs Bo's fuel,
Bo confirms or refuses. On confirmation, deduct fuel before moving; on refusal,
make no deduction and return the route choice to Cy. Ridge requires no Bo fuel.
After the stated number of turns, show the route marker and add 2 locker scrap.
Bo may then authorize repair, deducting 6 and starting the generator. Otherwise
the locker retains 6 for another use. No one can convert scrap into fuel during
this episode.

Replay the dispute: Cy proposes canal; Bo declines because he wants fuel for
the return. Cy proposes paying from the locker instead. That substitution is
unavailable: its unit is scrap and there is no exchange action. Cy chooses
ridge; after three turns the public marker is stable landing and the locker
contains 6. Bo approves repair; the locker becomes 0 and the generator works.
Bo still holds 1 personal fuel. This makes the refusal consequential while
leaving an available common plan.

Now reveal all role-card text and replay. If one participant chooses and
executes everything for the others, the formal protocol still needs each
retained confirmation. Whether the group honors that choice in practice needs
observation. If a design deliberately lets Bo delegate his fuel choice to Cy,
record that delegation and test its scope; do not reject it merely because
the roles become less independent.

## Make authority and dispute executable

Write an authority rule with scope, binding point and remedy. Separate proposal,
recording and effective change. A person maintaining the ledger does not acquire
the right to spend it merely by typing an entry.

For the invented crew, use this vacancy procedure: an accepted prior succession
applies as written. Otherwise, present members may propose a temporary
treasurer; it becomes effective only after every present member accepts the
named person and scope. Until then, no crew expense occurs. A member may still
start an expense-free survey. On disagreement, record the unresolved expense
and choose that free action, postpone play or close the expedition. This
procedure is one local design; another game may intentionally use majority
rule, unilateral leadership or a binding referee.

Replay an attempted overreach: Cy writes “Cy is treasurer” without Bo's
acceptance. The record is a proposal, not effective authority. Repair cannot
charge the locker under that entry. Bo and Cy then accept Cy for this single
repair; the bounded grant permits that expense and ends afterward. A future
purchase needs new authority.

For a deal, specify item or service, custody, fee, deadline, execution and
cancellation. Follow its actual access chain through
[resources and development](../../game-systems-design/references/resources-and-development.md#follow-storage-and-intermediation).
For removal, succession or persisted obligations use
[game state transfer](../../game-systems-design/references/game-state-transfer.md).
Do not silently convert social disagreement into an invented unanimous vote.

## Construct a feasible composition policy

Separate four designs: the ability being estimated, uncertainty of that estimate,
the rule assembling a playable roster, and visible rank/rewards. Then obtain
team size, required functions, role permissions, premade parties, arrivals,
departures, region/mode/time and allowed waiting or relaxation. A precise skill
estimate cannot create an absent role.

Evaluate all hard constraints on the same candidate population. Only relax a
preference when the game permits it. Construct what the waiting person sees:
the constraint blocking a match, available alternatives, whether choosing one
changes the task, and how to leave the queue. Do not promise a finite wait
from a queue with no source for the needed participant.

Riot's historical patch 10.6 notes report that separately promising autofill
and premade parity changes interacted badly with the desired skill matching.
Use that as a reason to inspect combined restrictions, not as a numerical
model of a current queue. [MM]

## Worked queue: the absent signal keeper

This original three-person task needs exactly one mapper, one winch operator
and one signal keeper. Roles are certified and exclusive in this example;
there are no premades, latency restrictions or skill-band exclusions. Every
candidate is otherwise compatible.

| Time in minutes | New candidates | Certified roles |
| --- | --- | --- |
| 0 | M1, M2, M3, M4, W1, W2 | Four mappers, two winch operators, no signal keeper |
| 3 | S1 | One signal keeper |
| 5 | S2 | One signal keeper |

At time 0 the maximum number of full groups is `min(4, 2, 0) = 0`.
Broadening a skill band leaves zero. At time 3 assign M1/W1/S1; M1 and W1
waited 3 minutes. At time 5 assign M2/W2/S2; M2 and W2 waited 5 minutes.
M3 and M4 are still waiting and their waits are right-censored at 5 minutes
in this record. An average over only the six matched people hides them.

Replay by crossing each assigned ID off the queue; a candidate cannot fill
two groups. A claimed two-minute maximum is refuted by these stated arrivals.
A valid control includes two signal keepers at time 0: two groups can start
immediately. No population prediction follows from either artificial schedule.

Construct an alternative only if it is acceptable to change the task: offer
an explicit two-person survey with a fixed signal beacon, or allow a verified
dual-role player to fill the missing function. Label the changed format and
reconsider its dependencies. Renaming a mapper “signal keeper” without giving
the required ability is not a solution. An honest wait or manual session
schedule is also a legitimate result.

If performance depends on the weakest member, teams `[0, 10]` and `[5, 5]`
have different modeled ability despite identical mean 5. If it depends on
the sum, they tie. Choose aggregation from the joint task, not convenience.

## Observe the appropriate outcome

The paper replays establish legal actions, dependencies and an impossible
composition under stated conditions. Runtime observer views can establish
which information an implementation exposed. Real negotiation, recognition
of authority and willingness to use a refusal need participant evidence.
Keep disagreement visible when people reasonably prefer different outcomes.

For queue evidence retain unmatched departures, incomplete waits, cohort,
build and role assignment as well as successful matches. A nominally shared
win rate does not establish fair access to a desired role. Use the shared
[environment contracts](../../game-design/references/environment-contracts.md)
for role-specific observations and data operations.

## Source anchors

- [TW] John Harper / *Blades in the Dark*, “Teamwork,” published SRD,
  assist, group action, protect and setup. [Primary rules](https://bladesinthedark.com/teamwork).
- [MM] Hanna “shio shoujo” Woo / Riot Games, *Patch 10.6 notes*, 2020-03-17,
  “Autofill Balance in Ranked.” [Primary patch notes](https://www.leagueoflegends.com/en-us/news/game-updates/patch-10-6-notes/).

The role cards, dispute, queue and numerical counterexample are original
synthetic constructions. Historical descriptions supply repertoire without
establishing their desirability for this group.
