# Publication evidence audit adjudication

## Decision

**The reported secret findings are confirmed content-hash false positives. The exact evidence exceptions described below are justified for the inspected bytes.** The proposed Betterleaks configuration passed all eight boundary controls. Final publication acceptance remains pending the primary's audit of the complete staged candidate, including the real owner policy and any newly packaged audit records.

This is a bounded independent review of publication scanner findings and their exceptions. The supplied brief requests a public pull request with the original checks and research evidence retained. The reviewer did not implement the product, modify repository files or configuration, stage files, alter original receipts, change authentication settings, or perform live credential validation.

The inspected runtime checkout was `1873993a6491b52fe8288c19837600a012e18d4d`. The initial Betterleaks config digest was `070980fba70d7b9b3e08f808e753bdd6275ad4f832b131c28ecf0db75eeaaae0`; the pinned ReleaseKit launcher digest was `fe4c3271e21ff560a3385313b1da340c48b13f271769bbabeb4d0f975a7a621d`.

## Secret findings

The reviewer independently replayed Betterleaks 1.8.1 over the comparison evidence, including ignored CI logs. It reported exactly 26 `generic-api-key` findings. Adding the behavior-independent-review archive did not change that count. The later final-product-review archive was separately scanned with the preserved original configuration and returned zero findings.

Every one of the 26 flagged source lines contains one of these three independently recomputed SHA256 values:

| Original content | Bytes | Findings | Recomputed SHA256 |
| --- | ---: | ---: | --- |
| Public access-and-return reference | 11,489 | 22 | `7c1f4c2a6c2862787c182f72f8ca9aa272126d23b5b38172a53be605010f50e1` |
| Synthetic Ink keep-token scenario | 1,484 | 3 | `bd8b9440c68a30de17b68a7ea172fa1e3d4dc1d4b98a1c75db3a8efec38c3501` |
| Redacted Claude authentication status receipt | 418 | 1 | `32cbafa4dbf86a55a202f3fac9ab1680ee98b602c759a43c325d9de270ce7747` |

The first input is `skills/game-participation-design/references/access-and-return.md`, ordinary public game-design guidance. The second is an original game scenario: its token is an inventory item, and its assertions concern story state and choices. The third retains a logged-out status, authentication method `none`, command metadata and an explicit no-credential-content scope. The last two inputs were also read directly from their published evidence ZIP members; their bytes match the original source inputs.

This conclusion depends on the source bytes and manifest/receipt context. It does not infer that arbitrary hexadecimal values, filenames containing “token,” or authentication-related files are safe. The exact 26 locations are recorded in `expanded-hash-adjudication.json`. No credential values were exposed or used to adjudicate them.

## Betterleaks exception boundary

`proposed-betterleaks.toml` preserves the default rule extension and adds three targeted allowlist blocks. Each requires all of the following:

- `targetRules = ["generic-api-key"]`;
- `condition = "AND"`;
- `regexTarget = "secret"` and a fully anchored, single exact digest;
- an anchored path matching one of the actual evidence files or actual ZIP members.

The proposed file digest is `8f896d42bc9b279ed565752ee46138ef738de15012fd54a6cfe34d6633652d78`. With it, the expanded comparison evidence scan changed from 26 findings to zero. No broad directory allowlist, generic 64-hex exception, filename exception, rule disable, or secret-engine disable was used.

| Independent control | Original config | Proposed config | Result |
| --- | ---: | ---: | --- |
| Exact allowed path and digest | 1 finding | 0 findings | Pass |
| Same path, changed digest | 1 | 1 | Pass |
| Same path, unrelated synthetic 64-hex credential | 1 | 1 | Pass |
| Same digest, different path | 1 | 1 | Pass |
| Allowed path with an added suffix | 1 | 1 | Pass |
| Exact allowed ZIP member and digest | 1 | 0 | Pass |
| Same ZIP, different member | 1 | 1 | Pass |
| A second detection rule at the allowed path and digest | Test-only rule | Second rule still detects | Pass |

The last control used a test-only additional detection rule in a separate configuration; that rule is absent from the proposed repository configuration. Synthetic control inputs were never sent to a credential provider. `scanner-boundary-probes.json` and the redacted command receipts preserve the results.

