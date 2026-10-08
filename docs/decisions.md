# Design decisions

**Status: current.**

This page records user-facing design choices that help maintainers understand
the package. It explains the rationale and the evidence that would justify
reconsidering a choice.

## Seven direct entries and one complete bundle

The package has seven entries with distinct subject areas and canonical owners
for shared relations. Direct entry supports both narrow tasks and changes that
cross several systems. The complete bundle keeps sibling references available
when the source is moved. Seven entries are a revisable organization choice,
not a measured optimum. Repeated discovery or reading problems would justify
revisiting the boundaries.

## Constructive procedures with conditional references

The methods ask the designer to build or revise an actual game relation. They
use references when those help answer a real design question. This keeps
general research and engineering processes in the separately maintained Assay
package while allowing game-specific judgment to remain with the subject
methods. A reference should be reconsidered when it adds process without
changing a decision or artifact.

## Explicit external method sources

Assay is an independent dependency, so the Game Design package does not assume
that its files share a parent directory or are installed in a particular
location. The optional source binding makes the selected method content
inspectable for a task. A consumer's actual permissions and enabled state must
still be established by that consumer; a readable file alone cannot prove
client authorization.

## Prepared client manifests

The repository contains source projections for plugin clients. Keeping those
projections derived from the same skill inventory avoids maintaining different
bundles by hand. Schema validation establishes structure only. Client listing,
selection, sibling resolution and lifecycle remain separate compatibility
questions that require the relevant client and build.

## Use existing tools for concrete game operations

The examples use available engine APIs, parsers and small consumers to make
action, geometry, migration, observation and content-selection relations
concrete. A new general engine, installer or model runner would add maintenance
without serving these examples. When a real game has a suitable importer or
query path, use that instead of translating it into an example format.

## Keep evidence proportional to the claim

A schema check can establish shape; a deterministic consumer can establish its
declared data behavior; neither establishes that a game is enjoyable, that a
person learned, or that an interface is accessible in use. The examples keep
human, material and perceptual questions visible so a technical result is not
mistaken for an experience claim. Claims should be revisited when their scope
or available evidence changes.

## Preserve legitimate alternatives

The authored materials include expressive play without victory, worlds whose
meaning is not reducible to simulation, alternate clue routes, permanent help,
purposeful repetition, asymmetric authority, and an accepted ending. These
examples make clear that a method is a way to reason about a design relation,
not a universal demand for a particular mechanic.

## Relation to existing approaches

The methods retain familiar concerns such as short feedback loops, progression,
access and the relationship between implementation and player experience.
Those concerns do not replace the package's procedures for changing a concrete
artifact and checking the consequence. The [comparison rationale](late-comparison.md)
summarizes this boundary and cites public sources. It does not claim a measured
comparison of agent performance.
