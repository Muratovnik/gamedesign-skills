# Integration review — initial findings and recheck log

**Current scoped verdict: PASS after correction and the hosted lifecycle receipt recheck below. Initial findings and pending statements are retained as historical records. No global-document or whole-repository approval is implied.**

## Scope and independence

This is a new bounded review of the dirty Game Design source rooted at `/workspace/scratch/e429285ef1e1/gamedesign-skills`, HEAD `a0db5af71146586cf861881670c991ad94d87e2b`. The initial 50-file snapshot and exact SHA-256 identities are in `identity.json`; supporting owner methods and requirements are in `support-identities.json`. The native CI implementation at `babfe5db84821bf8c77d5c95844108e22f650835` was retrieved through this repository's Git object store and equals the initial reviewed native script; see `native-ci-source-check.json`.

The reviewer did not author the subject and changed no product source, tests, configuration, client state or Git history. Probes used only task-owned copies under this report directory. An initial Python suite attempt used an environment without jsonschema and failed collection; it establishes no product failure or regression coverage. Corrected targeted checks used the already established dev-venv Python. Native output was independently read from the caller-provided hosted receipt, not reproduced locally by this reviewer.

Applied criteria: Game Design AGENTS, supplied OR-02/10/11/15/16 and GDE-01/04/08/09 (selected relevant sections, not a claim to have re-audited their entire bibliographies), and Assay independent-audit, test-audit, software-architecture and code-change with the applicable evidence, bounded review, dependency reuse, runtime, lifecycle and effective-check references at pinned Assay `94c517b0aac9ba2575086bf9aead1cc828aadb0d`.

## Initial verdict: FAIL; correction recheck pending

The initial glTF output guard demonstrably created the input at an aliased missing path. The initial native verifier demonstrably rejected valid native outputs and had material false-acceptance/evidence gaps. This is a verdict on the verifier/candidate as inspected; it does not assert native-client runtime defects. The observation metadata correction passes its bounded contract. Root is correcting the reported issues; the initial findings remain historical evidence until the exact corrected bytes are rechecked.

## Confirmed findings

### F1 — MEDIUM: glTF report can become its missing input through a path alias

Initial `skills/game-design/scripts/validate_gltf.cjs:198` compares only `path.resolve` strings. With an owned directory symlink `alias -> real`, run `node CLI alias/missing.gltf --output real/missing.gltf`. The conformance receipt reports unavailable/ENOENT, but `writeNewReport` resolves the output parent and creates the input's effective path containing the JSON receipt. No concurrent changes are needed. This violates the explicit separate-report contract including currently missing inputs.

Actual reproducer and preserved output: `gltf-alias-output.json`. Nearby valid control: missing `alias/distinct-missing.gltf` plus separate `real/valid-report.json` remains allowed, preserves the missing input and saves the exact stdout receipt; see `gltf-alias-valid-control.json`.

Supported correction: identify the effective prospective input/output destinations, including symlink ancestors and dangling aliases, and refuse equality before publication. Root's prospective-path correction is present but was not part of the initial test receipt.

### F2 — MEDIUM: native verifier rejects namespaced Codex skills and disabled Claude details

Initial `tools/qualify_native_clients.py:180-182` expects unqualified names. Codex 0.159.2 actually returns all seven `game-design:<skill>` names with the correct pluginId and enabled state. Initial line 235 requires exit 1 for disabled Claude details; Claude 2.1.289 returns 0 and the same component inventory while native `plugin list` reports enabled=false. These wrong expectations stop the later update/rollback scenarios, so they cannot provide lifecycle acceptance.

Observed evidence: first hosted receipt SHA-256 `aa15522a5db8c34d4f4054f707a9bb41414e6e6ed043b717debb37c5885ead88`, original file `/workspace/scratch/e429285ef1e1/research/native/native-client-first-receipt.json`. Both actual outputs were read, and both native versions are recorded there. The correct inventories/settings are counterevidence to a Game Design package failure. A new hosted run is needed after correcting the oracle.

### F3 — MEDIUM: Claude checks the cache instead of its reported effective load source

Initial line 240 hashes and executes `installPath`. The actual 2.1.289 receipt also returns `readFromFolder`, which the current official JSON field documentation identifies as the source sessions load in place. That source differs from the cache in the observed baseline. A candidate cache can be correct while a stale same-version folder remains the effective native source; bare skill names/version and cache hashes cannot discriminate that mismatch.

Supported correction: select readFromFolder when supplied, bind it to the intended source, record both path roles, and check/execute the effective bytes. The absence of this comparison is a verifier defect; no actual stale-source client bug is asserted.