The pinned upstream implementation explicitly supports targeted allowlists, AND conditions and the secret regex target: [config/config.go at v1.8.1](https://github.com/betterleaks/betterleaks/blob/v1.8.1/config/config.go), especially the targeted-list processing and `parseAllowlist`, and [config/allowlist.go at v1.8.1](https://github.com/betterleaks/betterleaks/blob/v1.8.1/config/allowlist.go). The executable controls establish the behavior used here.

## Exact ReleaseKit exceptions

Five archives and four CI logs were inspected. All 298 archive member payloads were reopened and hashed. The structural review found no unsafe ZIP member paths or symlinks. The public-rule probe found only the categories below; it found no additional built-in AI-attribution, internal-planning or machine-observation categories in these bytes.

All paths in this table are below `docs/reviews/2026-10-08-comparison/`:

| Exact path | Observed cause | Why an exception is justified |
| --- | --- | --- |
| `behavior-evidence.zip` | Five `.log` members; captured home-like paths in native receipts, tool paths and agent identities | Original execution and provenance evidence requested for publication; not installed path configuration |
| `integration-evidence.zip` | Four `.log` members | Raw glTF and observation test output |
| `native-model-preflight.zip` | One empty `.log` member | Original preflight stderr boundary, including its empty result |
| `behavior-independent-review.zip` | Native-catalog home paths and the archived replay script's sibling-directory reference | Captured catalog context and original replay implementation; not a claim that the archived script is portable without its evidence layout |
| `final-product-review.zip` | Three home-directory matches of a canonical reviewer agent identifier | Reviewer identity begins with the root task namespace; these occurrences are not filesystem locations |
| `ci-runtime-113456576647.log` | `.log` suffix | Original hosted CI output |
| `ci-runtime-113456576836.log` | `.log` suffix | Original hosted CI output |
| `ci-runtime-113456576892.log` | `.log` suffix | Original hosted CI output |
| `ci-runtime-113456576901.log` | `.log` suffix | Original hosted CI output |

Use these nine exact paths, without wildcard or parent-folder exclusions. Preserve the original evidence bytes and digests.

**ReleaseKit scope qualification:** its exact-path exclusion is not a per-rule structural allowlist. In the pinned code, it omits all suppressible rules for that path, including the general AI/internal-planning/machine-observation heuristics and ordinary archive-path findings. Declared private-value, owner-workflow, personal-data and private machine-observation patterns remain enforceable, together with archive inspection limits and external-content checks. Betterleaks is invoked independently and is not disabled by these exclusions. A direct synthetic-marker probe confirmed that all four private owner categories still propagate through the excluded-archive payload path.

This behavior was checked in the pinned `releasekit/exposure/audit.py` exclusion branch, `_owner_payload_details`, `UNSUPPRESSIBLE_KINDS`, and the separate `releasekit/engines.py` invocation. The actual private owner policy was not read by this reviewer. The primary's final owner audit remains required. An exact path is not a content-digest lock; replacement bytes at an excluded path need renewed review.

## CI log links and remaining gate

All four cited CI logs exist and were scanned. At inspection they were untracked and matched `.gitignore`'s `*.log` rule. The pinned Lychee integration materializes tracked files plus unignored candidates, which explains their absence from the initial audit snapshot. Stage the four exact owned logs and rerun the staged link audit; a link-check exclusion is unnecessary.

The primary owns the final complete staged audit, build and smoke checks. This review does not claim that those later checks have run or passed. New public packaging of these audit receipts must be included in that final scanner boundary. Product correctness, behavioral efficacy, billing and general security certification are outside this narrow adjudication.

## Receipts and process limits

`selected-public-receipts.json` identifies the report, read scope, decisive input identities, exact proposed config, raw redacted scans, and control results suitable for retention. Synthetic probe input directories are unnecessary for the publication record; the probe script and redacted outputs preserve what was executed. The script records the original fixed workspace and was executed while the repository still held the original 98-byte Betterleaks configuration.

The first control harness attempt failed while interpreting Betterleaks' JSON `null` for zero findings as an iterable. That harness error was corrected to treat it as an empty result, and all eight controls were rerun. The first attempt and its scanner outputs remain preserved separately. It was not a product or scanner failure.
