# Capability map

**Status: current.**

Use this reference to move from a design question to its method and a concrete
example. The seven complete directories under `skills/` are the supported
Game Design bundle. `catalog.json` assigns each a canonical owner; shared
relations belong to the `game-design` entry and domain-specific detail belongs
to the relevant sibling.

| Design question | Canonical method | Example or implementation pointer |
| --- | --- | --- |
| When can an actor act, receive a signal and respond? | [Actions and time](../skills/gameplay-design/references/actions-and-time.md) | [Quay Crossing](../examples/design-studies/harbour-of-echoes/quay-crossing.md); the [Godot episode](../examples/godot-episode/README.md) traces its own controller and geometry. |
| What can an actor know or do? | [Entities](../skills/gameplay-design/references/entities.md) and [inference](../skills/game-information-design/references/inference.md) | [Third bell gamebook](../examples/design-studies/harbour-of-echoes/gamebook.md) and [observer-specific views](../examples/analysis-lab/README.md#observer-specific-views). |
| How do space, movement and encounters constrain action? | [Space and situations](../skills/gameplay-design/references/space-and-situations.md) | [Godot episode](../examples/godot-episode/README.md): body collision, ray query and camera rectangle are separate observations. |
| How do players infer, learn or use help? | [Information design](../skills/game-information-design/SKILL.md) | [Lens workshop](../examples/design-studies/harbour-of-echoes/lens-workshop.md), [East Gate](../examples/adaptation/README.md) and the [third bell](../examples/design-studies/harbour-of-echoes/gamebook.md). |
| How do world relations produce conditional story? | [World relations](../skills/game-world-narrative-design/references/world-relations.md) and [conditional story](../skills/game-world-narrative-design/references/conditional-story.md) | [Third bell gamebook](../examples/design-studies/harbour-of-echoes/gamebook.md): public traces, private knowledge and changed scenes. |
| How do resources, loss and state transfer affect continuation? | [Systems design](../skills/game-systems-design/SKILL.md) | [Lantern Crew](../examples/systems-studies/README.md) and [analysis lab](../examples/analysis-lab/README.md): access, recovery, rights and migration. |
| How do joint decisions and access shape participation and return? | [Participation design](../skills/game-participation-design/SKILL.md) | [Shared play](../skills/game-participation-design/references/shared-play.md) and [access and return](../skills/game-participation-design/references/access-and-return.md). |
| How is a repertoire generated, filtered and selected? | [Content design](../skills/game-content-design/SKILL.md) | [Analysis lab](../examples/analysis-lab/README.md): follow generated content through filtering, selection and presentation. |
| How can an existing artifact adapt across language and device? | [Adaptation](../skills/game-design/references/adaptation.md) | [East Gate](../examples/adaptation/README.md): revise the clue and consume that same artifact in the target action. |

## What each trace establishes

The [environment contract](../skills/game-design/references/environment-contracts.md)
connects input, action, output and the downstream consumer. Follow the linked
example for its exact fixtures, procedures and evidence record. In particular:

- Godot evidence concerns the episode's declared input, controller and
  geometry. It does not establish human response, rendered readability or that
  every paper rule was executed.
- The analysis lab checks declared schemas and deterministic consumers. Its
  actor-view filtering concerns serialized data in that format; it does not
  isolate a model that has already read the full save.
- Paper replays make their assumptions and legal alternatives inspectable.
  They are not player studies or measured game feel.
- East Gate checks the declared content and action relations. Human linguistic
  quality, actual small-screen layout and device interaction remain separate
  observations.

Checks can refute a broken relation in the scope they inspect. They do not by
themselves establish enjoyment, learning, cultural interpretation, accessibility
in use or consent. The examples are synthetic and claim no user playtest or
model-quality result.
