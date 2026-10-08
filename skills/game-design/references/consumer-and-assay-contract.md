# Consumer and Assay contract

Read for first use, a changed provider/revision, or a handoff with unclear game
identity or authority. This owns package composition and game context, not a
second general research or engineering workflow.

## Bind an actual Assay source

The initial method dependency is the separately obtained complete Assay 0.17.1
collection at commit `1dbb7435d5349cb00cb4a2c8ffb5e00a2d703c03`.
The consumer supplies the permitted Game Design and Assay roots. Do not infer a
cache path, scan the machine for a provider, download mutable main as a silent
substitute or bypass a deliberately disabled provider.

For the supported explicit-source route, use the file reader directly or the
bounded verifier [bind_assay.py](../scripts/bind_assay.py). It accepts only the
supplied root, checks the selected owner's release-specific resource bytes and
can return the real text. The shipped [binding](../assets/assay-binding.json)
contains hashes and paths, never copied general instructions.
Identity includes `VERSION`, `catalog.toml` and the owning `LICENSE`; keep those
files and the license notice when exporting method text into a permitted workspace.

```sh
python3 "$GAME_DESIGN_ROOT/skills/game-design/scripts/bind_assay.py" \
  --assay-root "$ASSAY_ROOT" --provider-state enabled \
  --method evidence-research --read
```

`GAME_DESIGN_ROOT` and `ASSAY_ROOT` mean the consumer's actual extracted roots.
The `enabled` value must reflect the selected authorized source route. It is a
caller declaration, not proof of native client state. A disabled native provider
does not authorize reading its cache through this command. A separately chosen
direct-source route requires its own existing consumer authorization.

For a conditional resource, use `--resource references/evidence-and-claims.md`
with the same owner. For a sibling owner, use that owner's `--method` first.
Read the method before the decision it governs, and follow its applicable
references. Hash verification without reading is only integrity evidence.
Required resource failures leave the dependent operation unavailable; independent
subject work may continue with its precise limit.

| Work needed in this game task | Assay owner to read | Game Design retains |
| --- | --- | --- |
| Consequential source question, competing explanation or transfer | evidence-research | Subject relations and relevant game material |
| Multi-unit plan, readiness or continuation | implementation-planning | Current game identity and dependencies |
| Carry an authorized research/change cycle across stages | research-driven-change | Agreed game outcome |
| Material ownership, interface or placement choice | software-architecture | Game semantics of that interface |
| Change executable code or adapters | code-change | Intended player/world consequence |
| Add tests / assess a test claim | test-writing / test-audit | Game predicate and legitimate alternative |
| Requested independent review | independent-audit | Original game brief and artifact |
| Game menu/control UI or user documentation | ui-delivery / technical-writing | The gameplay purpose; UI convenience is not a universal game objective |

Do not run every owner in every task. Skill evaluation belongs to package
maintenance and a specifically authorized evaluation, not every game design task.
Subagent routing, hooks and profiles are optional Assay facilities and are not
required by this package.

## Failure meanings

The verifier reports `verified`, `unavailable` or `incompatible`, plus a local
reason. These are this package's messages, not claimed native Assay API codes.
Exit 0 means selected release resources were verified; exit 1 refutes the
compatibility condition; exit 2 means missing/invalid/unavailable evidence.

Examples: missing root/owner, disabled provider, unreadable resource and invalid
resource path are unavailable; changed required bytes or an unsupported source
revision are incompatible. Neither condition is repaired by guessing a matching
skill name. A native provider is an alternative only after its listing, qualified
name, exact identity and actual load have been established. An ambiguous duplicate
provider remains unresolved. No native automatic discovery is asserted here.

## Supply current game context

Reuse the consumer's existing brief and work record. Add only fields the current
operation needs; the following is a selection aid, not a required universal schema.

| Context | Examples of useful source material |
| --- | --- |
| Purpose and permitted change | Intended relation, audience, constraints, owner decision |
| Identity | Game/repository/artifact, build, mod set, language/platform, input versions |
| Game semantics | IDs, units, transitions, clocks, geometry, actor knowledge, rights |
| Evidence | Current map/config/save, event dictionary, cohort, capture, missingness |
| Authority | Permitted roots, read/edit/run/network scope, disposable outputs |
| Continuation | Accepted/rejected decisions, changed assumptions, pending dependent work |

Private saves, credentials, endpoints and game-specific adapters remain with the
consumer. Public examples are synthetic and do not supply a real game's current
state. Pass the actual artifact and its changed basis to another method, not a
summary that silently preserves an obsolete price, clue or owner.

Game state transfer is owned by [systems](../../game-systems-design/references/game-state-transfer.md).
The agent's unfinished work uses Assay's continuation procedure. These are different
states with different consumers.

## Source basis

This keeps the consumer contract aligned with Assay's
[composition contract](https://github.com/Muratovnik/assay/blob/1dbb7435d5349cb00cb4a2c8ffb5e00a2d703c03/docs/explanation/skill-composition.md)
defines optional-peer metadata and distinguishes reading from execution. The
[Agent Skills specification](https://agentskills.io/specification) defines the
skill format, not cross-package installation. The explicit hash-bound route is
local integration glue; it is not a new locator, installer or permission system.
