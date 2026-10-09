<div align="center">

# Game Design

Seven composable methods for creating and revising playable games.

[![License: MIT](https://img.shields.io/badge/License-MIT-blue?style=flat-square)](LICENSE)
[![Check](https://img.shields.io/github/actions/workflow/status/Muratovnik/gamedesign-skills/check.yml?branch=main&style=flat-square)](https://github.com/Muratovnik/gamedesign-skills/actions/workflows/check.yml)
[![Release](https://img.shields.io/github/v/release/Muratovnik/gamedesign-skills?style=flat-square)](https://github.com/Muratovnik/gamedesign-skills/releases/latest)

</div>

Game Design helps you turn a design question into a playable rule, scene, map,
resource model, paper episode or prototype change. Use one method for a focused
revision or combine methods around an existing game. A large design document,
score, victory condition or simulation is not required.

## What you can do

- Shape actions, timing, actor knowledge, space and encounters with
  [gameplay design](skills/gameplay-design/SKILL.md).
- Build inference paths and assistance that players can use with
  [information design](skills/game-information-design/SKILL.md).
- Connect places, world relationships and conditional scenes with
  [world and narrative design](skills/game-world-narrative-design/SKILL.md).
- Make resources, progression, loss, recovery and saved-state changes work
  together with [systems design](skills/game-systems-design/SKILL.md).
- Design shared decisions, access, stopping, returning and paid rights with
  [participation design](skills/game-participation-design/SKILL.md).
- Create and select a meaningful set of encounters or other game content with
  [content design](skills/game-content-design/SKILL.md).
- Compose and adapt those relationships across an existing game with
  [game design](skills/game-design/SKILL.md).

The supported package is the complete set of seven skill directories. Choose an
entry directly for a narrow task; the general `game-design` method is not a
mandatory router. The methods link to sibling references when a design decision
crosses their boundaries.

## Demonstration

[East Gate](examples/adaptation/README.md) is a small playable puzzle about
adapting a clue to a different language and display. Its Russian version presents
one line at a time, lets the player pin lines, and accepts the direction encoded
by their first letters. A correct choice opens a gate and supplies the next scene;
a wrong direction remains a valid retry. The example consumer checks the content
and action relationships, not language quality or human experience.

For tasks that need executable artifact evidence, use the optional
[strategy matrix](examples/strategy-matrix/README.md),
[Ink episode](examples/ink-episode/README.md), or
[glTF/GLB inspection](examples/gltf-artifacts/README.md). Their dependencies
are prepared in task-owned directories; paper and prose work installs none.

## Access

Browse the [source](https://github.com/Muratovnik/gamedesign-skills) or download
the [v0.1.1 source release](https://github.com/Muratovnik/gamedesign-skills/releases/tag/v0.1.1).
The release archive contains the complete source bundle under `game-design/`.
For direct use, give your agent the absolute path to that directory, your game's
root and current artifact, the intended change, and the actions it is permitted
to take. Have it read the applicable `skills/<name>/SKILL.md` and references.
This route does not require client registration.

Some tasks use general research or engineering methods maintained separately in
[Assay](https://github.com/Muratovnik/assay). The shipped binder is pinned to
Assay 0.17.2 at commit
[`94c517b0aac9ba2575086bf9aead1cc828aadb0d`](https://github.com/Muratovnik/assay/tree/94c517b0aac9ba2575086bf9aead1cc828aadb0d).
Obtain that source separately when the task needs it; the package does not
install Assay. For the verified explicit-source route and its caller-state
condition, see the [consumer contract](skills/game-design/references/consumer-and-assay-contract.md).

## Quick start

To apply a method, give your agent the current game artifact, your goal and the
actions it may take, then have it read the relevant skill and references. This
plain-source route needs no Python. To run the included East Gate consumer, use
Python 3.11 or newer. From the extracted `game-design/` directory, run this
command in Bash:

```bash
mkdir -p tmp
python3 examples/adaptation/consumer.py \
  --artifact examples/adaptation/fixtures/east-gate-ru.json \
  --expect-revision east-gate-ru-2 \
  --pin 1 --pin 2 --pin 3 --pin 4 --pin 5 --pin 6 \
  --choose east \
  --output tmp/east-gate-result.json
```

For Windows PowerShell instructions, see the [East Gate example guide](examples/adaptation/README.md#run-the-example).

The command prints an `executed` result with `gate` set to `open`. The JSON file
contains the pinned notebook, ferry token and next scene. The output file must be
new; choose another name if you have already run the command. This is a
deterministic example path, not a report of a run on your machine. The
[East Gate guide](examples/adaptation/README.md) explains the wrong-turn and
invalid-content cases.

## Documentation

- [Installation](docs/installation.md) separates direct source use from optional
  Codex and Claude Code plugin registration and its update/removal procedures.
- [Compatibility](docs/compatibility.md) records the current dependency and
  client-qualification boundaries.
- [Example guide](docs/examples.md) maps methods to playable studies and tools.
- [Russian quick start](docs/quickstart.ru.md) provides the first-use route in
  Russian.
- [Design decisions](docs/decisions.md) and [research limits](docs/late-comparison.md)
  explain the package's design basis.

## Limits

The examples are synthetic. Deterministic and headless checks establish only the
properties they inspect; they do not establish player perception, human
experience, automatic client discovery, arbitrary-engine compatibility or
general model quality. Recorded fresh-Linux checks exercised the local-source
manager lifecycle for Codex 0.159.2 and Claude Code 2.1.289, including installed
resource use. This is separate from automatic model selection or adherence;
see the [compatibility record](docs/compatibility.md#native-client-qualification).

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for source ownership and maintainer
checks.

## License

The package is available under the [MIT License](LICENSE). Technical
plugin-schema material has the additional terms described in [NOTICE.md](NOTICE.md).