Primary reference read: https://code.claude.com/docs/en/plugins/cli-reference (JSON output, readFromFolder/installPath and plugin details sections). The native receipt, not the web page, establishes the exact tested build's disabled-details behavior.

### F4 — MEDIUM: substring inventory check accepts a missing router skill

Initial line 238 tests `all(name in details.stdout ...)`. A correct plugin title `game-design 0.1.1` and Source already supply `game-design`, so a `Skills (6)` inventory missing that router still satisfies all seven expected substrings. The nearby seven-skill inventory also passes. These exact predicate controls are preserved in `native-oracle-controls.json`.

Supported correction: parse the native component inventory for the pinned build and compare exact names and reported count. This tests discovered components, not general mentions of their names.

### F5 — MEDIUM: exact revision comparison ignores additional installed runtime files

Initial `resource_action` lines 106-111 builds observed hashes only for expected source names. An installed tree containing every old file plus a candidate-only runtime reference passes as the old revision. The real resource_action and observation subprocess were executed against such a disposable tree, with a valid unchanged-tree control; see `native-extra-file-control.json`. The extra file was present but absent from verified_skill_files.

Supported correction: enumerate both source and installed skill file sets using the same deliberate cache exclusions, then compare sets and hashes. Otherwise rollback evidence establishes presence of old files but not restoration of the selected runtime tree. No native stale-cache behavior is asserted.

### F6 — MEDIUM: incomplete command evidence drops timeout output

Initial run() lines 50-52 append a command only after subprocess.run returns. A TimeoutExpired carrying partial stdout/stderr leaves commands empty; the ordinary completed-command control retains both streams. See `native-oracle-controls.json`. Initial codex_skills also gathers stderr but never stores it and can reduce queue.Empty to an empty error string, obscuring the failed protocol stage.

This undermines the workflow's promised preservation of actual incomplete evidence and OR-11's distinction between attempt, result and consequence. Supported correction: record the attempt before acquisition, preserve partial output/timeout status and protocol-stage diagnostics, and retain cleanup outcome. This is evidence loss, not an assertion that a timeout occurred in the first hosted run.

## Covered claims with no additional defect found

| Area | Observed basis | Bounded conclusion |
| --- | --- | --- |
| Official glTF mechanism | Actual installed README/index/ISSUES inspected; validateBytes owns parsing/link/data checks | Library delegation is real; local code owns authorization, classification and report publication |
| Dependency identity | SHA-512 of retained npm tarball equals package-lock integrity; seven inspected executable, license and documentation files match the archive | Exact probe dependency is identified; see dependency-integrity.json |
| Format vs game predicate | Empty and camera-only assets pass, invalid accessor fails, caller_predicate remains not_evaluated | No triangle/game-quality proxy imposed by CLI |
| External resource authorization | Shipped suite exercises no explicit root, remote HTTP request counter, path and symlink escapes plus permitted local counterparts | Controls discriminate denial and legal local input; concurrency is explicitly outside the filesystem guard claim |
| Resource/coverage status | Missing data and unsupported extension return unavailable; malformed recognized JSON and bad accessor refute | Missing evidence is separated from conformance failure as documented |
| Existing report protection | File/symlink overwrite and competing writers checked by shipped suite | Existing targets remain intact; F1 concerns a missing aliased target |
| Observation preservation | Two exact saved-report tests pass; removing the three metadata return fields makes the new test fail at missing conditions | New conditions, collection_method and units survive serialization/reopen; see observation-targeted-tests.log and observation-mutation-control.json |
| Human/material claims | Synthetic record kind and human_claim=not_established remain through saved output | Import success is not promoted into consent, learning, perception or a human study |
| Native safety scope | CLI requires disposable-user acknowledgement and Linux; workflow uses a disposable hosted user with exact client versions | No live owner client changes were performed by the reviewer; native evidence remains restricted to actual reached stages |

## Actual probes and limits

- Node v24.19.0, Linux x64; official gltf-validator 2.0.0-dev.3.10. Initial shipped glTF suite: 18 tests, 18 pass, no skips (`gltf-tests.log`).
- Independent fixture inspection verifies the original 36-byte position data and GLB layout; see `fixture-inspection.json`. Additional whitespace-prefixed valid JSON controls pass (`gltf-format-controls.json`).
- Python 3.12.14 with the existing project dev-venv for the two observation tests and real observation CLI calls. The unprepared default-environment failure is retained separately in `observation-tests.log`.
- Native first hosted receipt: Codex initial discovery and Claude baseline/install/disable reach their observed boundaries; later lifecycle stages are unreached because of F2. No local native settings were used by the reviewer.
- Native `plugin list.enabled` establishes the merged enable setting. Claude `details` displaying a disabled package cannot prove its absence from a model session. Automatic selection, model execution of a conditional sibling read, model quality, human experience and other operating systems remain separate claims.
- Initial check.yml does not run the new glTF suite, and the glTF route is not yet linked from the Game Design entry/environment route. Root explicitly identifies these as pending global integration work, so they are open handoff obligations rather than silently accepted coverage.
- Ink, matrix solver, unrelated domain edits, release archives and the rest of repository-wide behavior are outside this assignment. Reading their filenames does not count as review.

