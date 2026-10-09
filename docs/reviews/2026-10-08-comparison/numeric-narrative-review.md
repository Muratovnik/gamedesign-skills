# Independent review: numerical and native narrative operations

## Scoped verdict

**PASS for the frozen numerical and native narrative scope. No confirmed in-scope defect.** This is a local source/runtime review, not an acceptance statement for the whole PR, native client discovery, behavioral comparison, publication, or pending global documentation/CI integration.

The review used the task assignment, the Game Design `AGENTS.md` owner contract, and the supported journeys and interfaces declared by the two runtime references. Assay's independent-audit and test-audit methods supplied the audit procedure; the relevant code-change and software-architecture criteria supplied the responsibility, state, reuse, runtime and evidence checks. I did not implement the subject or edit its source, tests, documentation, configuration or Git history. I did not read behavioral evaluation packets or spawn children.

## Subject identity

- Actual Git root: `/workspace/scratch/e429285ef1e1/gamedesign-skills`.
- HEAD/base: `a0db5af71146586cf861881670c991ad94d87e2b`, with the supplied uncommitted candidate changes.
- Assay method HEAD verified: `94c517b0aac9ba2575086bf9aead1cc828aadb0d`.
- Scope: both new runtime scripts, their dependency declarations and references, both owning SKILL diffs, and all files under `examples/strategy-matrix` and `examples/ink-episode`.
- All 21 scoped files were hashed before probes and rechecked afterward. **No drift.** See `source-identity-initial.json` and `source-identity-final.json` for the full inventory.

| Executed runtime | SHA-256 |
| --- | --- |
| `skills/game-systems-design/scripts/solve_zero_sum.py` | `4e3e1aabb39f2da092e0a4a073137a3712061201e531ad7dfd64731cae58de10` |
| `skills/game-world-narrative-design/scripts/ink_artifact.cjs` | `71b26b510eed8646cd05ebcbee9fc84f856d4e3ca6d7421562856387d1df39ce` |
| Executed `inkjs/dist/ink-full.js` | `23d707b76e9b759a25803c193da8e32e04f727dd13a54ed1df8a6a59dd909b9e` |

Actual environment: Python 3.12.14, SciPy 1.17.0, NumPy 2.3.5, Node v24.19.0, inkjs 2.4.0. No global installation or client settings change occurred. All generated probe and test-temporary artifacts were under this review directory. The already installed, task-owned Ink dependency was read from `research/environment/ink-i1-deps-l4jwg44g/node_modules/inkjs`.

## Coverage and conclusions

| Area and required outcome | Evidence and conclusion |
| --- | --- |
| Explicit, bounded two-player zero-sum expected utility | **CONFIRMED.** Source validates the model declaration, cost/context descriptions, distinct players, nonempty named axes, rectangular finite binary64 payoffs, strict fields and duplicate JSON keys. The supported one-sided/singleton and intentionally dominant-action cases remain legal. General-sum preferences are not silently discarded. |
| Numerical solution and independent certificate | **CONFIRMED.** The two LP signs and free value-variable bounds match the documented maximin/minimax programs. Reported probabilities are checked before and after bounded drift repair. The certificate recomputes best-response arrays from the normalized matrix and reported mixtures, independently of LP constraints/status. Source checks finite quantities, simplex residuals, LP-value disagreement and normalized gap. Independent exact-arithmetic probes below corroborate these checks against the original input matrix. |
| Conditioning and useful representation | **CONFIRMED within the declared binary64/tolerance contract.** Positive affine normalization preserves the tested unequal-stakes, large-offset, maximum-finite and subnormal cases. The report retains named mixtures, original input/model identity, engine/options/status, normalized quantities and restored utility-unit values. The references accurately limit the tolerance and warn that restored decimal bounds can lose small distinctions around large offsets. |
| Genuine native Ink lifecycle | **CONFIRMED for selected language constructs and paths.** The adapter calls the real pinned compiler, `Story`, continuation/choice methods and native state serialization/load. Source is compiled, saved JSON is reopened, and a fresh process resumes the saved native state. Extra probes restored a changed global that the first scenario had not observed, confirming that the envelope does not replace native state with a scalar snapshot. |
| Caller choice and observation semantics | **CONFIRMED.** The adapter has no autonomous choice policy. Unavailable/ambiguous labels and invalid indices fail; an index selects the corresponding offered choice. Legal departure, sticky choices, ordinary Ink functions, uncalled external declarations, lists used as narrative text, and silent endings remain usable. Selecting undeclared globals or complex native values as scalars is unavailable. |
| State/report identity and assessment coverage | **CONFIRMED for the declared local handoff.** Saved compiled/dependency/native-state identities and fresh-runtime checkpoints are checked. Assessment requires exact compiled/scenario/adapter identities, complete observation/action counts, ordered observation steps, all selected scalar variables, valid choice/terminal shape and matching requested actions. Stale or malformed evidence produces exit 2; a false predicate in usable evidence produces exit 1; no predicates cannot pass. Hashes are correctly described as identity checks, not authentication. |
| Resource and external-operation boundary | **CONFIRMED within the explicit scope.** Actual includes are denied through the compiler file handler, host calls have no binding, and even a supplied Ink fallback remains unavailable under the documented policy. Ordinary native functions and commented/ordinary uses of the word INCLUDE remain valid neighbors. Native loops hit the continuation/deadline boundary without a completed state; an exact output-character bound admits its valid neighbor. The worker is described as a deadline boundary, not a security sandbox. |
| No clobber and ownership | **CONFIRMED.** CLI probes preserved ordinary files, directories, existing symlinks and dangling symlinks as applicable. Scripts require new output locations and use exclusive creation. Runtime dependencies/resources are local to each skill contract; checkout fixtures and tests are not runtime dependencies. |
| Dependency mechanism and terms | **CONFIRMED for the inspected packages.** SciPy performs optimization; NumPy provides arrays; inkjs performs parsing, compilation, interpretation and save serialization. Node's standard library provides argument parsing, files, hashes and workers. Owned code remains the model/scenario contracts, numerical certificate, explicit action adapter and predicate assessment. Installed SciPy metadata confirms NumPy `>=1.26.4,<2.7`; the inspected runtime satisfies that range. SciPy and NumPy's project notices use BSD terms, and their binary distributions retain additional bundled-component notices; inkjs's MIT notice and lack of runtime npm dependencies match the reference and lock. No dependency implementation is vendored in this scope. |
| Optional game-design route | **CONFIRMED as source instructions.** Both references route to execution only for an actual numerical or native-artifact claim. They preserve sufficient paper work, expressive scenes, accepted endings and intended hierarchy. None of the runtime results certifies human understanding, enjoyment, balance or global story reachability. Model behavior in applying these instructions remains outside this review. |

