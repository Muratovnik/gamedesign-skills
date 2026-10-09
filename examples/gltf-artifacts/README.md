# Original glTF conformance examples

These small synthetic artifacts exercise the optional Game Design glTF consumer.
They are original fixtures, not copied sample assets or a prototype of a complete
game. The production CLI calls the official Khronos validator on their actual
bytes. It does not decode GLB locally or equate a triangle count with general
game quality.

## Prepare and run

From the source repository root, with Node 20+ and an authorized optional
dependency installation:

```sh
gltf_tools=$(mktemp -d)
cp skills/game-design/scripts/validate_gltf.cjs \
   skills/game-design/scripts/package.json \
   skills/game-design/scripts/package-lock.json "$gltf_tools/"
npm ci --prefix "$gltf_tools" --ignore-scripts --no-audit --no-fund
GD_GLTF_SCRIPT="$gltf_tools/validate_gltf.cjs" \
  node --test examples/gltf-artifacts/test_validation.cjs
node "$gltf_tools/validate_gltf.cjs" \
  examples/gltf-artifacts/fixtures/external.gltf \
  --resource-root examples/gltf-artifacts/fixtures
```

The tests require the actual pinned dependency; missing setup is a failed test,
not a skipped success. They create and remove temporary inputs and reports. One
test owns a local HTTP server to observe whether the adapter attempts a network
request; the adapter must reject the URI without contacting it. No model, native
agent client, engine import or human observation is part of this suite.

## What the fixtures distinguish

| Fixture | Independent construction / expected boundary |
| --- | --- |
| `signal-wedge.gltf` | Three positions `(-0.5, 0, 0)`, `(0.5, 0, 0)`, `(0, 0.75, 0)` as nine little-endian float32 values in an embedded data URI; one default triangle primitive; supported conformance |
| `signal-wedge.glb` | The same original scene with its 36 data bytes in a GLB BIN chunk; supported conformance |
| `bad-accessor.gltf` | Claims four VEC3 values in the same 36-byte view, which holds only three; `ACCESSOR_TOO_LONG` refutes conformance |
| `empty.gltf` | An asset declaration without geometry; legal format content, supported |
| `camera.gltf` | A perspective camera in a scene without meshes; supported |
| `external.gltf` + `positions.bin` | The original wedge with a local sidecar; supported only with its explicit resource root and successfully read bytes |
| `missing-resource.gltf` | Refers to an absent sidecar; unavailable evidence, not a conformance refutation caused merely by `IO_ERROR` |
| `remote-resource.gltf` | Refers to an HTTPS sidecar; unavailable under the local-only policy |
| `unsupported-extension.gltf` | Uses an intentionally unimplemented synthetic vendor extension; zero errors cannot establish extension conformance |
| `malformed.gltf` | Starts as JSON but is incomplete; the official `INVALID_JSON` error refutes conformance |
| `unrecognized.dat` | Is neither detected JSON glTF nor GLB; the API cannot perform the conformance check |

The GLB fixture has the standard 12-byte header, a JSON chunk padded with spaces
to a multiple of four bytes, and a 36-byte BIN chunk. It was constructed only as
test data and then checked by the real external validator. There is no production
GLB writer or parser in this example.

The suite also constructs temporary boundary cases: encoded local filenames,
outside-root paths, an escaping symlink with readable valid data, an allowed
in-root symlink, missing explicit resource permission, missing adjacent
dependency, zero-byte input, existing output files/symlinks and competing report
writers. The valid data behind an escaping symlink makes a failed containment
guard observable as an incorrect pass.

## Conformance and a caller's predicate

The Signal Wedge fixture contract independently expects one triangle, and its
test asserts that vendor-reported fact. The empty and camera fixtures are
accepted by the same CLI. A consumer expecting a visible wedge would still need
to reject or replace those artifacts for its own handoff; a consumer expecting a
camera could accept the camera artifact. The CLI receipt leaves this additional
predicate `not_evaluated`.

For an actual game, retain the checked artifact identity and perform the needed
import/action through that game's consumer. Shape, scale, collision, materials,
resource budgets, extension behavior and perceptual quality have their own
observations; a format report does not settle them. Full CLI statuses and report
semantics are in
[glTF artifacts](../../skills/game-design/references/gltf-artifacts.md).

Dependency: `gltf-validator` `2.0.0-dev.3.10`, official Khronos package, Apache-2.0
with bundled `NOTICES`. It is separately installed from the checked-in npm lock;
its bytes and third-party example assets are not distributed here.
