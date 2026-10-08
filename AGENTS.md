# Game Design source and contribution contract

This repository publishes the Game Design methods and examples. It does not own
general research, implementation, testing, audit or skill-evaluation methods;
those remain with the separately maintained Assay project. Read the actual
method required for a task through the consumer's authorized source.

## Scope and ownership

The seven complete directories under `skills/` are the canonical methods and
the supported bundle. Each sibling reference has one owning location. The
`game-design` entry covers intent, composition, adaptation and shared consumer
contracts; the other entries cover gameplay, information, world and narrative,
systems, participation, and content. Use an entry directly when it fits. A
score, victory condition, simulation or temporary-only help is not required for
a good result.

Preserve legitimate alternatives, including expressive play without victory,
permanent assistance, purposeful repetition and an accepted ending. Teach
construction and revision through actual game artifacts rather than checklist
compliance.

## Sources and language

Methods and technical documentation use English. Public primary sources support
claims where they matter; distinguish reported evidence, transfer and local
design judgment. Do not redistribute source material wholesale or use another
game-design package as a template. Examples are original and synthetic unless
they explicitly say otherwise.

## Packaging and verification

`VERSION` and `catalog.json` define release identity and inventory. Generated
client projections must stay derived from that inventory. Runtime resources,
including required scripts and schemas, live inside their skill directories.
Maintenance tools and tests stay outside runtime content.

Use established parsers and technical libraries where they fit. A schema check,
import or successful command does not establish human experience or game
quality. Checks must distinguish a disproven property from missing or invalid
evidence and must not pass on an empty inspected set. Record source versions and
actual outputs when they are relevant to a published support claim.

Use project-local scratch or an isolated development environment. Never claim
automatic discovery based on an explicit file read. Changes to client settings,
live installations or publication are separate actions and require the owner's
authorization.

## Changes

Preserve unrelated work. Do not reset, clean, stash or mutate files outside the
change's ownership. Each change should identify its user-facing consequence,
the affected method or package boundary, the evidence that supports it and the
targeted checks needed to validate it. Keep release, client and human-evaluation
claims within the evidence actually available.