## Executed checks and their oracles

### Delivered suites

Both suites were read before execution. Their expectations were compared with the public contract and relevant source, not accepted solely from an author summary.

- `python -B -m unittest discover -s <repo>/examples/strategy-matrix -p 'test_*.py' -v`: **18 tests passed**, real SciPy dependency, no skips. Receipt: `matrix-suite.json`.
- `node --test <repo>/examples/ink-episode/test_ink_artifact.cjs`: **8 tests passed**, exact installed inkjs dependency, no skips. Receipt: `ink-suite.json`.

The mathematical suite's useful oracles include exact unequal-cycle fractions, affine transformations, negative and rectangular values, degenerate optima, named-axis permutation, legal dominant/singleton cases and refusal of corrupted solver candidates. Candidate/status corruption runs through the real solver and CLI but proves the adapter's guard, not the solver's intrinsic failure behavior.

The native suite's strongest negative control removes only the sharing guard from a story that still compiles and executes. The unchanged assessor refutes precisely the first availability predicate. A compiler failure cannot substitute for this control. Fresh-process save/resume, legitimate departure, terminal/no-action behavior, identity failures, choice ambiguity, native runtime errors, includes/host functions, loops and collisions reach their actual operation boundaries.

### Independent matrix probes

Command: the primary-runtime Python executing `probe_numeric.py` from this review directory. Receipt: `numeric-probes-summary.json`; every selected input, persisted report and command/stdout/stderr receipt remains under `numeric/`.

**19 successful CLI calculations** were checked with a separate exact-Fraction oracle. For two-row games the oracle maximizes the lower envelope of all column payoff lines at endpoints and pairwise intersections. It does not call the product's normalization, LP construction or certificate helpers. A second check evaluates original binary64 payoff values and emitted probabilities in exact rational arithmetic to recompute the response bounds.

The selected cases include twelve deterministic asymmetric/rectangular matrices, maximum-finite constant/symmetric/asymmetric matrices, a near-maximum common offset, the smallest subnormal scale, an asymmetric subnormal matrix and a valid new-output control. The largest independently recomputed normalized gap was **1.376676550535194e-16**. File, directory, ordinary-symlink and dangling-symlink collisions were rejected with `output_unavailable`, preserving the existing objects and bytes.

### Independent native probes

Command: the primary-runtime Python executing `probe_ink.py` from this review directory. Receipt: `ink-probes-summary.json`; all **34 final CLI commands** produced their expected result. Native sources, selected scenarios, compiled outputs, save envelopes, reports, assessments and exact command receipts remain under `ink-v2/`.

The additions cover native sticky-choice state, restoring a previously unobserved changed global, no text replay on resume, a truly silent native END, valid uncalled externals and ordinary Ink functions, rejected external fallback calls, commented INCLUDE, a native list's useful text representation versus unavailable scalar observation, an unavailable global, exact output limits, malformed report structure, adapter/story byte drift and file/symlink collisions.

One initial review-harness expectation was wrong: a fresh silent END generated one `{text: "", tags: []}` chunk, rather than an empty chunk list. The native behavior was retained; the probe was corrected to assert empty concatenated emitted text. The initial script, observations and failure explanation remain in `probe_ink-initial.py`, `ink/` and `ink-probe-initial-oracle-failure.json`. This was a probe-oracle failure, not a product defect or hidden skipped check.

## Limits and remaining owner work

- Global docs/CI integration was explicitly still pending and is not certified here. Neither its pending status nor absence of a full-PR gate was treated as a runtime defect.
- This review does not establish client discovery, engine/editor import, publication, behavioral improvement, human comprehension/dramatic effect, general-sum analysis, every Ink construct/branch or state migration. The product references make the corresponding limits visible.
- The pinned SciPy API documentation was successfully read at `https://docs.scipy.org/doc/scipy-1.17.0/reference/optimize.linprog-highs.html`. The web tool blocked the pinned GitHub metadata/license pages; exact installed package metadata and license notices were inspected instead. Full dependency evidence is in `dependency-evidence.json`. This does not certify every historical provenance assertion about upstream commits or re-run the earlier original-package comparison.
- No product fixes are requested by this scoped review. Reuse is substantive: the adapter delegates the technical mechanics to the maintained numerical and native narrative libraries while retaining game-specific contracts and evidence checks locally.
