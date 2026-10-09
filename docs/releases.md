# Prepare a source release

**Status: current.**

This procedure is for maintainers preparing a Game Design source release. The
repository's pinned project-native Release Kit in `.github/relkit.pyz` reads
`relkit.toml`; that configuration defines the archive assets, local checks,
smoke test, owner audit and required publication guard. Use this repository
entry point so the configured policy is applied.

The public [v0.2.0 release](https://github.com/Muratovnik/gamedesign-skills/releases/tag/v0.2.0)
is an existing release record. For a future candidate, choose the intended
version, update `VERSION` and `CHANGELOG.md`, and finish the source changes from
the repository root. Before preparation, commit those files and all other
candidate source changes; the checkout must be clean because the candidate is
pinned to a Git revision. The project-native tool is Release Kit 0.31.0. Inspect
its supported interface without preparing a candidate:

```text
python .github/relkit.pyz --version
python .github/relkit.pyz release --help
python .github/relkit.pyz audit --help
```

These commands print the pinned tool version and available options. They do not
prepare or publish a release.

## Validate the checkout

Run the owner audit with history after committing the candidate changes and
confirm the working tree is clean. `--history` inspects publishable branches and
tags and requires a clean worktree; `--owner` requires the private owner policy
and managed pre-push guard. This matches the repository's `owner_audit` and
`require_guard` release settings. The audit checks publication policy, secrets,
links, history and owner requirements. The local project and example checks
are listed in [Contributing](../CONTRIBUTING.md#run-the-maintainer-checks) and
are also configured to run during candidate preparation.

```text
git status --short
python .github/relkit.pyz audit --history --owner
```

Run from the repository root with Python 3.11 or newer and the development
dependencies installed from `requirements-dev.txt`. On Windows, use
`.venv\Scripts\python.exe` in place of `python` when working in the
repository's virtual environment. `git status --short` must print no paths
before the audit; the audit must pass before candidate preparation. Passing it does not
establish human experience, automatic discovery or model effectiveness.

## Prepare and review a candidate

After the checkout is ready, the native `release prepare` command runs the
configured local checks, builds the versioned source assets and records a
candidate for review. The configured assets are
`gamedesign-skills-<version>-source.zip` and `SHA256SUMS`. Use a version that
matches the reviewed `VERSION` and changelog entry.

```text
python .github/relkit.pyz release prepare <version>
python .github/relkit.pyz release plan <version>
```

Replace `<version>` with the intended stable version, for example `0.1.2` for a
new patch candidate. Preparation produces a candidate and its configured
assets; planning prints the proposed tag, destination and publication effects
for review. Confirm the planned source revision, asset names and digest before
continuing. If the plan is wrong or the checks fail, stop and correct the
candidate before planning again.

## Publish reviewed bytes

Publication is a separate explicit command. Read the plan and use its exact
fingerprint as `<plan-hash>`; `--publish` authorizes the reviewed tag,
destination and publication effects. The project requires its configured
publication guard. The GitHub publisher also needs the configured repository
and sufficient access.

```text
python .github/relkit.pyz release run <version> --publish --plan-hash <plan-hash>
```

The result records publication status and the tool's receipts. Verify the
published source revision and both configured assets before treating the
release as complete. For a recorded attempt that was interrupted, inspect its
status and follow the native tool's `resume` procedure; do not prepare a second
candidate from an unknown partial state. The project-pinned
[Release Kit local-release guide](https://github.com/Muratovnik/release-kit/blob/v0.31.0/docs/local-releases.md)
covers the native release lifecycle and interrupted attempts.
