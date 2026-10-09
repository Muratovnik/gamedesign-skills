# Check a glTF artifact at the consumer boundary

Use this route when the actual handoff is a `.gltf` or `.glb` asset and checking
its format, links or accessor data could change the next action. Prefer the
consumer's existing suitable validator/import path. A task with no glTF artifact
does not need this dependency or an export into this format.

The optional [CLI](../scripts/validate_gltf.cjs) sends the artifact's actual bytes
to the official Khronos `gltf-validator`. It does not parse GLB itself or impose a
mesh, triangle, material or scene minimum. A valid empty document or camera-only
asset can satisfy this conformance check. Whether that artifact satisfies the
requested game handoff is a separate question.

## Run against the intended artifact

The adjacent [manifest](../scripts/package.json) and
[lock](../scripts/package-lock.json) pin `gltf-validator` to `2.0.0-dev.3.10`.
The CLI uses Node 20+ APIs. When installing this optional dependency is within
the task's authority, copy these three files to a task-owned tools directory and
install there. Do not install into the skill bundle, a global environment or an
unrelated project. The CLI deliberately requires this adjacent install instead
of searching an ambient parent or global package.

With `game_design_root` set to the actual resolved skill directory:

```sh
gltf_tools=$(mktemp -d)
cp "$game_design_root/scripts/validate_gltf.cjs" \
   "$game_design_root/scripts/package.json" \
   "$game_design_root/scripts/package-lock.json" "$gltf_tools/"
npm ci --prefix "$gltf_tools" --ignore-scripts --no-audit --no-fund
node "$gltf_tools/validate_gltf.cjs" /task/artifacts/marker.gltf \
  --resource-root /task/artifacts --output /task/evidence/marker-gltf.json
```

Use real task paths and an existing output parent directory. Omit `--output` to
receive the full JSON receipt on stdout. With `--output`, the same receipt is
also written to a new file; an existing file or symlink is never replaced. The
write publishes complete bytes with a same-filesystem hard link, so an output
filesystem without that operation leaves report delivery unavailable. Reopen the
saved receipt before handing it to the next consumer.

Embedded data URIs and GLB data are handled by the official validator. External
files are allowed only with an explicit `--resource-root`. URI paths resolve
against the canonical artifact location; a local file URL must also stay inside
that root. The resolver checks containment before and after `realpath`, rejects
escaping symlinks, and reads only regular files. Remote authorities/protocols,
query strings and fragments are unavailable through this route; it performs no
network fetch. Missing files and denied paths remain missing evidence even when
the underlying validator reports them as `IO_ERROR`.

Use stable, task-owned input directories. These path checks are not an operating
system sandbox against another process concurrently replacing ancestor paths or
changing file contents. Preserve the recorded bytes when reproducing a result.

## Interpret the receipt

| Exit / status | Meaning | Next consequence |
| --- | --- | --- |
| `0` / `supported` | The recorded validator completed its implemented checks with no errors, no reported coverage gap and the resources it requested available | Inspect remaining warnings and the actual consumer's requirements |
| `1` / `refuted` | The validator reported a conformance error in the inspected bytes | Revise the affected artifact or explain why this consumer requires a different valid representation |
| `2` / `unavailable` | Inputs, dependency, resource access, format detection or required validator coverage were unavailable | Obtain the missing means or use another suitable consumer; keep the unverified property open |

Recognizable malformed JSON can be **refuted** by the validator's `INVALID_JSON`
report. Empty bytes or an unrecognized format that causes the API to reject are
**unavailable** through this check. An unsupported or incompletely supported
extension also yields `unavailable`, even when `numErrors` is zero. If unavailable
resources or coverage coexist with reported errors, the overall result stays
unavailable; the complete original error report is retained for diagnosis.

The receipt contains the artifact path/size/SHA-256, successfully read sidecars
and failures, CLI/manifest/lock identities, exact installed package and runtime
versions, hashes of the executable dependency and its notices, and the original
validator report. Lock integrity identifies the expected npm archive; installed
file hashes identify the files used here. They do not assert that a modified
local installation still has the archive's integrity. Missing stages retain null
identities rather than fabricated ones.

If writing the requested report fails, exit `2` returns a `report_output` error
and the completed conformance receipt under `validation` on stdout. This delivery
failure does not turn a valid asset into a format violation.

## Keep the game requirement separate

Read `validator_report` for the predicate the validator actually checked. Leave
`caller_predicate` as `not_evaluated` until a separate consumer supplies its own
justified observation. For example, the original Signal Wedge fixture in the
source examples deliberately contains one triangle; an assertion about that
fixture is a different claim from whether a camera-only handoff is valid.

A game's visible marker might need a particular silhouette, scale and collision
behavior. Passing this CLI does not establish those properties. Import the
identified result into the actual consumer and test the relevant action there.
Likewise, an unsupported extension needs a checker or consumer that understands
it; suppressing the information message cannot provide that evidence. Preserve
both the conformance result and any separate caller result, each bound to the
artifact identity. Do not replace one with the other.

## Component and scope

Reuse: the official `gltf-validator` performs format, link and data checks; Node
provides URI/file handling, hashing and CLI argument parsing. The local adapter
owns only resource authorization, evidence classification and report delivery.
No validator implementation or third-party asset is vendored.

The package declares Apache-2.0 and includes `LICENSE` and `NOTICES` for bundled
components. Those files remain with the separately installed npm dependency.
The API and issue-code basis is the package's `README.md`, `index.js` and
`ISSUES.md` at `2.0.0-dev.3.10`; the associated
[upstream source](https://github.com/KhronosGroup/glTF-Validator/tree/bcd52cc4ba5f333b2999a58f67cc05ddf28b4fb1)
is a reference, not an installation of a newer default branch. The current
dependency's supported-extension list and coverage messages are preserved in
every completed receipt. Successful validation does not establish native skill
discovery, target-engine compatibility or human experience.
