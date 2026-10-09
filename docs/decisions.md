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

## Optional native operations under existing owners

The comparison adds SciPy utility calculation to systems design, native Ink
execution to conditional narrative, and Khronos glTF conformance to the shared
environment. These are original adapters around established implementations.
They exist because the concrete operation was absent; a second parser, solver,
narrative VM or general workflow would duplicate a more appropriate owner.
Dependencies are obtained in task-owned environments only when selected.

The input model, game predicate and uncertainty stay explicit. Intentional
dominance is not rejected as bad design; a silent or common ending remains legal;
an empty or camera-only glTF can be conformant. Reconsider each adapter if an
existing game's native consumer already performs the operation, a qualified
dependency no longer fits, or repeated observed tasks expose a concrete missing
contract. A new package name alone is insufficient reason to broaden it.

## Preserve evidence meaning through serialization

Observation conditions, collection method and units are required input meaning,
so the saved report now carries them. A digest of a separate manifest does not
make an isolated report interpretable. This corrects the implementation of an
existing requirement and its regression test; it adds no new universal
playtesting or assistance rule.

## Qualify native sources rather than assume cache behavior

The exact Linux native lifecycle is exercised through real Codex and Claude
managers. The verifier records the effective source, full runtime file set and
content before executing an installed resource; Claude may read a retained local
source while also having a cache. It tests same-version replacement and rollback
and preserves a separate plugin. Native listing, enabled metadata, resource
loading and a model's actual selection remain distinct compatibility claims.
