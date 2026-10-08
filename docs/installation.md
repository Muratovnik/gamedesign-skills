# Use, update and remove Game Design

## Read from a local source tree

The simplest route is to keep the complete repository in a location the
consumer is authorized to read. Give the agent the absolute Game Design root,
game root and current artifact, along with the goal and relevant permissions.
Have it read the applicable `SKILL.md` and any references needed for the task.
This explicit source route needs no global registration.

Use the full seven-skill bundle. A single entry can depend on a sibling
reference, so copying one directory alone is outside the supported package
contract. General methods are maintained separately by Assay. Provide the
consumer's authorized Assay source when the operation needs one; the optional
[binding tool](../skills/game-design/scripts/bind_assay.py) can verify and read
the selected method. It cannot attest that a client has granted permission.

## Client projections

The root `plugin.json` and `.claude-plugin/plugin.json` are prepared source
projections over the shared `skills/` directory. Schema validation checks
structure only. Client listing, namespacing, automatic selection, sibling
resolution, disabled behavior and removal require testing with the relevant
client and build. No automatic discovery or native lifecycle support is
claimed here.

For Codex's local skill route, a consumer may use its existing management
tools to place the complete bundle in an authorized project or user
`.agents/skills` location. Check the current client documentation and actual
enabled inventory; a readable cache does not prove that a skill is enabled.
System-owned directories are not managed by this package.

## Lifecycle guidance

Before registering a copy, inspect existing entries, target paths, link targets
and their owner. Resolve same-name or modified-file conflicts with the owner.
Keep an earlier source copy available while evaluating an update.

| Operation | Guidance | Acceptance boundary |
| --- | --- | --- |
| Use | Read the complete source bundle from an authorized path | Fresh task context reads the intended entry and its required references |
| Update | Obtain a new source copy beside the current one and inspect the method, contract and dependency changes | The selected source bytes and relevant consumer behavior are checked |
| Disable | Use the client's documented control for the registration route in use | A fresh session does not activate the disabled registration; already read text may remain in context |
| Remove | Remove only package files and registrations whose ownership is established, through their owner | No package-owned activation route remains; unrelated skills, game files and saves are preserved |
| Roll back | Restore the prior package source and compatible dependency selection | Re-run the affected consumer path; package rollback does not reverse a game-save migration |

Client-native lifecycle operations are consumer actions. The source repository
does not change a user's client settings, game files or registrations.
