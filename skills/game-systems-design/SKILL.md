---
name: game-systems-design
description: Design or revise game resources, prices, storage, exchange, progression, loss, recovery and state transfer across attempts, rosters, seasons or rule versions. Use when these rules change an actor's available plans. Skip purely cosmetic counters, business forecasts, generic database migrations and the agent's own task continuity.
license: MIT
---

# Game systems design

Build a usable rule and the states that show what it lets someone do next.
An economy can be a handful of tokens; progression can be a new responsibility;
loss can be the intended end of a campaign.

## Start with the action the system must support

Use the established [consumer and Assay binding](../game-design/references/consumer-and-assay-contract.md).
For a direct invocation, establish that binding before a dependent operation.
Reuse the current task's supplied intent, rule version and state; request only
missing facts that change this decision. A fully specified invented game needs
no external confirmation of its fictional values.

1. **Name the next meaningful plan.** Identify its actor, required action,
   resource or right, earliest relevant occasion, and competing use. “Reach
   level 8” needs the action or recognition that level 8 changes.
2. **Trace the complete enabling chain.** Write the holder, unit, source,
   storage, transfer, choice of use, execution and resulting state. Include
   an absent owner or mediator when that changes access. A group's total is
   not every member's spendable budget.
3. **Construct the smallest useful rule change.** Supply actual prices,
   conditions, allowed operations and affected material. For open design,
   compare alternatives that change a causal relationship: when the choice is
   made, who owns it, which action it enables, or what risk it carries. For a
   settled local edit, implement that edit without reopening the whole economy.
4. **Follow the changed plan through an episode.** Start from applicable
   states, pay the cost, use the acquired ability, incur the relevant loss,
   and take the next action. Inspect the route that may now dominate or become
   impossible. Use a calculation or a short state witness when it answers the
   question; do not require a simulation for its own sake.
5. **Revise the responsible relationship.** Change a source, price, holding
   rule, ability, scene, recovery route or transfer operation according to the
   failed link. More rewards do not repair an unused ability, a missing role
   or a right held by somebody who has left.
6. **Deliver the rule and its consequences.** Return the changed artifact,
   a reproducible before/after state, the remaining choice and the actual
   verification boundary. Distinguish a proposed rule, a formal consequence,
   an observed runtime operation and evidence about people.

## Read the procedure for this decision

| Decision | Read before constructing or changing it |
| --- | --- |
| Endowment, income, price, chance, storage, exchange, intermediation or an unlock | [Resources and development](references/resources-and-development.md) |
| Death, exhaustion, destroyed production, recovery, retirement or a finale | [Loss and continuation](references/loss-and-continuation.md) |
| New attempt, roster, season, mode, save format or rules version | [Game state transfer](references/game-state-transfer.md) |

Read multiple branches when one rule crosses them. Replacing a stored recipe
with a transferable currency changes both later choice and migration. Each
reference includes a complete synthetic example and a legitimate alternative.

## Compose at the owned boundary

Read [actor knowledge](../gameplay-design/references/entities.md) when a saved
fact or unlock changes what an actor may know. Read
[learning and help](../game-information-design/references/learning-and-help.md)
when the question concerns a person's understanding or use of an ability.
Read [conditional story](../game-world-narrative-design/references/conditional-story.md)
when history, one-time events or changed resources affect a scene.

Use [participation](../game-participation-design/SKILL.md) for joint authority,
access, return and paid or timed participation. This skill owns the game state
transformation; participation owns how people choose or use it. Use
[content design](../game-content-design/SKILL.md) when the unlock needs a
revised range of encounters. The shared
[environment contracts](../game-design/references/environment-contracts.md)
bind calculations, saves, imports and runtime observations to their actual scope.

Preserve meaningful alternatives: accumulating advantage, intentional scarcity,
irreversible biography, a full reset and campaign completion can all be valid.
Judge them against the agreed game, not a universal demand for equal wealth,
permanent growth or endless continuation.
