<div align="center">

# Game Design

Seven composable methods for making and revising playable games.

[![License: MIT](https://img.shields.io/badge/License-MIT-blue?style=flat-square)](LICENSE)
[![Version](https://img.shields.io/badge/version-0.1.1-informational?style=flat-square)](VERSION)

</div>

Game Design supplies concrete procedures for actions, information, worlds,
systems, participation, content and adaptation. Use one directly for a narrow
task, or compose them around an existing game. The result can be a rule, scene,
map, resource model, playable paper episode, consumed data change or running
prototype. A large design document is optional.

The package includes original playable studies, a Godot input and physics
episode, renderable sound-and-light scores, semantic Python consumers, state
migration and analysis examples. General research and engineering methods come
from the separately maintained [Assay](https://github.com/Muratovnik/assay)
package; Game Design does not install or embed Assay.

## What you can do

| Entry | Useful output |
| --- | --- |
| [game-design](skills/game-design/SKILL.md) | A coherent concept, connected revision or transfer to another language/device |
| [gameplay-design](skills/gameplay-design/SKILL.md) | Action timing, actor knowledge, spatial opportunities and encounters |
| [game-information-design](skills/game-information-design/SKILL.md) | A solvable inference path, independent learning or usable assistance |
| [game-world-narrative-design](skills/game-world-narrative-design/SKILL.md) | World relationships, conditional scenes and expressive consequences |
| [game-systems-design](skills/game-systems-design/SKILL.md) | Resource access, development, loss/recovery and state transfer |
| [game-participation-design](skills/game-participation-design/SKILL.md) | Joint decisions, matching, access, stopping/returning and paid rights |
| [game-content-design](skills/game-content-design/SKILL.md) | A meaningful repertoire and compatible generated/selected content |

All seven directories form the supported bundle. Entries read sibling
references where their owned relation matters; `game-design` is not a mandatory
router. Neither a score, victory, simulation nor temporary-only help is required
for a good result.

## Demonstration

Start with [East Gate](examples/adaptation/README.md), a small existing puzzle
adapted into Russian and a one-line display. Its actual content is consumed by
pin and direction actions, opening the gate and supplying the next scene.
Python 3.11 or newer is sufficient for this example:

```bash
python3 examples/adaptation/consumer.py --artifact examples/adaptation/fixtures/east-gate-ru.json --expect-revision east-gate-ru-2 --pin 1 --pin 2 --pin 3 --pin 4 --pin 5 --pin 6 --choose east --output /tmp/east-gate-result.json
```

Use a fresh output filename. Read the notebook, token and next scene in the
result. A broken acrostic or later sign is rejected before play; a wrong player
choice stays a legitimate retry. For engine work use the
[Godot episode](examples/godot-episode/README.md). For resources, migration,
observer views, content selection and telemetry use the
[analysis lab](examples/analysis-lab/README.md). More paper studies are listed in
the [example guide](docs/examples.md).

## Access

The source can be read directly from a local checkout. Give the agent the
absolute Game Design root, the game root, the current artifact and the relevant
goal and permissions. Have it read the applicable `SKILL.md` and references.
This explicit source route does not require client registration.

General methods are maintained separately in Assay. The shipped binding requires
Assay **0.17.2**, commit `94c517b0aac9ba2575086bf9aead1cc828aadb0d`, obtained
separately. From the Game Design root, the binding tool verifies the pinned
source bytes before reading a method:

```bash
python3 skills/game-design/scripts/bind_assay.py --assay-root /absolute/assay --provider-state enabled --method evidence-research --read
```

Replace `/absolute/assay` with the actual authorized source path. The provider
state is a caller declaration, not proof of client permission. Required Assay
methods depend on the operation; see the
[consumer and Assay contract](skills/game-design/references/consumer-and-assay-contract.md).

For native use, the generated Codex and Claude marketplaces identify the full
bundle as `game-design@game-design-source`. Follow the
[installation and lifecycle procedures](docs/installation.md) for the chosen
client's commands, scope, conflicts, update and rollback. These procedures use
native plugin managers; client/build qualification remains
[pending](docs/compatibility.md#native-client-qualification). The direct source
route above is available without registration.

## Quick start

From the repository root, create an isolated development environment and run
the scoped checks:

```bash
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements-dev.txt
.venv/bin/python tools/check.py
.venv/bin/python -m unittest discover -s tests -v
.venv/bin/python -m unittest discover -s examples/adaptation -p 'test_*.py' -v
```

Use the example READMEs for their additional checks and a separately obtained
Godot executable where needed. Checks do not launch model runs. Prepare a
versioned source archive with:

```bash
python tools/release.py build --output dist --version 0.1.1
```

This creates `gamedesign-skills-0.1.1-source.zip` and `SHA256SUMS` in `dist/`.
It prepares source files; it does not publish or register the package.

## Documentation

- [Example guide](docs/examples.md): where design methods and cross-domain traces are exercised.
- [Capability map](docs/traceability.md): methods, examples and implementation boundaries.
- [Environment contract](skills/game-design/references/environment-contracts.md): input → action → output → consumer and precision boundaries.
- [Compatibility](docs/compatibility.md): dependencies and observed versus pending support.
- [Design decisions](docs/decisions.md): rationale, evidence and reconsideration conditions.
- [Research and evidence limits](docs/late-comparison.md).
- [Release preparation](docs/releases.md): build a local source archive.
- [Russian quick start](docs/quickstart.ru.md).

## Limits

The examples are authored and synthetic. Headless engine checks establish
specific input, timing, geometry and state properties, not perception or human
experience. No model-quality campaign, user playtest, automatic client
discovery or arbitrary-engine qualification is claimed.

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for ownership, source-based method changes
and targeted verification. [CHANGELOG.md](CHANGELOG.md) records this release's
public contract.

## License

[MIT](LICENSE), with the technical schema material under Apache-2.0 described
in [NOTICE.md](NOTICE.md).