## Source drift and corrections

`drift-check-1.json` observed task-owner fixes only in validate_gltf.cjs and qualify_native_clients.py relative to the initial snapshot. Rechecks must bind to corrected source identities. No prior baseline review is reused as independent approval of these new files.


## Correction recheck — local result PASS, hosted lifecycle pending

The caller finalized the requested repairs and explicitly extended this review to `tests/test_native_qualification.py`, the Game Design SKILL routing edits and the narrow environment-contract links. Exact corrected identities are in `correction-identity.json`. The subsequent `correction-drift-check.json` is empty for all twelve scoped corrected files.

The corrected glTF script SHA-256 is `41c4922e4e5eb4bcf5819decf5b07b41280aa13beac7469dee1110e0dd69e44b`. Its shipped suite passes **19/19** with no skips, including the added missing-input directory-alias, dangling-symlink and distinct-report controls (`gltf-correction-tests.json`, `gltf-correction-tests.log`). F1 is closed for the tested Linux filesystem boundary. Existing concurrent-filesystem limitations remain explicit; other OS filesystem behavior is not established by this run.

The corrected native verifier SHA-256 is `b3eac3ae3d2355ce468355aa5a5cacf1714101a41c9796e7129cc9d7e2161321`. All **3/3** new native-oracle tests pass (`native-correction-unit-tests.json`): real command timeout preserves attempt/partial output, exact component parsing does not derive a skill from the plugin title, and the actual runtime operation succeeds on a normal tree then refuses a surplus runtime file. These are verifier checks, not new native client runs.

Additional normal and invalid-JSON app-server controls used actual owned synthetic child processes. The corrected verifier retains the method, invalid response/error, stderr and exit status, and both owned processes are observed stopped (`native-protocol-correction-controls.json`). No real client settings, model session or remote process was used.

The corrected exact parser and namespace expectation were also applied to the independently preserved **actual** first-run outputs: both Claude details inventories and the Codex seven-skill list now match the expected identities (`native-captured-response-recheck.json`). The source now chooses and checks Claude readFromFolder as its effective source and records that role; installed path sets and hashes are compared symmetrically. F2–F6 are closed as the concrete local oracle/implementation defects, with hosted rerun still required to establish formerly unreached lifecycle stages.

The new Game Design description explicitly includes requested glTF/GLB checks and importing observations. Its early branch sends an established artifact-operation task directly to the environment route. Both the SKILL owner table and environment table now lead to the skill-local glTF reference, which leads to the actual CLI, manifest and lock. The routing keeps conformance separate from game requirements and does not force concept development or a new format onto an adequate paper task. Ink/matrix links were checked only for their conditional placement and target existence; their implementation remains with the separately assigned reviewers. No model-selection or behavioral-improvement result is inferred from these authored routing edits.

Current check.yml invokes the new glTF suite in `artifact-operations`, installing the locked tools into RUNNER_TEMP and passing GD_GLTF_SCRIPT to that copy. `tests/test_native_qualification.py` is covered by the existing root unittest discovery. The native job uses its exact clients and previous source and preserves its receipt/lock even on an incomplete run. This source check closes the initial missing-wiring obligation; the future hosted outcome remains a separate claim.

No additional in-scope defect was found during the recheck. The overall native lifecycle acceptance remains INCONCLUSIVE until the corrected hosted receipt verifies the required stages. This is not a reason to repeat unchanged local tests.


## Hosted lifecycle receipt recheck — PASS for the stated native scope

The caller supplied the completed GitHub artifact for run `37819498740`, native job `113456576892`, artifact `11568218182`, candidate `1873993a6491b52fe8288c19837600a012e18d4d`, tree `237e2892adefbf170c149ac644b0c4a18b31ba76`. The reviewer independently read the archive and materialized receipt, compared their bytes, checked Git object contents and the corrected twelve scoped source identities, and derived expectations from the two Git revisions and fixture contents. Native clients were not rerun by this reviewer; GitHub run identifiers and server-download provenance are caller-supplied rather than independently authenticated here.

