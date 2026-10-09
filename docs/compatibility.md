# Compatibility and claim boundaries

The supported Game Design unit is the complete seven-skill source bundle. A
package version does not qualify every client, engine or game. For a reproducible
operation, record the package and relevant dependency versions, the client/build
and access route, interpreter or engine, artifact schema, and game revision.

| Component or route | Current boundary |
| --- | --- |
| Game Design | Version 0.2.0; use the complete source bundle |
| Assay | The shipped binder requires 0.17.2 at commit `94c517b0aac9ba2575086bf9aead1cc828aadb0d`; it does not install Assay |
| Python | Examples require Python 3.11 or newer; that does not establish other environment combinations |
| Python packages | Development dependencies are listed in `requirements-dev.txt`; reading a skill downloads no package |
| Godot | The included episode is checked with 4.7.2; this does not qualify other engines or arbitrary projects |
| Plugin manifests and marketplaces | Generated for the complete bundle; static gates check the selected local source, identity and required metadata |
| Codex native route | CLI 0.159.2, fresh Linux user; recorded local-source manager lifecycle, exact inventory and installed-resource action |
| Claude Code native route | 2.1.289, fresh Linux user and local scope; recorded manager/effective-source action; disabled model-session exclusion unestablished |
| GitHub marketplace installation | Official client source type; the package's recorded native lifecycle has not exercised this installation route |
| Zero-sum operation | SciPy 1.17.0; finite two-player zero-sum binary64 utility, independent best-response bounds; [contract](../skills/game-systems-design/references/zero-sum-analysis.md) |
| Ink | inkjs 2.4.0, compiled format 21; selected UTF-8 source/action/state contract; [boundary](../skills/game-world-narrative-design/references/ink-artifacts.md) |
| glTF/GLB | glTF-Validator 2.0.0-dev.3.10; resource and coverage limits, separate caller predicates; [contract](../skills/game-design/references/gltf-artifacts.md) |
| Other native platforms/builds | Not qualified by the retained Linux receipts; Windows package checks establish a different boundary |
| Human and material observations | Examples are synthetic; no user study or perceptual result is claimed |
| Model comparison | Six pairs with explicit source loading; [scoped results](reviews/2026-10-08-comparison/model-comparison.md), no discovery or general superiority claim |

The technical plugin schema is a separately attributed component. Game-specific
schemas are small contracts for the examples. This package does not claim
unbounded compatibility with all Assay, Godot or client versions.

## Native client qualification

[Installation](installation.md) describes the short GitHub-backed route and
the independently qualified local-source route. The receipts below cover
**local-source registration on Linux**, not GitHub-backed installation or
native Windows installation. Source identity, scope, conflicts, updates and
rollback have different requirements for each route. Manifest validation,
CLI help and explicit source reading are not automatic discovery evidence.

The fresh-user Linux job in
[run 37819498740](https://github.com/Muratovnik/gamedesign-skills/actions/runs/37819498740)
executed the real Codex 0.159.2 and Claude Code 2.1.289 managers. Its retained
receipt contains **72 commands and 24 observations**. Initial installed-plugin
inventories were empty; a separate original sentinel plugin was added to detect
registration interference. Both clients installed main, disabled and reenabled
it, replaced it with the candidate, restored main and removed the target. The
sentinel registration survived the target lifecycle; owned sentinel cleanup left
installed-plugin inventories empty. Task-owned work directories were retained.

| Boundary | Codex observation | Claude Code observation |
| --- | --- | --- |
| Inventory | Seven `game-design:<skill>` names with the intended plugin ID | Seven exact component names and local scope |
| Enabled state | Fresh app-server `skills/list` includes enabled target and omits disabled target | Native list's merged `enabled` changes; `details` still describes disabled components |
| Effective files | Managed plugin source paths; complete file sets and hashes match | `readFromFolder` is active for the local source, despite a separate cache; exact source paths/files checked |
| Replacement and rollback | Candidate 59-file runtime; restored main 48-file runtime | Same exact source-file comparisons, including surplus-file rejection |
| Useful operation | Verifier calls the installed observation resource and reopens its report | Verifier calls the effective-source observation resource and reopens its report |
| Model selection/adherence | Not established by this manager/metadata test | Not established; false enabled metadata is not a model-session exclusion test |

The replacement is uninstall/remove marketplace/add/install against retained
sources, including two different byte sets both labeled 0.1.1. It does not
qualify automatic marketplace upgrade, release-version migration or rollback of
game saves. The sentinel checks registration interference, not arbitrary plugin
persistent data. Source identity and output rows are checked; no arbitrary
consumer-project safety claim follows.

An independent reviewer verified the archive/receipt against both Git revisions
and all corrected scoped source hashes. Its 144 assertions inspect this one
receipt; they are not 144 separate game scenarios. The
[review and raw receipts](reviews/2026-10-08-comparison/README.md) preserve this
scope, the first failed verifier attempt and the subsequent corrections.

### Earlier attempts and model transport

The historical isolated bootstrap attempt failed before client metadata handling
because its filesystem lacked `/proc/self/exe`; attempted namespaces were denied.
That historical result is superseded for the successful hosted Linux manager
route, not erased or interpreted as package rejection.

In the current workspace, authenticated Codex metadata calls expose the model
and project skills, while attempted model turns did not begin. The bounded
attempts and the completed alternate comparison harness are retained in the
[model comparison](reviews/2026-10-08-comparison/model-comparison.md). An
authentication status or `model/list` result is not a completed model turn.
A separate read-only Claude 2.1.289 authentication check returned `loggedIn=false`
and `authMethod=none`; its hosted manager run did not have an authenticated
model conversation. The redacted result is retained in the verification record.
These limitations do not negate the observed native manager lifecycle and cannot
be filled by a verifier's explicit file read.

## Runtime needs

Plain methods and paper examples require an authorized text reader. Source
binding and East Gate use Python's standard library. Schema validation and
analysis examples use dependencies listed with the relevant source. Godot is
needed only for the native episode. Reading a skill downloads no runtime
dependency. The three optional operation references describe task-local
dependency preparation; reading a skill installs none.

## Recheck after changes

Read the affected source delta, rebuild relevant fixtures and check the changed
boundary, including a lawful alternative and a known defect where applicable. A
client update can invalidate discovery evidence without changing game rules; a
schema or game update can invalidate a consumer path while client listing still
works. Record those outcomes separately. The retained comparison records qualify
runtime snapshot `1873993a6491b52fe8288c19837600a012e18d4d` and their recorded
source identities. Changed adapter bytes require new runs and reports; historical
receipts are not rewritten to describe a later release.
