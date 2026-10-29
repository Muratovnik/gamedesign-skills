# Changelog

## [Unreleased]

## [0.3.0](https://github.com/Muratovnik/gamedesign-skills/compare/v0.2.0...v0.3.0) (2026-10-29)

### Added

- Compose two rules that respond to one event: which applies first, whether one action is credited twice, whether a rule assumes a state the other already changed, contradictory feedback and a combination no rule names. ([eaa6e01](https://github.com/Muratovnik/gamedesign-skills/commit/eaa6e013ff21e98cd519630224cbe82958d629ea))
- Systems design points rules that share an event, such as one action that pays a reward and counts toward another rule, to that composition check. ([b076de9](https://github.com/Muratovnik/gamedesign-skills/commit/b076de93fc1b56c64b6654f93e9f4111434cddd9))

### Changed

- Shorter installation and first use, tighter onboarding copy and a documented GitHub marketplace uninstall lifecycle. ([0f88226](https://github.com/Muratovnik/gamedesign-skills/commit/0f88226ac971c3c7c620f9ac5b5aa15d420cfc36), [77ca8e5](https://github.com/Muratovnik/gamedesign-skills/commit/77ca8e58e9cfad9d6e8c2b7ef403fe566506b3e0), [90f1ba7](https://github.com/Muratovnik/gamedesign-skills/commit/90f1ba77730cde400ec1094102cea6061e9a8336))

### Fixed

- The junction test reads `mklink` output in any console code page, so it no longer fails on a non-English Windows console in UTF-8 mode. ([e66b05b](https://github.com/Muratovnik/gamedesign-skills/commit/e66b05b9fef48411b62f4e35927e2b5f1540d132))

## [0.2.0](https://github.com/Muratovnik/gamedesign-skills/compare/v0.1.1...v0.2.0) (2026-10-09)

### Added

- Optional two-player zero-sum calculation with declared utility and context, independent best-response bounds and original strategy examples. ([1873993](https://github.com/Muratovnik/gamedesign-skills/commit/1873993a6491b52fe8288c19837600a012e18d4d))
- Native Ink compile, explicit choices, save, fresh-process resume and selected-predicate assessment, including valid departure and ending examples. ([1873993](https://github.com/Muratovnik/gamedesign-skills/commit/1873993a6491b52fe8288c19837600a012e18d4d))
- glTF/GLB conformance inspection with explicitly permitted local resources, full native reports and coverage gaps kept separate from game-specific properties. ([1873993](https://github.com/Muratovnik/gamedesign-skills/commit/1873993a6491b52fe8288c19837600a012e18d4d))

### Fixed

- Reject malformed UTF-8 in Ink source, compiled story, scenario, report, saved state and dependency metadata before interpreting it; valid Unicode remains supported. ([513bbd7](https://github.com/Muratovnik/gamedesign-skills/commit/513bbd78330f4ee0d0c94cedaa81b771b78f09b6))
- Preserve observation conditions, collection method and units in saved reports so equal counts under different assistance remain interpretable. ([513bbd7](https://github.com/Muratovnik/gamedesign-skills/commit/513bbd78330f4ee0d0c94cedaa81b771b78f09b6))

### Changed

- Start with direct source use and a first playable result; retain Windows instructions and make client registration optional. ([95dcd7e](https://github.com/Muratovnik/gamedesign-skills/commit/95dcd7eab179b942a096986862e5ac0c6deb724c))
- Route a requested artifact operation to its existing owner, with task-local dependencies and the complete seven-skill bundle. ([513bbd7](https://github.com/Muratovnik/gamedesign-skills/commit/513bbd78330f4ee0d0c94cedaa81b771b78f09b6))
- Document the exercised Linux client manager/source lifecycle separately from model selection, other client builds, platforms and human experience. ([513bbd7](https://github.com/Muratovnik/gamedesign-skills/commit/513bbd78330f4ee0d0c94cedaa81b771b78f09b6))

## [0.1.1](https://github.com/Muratovnik/gamedesign-skills/compare/v0.1.0...v0.1.1) (2026-10-08)

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
