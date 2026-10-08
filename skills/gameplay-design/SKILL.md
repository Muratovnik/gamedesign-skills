---
name: gameplay-design
description: Create or revise game actions, controls, actor behavior and knowledge, spaces, encounters, shared timing, or free audiovisual play. Use for an executable action contract, behavior, layout, encounter or controllable phrase. Skip pure economy, lore, subscription policy, technical refactors and wording changes that leave these game relationships unchanged.
license: MIT
metadata:
  assay-optional-skills: "evidence-research code-change test-writing"
---

# Gameplay design

Make the player's available action and its consequences concrete. A useful result
can be a move, a behavior, a placed obstacle, a whole encounter, or a controllable
sound-and-image phrase. Start directly with the relevant relationship; a known
local change does not require designing the whole game.

## Construct the playable relationship

1. **Recover the current opportunity.** Identify the intended activity and the
   current artifact: what the participant can observe, choose and perform in the
   relevant starting state. For an existing game, use its actual action rules,
   camera, actor information and geometry. For a new design, give unspecified
   parameters explicit provisional values or variables. Choose units that let
   another person reproduce the important sequence.
2. **Make the change in its material.** Write the transition, behavior rule,
   geometry or control mapping that creates the intended opportunity. Preserve
   a useful commitment, pause or constraint when it carries the design. When
   alternatives are needed, vary a causal relationship: paying to interrupt an
   action differs from shortening every recovery; changing an enemy's knowledge
   differs from reducing its damage. Develop the selected version beyond labels.
3. **Join the relationships that determine this episode.** A warning is useful
   only relative to a permitted response in the participant's view; a route is
   useful relative to the controller and other active threats; an actor's spoken
   intention needs both an information source and an executable role. Use the
   smallest shared state or timeline that preserves those dependencies.
4. **Replay a discriminating sequence.** Resolve the boundary that could change
   the result: command before/at readiness, hidden target movement, a blocked
   role, a second threat, a phase boundary or two simultaneous controls. Carry
   the effect into the next meaningful choice. Revise the responsible rule or
   placement and replay its affected relation.
5. **Deliver the changed artifact and its consequence.** Show enough initial
   state, actions and resulting state to use the design. Name what the
   representation establishes. A timeline establishes its declared order;
   responsive control, perceived clarity and musical quality need the relevant
   execution or human material.

## Read the branch that supplies the missing construction

| Decision | Read | Construct |
| --- | --- | --- |
| Input, cost, commitment, cancellation, contact or return of control | [Actions and time](references/actions-and-time.md#action-commitment) | Action transitions and a timed example |
| A threat should be read and answered | [Signal and available response](references/actions-and-time.md#signal-and-available-response) | Participant cue, response deadline and a legal route |
| Shared beat, simultaneous actions, pause or resumption | [Shared clock](references/actions-and-time.md#shared-clock) | Resolution order and phrase on one time base |
| Sound, image or movement is the playable material, including no-win play | [Free audiovisual form](references/actions-and-time.md#free-audiovisual-form) | Control mapping, controllable phrase and changed composition |
| Detection, search, rumors, testimony or coordinated behavior | [Entities](references/entities.md) | Allowed knowledge, role and fallback behavior |
| Traversal, cover, placement or combined threats | [Space and situations](references/space-and-situations.md) | Scaled placement and an encounter sequence |

For a change crossing owners, use the shared
[relations and context](../game-design/references/relations-and-context.md).
The [consumer and Assay contract](../game-design/references/consumer-and-assay-contract.md)
owns access to the actual project and general methods; the
[environment contracts](../game-design/references/environment-contracts.md)
own what an operation can establish. Optional peer metadata does not load them.

## Connect to the other game decisions

This skill owns actor knowledge, including the distinction between world fact,
belief and expressed position. [Inference](../game-information-design/references/inference.md)
owns the participant's available grounds and expression of a conclusion.
[World relations](../game-world-narrative-design/references/world-relations.md)
own the social or material relationship being expressed; [conditional story](../game-world-narrative-design/references/conditional-story.md)
owns scene availability and dramatic consequences. Use [resources and development](../game-systems-design/references/resources-and-development.md)
when an action changes future access, and [access and return](../game-participation-design/references/access-and-return.md)
when who can perceive or execute it changes. A generated encounter also needs
the selection policy in [repertoire](../game-content-design/references/repertoire.md).
