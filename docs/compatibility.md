# Compatibility and claim boundaries

The supported Game Design unit is the complete seven-skill source bundle. A
package version does not qualify every client, engine or game. For a reproducible
operation, record the package and relevant dependency versions, the client/build
and access route, interpreter or engine, artifact schema, and game revision.

| Component or route | Current boundary |
| --- | --- |
| Game Design | Version 0.1.1; use the complete source bundle |
| Assay | The shipped binder requires 0.17.2 at commit `94c517b0aac9ba2575086bf9aead1cc828aadb0d`; it does not install Assay |
| Python | Examples require Python 3.11 or newer; that does not establish other environment combinations |
| Python packages | Development dependencies are listed in `requirements-dev.txt`; reading a skill downloads no package |
| Godot | The included episode is checked with 4.7.2; this does not qualify other engines or arbitrary projects |
| Plugin manifests and marketplaces | Generated for the complete bundle; static gates check the selected local source, identity and required metadata |
| Codex native route | Concrete local marketplace procedure for CLI 0.159.2; isolated version command passed, marketplace listing stopped at bootstrap; native lifecycle unverified |
| Claude Code native route | Procedure based on the documented v2.1.289 CLI interface, using explicit local scope; exact-build lifecycle receipt pending |
| Human and material observations | Examples are synthetic; no user study or perceptual result is claimed |
| Model comparison | No model-quality campaign or improvement claim is made |

The technical plugin schema is a separately attributed component. Game-specific
schemas are small contracts for the examples. This package does not claim
unbounded compatibility with all Assay, Godot or client versions.

## Native client qualification

[Installation](installation.md) describes the source, identity, scope, conflict
handling, commands, update, disable, removal and rollback procedures. These
routes remain part of the delivery obligation. Manifest validation, CLI help and
an explicit file read do not qualify automatic discovery or native lifecycle.

Before claiming a client/build combination supported, retain its exact version,
source revision or checksum, actual settings scope and native outputs from an
authorized disposable environment. Observe add/install, listing of all seven
skills, a selected method and its conditional sibling read, disable in a fresh
session, removal, an update and restoration of the earlier revision. Check that
unrelated registrations and consumer artifacts remain intact. Record native
listing, actual loading and model selection separately; selection or quality
claims require their own authorized model runs.

On 2026-10-08 a copied Codex 0.159.2 binary returned `--version` successfully
inside a verified disposable filesystem root. `plugin marketplace list --json`
then exited 1 during bootstrap because `/proc/self/exe` was unavailable. Creating
a separate procfs in fresh user, mount and PID namespaces failed with `EPERM`
before the next client payload ran. The registry and Game Design metadata were
not reached; this probe provides no native metadata acceptance or rejection.
No add/install, effective disable, removal, update or rollback was executed.

Those native lifecycle receipts, Claude Code execution and Windows behavior are
still pending. Replacing only `CODEX_HOME` does not establish an isolated client
environment: project, personal and managed lookup paths must also be accounted
for. Use a disposable machine or a verified complete isolation boundary for
qualification, rather than probing an owner's live configuration. A static
packaging check does not imply a model campaign.

## Runtime needs

Plain methods and paper examples require an authorized text reader. Source
binding and East Gate use Python's standard library. Schema validation and
analysis examples use dependencies listed with the relevant source. Godot is
needed only for the native episode. Reading a skill downloads no runtime
dependency.

## Recheck after changes

Read the affected source delta, rebuild relevant fixtures and check the changed
boundary, including a lawful alternative and a known defect where applicable. A
client update can invalidate discovery evidence without changing game rules; a
schema or game update can invalidate a consumer path while client listing still
works. Record those outcomes separately.