The archive SHA-256 is `f78b01ed5ec0bab19c9a7a6b26e678aacbee6027b3d47c4d50f3fe058391a24f`; the receipt SHA-256 is `87d9d9c379cc6df24b79e5447fa83953937bef3fb55aa469ad2abe9a3973da24`. The archive receipt exactly equals the supplied JSON. The local HEAD/tree match the candidate, and all twelve corrected scoped file identities remain unchanged. The reviewed native verifier remains `b3eac3ae3d2355ce468355aa5a5cacf1714101a41c9796e7129cc9d7e2161321`.

Independent check details and a reproducible read-only verifier are in `native-qualified-verification.json` and `verify_native_qualified.py`: **144/144 assertions pass**. These assertions inspect receipt contents; they are not 144 new product scenarios. The receipt contains 72 completed commands, 24 observations, no errors and status `supported`. The sole nonzero command is the deliberately requested Claude details lookup after target removal (exit 1). Recorded executables report Codex `0.159.2`, Claude Code `2.1.289`, and their packaged lock versions agree. The environment is Linux `6.17.0-1022-azure`, x86_64/glibc2.39, Python `3.12.15`.

| Observed property | Codex | Claude Code |
| --- | --- | --- |
| Initial owned installation state | Registered-plugin inventory empty | Registered-plugin inventory empty |
| Baseline installation | Exact seven namespaced target skills enabled; source file set/hash match baseline | Local enabled setting true; exact seven component names; effective readFromFolder matches baseline |
| Disabled stage | Setting false; target absent from a fresh app-server skills/list; sentinel remains | Setting false; details still exits 0 with the same seven-skill inventory |
| Reenabled stage | Seven target skills return; actual resource operation succeeds | Setting true; component inventory correct; effective-source resource operation succeeds |
| Candidate replacement | Native seven-skill inventory; all 59 candidate skill files match Git | Native inventory; effective source changes to candidate; all 59 skill files match Git |
| Rollback | Native seven-skill inventory; exact baseline set of 48 files restored | Effective source returns to baseline; exact baseline set of 48 files restored |
| Target removal and sentinel cleanup | Target absent from native inventory; sentinel registration retained unchanged; final registered-plugin inventory empty | Target details exits 1; sentinel registration retained unchanged; final registered-plugin inventory empty |

All six Codex app-server processes complete with exit 0. Each captured protocol skills/list result equals its recorded inventory observation, with one workspace and no parser errors. The sequence contains seven, zero, seven, seven, seven, zero target skills respectively. System-provided skills coexist and are not mistakenly counted as target or sentinel components.

The eight recorded resource operations, four per client, are baseline → reenabled → candidate → rollback. Full skill path sets and all SHA-256 values independently equal the intended Git revision, including the 48 → 59 → 48 transition even though both releases identify themselves as version 0.1.1. The imported CSV rows and manifest hashes match the actual Git fixtures. Candidate outputs preserve conditions, collection_method and units exactly; rollback outputs restore the baseline shape. Every report remains synthetic, has the expected four rows and counts, and retains human_claim=not_established. This verifies persistence and code identity for the exercised resource operation without upgrading synthetic input into empirical game evidence.

### Exact limits of the now-supported claim

This receipt establishes fresh disposable-user, Linux, local-source **registration and inventory lifecycle** on the exact pinned client versions. It exercises candidate replacement and rollback by uninstalling, replacing marketplace registration and reinstalling at the same plugin version. It does not establish automatic marketplace upgrade, a package version migration, compatibility with other client versions or other operating systems.

Claude's disabled merged setting is observed false, but details remains an inventory operation and proves neither model-session activation nor deactivation. Codex's native skills/list does establish inventory disappearance for the disabled target in a fresh app-server. All resource actions are executed by the external verifier. Automatic method selection, a model following a skill, behavioral improvement and human play quality remain untested by this receipt.

The full sentinel registration records remain unchanged across the target lifecycle. This is a valid neighboring control for registration interference. Final registered-plugin lists are empty after owned cleanup. It does not imply all task-owned work/config directories were deleted, nor establish preservation or restoration of arbitrary game saves, unrelated settings or plugin persistent data; those objects were not seeded and tested.

The formerly pending native hosted lifecycle obligation is now closed within these limits. No new in-scope defect was found. F1–F6 remain closed by the previously recorded fixes and targeted controls. No unchanged local tests were unnecessarily repeated. Ink and matrix implementations, global documentation, complete release/CI outcomes and the remainder of the repository remain outside this scoped review.
