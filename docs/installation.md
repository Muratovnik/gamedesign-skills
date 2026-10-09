# Install and use Game Design

Install the whole Game Design plugin through a native marketplace, or read the
skills directly from a source directory. Installing the skills does not require
Python or a game engine. Optional executable examples describe their own
dependencies.

## Install from GitHub

Use a plugin-capable Codex or Claude Code CLI. The public repository contains
both marketplace manifests, so no source archive or manual checkout is needed
for this route. These shell commands also work in Windows PowerShell.

### Codex

```bash
codex plugin marketplace add Muratovnik/gamedesign-skills
codex plugin add game-design@game-design-source
codex plugin list --marketplace game-design-source --json
```

Confirm the installed identity and the skill inventory. The Codex marketplace
registration and plugin installation are client-managed, not scoped to one game
repository. To control whether the plugin is enabled in a trusted repository,
use the [project configuration](#codex-registered-local-marketplace) below.

### Claude Code

Run from the game repository to use its `local` settings rather than a
user-wide scope:

```bash
claude plugin marketplace add Muratovnik/gamedesign-skills --scope local
claude plugin install game-design@game-design-source --scope local
claude plugin list
claude plugin details game-design
```

Check that the intended plugin and skills are listed, then start a fresh
session. If `game-design-source` or `game-design` already exists, inspect its
source and scope first. Do not replace another provider's registration.

The native GitHub-source format is described in
[Codex plugin packaging](https://developers.openai.com/plugins/build/plugins#add-a-marketplace-from-the-cli)
and [Claude Code marketplaces](https://code.claude.com/docs/en/plugin-marketplaces#host-your-marketplace).
The project's recorded native lifecycle checks use **local sources** on Linux;
they do not yet qualify the GitHub-source commands or native Windows
installation. See [compatibility](compatibility.md#native-client-qualification).

## First use

Open a new session. Name the appropriate skill and supply a game artifact,
intended change and allowed actions. To try a method without a game repository:

> Use Game Design's `gameplay-design` skill. An enemy charges for 0.6 seconds
> and strikes one tile, but its warning appears only 0.1 seconds before
> impact. Revise the warning and player-response rules. Give exact timing,
> legal responses and a failure case. Do not change code.

This is an example prompt, not a recorded model run or a player playtest. The
[Russian quick start](quickstart.ru.md) gives the same first-use route.

## Use source files directly


Start with an authorized checkout or download the
[v0.2.0 source archive](https://github.com/Muratovnik/gamedesign-skills/releases/tag/v0.2.0)
and extract it. For an archive, verify its checksum against the accompanying
`SHA256SUMS`. Keep the full `game-design/` directory in a
location you own, outside client caches. Record `VERSION` and the archive
checksum or checkout commit; a version label alone does not identify edits in a
checkout.

The commands below use Bash. Replace these example paths with the actual source
and game locations; keep the quotes if a path contains spaces:

```bash
GAME_DESIGN_ROOT="/absolute/packages/game-design-0.2.0/game-design"
GAME_ROOT="/absolute/my-game"
```

In Windows PowerShell, use `$GameDesignRoot` and `$GameRoot` instead of the
Bash variables, or put the actual absolute path in quotes:

```powershell
$GameDesignRoot = "C:\\packages\\game-design-0.2.0\\game-design"
$GameRoot = "C:\\projects\\my-game"
```

For direct source use, give the authorized text reader those two roots, the
current game artifact, the intended change and relevant permissions. Have it
read the applicable `skills/<name>/SKILL.md` and conditional references. This
route requires no client registration. To stop using it, remove the source path
from the consumer's active instructions; delete only a source copy you own.

## Advanced: register a local source directory

Use the following commands only when you have an extracted source directory
that you want the native client to register, rather than the GitHub
marketplace above.

Both generated marketplaces expose **`game-design@game-design-source`**. Their
`./` source is the package root, so a native manager receives the whole bundle.
`tools/render.py` owns both marketplace files and plugin manifests;
`catalog.json` and `VERSION` own inventory and release identity. Do not edit a
generated marketplace to make an installed copy appear to be a second package.

Before adding or changing a registration, list the client's marketplaces and
plugins. Confirm that any existing `game-design-source` and `game-design` entry
belongs to this package and has the expected source, scope and revision. Resolve
a foreign same-name entry, second provider or modified installed files with its
owner before proceeding. Keep local changes outside managed caches. Native
registrations and caches can be shared across projects: replacing their source
requires ownership of the affected uses, even when a project's enable setting
is local. Keep using a separate explicit source while such a conflict is open.

These procedures use the Codex CLI **0.159.2** interface and the documented
Claude Code **v2.1.289** interface. The latter supports
[validating a root containing both manifests](https://code.claude.com/docs/en/plugins/cli-reference#validate-a-directory).
Recorded fresh Ubuntu/Linux checks exercised install, exact seven-skill
inventory, disable/re-enable, source replacement, rollback, removal, preservation
of an unrelated registration, execution of the installed observation resource,
and reopening of its report.
The [compatibility record](compatibility.md#native-client-qualification) names
the tested source and boundary. Manager evidence does not establish model
selection, adherence or another operating system. Run the relevant `--version` and
subcommand `--help` before applying these commands to a different build.

### Codex: registered local marketplace

This route uses Codex's configured marketplace registry and managed plugin
cache. Its CLI has no installation `--scope` flag. Run from the game repository:

```bash
cd "$GAME_ROOT"
codex plugin marketplace list --json
codex plugin list --json
codex plugin marketplace add "$GAME_DESIGN_ROOT" --json
codex plugin add game-design@game-design-source --json
codex plugin list --marketplace game-design-source --json
```

Check the returned source and installed identity before starting a fresh
session. In this build skill names are namespaced, for example
`game-design:game-systems-design`; metadata records source path and enabled state.
The qualifier compared the complete runtime file set and hashes.
The generated `.agents/plugins/marketplace.json` makes the package
available; installation remains an explicit native action. This uses the
[Codex local marketplace format](https://developers.openai.com/plugins/build/plugins#marketplace-metadata)
and commands exposed by `codex plugin --help`.

For a trusted game repository, merge this table into its `.codex/config.toml`,
preserving other settings:

```toml
[plugins."game-design@game-design-source"]
enabled = true
```

Set the value to `false` to disable the package for that repository. Project
configuration is loaded only for trusted projects; a disabled plugin may still
have cached files. This setting does not remove text already in a conversation.
The native
[project enable rules](https://developers.openai.com/plugins/build/plugins#enable-or-disable-a-plugin-for-a-repo)
apply to that repository; the registry and cache remain client-owned.

To remove this owned registration and cache:

```bash
codex plugin remove game-design@game-design-source --json
codex plugin marketplace remove game-design-source --json
```

Remove the corresponding project table only if this installation owns it. Keep
other configuration and the saved source copies. Re-list the native inventory
and check a fresh session for activation through another provider.

### Claude Code: local scope in the game repository

Use `local` for this user in this game repository. It writes the repository's
`.claude/settings.local.json`; `project` would share the declaration and `user`
would apply across projects. Keep the same scope throughout the lifecycle. The
[native scope rules](https://code.claude.com/docs/en/discover-plugins) explain
precedence when another scope already enables the package.

```bash
cd "$GAME_ROOT"
claude plugin marketplace list
claude plugin list
claude plugin validate "$GAME_DESIGN_ROOT"
claude plugin marketplace add "$GAME_DESIGN_ROOT" --scope local
claude plugin install game-design@game-design-source --scope local
claude plugin list
claude plugin details game-design
```

Expect the intended identity, local scope and seven skills in the component
inventory. A successful validator checks structure; the final inventory and
fresh-session checks establish later boundaries. The package uses a
[relative source in a local marketplace](https://code.claude.com/docs/en/plugin-marketplaces#write-relative-paths-from-the-marketplace-root).

In this build native listing may expose `readFromFolder` for the effective
local source and `installPath` for a separate cache. Verify the effective files;
`details` can still describe disabled components. A disabled metadata entry
does not establish exclusion from a fresh model session.

The [native lifecycle commands](https://code.claude.com/docs/en/plugins/cli-reference)
for this scope are:

```bash
claude plugin disable game-design@game-design-source --scope local
claude plugin enable game-design@game-design-source --scope local
```

Run the command for the desired state, then start a fresh session. To remove:

```bash
claude plugin uninstall game-design@game-design-source --scope local --keep-data
claude plugin marketplace remove game-design-source --scope local
```

Remove the marketplace only after checking its other consumers: removing its
last declaration can uninstall its remaining plugins. `--keep-data` preserves
plugin data during the explicit uninstall; the game and saves should already
live in the consumer's workspace. Do not delete client state directories by
hand. Re-list the inventory and check a fresh session for other activation
routes.

For a session-only development load, use the native alternative
`claude --plugin-dir "$GAME_DESIGN_ROOT"`. End that session and omit the flag to
stop that route. This can take precedence over an installed package of the same
name, so it is not evidence that registration works.

## Update or roll back

For GitHub-backed installations, the clients expose marketplace refresh
commands (`codex plugin marketplace upgrade game-design-source` and
`claude plugin marketplace update game-design-source`). Claude Code also
offers `claude plugin update game-design@game-design-source --scope local`.
Check the installed revision and skills again after updating; a marketplace
refresh alone is not evidence that the installed files changed. The recorded
project qualification covers local-source replacement, not GitHub upgrade.

### Local-source replacement and rollback


For either client, retain the earlier source, matching Assay selection, native
inventory and relevant settings outside managed roots before changing them.
Review the new release's methods, resources and dependency delta. Extract it to
a new directory and verify its checksum; keep the old directory intact.

For the local-source routes above, replace a registration explicitly:

1. Confirm ownership of the existing identity and its affected scopes. Disable
   it, then use the client removal commands above for that exact identity and
   marketplace. Stop if the native manager reports a conflict or partial failure.
2. Set `GAME_DESIGN_ROOT` to the new validated directory. Repeat that client's
   add/install sequence with the same identity and scope. Restore the intended
   enabled setting, including an intentionally disabled state.
3. In a fresh session, verify the source/revision, full skill inventory and
   required sibling reads. If verification fails, remove the failed registration
   and repeat the same sequence with the retained source and its Assay revision.
   Restore only the settings this change owned.

This replacement route handles rollback and same-version development copies
without relying on a cache refresh to imply different bytes. If the old copy
predates native packaging, remove the new registration and return to its
explicit-source route. Package rollback does not undo changes to game artifacts
or save formats; use the game's recovery path for those.

For a separately chosen Git-backed marketplace, the clients also expose
`codex plugin marketplace upgrade game-design-source` and
`claude plugin marketplace update game-design-source`; Claude then offers
`claude plugin update game-design@game-design-source --scope local`. These
refresh the configured source, not an arbitrary prior version. Record its
immutable revision and use the source-replacement procedure above for an exact
rollback. Do not run an unqualified refresh across unrelated marketplaces.
