# Compatibility and claim boundaries

The supported package is the complete seven-skill source bundle. A version
label alone does not establish support for every consumer, engine or game. Record
the package revision/digest, relevant dependency versions, client/build and route,
interpreter or engine, artifact schema and actual game revision.

The comparative additions are unreleased changes on the 0.1.1 source line. Their
qualified runtime snapshot is commit
`1873993a6491b52fe8288c19837600a012e18d4d`; later documentation/evidence revisions
do not change that snapshot's identity. The
[verification record](reviews/2026-10-08-comparison/README.md) records final scope
and any later drift. No new release is implied by this PR.

| Component or route | Current boundary |
| --- | --- |
| Game Design | Complete seven-skill bundle; exact revision matters for unreleased additions |
| Assay | Binder requires 0.17.2 at `94c517b0aac9ba2575086bf9aead1cc828aadb0d`; separately obtained, no automatic installation |
| Python | Existing examples require Python 3.11 or newer; actual new numerical tests use 3.12.14 locally and 3.12.15 in CI |
| Development packages | `requirements-dev.txt`; nothing is downloaded on skill load |
| Zero-sum operation | SciPy 1.17.0 with NumPy 2.3.5 in review/paired tasks and 2.5.3 in a fresh documented install, actually exercised on Linux; finite two-player zero-sum binary64 utility only |
| Native Ink | Node 24.19.0 locally, inkjs 2.4.0, compiled format 21; explicit documented source/action/state contract, no host integration claim |
| glTF/GLB | Node 24.19.0 locally, glTF-Validator 2.0.0-dev.3.10; conformance with declared resource/coverage boundaries, no engine import or asset-fidelity claim |
| Godot | Earlier episode receipts use 4.7.2; reused only for unchanged episode files and claims, not rerun as part of the new adapters |
| Package gates | Static/projection/build/smoke and existing Python suites passed in Linux and Windows CI at the qualified snapshot |
| Codex native route | CLI 0.159.2, fresh Linux user, local marketplace and trusted project setting; exact inventory/lifecycle and installed-resource action observed |
| Claude Code native route | 2.1.289, fresh Linux user, local scope; exact inventory/lifecycle and effective-source action observed; disabled model-session exclusion unestablished |
| Other native client/platform combinations | Not qualified by these Linux native receipts; Windows package gates are a different claim |
| Human and material observations | Examples are synthetic; no user study or perceptual result |
| Model comparison | Six completed pairs using explicit source loading; all four changed operations used; scoped outcomes in the [model record](reviews/2026-10-08-comparison/model-comparison.md), no general superiority inferred |

## Native client qualification

[Installation](installation.md) defines source identity, scope, conflict handling
and commands for use, update, disable, removal and rollback. Manifest validation,
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

## Runtime needs and recheck policy

Plain methods and paper examples require an authorized text reader. Source
binding and East Gate use Python's standard library. Schema validation and
analysis use their listed packages. Godot is needed only for its native episode.
The three new references explain task-local dependency preparation and exact
artifact boundaries. No dependency is installed when a skill is read.

After a change, read the affected delta and check its actual action/consumer,
including a valid neighbor and a discriminating defect where relevant. A client
update can invalidate discovery evidence without changing game rules; a schema
or game update can invalidate a consumer path while listing still works. Retain
only the historical checks whose bytes, conditions and claims remain applicable.
