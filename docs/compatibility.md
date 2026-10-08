# Compatibility and claim boundaries

The supported package is the complete seven-skill source bundle. A version
label alone does not establish support for every consumer, engine or game. A
reproducible operation should record the package version, relevant dependency
versions, client/build and route, interpreter or engine, artifact schema, and
actual game revision.

| Component or route | Current boundary |
| --- | --- |
| Game Design | Version 0.1.0; use the complete source bundle |
| Assay | The shipped binder requires 0.17.1 at commit `1dbb7435d5349cb00cb4a2c8ffb5e00a2d703c03`; no automatic installation |
| Python | Examples require Python 3.11 or newer; other environment combinations are not established by that statement alone |
| Python packages | Development dependencies are listed in `requirements-dev.txt`; no package is downloaded on skill load |
| Godot | The included episode is checked with 4.7.2; this does not qualify other engines or arbitrary projects |
| Plugin manifests | Schema validity establishes manifest structure, not successful client loading |
| Client discovery and lifecycle | Automatic discovery, selection and removal need verification in the target client's current build |
| Human and material observations | Examples are synthetic; no user study or perceptual result is claimed |
| Model comparison | No model-quality campaign or improvement claim is made |

The technical plugin schema is a separately attributed component. Game-specific
schemas are small contracts for the examples. There is no unbounded compatibility
claim for all Assay, Godot or client versions.

## Runtime needs

Plain methods and paper examples require an authorized text reader. Source
binding and East Gate use Python's standard library. Schema validation and
analysis examples use the dependencies listed with the relevant source. Godot
is needed only for the native episode. No runtime dependency is downloaded when
a skill is read.

## Recheck after changes

Read the affected source delta, rebuild relevant fixtures and test the changed
boundary, including a lawful alternative and a known defect where applicable.
A client update can invalidate discovery evidence without changing game rules;
a schema or game update can invalidate a consumer path while client listing
still works. Keep those outcomes separate.
