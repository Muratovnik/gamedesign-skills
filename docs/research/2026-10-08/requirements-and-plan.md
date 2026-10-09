# Comparative change: requirements and plan addendum

This is the implementation delta to the supplied project brief, operational and
domain requirements, domain research, Assay mapping and project plan. It does
not replace those sources or create a second general methodology. The
[comparison](comparison.md) provides the source evidence and rejected/conditional
alternatives; the [capability map](../../traceability.md) locates current owners.

The initial source baseline and attached-document identities were checked before
changes. The recovered project-plan text is a normalized working copy, not a
byte-identity claim. Requirement IDs below refer to those supplied documents.

## Requirement findings

The research did not justify a new universal requirement for competition,
equilibria, branching, playtest rituals, workflow stages or a specific engine.
It did identify one existing requirement violated by an output and three useful
concrete environment operations. “Optional” here describes applicability: once
the operation is selected, its declared acceptance checks are required.

| Requirement and reason | Before | Accepted refinement and canonical owner | Dependent implementation and check |
| --- | --- | --- | --- |
| GDE-02; GDR-18; OR-11/15: reproducible model consequences with bounded interpretation | Systems method and resource examples explain utility/access/sensitivity; no native matrix calculation | For a stated finite two-player zero-sum utility model, return certified mixtures/value or explicit unavailable evidence. Preserve intended hierarchy, singleton and asymmetric action sets. Systems owns the utility model; SciPy owns optimization. | `zero-sum-analysis.md`, `solve_zero_sum.py`, optional SciPy requirement; exact rational, affine, negative/rectangular, invalid input, certificate-corruption and output-preservation cases. |
| GDE-09; GDR-10/11; OR-11/15: observation conditions survive downstream interpretation | Input schema requires conditions/method/units, but importer drops them | Carry required context in the saved report itself. This corrects an implementation/acceptance defect; existing human/material method remains the owner. | Existing observation importer, environment paragraph and actual CLI/save/reopen regression with equal counts but different assistance; preserve synthetic/unknown boundaries. |
| GDE-01/05/06; GDR-13/14/22: consume narrative state and preserve the next legal choice | Rich conditional-story/state procedures and paper/JSON examples; no shipped Ink runtime operation | When native Ink is the selected consumer, compile/reopen, execute explicit actions, save/load native state in a fresh process, then check the declared choice/state predicate. A native save is not all host game state. Narrative owns scene meaning; the host owns external state. | `ink-artifacts.md`, `ink_artifact.cjs`, inkjs lock and original episode; missing guard, legitimate departure/silent ending, unavailable dependency/host work, identity drift and fresh-process continuation. |
| GDE-01/04; OR-11/15: distinguish an artifact from a checked relation | Shared environment contract requires actual bytes/consumer; no glTF conformance operation | When glTF/GLB is the selected format, preserve raw native validator evidence, local-resource identity and coverage gaps. Conformance does not imply mesh presence, geometry suitability, rendered fidelity or target import. Shared environment owns this cross-domain boundary. | `gltf-artifacts.md`, `validate_gltf.cjs`, Khronos lock and original fixtures; native valid/error/unsupported/missing-resource cases, valid empty/camera assets, bounded resource paths and alias-safe outputs. |
| DEP-02/10; plan C4/U02/U18/U19: concrete installation, discovery and lifecycle. OR-02/11/15 apply only to source/context identity and the limits of evidence. | Static manifests/projections and documented client procedures; previous bootstrap blocker | Native package identity, effective source, complete inventory, enabled state, source bytes, resource execution and model selection are separate claims. Use exact client/build/OS/route; retain rollback bytes and unrelated registrations. | `qualify_native_clients.py`, three discriminating verifier tests, disposable Linux native-client job, receipt and updated installation/compatibility documentation. This does not demonstrate OR-03's construction of game possibilities or OR-05's expressive composition; subject behavior stays a separate evaluation. |

OR-16 concerns restoring agent work, not merely restoring game state. Ink native
state does not satisfy agent continuity by itself. GDE-08 concerns actual data
provenance/frequency: solver mixtures and synthetic observations cannot establish
real player statistics. GDE-05 requires the requested runtime; an unrelated
demonstration does not prove a change to an existing game.

## Dependent plan changes

| Existing plan boundary | Delta and exit condition |
| --- | --- |
| C3; U07/U08/U11/U12/U13: artifact representations, tools and consumers | Add the three conditional operations to existing owners and keep dependencies outside skill loading. Each selected operation has input → action → saved output → actual consumer → bounded predicate. No universal parser, narrative VM or optimizer is created. |
| Plan §4.2: choose existing technical tools per operation | Qualify SciPy 1.17.0/NumPy 2.3.5, inkjs 2.4.0 and glTF-Validator 2.0.0-dev.3.10 for the declared examples. Existing game/engine formats remain preferred when they already provide the needed operation. Yarn, graph libraries and engine bridges remain conditional candidates. |
| Plan §4.3: justify an original integration by a missing operation or lost semantics | M2 repairs lost observation meaning; M1 adds model declaration/certification around the solver; I1 binds explicit action/state evidence around the native runtime; G1 binds artifact/resource identity and coverage around the native validator. These are concrete adapter responsibilities, not substitutes for their technical dependencies. |
| C4; U02 → U18 → U19: first use and lifecycle | Exercise exact native managers on a disposable machine, including same-version source replacement, disable/re-enable, rollback and removal. Verify the effective source rather than assuming the cache is active. Add a sentinel registration and consumer artifact to detect collateral changes. Record model-based selection/use separately. |
| Changed behavior and evaluation | Compare main and candidate with frozen task packets, rubrics, common Assay and equal external primitives; separate changed-operation tasks from sufficient paper/expressive controls. Retain unavailable attempts. A single local campaign is bounded evidence, not population-level superiority. |
| Independent review and final release boundary | New code and changed routing receive fresh review; historical approval is not inherited. Preserve original findings and corrections. Final package/projection/link/build checks use final bytes. Creating a PR is not publishing a release or qualifying an untested client/engine. |

## Ownership and scope decisions

The seven skills remain the supported bundle. Shared consumer contracts belong
to `game-design`; numerical game systems belong to `game-systems-design`;
conditional narrative belongs to `game-world-narrative-design`. The broad entry
can route an established artifact operation directly to its contract without
forcing concept development. Local gameplay, information, participation and
content work retain their direct entries.

Assay remains pinned at 0.17.2, commit
`94c517b0aac9ba2575086bf9aead1cc828aadb0d`, obtained separately. No new Assay rule,
permission scheme, model route, agent loop or mandatory cycle is duplicated in
Game Design. Maintainer tests and evidence stay outside installed runtime files.
The source archive may include public review evidence in `docs/reviews`; it is
not an installed skill directory. Final review therefore removed the package
receipt's unconditional `evaluation_included: false` claim and added a real
archive test separating public evidence from excluded runtime `evals` paths.
The receipt's exact file inventory remains the source for archive membership.

Deferred components do not become release gates: Blender/Unity bridges, live
Godot injection, Yarn, generic quest reachability and another concept-search
example need the particular consumer or observed deficit stated in the
comparison. An unavailable native model transport is recorded as an execution
blocker, not converted into a passing task or an invented requirement change.
