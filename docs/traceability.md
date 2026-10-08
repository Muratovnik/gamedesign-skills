# Capability map

**Status: current.**

Use this map to find where the package develops a design capability and where
an example makes it concrete. It is a navigation aid, not an expertise scale or
evidence that a player experienced a particular result. Each example states
what its technical or paper evidence can and cannot establish.

## Methods and examples

| Capability | Canonical method | Example or useful contrast |
| --- | --- | --- |
| Action timing, signals and available response | [Actions and time](../skills/gameplay-design/references/actions-and-time.md) | Quay Crossing compares a legal response with an off-camera signal and a no-input case. |
| Actor knowledge, roles and coordination | [Entities](../skills/gameplay-design/references/entities.md) | Harbour's gamebook and serialized actor views distinguish what each participant can know and do. |
| Space, movement and encounters | [Space and situations](../skills/gameplay-design/references/space-and-situations.md) | The Godot episode contrasts body clearance, a point ray and camera visibility. |
| Inference, learning and assistance | [Information design](../skills/game-information-design/SKILL.md) | Harbour, East Gate and Lens Workshop explore clue paths, transfer and permanent help. |
| World relations and conditional narrative | [World relations](../skills/game-world-narrative-design/references/world-relations.md) and [conditional story](../skills/game-world-narrative-design/references/conditional-story.md) | Harbour connects public traces, private knowledge and changed scenes. |
| Resources, development, loss and state transfer | [Systems design](../skills/game-systems-design/SKILL.md) | Lantern Crew and the analysis lab examine access, recovery, rights and migration. |
| Joint decisions, participation and return | [Participation design](../skills/game-participation-design/SKILL.md) | Proposal/refusal replay, private choice, assistance, pause and cancellation. |
| Repertoires, generation and selection | [Content design](../skills/game-content-design/SKILL.md) | The analysis lab follows generated content through filtering and actual selection. |
| Adaptation across language and device | [Adaptation](../skills/game-design/references/adaptation.md) | East Gate changes an existing puzzle and consumes its revised content in a target action. |
| Explicit simultaneous zero-sum utility | [Zero-sum analysis](../skills/game-systems-design/references/zero-sum-analysis.md) | A real LP, independently checked best responses, changed utilities and valid intended hierarchy. |
| Native conditional narrative and continuation | [Ink artifacts](../skills/game-world-narrative-design/references/ink-artifacts.md) | Listening Room compiles, consumes explicit actions, saves/reopens native state and continues; a missing guard is refuted while departure remains legal. |
| Native asset conformance | [glTF artifacts](../skills/game-design/references/gltf-artifacts.md) | Actual glTF/GLB validation separates bad accessors, missing resources and unsupported coverage; empty/camera-only conformance does not assert a mesh predicate. |
| Observation context at handoff | [Human and material route](../skills/game-design/references/environment-contracts.md#human-and-material-route) | Saved/reopened observations retain conditions, collection method and units; equal counts with different assistance remain distinct. |

The [comparative requirement and plan addendum](research/2026-10-08/requirements-and-plan.md)
maps these changes to the supplied GDR/GDE/OR and C3/C4 boundaries. Dependencies
implement technical operations; they do not own subject judgment or Assay's
general methods.

## Cross-domain traces

**Action to signal to space to threat.** Quay Crossing supplies the design
relation; the Godot miniature consumes baseline and candidate fixtures. Its
native trace concerns the miniature's input and geometry, not human response or
every paper rule.

**Fact to clue to actor knowledge to scene.** Harbour records who can know each
fact and when. Removing a message path changes the available scene. The
technical actor-view example tests serialized permission filtering and
downstream choice for its declared save format; it does not isolate a model
that has already read the full save.

**Resources to loss to rights to return.** Lantern Crew includes a paper replay
and lawful contrasts. The technical lab has a separate versioned recovery and
migration policy; it does not claim to execute the paper variant's different
survey or repeat behavior.

**Language and device to clue and help to target action.** East Gate changes
the source artifact and consumes it in the target puzzle. Whole-line pins
support comparison while the player still chooses the direction. Human
linguistic quality and a rendered device interaction remain separate
observations.

## Evidence boundaries

The [environment contract](../skills/game-design/references/environment-contracts.md)
connects input, action, output and downstream consumer. The paper examples make
assumptions and legal alternatives inspectable. Engine and Python checks can
refute broken data, timing, geometry or state behavior in their declared
formats. They do not establish enjoyment, learning, cultural interpretation,
social consent or accessibility in use. The examples are synthetic; no
user-playtest result is claimed. Current scoped model tasks, native discovery
and independent review are reported in the
[verification record](reviews/2026-10-08-comparison/README.md), separately from
these examples and historical evidence.
