<div align="center">

# Game Design

Game design skills for AI agents working on playable games.

[![License: MIT](https://img.shields.io/badge/License-MIT-blue?style=flat-square)](LICENSE)
[![Check](https://img.shields.io/github/actions/workflow/status/Muratovnik/gamedesign-skills/check.yml?branch=main&style=flat-square)](https://github.com/Muratovnik/gamedesign-skills/actions/workflows/check.yml)
[![Release](https://img.shields.io/github/v/release/Muratovnik/gamedesign-skills?style=flat-square)](https://github.com/Muratovnik/gamedesign-skills/releases/latest)

</div>

Game Design is a skills plugin for Codex and Claude Code. It helps you design
or revise game actions, puzzles, worlds, economies and content in a new or
existing game. Work on one concrete rule or combine methods for a change
across systems. A large game design document, score, victory condition or
simulation is not required.

## What you can do

- Design actions, combat timing, actor behavior and encounters with
  [gameplay design](skills/gameplay-design/SKILL.md).
- Build puzzles, clues, learning sequences and player assistance with
  [information design](skills/game-information-design/SKILL.md).
- Connect places, inhabitants, quests and conditional scenes with
  [world and narrative design](skills/game-world-narrative-design/SKILL.md).
- Work out economies, progression, loss, recovery and persistent state
  together with [systems design](skills/game-systems-design/SKILL.md).
- Design shared play, access, leaving and returning with
  [participation design](skills/game-participation-design/SKILL.md).
- Create and select encounters, items and other related game content with
  [content design](skills/game-content-design/SKILL.md).
- Reconcile cross-system decisions or adapt an existing game with
  [game design](skills/game-design/SKILL.md).

The supported package is the complete collection listed in
[`catalog.json`](catalog.json). Choose a specialist directly for a focused task;
the general `game-design` method is not a mandatory router. Skills link to
related references when a decision crosses their boundary.

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

## Install

Use a plugin-capable Codex or Claude Code CLI. The commands below fetch the
public GitHub repository through each client's native plugin manager; they can
be entered in Bash or Windows PowerShell. Check the source and scope of any
existing `game-design-source` registration before adding another one.

**Codex**

```bash
codex plugin marketplace add Muratovnik/gamedesign-skills
codex plugin add game-design@game-design-source
codex plugin list --marketplace game-design-source --json
```

**Claude Code** — run from your game repository so `--scope local` applies to
that project.

```bash
claude plugin marketplace add Muratovnik/gamedesign-skills --scope local
claude plugin install game-design@game-design-source --scope local
claude plugin details game-design
```

Verify that the installed component inventory shows the Game Design skills,
then start a new session. The GitHub-source syntax is documented
by both clients, but this project's recorded native installation checks use a
**local source directory**, not the GitHub route. See
[installation and scope](docs/installation.md) and
[compatibility evidence](docs/compatibility.md#native-client-qualification).

For use without plugin registration, download the
[v0.2.0 source release](https://github.com/Muratovnik/gamedesign-skills/releases/tag/v0.2.0)
or clone the repository, then give your agent the authorized source directory,
game root and the applicable `skills/<name>/SKILL.md`. Reading methods this way
needs neither Python nor a plugin manager. General research and engineering
methods are maintained separately in
[Assay](https://github.com/Muratovnik/assay); Game Design does not install
Assay. Its exact pinned revision and conditional requirements are in the
[consumer contract](skills/game-design/references/consumer-and-assay-contract.md).

## Quick start

After installing the plugin, start a fresh session. To try one method without
preparing a game repository, send the following prompt:

> Use Game Design's `gameplay-design` skill. In a top-down game an enemy
> charges for 0.6 seconds and strikes one tile. The warning appears only
> 0.1 seconds before impact. Revise the warning and player-response rules.
> Give exact timings, the available player responses, and a failure case to
> check. Do not change code.

The result should describe a concrete action sequence with a plausible
failure case, rather than just naming design principles. This is an example
request, not a tested model run or player playtest.

For an existing game, supply its current rules or files, the desired change
and the actions the agent may take. Name the skill explicitly; installation
does not guarantee automatic selection. See the
[Russian quick start](docs/quickstart.ru.md).

## Documentation

- [Installation](docs/installation.md) covers GitHub installation, direct
  source use, scopes, updates and removal.
- [Compatibility](docs/compatibility.md) records the current dependency and
  client-qualification boundaries.
- [Example guide](docs/examples.md) maps methods to playable studies and tools.
- [Russian quick start](docs/quickstart.ru.md) provides the first-use route in
  Russian.
- [Design decisions](docs/decisions.md) and [research limits](docs/late-comparison.md)
  explain the package's design basis.

## Limits

The examples are synthetic. Deterministic and headless checks establish only
their inspected properties, not player perception, arbitrary-engine
compatibility or general model quality. Installed-resource loading and
automatic model selection are separate claims; their recorded evidence and
limits are in [compatibility](docs/compatibility.md).

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for source ownership and maintainer
checks.

## License

The package is available under the [MIT License](LICENSE). Technical
plugin-schema material has the additional terms described in [NOTICE.md](NOTICE.md).
