# Prepare a source release

**Status: current.**

Release preparation builds a deterministic source archive and records its
digest. It does not publish the repository, create a remote release or register
skills in a client.

From the repository root, build the selected version into a new output
directory:

```bash
python tools/release.py build --output dist --version 0.1.0
```

The command creates `gamedesign-skills-0.1.0-source.zip` and `SHA256SUMS` in
`dist/`. Check the command result and digest before sharing the archive. Keep
the source version and archive identity together when recording a later
compatibility or support claim.

The prepared archive is source material. Native client discovery and lifecycle,
human playtest results, model comparisons and arbitrary-engine support require
their own evidence and are not implied by a successful build.

## Check the candidate

Create the isolated environment described in [the README](../README.md#quick-start).
On Windows its interpreter is `.venv/Scripts/python.exe`; on Unix it is
`.venv/bin/python`. Run the source and example unit suites, then:

```text
python .github/relkit.pyz audit
python tools/smoke.py --assets dist --version 0.1.0 --temp tmp/release-smoke
```

The smoke consumes the built archive, checks its checksum and version, extracts
it into a new directory, and plays East Gate through its later ferry consumer.
It does not rebuild the candidate. Use a fresh `--temp` path for another run.
Before publication, commit the reviewed files and run
`python .github/relkit.pyz audit --history`. An owner checkout also runs
`audit --history --owner` and `protect check` against its local private policy.

## Publish the reviewed bytes

`relkit.toml` selects the native GitHub publisher for
`Muratovnik/gamedesign-skills`. Release preparation and publication are separate:

```text
python .github/relkit.pyz release prepare 0.1.0
python .github/relkit.pyz release plan 0.1.0
python .github/relkit.pyz release run 0.1.0 --publish --plan-hash REVIEWED
```

Use the isolated environment's interpreter so the source checks have their
declared dependencies. Replace `REVIEWED` with the exact plan hash after reading
its source, assets and effects. Publication requires an existing GitHub
repository, GitHub CLI 2.98.0 or newer, the necessary repository access and
release immutability enabled. The first two commands do not authorize the third.
The optional hosted check matrix runs only for public repositories; it is not
required by this native publisher.

The [Release Kit local-release guide](https://github.com/Muratovnik/release-kit/blob/v0.31.0/docs/local-releases.md)
describes interrupted publication and verification. Keep candidate receipts
until the published files and source revision are verified.
