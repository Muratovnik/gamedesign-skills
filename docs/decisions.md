# Design decisions

**Status: current.**

This page explains the package choices a maintainer may need to revisit. Each
decision gives the reason for the current choice and the kind of evidence that
would justify changing it.

## Seven direct entries, distributed as one bundle

The seven entries give narrow tasks a direct starting point while preserving
cross-domain context in sibling references. The package distributes them as one
complete bundle so a moved skill can still resolve its local references.
`catalog.json` is the inventory. The number and boundaries are organizational
choices, not a measured optimum. Repeated
navigation or reading problems would justify revisiting them.

## Build around a concrete game relation

The methods ask designers to construct or revise an actual game artifact and
inspect the consequence. They include references when a research distinction or
technical boundary changes that design decision. General research,
implementation and evaluation procedures remain in the separately maintained
[Assay project](https://github.com/Muratovnik/assay); Game Design uses the
identity and selected owner resources recorded in its optional
[Assay binding](../skills/game-design/assets/assay-binding.json). A reference
earns its place when it changes the decision or artifact under discussion.

## Keep source binding separate from discovery claims

The Assay binding pins source identity and selected resource digests so a
consumer can inspect which external method version was selected. It does not
install that source, establish a client's permissions, or prove automatic
discovery. Reading a file is evidence of readability only. Change this boundary
only with evidence from the relevant consumer lifecycle.

## Derive projections from the catalog

Client-facing source projections are generated from the same seven-entry
inventory. This avoids maintaining conflicting hand-written bundle lists. The
local checks validate projection structure and links; they do not establish
client listing, selection, sibling resolution or lifecycle. Reconsider the
projection contract when a supported consumer's actual behavior requires a
different representation.

## Reuse concrete tools at the example boundary

Examples use their relevant engine APIs, parsers and small consumers to make a
specific action, geometry, migration, observation or content-selection relation
inspectable. Adding a general engine, installer or model runner would add
maintenance without serving those cases. When a real game has a suitable
importer or query path, the example should use that path rather than inventing a
parallel format.

## Match each claim to its evidence

A schema check establishes shape; a deterministic consumer establishes only its
declared data behavior. Neither demonstrates that a game is enjoyable, that a
person learned, or that an interface is accessible in use. The examples keep
those questions visible so technical results are not read as experience claims.
Revisit a claim when its scope or evidence changes; see the
[capability map](traceability.md) and [research and evidence limits](late-comparison.md).

## Preserve legitimate alternatives

The authored examples include expressive play without victory, worlds whose
meaning is not reducible to simulation, alternate clue routes, permanent help,
purposeful repetition, asymmetric authority and an accepted ending. These are
valid design outcomes. The methods support reasoning about a design relation;
they do not require a particular mechanic or a single form of success.

## Relation to established approaches

The methods retain familiar concerns such as feedback, progression, access and
the relation between implementation and player experience. Their contribution
is to connect those concerns to a concrete artifact and an inspectable change.
The [research and evidence page](late-comparison.md) records the source basis
and limits; it does not report a measured comparison of agent performance.
