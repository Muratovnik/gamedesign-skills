# Domain agent landscape and transfer decisions

> Historical research-stage record, retained with its original scope and findings.
> Implementation and final dispositions are in [the integrated comparison](comparison.md);
> proposal wording in this record does not create an additional requirement.

Research worker record, 2026-10-08. Product was read only. The source baseline for
every local comparison is `Muratovnik/gamedesign-skills`
`4fc654c2cb92989582c30bc048742f2cce7659ba`; Assay methods were read from
`94c517b0aac9ba2575086bf9aead1cc828aadb0d`. This record is a research-to-choice
handoff, not an implementation or publication receipt. All examples/probes authored
here are synthetic. No humans were recruited or simulated as evidence of human play.

## Decision

Two concrete changes are supported particularly well:

1. **Adapt the component idea and connect a numerical library for an optional,
   narrowly specified interaction-matrix calculation.** The existing game systems
   method already describes causal scope and dominance; it does not supply an
   executable matrix operation in the inspected runtime and analysis examples.
   `scipy.optimize.linprog` can calculate a bounded zero-sum model, with separately
   checked best-response bounds. Do not import apetrov's analysis/redesign workflow
   or confuse its ordinal counter graph with a payoff model.
2. **Fix the existing observation data path, rather than add another research
   instruction.** The current importer requires `conditions`, `collection_method`
   and `units` in its input manifest, then drops them from the saved output. This
   is reproduced on the exact baseline. Preserve these fields with observations
   so a later interpretation retains what participants were shown and how the
   evidence was collected. A SHA of a separate manifest is useful identity, but
   does not carry its meaning into a report handed onward by itself.

Two additional decisions are narrower:

3. **Test further, without extending runtime rules:** an original concept-search
   example may help demonstrate how to vary a mechanism while preserving an
   uncertain aesthetic or social promise. Current `relations-and-context.md`
   already does substantive causal variation. No observed agent trace establishes
   that another instruction or a fixed search population would help.
4. **Retain the present narrative distinctions; test further only when a concrete
   consumer needs static graph machinery.** ncdlek provides a substantive quest
   schema and executable validator, but the validator's actual coverage and
   hardcoded design policies are narrower than its claims. Existing conditional
   story guidance already distinguishes past return, current possession,
   knowledge, delivery of a reveal, interruption and a meaningful common ending.

Neither blanket installation nor blanket rejection by repository size is justified.
Each disposition below concerns a resource, a consumer and a protected game relation.
Assay retains general research, implementation, testing, review, stopping, permissions
and agent orchestration.

## Questions and coverage

| Question | Examined evidence | Finding and next useful decision |
| --- | --- | --- |
| Are there substantive concept methods? | baxatron `game-vision-architect`; Donchitos `brainstorm` actual creative phases; abagames concept SKILL and its three method/record/guard references | Yes. The supplied report's claim of absent concept skills is contradicted. Current local method also already has creative construction. Evaluate a new example, not a new owner. |
| Can a balance claim be computed rather than merely narrated? | apetrov actual matrix script, all 34 tests and relevant theory references; local system/runtime inventory; SciPy versioned API and executable probe | A precise bounded calculation is useful. Upstream source has semantic and validation limits; connect an established solver with an explicit model contract. |
| Are playtest methods absent outside baxatron? | Donchitos playtest SKILL, CD-PLAYTEST gate and actual test specification; edhahn eval SKILL and tabletop branch; local observation importer/schema | No. Reporting and simulation examples exist. Local data-path loss is the actionable defect; a universal playtest ritual is unnecessary. |
| Does prototype refinement have a useful stopping alternative to adding rules? | abagames `refining-game-prototypes` and both referenced files; baxatron prototype SKILL; local concept/adaptation/environment method | A concrete cost/benefit comparison can justify an unresolved stop before a quota. This is already Assay's responsibility. Preserve the decision in its record; do not copy a second loop. |
| Are narrative knowledge representations substantive? | ncdlek quest state/graph/schema references and complete validator; baxatron narrative SKILL; local conditional story and state boundaries | Yes, including current-state versus event counters and graph satisfiability. Much of the local knowledge is already present. Generic graph connectivity cannot establish mutable-state reachability. |
| Do tests demonstrate agent quality or game quality? | apetrov executable unit tests; Donchitos test specs, skill-test entry and GDD shell checker | 34 passing Python tests demonstrate tested script cases. CCGS playtest document is a specification, not a run receipt. GDD heading presence explicitly is not completeness. No comparative model benefit established. |
| Can exact resources be redistributed? | Tracked license inventories, file/header searches and declared upstream provenance, summarized below | MIT terms exist for five agent repositories; baxatron has an MIT label without accompanying license text. No source bytes are selected for transfer. API dependency and original reimplementation are distinct operations. |

