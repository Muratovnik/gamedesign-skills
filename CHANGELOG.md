# Changelog

## [Unreleased]

## [0.1.1] - 2026-10-08

### Fixed

- Reject invalid telemetry outcome definitions before counting results; apply the same knowledge, unlock, right, participation and history conditions to content choice and recovery. ([7b38546](https://github.com/Muratovnik/gamedesign-skills/commit/7b385469b95ffe40562e7161ea9c3cab7bec2b94))
- Require ordered save/reset/load and dialogue evidence, plus consistent saved and downstream state, before accepting a Godot reload claim. Validate threat identities and clock bounds, with warnings starting at tick 1. ([7b38546](https://github.com/Muratovnik/gamedesign-skills/commit/7b385469b95ffe40562e7161ea9c3cab7bec2b94))
- Keep refusal dialogue consistent before and after repair, and give the cloth-rack action a visible initial and changed state. ([7b38546](https://github.com/Muratovnik/gamedesign-skills/commit/7b385469b95ffe40562e7161ea9c3cab7bec2b94))
- Offer pin actions only when the content provides the aid; reject malformed Loom input without output files and return structured unavailable results for unreadable Assay resources. ([7b38546](https://github.com/Muratovnik/gamedesign-skills/commit/7b385469b95ffe40562e7161ea9c3cab7bec2b94))

### Changed

- Use the reviewed Assay 0.17.2 source with the binding verifier; Assay remains a separately obtained dependency. ([7b38546](https://github.com/Muratovnik/gamedesign-skills/commit/7b385469b95ffe40562e7161ea9c3cab7bec2b94))

### Added

- Configure the native Godot runner's finite phase timeout with `--timeout-seconds`, retaining the 30-second default. ([7b38546](https://github.com/Muratovnik/gamedesign-skills/commit/7b385469b95ffe40562e7161ea9c3cab7bec2b94))
- Include full-bundle Codex and Claude marketplaces and instructions for installation, scope, conflicts, update, disable, removal and rollback. Native client lifecycle qualification remains unverified; see [compatibility](https://github.com/Muratovnik/gamedesign-skills/blob/v0.1.1/docs/compatibility.md#native-client-qualification). ([7b38546](https://github.com/Muratovnik/gamedesign-skills/commit/7b385469b95ffe40562e7161ea9c3cab7bec2b94))

## [0.1.0] - 2026-10-08

First stable source release of Game Design: seven composable methods for
creating and revising playable games, with original paper and executable
examples, semantic consumers, and versioned state and content adapters. The
supported unit is the complete seven-skill bundle. This release does not claim
native client discovery, human playtest results, model-comparison results or
qualification for arbitrary game engines.
