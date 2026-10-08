# Install, update and remove Game Design

Use the complete seven-skill bundle. Its sibling references and runtime resources
must stay together. Choose direct source reading, or register that same bundle
through the client's native plugin manager. Assay is obtained separately; see the
[consumer contract](../skills/game-design/references/consumer-and-assay-contract.md)
for the required revision and conditional method reads.

## Prepare a versioned source

Start with an authorized checkout or extract the source archive described in
[release preparation](releases.md). Verify its checksum against the accompanying
`SHA256SUMS`. Keep the complete extracted `game-design/` directory in a location
you own, outside client caches. Record `VERSION`, the archive checksum or checkout
commit, and the selected Assay revision. A version label alone does not identify
an edited checkout.

The shell examples use Bash. Replace both paths with your actual locations;
spaces are allowed when the variables stay quoted:

```bash
GAME_DESIGN_ROOT="/absolute/packages/game-design-0.1.1/game-design"
GAME_ROOT="/absolute/my-game"
```

Keep this source directory unchanged while it is registered. Updates use a new
directory so the previous bytes remain available for rollback. Client commands
below are actions for the installation owner; preparing an archive does not run
them or authorize changes to someone else's settings.

## Read directly

Give the agent these two roots, the current game artifact, the intended change
and relevant permissions. Have it read the applicable `skills/<name>/SKILL.md`
and conditional references. This route requires an authorized text reader and
no registration. To update or roll back, select the appropriate retained source
and matching Assay revision in a fresh task context. To stop using this route,
remove it from the consumer's active instructions; delete only a copy you own.

## Native package identity and ownership

Both generated marketplaces expose **`game-design@game-design-source`**. Their
`./` source is the package root, so the native manager receives the whole bundle.
`tools/render.py` owns both marketplace files and both plugin manifests;
`catalog.json` and `VERSION` own inventory and release identity. Do not edit a
generated marketplace to turn an installed copy into a second package.

Before adding or changing a registration, list the client's marketplaces and
plugins. Confirm that any existing `game-design-source` and `game-design` entry
belongs to this package and has the expected source, scope and revision. Resolve
a foreign same-name entry, a second provider or modified installed files with its
owner before proceeding. Keep local changes outside managed caches. Native
registrations and caches can be shared across projects: replacing their source
requires ownership of the affected uses, even when a project's enable setting
is local. Keep using a separate explicit source while such a conflict is open.

These procedures use the Codex CLI **0.159.2** interface and the documented Claude
Code **v2.1.289** interface. The latter supports
[validating a root containing both manifests](https://code.claude.com/docs/en/plugins/cli-reference#validate-a-directory).
The isolated Codex check on 2026-10-08 reached `--version`; marketplace listing
stopped during client bootstrap before registry or package metadata handling.
Native installation and lifecycle remain unverified for both clients;
[compatibility](compatibility.md#native-client-qualification) records the blocker
and the required receipts.
Run the relevant `--version` and subcommand `--help` before applying them to a
different build.

## Codex: registered local marketplace

This route uses Codex's configured marketplace registry and managed plugin cache.
Its CLI has no installation `--scope` flag. Run from the game repository:

```bash
cd "$GAME_ROOT"
codex plugin marketplace list --json
codex plugin list --json
codex plugin marketplace add "$GAME_DESIGN_ROOT" --json
codex plugin add game-design@game-design-source --json
codex plugin list --marketplace game-design-source --json
```

Check the returned source and installed identity before starting a fresh session.
The generated `.agents/plugins/marketplace.json` makes the package available;
installation remains an explicit native action. This uses the
[Codex local marketplace format](https://developers.openai.com/plugins/build/plugins#marketplace-metadata)
and the commands exposed by `codex plugin --help`.

For a trusted game repository, merge this single table into its
`.codex/config.toml`, preserving other settings:

```toml
[plugins."game-design@game-design-source"]
enabled = true
```

Set this value to `false` to disable the package for that repository. Project
configuration is loaded only for trusted projects; a disabled plugin may still
have cached files. The setting does not remove text already in a conversation.
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
and check a fresh session for remaining activation through another provider.

## Claude Code: local scope in the game repository

Use `local` for this user in this game repository. It writes the repository's
`.claude/settings.local.json`; `project` would share the declaration and `user`
would apply across projects. Keep the same scope throughout the lifecycle.
The [native scope rules](https://code.claude.com/docs/en/discover-plugins)
also explain precedence when another scope already enables the package.

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

The [native lifecycle commands](https://code.claude.com/docs/en/plugins/cli-reference)
for this scope are:

```bash
claude plugin disable game-design@game-design-source --scope local
claude plugin enable game-design@game-design-source --scope local
```

Run one according to the desired state, then start a fresh session. To remove:

```bash
claude plugin uninstall game-design@game-design-source --scope local --keep-data
claude plugin marketplace remove game-design-source --scope local
```

Remove the marketplace only after checking its other consumers: removing its last
declaration can uninstall its remaining plugins. `--keep-data` preserves plugin
data during the explicit uninstall; the game and saves should already live in
the consumer's workspace. Do not delete the client's state directories by hand.
Re-list the inventory and check a fresh session for other activation routes.

For a session-only development load, the native alternative is
`claude --plugin-dir "$GAME_DESIGN_ROOT"`. End that session and omit the flag to
stop that route. This can take precedence over an installed package of the same
name, so use it as an explicit alternative, not as evidence that registration
works.

## Update and roll back a registered copy

For either client, retain the earlier source, matching Assay selection, native
inventory and relevant settings outside managed roots before changing them.
Review the new release's methods, resources and dependency delta. Extract it to
a new directory and verify its checksum; keep the old directory intact.

For the local-source routes above, replace the registration explicitly:

1. Confirm ownership of the existing identity and its affected scopes. Disable
   it, then use the client's removal commands above for that exact identity and
   marketplace. Stop if the native manager reports a conflict or partial failure.
2. Set `GAME_DESIGN_ROOT` to the new validated directory. Repeat that client's
   add/install sequence with the same identity and scope. Restore the intended
   enabled setting, including an intentionally disabled state.
3. Verify the source/revision, full skill inventory and required sibling reads
   in a fresh session before accepting the replacement. If it fails, remove the
   failed registration and repeat the same sequence with the retained source and
   its Assay revision. Restore only the settings this change owned.

This replacement route also handles rollback and same-version development
copies without relying on a cache refresh to imply different bytes. If the old
copy predates native packaging, remove the new registration and return to its
explicit-source route. Package rollback does not undo changes to game artifacts
or save formats; those need the game's own recovery path.

For a separately chosen Git-backed marketplace, the clients also expose
`codex plugin marketplace upgrade game-design-source` and
`claude plugin marketplace update game-design-source`; Claude then offers
`claude plugin update game-design@game-design-source --scope local`. These
refresh the configured source, not an arbitrary prior version. Record its
immutable revision and use the source replacement above when an exact rollback
is required. Do not run an unqualified refresh across unrelated marketplaces.