## Source identity, terms and reading scope

`repository-manifest.json` records exact remotes, HEADs, commit timestamps, tracked
file counts, canonical skill paths and license-file inventories. Commit timestamps
describe these commits; they are not release dates, maintenance verdicts or evidence
of comparative quality. Star counts were not used.

| Repository | Exact inspected revision | Terms checked for selected resources | Material read |
| --- | --- | --- | --- |
| [baxatron-git/claude-game-design-suite](https://github.com/baxatron-git/claude-game-design-suite/tree/5dd265ac2b143d13683766cdaae9695d3d871909) | `5dd265ac2b143d13683766cdaae9695d3d871909` | README lines 93–95 say MIT. No LICENSE/NOTICE in 27 tracked files; selected SKILLs have no license header. Treat this as an MIT claim with missing attached terms/copyright provenance, not as a verified complete grant for the selected bytes. | Full game-vision, playtest-protocol, prototype-scope and narrative-systems SKILLs; coherence SKILL through its operations/triggers; selected systems-mapper description/output sections; tracked tree. The coherence link to `references/suite-topology.md` points to a resource absent from this tree. |
| [apetrovCode/game-design-skills](https://github.com/apetrovCode/game-design-skills/tree/b8bc2c4d99ccd6e8b2fb3a5fed63fec66dfce35c) | `b8bc2c4d99ccd6e8b2fb3a5fed63fec66dfce35c` | Root MIT, copyright 2026 apetrovCode; no more-specific terms found in selected script/SKILLs/tests. Two theory references declare `source_material: Rock Paper Scissors 2 (YouTube Video by Fractal Philosophy)`; this provenance is not an independently verified right to redistribute that source's expression. | Both full SKILLs; full interaction-structure and analysis-workflow references; all matrix script; all matrix tests; CI test command; tracked tree. Remaining fun/levers/design-moves material is not claimed read. |
| [Donchitos/Claude-Code-Game-Studios](https://github.com/Donchitos/Claude-Code-Game-Studios/tree/be8993bbc5a1f016bc770b2846ce06272d284526) | `be8993bbc5a1f016bc770b2846ce06272d284526` | Root MIT, copyright 2026 Donchitos; file-specific search found no override in selected resources. | `brainstorm` lean branch and creative phases 1–3; full playtest-report SKILL, CD-PLAYTEST and its test spec; selected map-systems dependency/order/handoff sections; design-system entry and reference 4 sections A/E/F/G/H; full GDD structure script; skill-test through static checks 1–3. Other director/engine/workflow coverage is unexamined. |
| [abagames/agentic-gamedev-skills](https://github.com/abagames/agentic-gamedev-skills/tree/72309959e3422acdcb95d30e3b0ffd9ed2bd149d) | `72309959e3422acdcb95d30e3b0ffd9ed2bd149d` | Root MIT, copyright 2026 abagames; no more-specific terms in the selected canonical `.agents/skills/` resources. Generated plugin duplicates are not counted as independent methods. | Full exploring-game-design-space SKILL plus search-method/concept-record/search-guards; full evaluating-gameplay-balance and designing-minimal-game-rules SKILLs; full refining-game-prototypes SKILL and stage-checks/revision-log. The large simulation-harness branch was not fully read or executed. |
| [edhahn/agent-skills](https://github.com/edhahn/agent-skills/tree/ffc6fc4bf1408bc3cac522916bb58e603f39ab45) | `ffc6fc4bf1408bc3cac522916bb58e603f39ab45` | Root MIT, copyright 2026 Edward Hahn; no file-specific override found for selected material. | Full game-designer and eval-driven-game-development SKILLs; tabletop reference's model/observation/version/blind-play branches (numeric metrics subsection not fully read). No executable harness supplied by the inspected files; code generation advice is not execution evidence. |
| [ncdlek/game-dev-agent-skills](https://github.com/ncdlek/game-dev-agent-skills/tree/20d63af5f6374f9b7d5a41caf501d8d443c9b100) | `20d63af5f6374f9b7d5a41caf501d8d443c9b100` | Root MIT, copyright 2026 Engin Yazılan; no selected-file override or external source attribution found. | Quest SKILL context/principles/pipeline/output; quest-system state model and stored/derived counter branch; full graph/softlock reference; entire 621-line quest validator; dialogue reference headings only. Narrative quality and broad engine integration remain unverified. |

MIT redistribution requires retaining the copyright and permission notice with
copies or substantial portions. No selected operation below copies these agent
packages' bytes. Studying an idea does not require importing its entire workflow,
and a dependency would have its own versioned terms and execution boundary.

## Transfer M1 — bounded matrix calculation

**Decision:** adapt the resource idea; connect SciPy through its API if the parent
chooses to deliver this operation. Do not copy apetrov's script or skill. This is
a new concrete environment capability, not proof that the current language model
cannot reason about matrices.

**Protected outcome:** for a fully stated simultaneous two-player zero-sum model,
return actual consequences of its utilities: candidate mixtures, value and
best-response bounds. Distinguish a counter relation, an effectiveness table,
raw payoff and observed strategy frequency. GDE-02 explicitly calls for
reproducible calculations, changed-input sensitivity and bounded model claims;
GDR-18 connects resource/choice consequences; GDE-08 forbids interpreting modeled
frequencies as observed play.

**Source unit:** apetrov `game-analysis/scripts/matrix_analysis.py` and SKILL Step
6, revision above, are the comparative trigger. The script computes ordinal
outcomes, graph cycles, weak outcome dominance, unbeaten subsets and a damped
eigenvector heuristic. The SKILL correctly warns that its heuristic is not a
play-rate/equilibrium estimate, but `references/interaction-structure.md` §3.4
still calls it true underlying viability. Its restrictions are not an adequate
universal balance model.

**Existing counterpart:** local `skills/game-systems-design/SKILL.md` steps 2/4/6,
`references/resources-and-development.md`, shared `environment-contracts.md`, and
the resource/state calculations in `examples/analysis-lab`. These already protect
scope and interpretation. An `rg` scan of runtime skills, tools, tests and this
lab found no matrix/equilibrium calculation. Do not add another standing
“always use math” rule; add an optional operation with an explicit reading route.

**Concrete integration contract suggested:**

- Explicit model type `two-player-zero-sum` and a finite nonempty rectangular
  row-utility matrix, named row actions and named column actions. Do not guess
  binary-versus-weighted mode from the numbers. Non-zero-sum inputs need a
  different method, not a silent transform.
- Inputs specify state, action availability and utility meaning. A damage
  multiplier need not equal preference; different prices, geometry and timing
  require the relevant layer/model rather than a dominance verdict about the game.
- Ask the library to maximize the row's guaranteed payoff and minimize the
  column's maximum concession. Value variables must be unbounded in sign;
  probabilities are nonnegative and sum to one.
- Preserve input digest, library version, method, numerical tolerance and solver
  status. Independently compute `min(p @ A)` and `max(A @ q)` and check simplex
  feasibility and their gap before accepting the result. A solver failure,
  nonfinite input or unavailable dependency is unavailable/invalid evidence,
  not a game-design failure.
- Report pure/weak dominance descriptively, if included. Do not fail a build or
  force redesign merely because a strategy is dominated; intended hierarchy,
  role asymmetry and an authored inferior choice can be part of the game.
- Do not include graph-specific “2-Paradox” checks unless that exact property is
  requested. A zero-member checked subset must not certify a relevant game claim.

**Library evidence:** installed SciPy is `1.17.0`, NumPy `2.3.5`. SciPy v1.17.0
annotated tag resolves to commit `8c75ae75176236f233824e9a0483c26a69e6dfec`.
[Versioned linprog-highs documentation](https://docs.scipy.org/doc/scipy-1.17.0/reference/optimize.linprog-highs.html)
was read for objective, equality/inequality, bounds, status and tolerances.
The installed `_linprog.py`/`_linprog_highs.py` headers identify the actual HiGHS
adapter; this is genuine API use, not an unused import alongside a hand-coded LP.
[SciPy LICENSE.txt](https://github.com/scipy/scipy/blob/8c75ae75176236f233824e9a0483c26a69e6dfec/LICENSE.txt)
is BSD-3-Clause (Enthought/SciPy developers); `LICENSES_bundled.txt` identifies
HiGHS under MIT. The exact submodule is `scipy/HiGHs`
`222cce79a2bca866dbfbcd91b55da11336ae88f4`; its
[LICENSE.txt](https://github.com/scipy/HiGHS/blob/222cce79a2bca866dbfbcd91b55da11336ae88f4/LICENSE.txt)
was read (MIT, copyright 2024 HiGHS). The proposed operation is an external
dependency API call, without vendoring either package or solver source.

Nashpy's [minimax API](https://nashpy.readthedocs.io/en/stable/how-to/use-minimax.html)
and [zero-sum model derivation](https://nashpy.readthedocs.io/en/stable/text-book/zero-sum-games.html)
were examined as an alternative. Nashpy `0.0.43` documentation exposes a ready
`Game.linear_program()` restricted to zero-sum games. It is not installed here.
For this narrow operation direct SciPy avoids another package and exposes status
for the needed certificate. A broader bimatrix task would justify reconsidering
Nashpy or another specialist solver rather than extending this operation casually.

**Execution evidence:** `minimax_feasibility.py` is original research code, not a
production validator, and `minimax_feasibility.json` is its actual output. The
unequal-stakes cycle `[[0,-1,2],[1,0,-3],[-2,3,0]]` produces probabilities
`(1/2,1/3,1/6)` for both parties and certificate gap approximately `5.55e-17`.
Adding 5 to every payoff preserves the mixture and adds 5 to the value. A 1×2
matrix with negative values and a 2×3 role-asymmetric matrix also solve. A model
with deliberate pure dominance returns that result without treating it as bad
design. These runs prove narrow feasibility in this environment, not broad
client compatibility, player behavior or the quality of the chosen utilities.

**Cost:** optional binary numerical dependency and its NumPy requirement
(`numpy>=1.26.4,<2.7` in installed SciPy metadata); a small model adapter and
validation/schema/docs/tests; version/platform qualification. It should remain
conditional so paper scenes and expressive work need no numerical installation.
Root can choose a smaller first delivery (explicit payoff/dominance report) if
equilibria are outside the change; do not name that smaller component a solver.

**Adjacent valid controls:** intentional unequal action power; different action
counts per role; negative utility; a single legal action; a noncompetitive sound
score requiring no payoff matrix; rock-paper-scissors whose three pairs have no
single counter although the 1v1 game remains coherent. Appropriate outcome depends
on the agreed game, not the absence of every “doom-stack”.

## Transfer M2 — preserve observation context across the existing importer

**Decision:** accept a local data-path fix informed by comparative reporting
examples. Reimplement no external behavior and copy no external template.

**Protected outcome:** a recipient can distinguish first exposure, prior teaching,
the actual aid supplied, material/device conditions, and how evidence was captured
when interpreting an observed action. GDR-10/GDR-11 and GDE-09 explicitly distinguish
understanding, permitted assistance, actual observation, report and interpretation.

**Sources:** Donchitos `.claude/skills/playtest-report/SKILL.md` records build,
platform, input and session type with findings. Its test spec preserves missing
pillars rather than inventing them. edhahn
`eval-driven-game-development/references/tabletop.md` preserves rules/card version,
seats and experience context with observed behavior and quotations. These are useful
reporting representations; neither is evidence of a universal successful protocol.
Both repository MIT licenses and selected file-specific terms were checked above.

**Own counterpart and defect:**

- `skills/game-design/assets/observation.schema.json` makes `conditions`,
  `collection_method` and `units` mandatory.
- `scripts/observe_evidence.py::import_observations` validates that manifest,
  retains individual rows and some manifest fields, but omits all three from its
  returned report.
- `examples/analysis-lab/test_semantics.py::test_synthetic_import_retains_unknown_and_assisted_cases`
  verifies synthetic status/counts/empty-set rejection, not context preservation.
- Shared `environment-contracts.md#human-and-material-route` already tells the
  agent to record these conditions. This is an output/acceptance defect, not
  missing methodological guidance or a proven routing failure.

**Exact baseline reproduction:** the five necessary original files were retrieved
with `git show 4fc654...:<path>` under `notes/baseline/`. The existing importer ran
using the existing development environment and baseline synthetic fixtures. It
exited 0. `observation-baseline-report.json` contains no `conditions`,
`collection_method` or `units`, while `observation-loss-check.json` shows their
presence in the valid input. Record hashes and `human_claim=not_established` survive.
This means a user who still has the input can recover the omitted information;
the defect concerns a report consumed on its own, not destruction of the source.

**Transferred unit:** retain the three validated manifest fields in the report,
or retain the complete validated manifest under a clearly named context field.
Test field preservation in the existing test suite. If a manifest path is added,
consider whether it is portable to the receiving consumer; a local path alone is
not a replacement for the data. No new logging service, new runner or new skill.

**Discriminating case and control:** two synthetic sessions can have identical
completion counts and `assistance=persistent-aid`. In one, the aid reads the
written card aloud; in the other, it highlights the correct answer. Both are
legitimate chosen forms of support, but only the first leaves that particular
choice to the learner. The output must preserve the differing conditions, without
declaring either row proof of learning or wrongly removing the permitted aid.
Also preserve unknown outcomes and a declined attempt: absent data must not be
converted to failure. The current importer already protects these distinctions;
the repair should leave them intact.

**Cost:** a small local output addition and a meaningful preservation assertion;
no dependency or installation change. Unknown human validity remains unknown.
An original optional capture example is useful only if it helps consumers prepare
this route; it is not needed to repair the demonstrated data loss.

## Transfer M3 — creative concept variation without a new universal workflow

**Decision:** retain current method; test further an optional original worked
example if broad concept exploration is selected. Do not add another runtime
skill or import fixed quotas/stopping thresholds.

**Source unit:** abagames `.agents/skills/exploring-game-design-space/` at
`723099...`, especially `references/search-method.md` mutation operators and
`search-guards.md` treatment of unknown embodiment/authored meaning/social response.
The useful distinction is a changed causal relation versus a reskin, with a
small next artifact capable of resolving the remaining question. MIT applies;
the proposed operation is idea study with original prose/artifacts.

**Existing counterpart:** `game-design/SKILL.md` explicitly varies knowledge,
action, persistence, payment and response timing, without an idea quota.
`relations-and-context.md` already turns “a port remembers its people” into a
marked tool, maintained route or inherited obligation, and develops Signal House
public versus privately known coil damage. It also accepts a quiet expressive
variant. `free-form-loom.md` supplies an original noncompetitive material result.
There is no demonstrated absence of concept capability to repair.

**Possible unit to evaluate:** a short original concept study with several
distinct starting relations (for example an inherited obligation, a shared tool
whose use alters another participant's view, and a free audiovisual transformation),
each developed into usable material and its next uncertainty. Include an
intentional close variant rather than automatically collapsing it as duplicate.
Cost is added example/context maintenance, not runtime dependency. Benefit remains
a hypothesis until a comparable natural-use run shows better actual artifacts.

**Protected outcome and control:** prevent three pitches that change only theme
nouns from being represented as three different mechanical choices when diversity
is requested. Preserve a deliberate comparative reskin or translation when the
research question is about meaning, culture, sensory identity or communication.
Do not forbid presentation-dependent value in an expressive or performative game.

**Prototype-stop finding:** abagames `refining-game-prototypes/SKILL.md` decision
6 and `references/revision-log.md` allow zero attempts when concrete candidate
cost/risk comparisons justify stopping and keep the finding unresolved. That
is a useful contrast for an evaluation, but Assay already owns deciding whether
another search/repair can change the outcome. Do not copy the four-stage loop,
three-attempt cap or requirement that intent must predate a finding in order to
accept it. A designer may legitimately discover a desirable accidental property
during play and revise the intention afterward.

## Transfer M4 — narrative state and graph machinery

**Decision:** retain current narrative method; reject direct validator adoption;
defer an executable graph adapter until a concrete consumer/model requires it.

**Source unit:** ncdlek quest SKILL, `references/quest_system_architecture.md`
§4.2, `references/quest_dependency_and_softlock_audit.md` §1 and actual
`scripts/validate_quest_graph.py`, revision `20d63...`, MIT. The references name
stored action counts versus current-state derived counts and combine prerequisites,
exclusive groups and actor/item policies. This is substantive knowledge
representation, not only a GDD outline.

**Existing counterpart:** local conditional-story's `docket_returned` versus
`docket_owner`, delivery-point `reveal_delivered`, scene eligibility/priority,
clock and merge distinctions. The original harbour already makes the consequence
visible without requiring another ending. Its source contract allows a simple
stage number where states are exclusive. Local game-state-transfer owns saves;
entities owns actor knowledge. These remain the fitting owners.

**Actual validator limits:** `prerequisite_ids` extracts only `QuestState` IDs,
ignoring required `equals` values and other conditions. `check_reachability`
treats every extracted prerequisite as an AND dependency, not a general dynamic
world model. The reference's mutually exclusive faction example distinguishes
either from both, but the examined extraction has no OR semantics. As such its
success must not be called general satisfiability of the story.

Furthermore, in `main`, actor and item checks run only if nonempty global
`policies`/`item_rules` dictionaries were loaded; local policy entries alone do
not enable these checks. The synthetic `notes/ncdlek-missing_policy/quest.json`
references `npc_clerk` as giver and objective target with no policy. Executing
the unmodified validator exits 0 and says zero errors/warnings. A top-level JSON
array instead crashes at `data.get` before schema validation, despite E000's
claimed malformed-input route. Exact output files accompany both inputs.

**Useful future unit:** if a consumer supplies an actual declarative story
format, use its real interpreter/parser to test promised transitions and report
which condition language was inspected. Static dependency/cross-reference lint
can remain narrower. Do not turn all narrative into this particular quest schema
or write a replacement general-purpose satisfiability solver inside Game Design.
Costs include adapter/version support, semantic fixtures, and possibly an
existing parser/solver dependency. There is no current consumer evidence to
justify that integration here.

**Control:** a return-the-docket scene must remain available after it was handed
over; a task to bring a currently held item must cease to be ready after selling
it. Both use similar nouns but different state meanings. A history-of-visiting
objective must not reset merely because the actor left the current zone. A
deliberately failed or expired optional quest may be a complete authored outcome;
not every objective must be completable from every reachable state.

## Hard rules and heuristic transfers to reject or narrow

These are judgments about the local consumer constraints, not global claims that
the upstream author must change their product.

| External rule / exact location | Protected intent it may serve | Local disposition and legitimate neighboring case |
| --- | --- | --- |
| apetrov game-redesign: mandatory prior audit, exactly three proposals with wildcard, exact installed `~/.claude/skills/game-analysis` | Ground designs and keep experimentation varied | Reject workflow. A fully specified local redesign or an authorized single original concept needs no extra audit/portfolio; Assay owns review and host bindings. |
| apetrov game-redesign Step 5: no new dominated nodes as universal pass bar | Avoid unintended inferior choices | Reject universal gate. A costly upgrade can intentionally dominate a starter move; role access/timing matter. Report formal relation and context. |
| apetrov interaction-structure §3.4: true viability from eigenvectors | Make asymmetric charts computable | Reject interpretation. Exact mixtures for a utility model and human choice rates are different questions; no ordinal centrality can establish either universally. |
| baxatron game-vision: market fit plus 1–3 psychographic personas and one-sentence fantasy required | Focus an audience proposition | Retain as optional commercial framing only. An expressive local installation or a small mod repair can have known users and no market gap/personality profile. |
| baxatron playtest: every question/intervention is a design failure; five reports form a pattern | Notice confusion | Reject inference. Negotiation and inquiry may be intended play, and agreed access assistance is valid. Single decisive counterexamples and heterogeneous observations require their actual context, not a quota. |
| baxatron prototype: all prototypes hypothesis-only, disposable, never demo/foundation; more than two weeks implies reduce scope | Avoid overspending before learning | Reject universal scope. A prototype can discover a relation or must include sensory fidelity/physical fabrication; useful production work can be retained. |
| baxatron narrative: a shared outcome is fake agency, optional skippable exposition is system failure, unified mechanics/story ideal | Preserve promised consequence | Reject hierarchy. The harbour's common repair with different public records is a valid expressive consequence; optional lore and deliberate dissonance can be authored choices. |
| Donchitos brainstorm: fixed three concepts and unconditional concept-selection question | Preserve creative ownership | Reject imported permission flow/quota. User can delegate a reversible design choice; their existing authorization and Assay workflow prevail. Keep useful verb/experience approaches as options. |
| Donchitos playtest test case: never-opened crafting menu automatically routed to design change | Surface mismatch with intended use | Narrow to a question. The session may omit the qualifying opportunity or the recording may miss it; fix evidence/implementation/expectation as warranted. |
| Donchitos GDD structure checker / skill-test static headings | Make structural inspection cheap | Retain as information about their package only. Their script explicitly says presence is not completeness. A runnable one-page episode can be complete without eight GDD sections or their verdict vocabulary. |
| abagames exploring: 18 roots/6 survivors/4 finals; half must avoid first tuple; 4-of-5 duplicate threshold | Explore beyond anchoring | Reject mandatory quotas and similarity threshold. A narrow design change may have two sufficient alternatives; a thematic close variant may be the requested object. |
| abagames minimal-rules: appeal must survive without authored content/presentation; score and danger causally coupled | Seek compact challenge games | Reject generalization beyond that skill's stated compact-game scope. A musical instrument, meaningful ritual or authored narrative can depend on presentation and lack score/danger. |
| abagames evaluating balance: exact n/min–max nonoverlap gates; idle optimum automatically defect | Avoid tuning from noisy weak policies | Reject statistical/design universality. Overlap of sample extremes is not the question's inferential test; purposeful waiting, accepted endings and noncompetitive play remain valid. General inference remains Assay's. |
| abagames refining: only prior written intent can close an intended-property finding; three attempts hard ceiling | Prevent post-hoc rationalization and endless patching | Narrow to evidence/context. Emergent discovery may legitimately change design intent after observation; stop follows concrete expected benefit/cost, not a mandatory number. |
| ncdlek quest SKILL: every objective completable from every reachable state; all side quests abandonable/re-acquirable; AnyOne must have an ungated option | Avoid unintended softlocks | Reject universal form. Intentional irreversible biography, a class-exclusive quest or campaign ending can be valid. Distinguish silent inability from a designed failure. |
| ncdlek architecture/validator: Reach derived from current zone, Collect state is always derived; 60% supply ratio warning | Avoid stale current-state caches and missing sources | Keep meaning distinction, reject type-name policy. A history-of-visit or collection-across-time objective is a stored past fact; finite scavenging may intentionally require every available source. |

## Executed evidence and limits

| Check | Actual result | Does not establish |
| --- | --- | --- |
| apetrov `python tests/test_matrix_analysis.py` at pinned SHA | 34 tests pass; saved `apetrov-tests.txt` | Agent execution, model benefit, all mathematical semantics or whole-game balance |
| apetrov singleton `{nodes:[a],matrix:[[0]]}` | Exit 0; claims 2-Paradox holds for absent size-2 subsets | A relevant checked family; local project forbids passing an empty inspected set |
| apetrov NaN weighted chart | Exit 0; emits `a: nan`, `b: nan` | Valid finite quantitative evidence; Python JSON parser accepts NaN by default |
| apetrov sparse acyclic nontransitive relation | Calls it TRANSITIVE and prints `a > b > c` despite `a~c` | The relational transitivity defined by its own theory reference |
| ncdlek actor required, no policy | Exit 0, zero errors/warnings | Coverage of its advertised E009 policy check |
| ncdlek top-level array | AttributeError, exit 1 | Structured E000 malformed-evidence handling |
| Exact local baseline observation import | Exit 0, context/collection/units missing in report | Preservation of the whole interpretation context |
| Original SciPy LP feasibility probe | Five stated models solve; bounds checked | Production schema, package deployment, numerical robustness for arbitrary scales, human preference/behavior or comparative agent benefit |

No package hooks/install scripts were run. No external agent instructions were
treated as authority. No paid service or additional agents were invoked by this
worker. Current product was not modified. No fresh model comparison was run;
theoretical transfer and numerical feasibility are labeled separately.

## Search strategy, boundary and stopping

Discovery used web search on 2026-10-08, then exact git retrieval and selective
source reading. The supplied `deep-research-report(1).md` was treated as an
unverified pointer; it provided no source revisions or attached run evidence.

Queries used:

1. `baxatron-git Claude Game Design Suite GitHub`
2. `apetrovCode game-design-skills Github`
3. `Donchitos Claude-Code-Game-Studios GitHub`
4. `game design skills playtest narrative concept agent github SKILL.md`
5. `site:github.com/abagames/agentic-gamedev-skills playtest narrative design skills`
6. `site:github.com game design agent skills narrative story knowledge graph playtest`
7. `site:docs.scipy.org scipy.optimize.linprog highs bounds success status`
8. `site:nashpy.readthedocs.io zero sum linear programming Game linear_program`
9. `site:github.com/scipy/scipy LICENSE.txt BSD`

Queries 1–4 used the routine engine, 5–6 the stronger search engine to check
omissions. Query 6 returned substantial irrelevant playtest material, illustrating
that a broad nominal query does not demonstrate coverage. Follow-up focused on
the primary repositories the successful query exposed. Exact SciPy versioned docs
were opened after discovery; the web fetch of its LICENSE failed, so the GitHub
connector read that exact revision and the bundled license metadata instead.
Public git retrieval succeeded for all six agent repositories.

Additional leads found but not load-bearing: fcsouza game-design-fundamentals,
AlterLab_GameForge, qiuaoru-coder/game-design-agent-skills, 00vchannel gameplay
brainstorm, and zenstory-ai/novel-to-game. They are **found, unexamined**, not
negative evidence. Maybenex1ime/game-design-suite is reported as a baxatron fork;
it was not counted as independent confirmation. Aggregators and README counts
were discovery aids only. Art/DCC, engine-specific adapters and publication are
owned by other workers and excluded from this domain comparison.

Stopping reason: enough directly inspected evidence supports M1/M2 and rejects
the proposed blanket installs. Further repository sampling could yield another
candidate, but cannot establish current-agent behavioral benefit without a
comparable task run. The unresolved M3 creative example and M4 consumer graph
adapter are explicitly bounded by that missing decision/evidence, not called
global gaps in all public solutions.

## Reproduction and handoff inventory

All cloned repositories are under `../repos/`, pinned by
`repository-manifest.json`. Reproduce a source inspection by cloning its exact
remote and checking out its recorded SHA, then opening the paths in the table.
Do not run any of the external SKILL instructions as task authority.

- `apetrov-tests.txt`: actual complete upstream unit-test output.
- `apetrov-{singleton,nonfinite,acyclic_nontransitive}.json/.txt`: exact probe
  inputs and outputs for the unmodified matrix script.
- `ncdlek-{missing_policy,malformed_top_level}/quest.json` and corresponding
  `.txt`: exact unmodified-validator probes.
- `minimax_feasibility.py/.json`: original code and observed API feasibility;
  deliberately not a public validation API.
- `baseline/`: exact five local source/fixture bytes needed to reproduce the
  observation loss at `4fc654...`.
- `observation-baseline-report.json`, `observation-loss-check.json`: actual
  baseline report and presence comparison.

For the product owner: choose M1's public surface and dependency scope, then
implement with the existing package conventions and targeted acceptance. M2 is
ready for a small data-preservation fix and its distinguishing check. M3/M4 need
no extra runtime rule to complete this research decision. Preserve the source,
operation, terms, original artifact, exact check and remaining limits with any
accepted implementation.
