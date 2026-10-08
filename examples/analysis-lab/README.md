# Lantern Crew analysis lab

This original synthetic campaign joins owned resources, a state migration,
permitted observer views, content selection, telemetry meaning and observation
import. Each operation has a real file input and a downstream consumer. It uses
Python's JSON, CSV and SQLite facilities plus the installed JSON Schema library;
it does not implement a general game engine, narrative VM or analytics service.

**Problem:** Ava is away with a personal archive pass. Bo returns with the winch
unlock; Cy contributes a route decision. The crew has four scrap pieces and a
lost generator; repair costs six. A free survey yields two. Migration must keep
who owns what, who knows what, and the already-emitted archive-message history.
Accepted election can move treasury authority from Ava to Bo; absence alone
does not assign another participant's personal pass.

## Prerequisites and output handling

Use Python 3.11+ with `jsonschema==4.26.0` in a disposable or project virtual
environment. The recorded environment used Python 3.12.14. From the repository
root, create an isolated environment if needed:

```bash
python3 -m venv .venv
.venv/bin/python -m pip install -r examples/analysis-lab/requirements.txt
```

Commands below run from the repository root. Set `PYTHON` to the chosen
environment's executable. Outputs must be new paths: commands do not replace
an existing save, report or database.

```bash
PYTHON=.venv/bin/python
OUT=$(mktemp -d)
```

All JSON shape checks call the real
[Draft 2020-12 validator](https://python-jsonschema.readthedocs.io/en/stable/validate/).
The schemas and reusable validator live inside
`skills/game-design/assets/` and `skills/game-design/scripts/`. Passing one
establishes a data-format condition. The consumer operations below establish
the narrower relations actually exercised.

The shared JSON boundary rejects non-finite numbers, including overflowing
numeric literals. Save roots and versions are checked before accessing their
fields; nested records and boolean values are then checked by JSON Schema.
Malformed artifacts return structured invalid/missing evidence with exit 2.
They do not count as a refuted game property or create a changed output save.

## Resource stocks, transfers and conversion

```bash
"$PYTHON" examples/analysis-lab/lab.py resources \
  --input examples/analysis-lab/fixtures/resource-model.json \
  --output "$OUT/resources.json"
```

The four-row trace begins with crew=4, Ava=2, Bo=0 scrap pieces. The personal
transfer changes Ava to 0 and Bo to 2 without changing total scrap. The free
survey adds two crew pieces; conversion consumes six crew pieces and produces
one generator device. Final scrap is crew=0, Ava=0, Bo=2. Adding generators to
scrap would mix units, so the report records separate quantities.

The model's independent balance relation is `6 + 2 - 6 = 2` scrap pieces.
The generated device is a separate output. Setting survey yield to zero
refutes this repair path because four pieces cannot pay six. Transfers reject
overspending and invalid owners before changing the supplied stock. This is a
conditional resource model, not measured production-economy behavior.

## Waiting distribution and sensitivity

```bash
"$PYTHON" examples/analysis-lab/lab.py waiting \
  --p 0.1 --horizon 30 --guarantee-at 12 --output "$OUT/waiting-p01.json"
"$PYTHON" examples/analysis-lab/lab.py waiting \
  --p 0.2 --horizon 30 --guarantee-at 12 --output "$OUT/waiting-p02.json"
```

These are analytic calculations for independent, identical attempts until the
first desired result, using Python floating-point arithmetic. Each output includes
the probability at every attempt through the horizon and the remaining tail.
They do not use sampled participants or a random seed.

| Parameter | Mean attempts | 95th-percentile attempt | Still waiting after 30 | Mean with a guarantee at attempt 12 |
| --- | ---: | ---: | ---: | ---: |
| p=0.1 | 10 | 29 | 0.0423912 | 7.17570 |
| p=0.2 | 5 | 14 | 0.00123794 | 4.65640 |

The geometric tail is `(1-p)^n`; mean waiting with a guarantee is
`(1-(1-p)^k)/p`. Those assumptions justify the calculation, not a claim about
players' patience. A guarantee also changes expected issuance, so it cannot be
described as affecting only unusually unlucky players.

The implementation uses
[`log1p` and `expm1`](https://docs.python.org/3.12/library/math.html#power-and-logarithmic-functions)
to avoid subtractive cancellation in the quantile and guaranteed mean. At
p=1e-18, the capped mean remains approximately 12 attempts. The p=1 endpoint
returns one attempt. A probability must produce both a finite mean and a finite
floating-point p95 estimate; otherwise the command returns 2 with a numerical
range explanation and writes no output. On the recorded binary64 host, the
smallest accepted probability at that boundary was
`1.6664313922428326e-308`; its adjacent smaller float
`1.666431392242832e-308` and the smallest positive float `5e-324` were rejected.
These are host observations, not a portable decimal cutoff. At enormous counts,
the quantile estimate has coarse integer resolution; very small probabilities
can make the printed survival tail round to one. The runtime float limits are
described by [`sys.float_info`](https://docs.python.org/3.12/library/sys.html#sys.float_info).

## State migration

```bash
"$PYTHON" examples/analysis-lab/lab.py migrate \
  --input examples/analysis-lab/fixtures/save-v1.json --output "$OUT/save-v2.json"
"$PYTHON" examples/analysis-lab/lab.py migrate \
  --input "$OUT/save-v2.json" --output "$OUT/save-v2-repeat.json"
```

The native JSON consumer reopens and validates the written save. Schema 1 keeps
resources and rights inside member records; schema 2 creates explicit accounts
and right owners, while retaining actor identities, history, facts, knowledge,
unlocks and the shared rights clock. The world and save IDs remain
`lantern-quay` and `quay-campaign-07`.

| Relation after this migration | Consumer consequence |
| --- | --- |
| Ava still owns `archive-pass-ava`; expiry is `2026-10-15T20:00:00Z` | Her absence does not give Bo paid archive hosting |
| Bo still owns `winch` and knows `winch-procedure` | His active role can operate the recovery winch |
| Cy knows the public survey map; neither Bo nor Cy knows the archive code | The free route is available without leaking Ava's private fact |
| `archive-message` remains emitted once | Content selection does not grant it again after return |
| The accepted election makes Bo treasurer | Bo may spend crew scrap; an unaccepted election leaves absent Ava's authority in place |
| Crew scrap remains 4 | Individual departure does not delete the shared stock |

Repeated schema-2 migration is explicitly idempotent in this technical example.
Unknown schema versions are rejected. A permitted new election or delegation
must be represented by its own accepted record; migration does not invent it.

Now let the restored state fund a real consumer operation, then reopen it for
the next survey:

```bash
"$PYTHON" examples/analysis-lab/lab.py recover \
  --input "$OUT/save-v2.json" --operation-id recovery-1 --output "$OUT/recovered.json"
"$PYTHON" examples/analysis-lab/lab.py survey \
  --input "$OUT/recovered.json" --operation-id expedition-2 --output "$OUT/resumed.json"
"$PYTHON" examples/analysis-lab/lab.py survey \
  --input "$OUT/resumed.json" --operation-id expedition-2 --output "$OUT/replayed.json"
```

Recovery performs `4 + 2 - 6 = 0` crew scrap, repairs the generator, and records
Cy's survey and Bo's spending. The resumed source produces two pieces. Replaying
the same operation ID returns `already_applied` with identical game state;
it does not award the two pieces twice. If the active winch holder or route
contributor is missing, or the treasurer is absent, recovery is refuted without
writing a changed save.

**Local operation identity:** an operation
ID is nonempty and contains no `:`. This example reserves that separator for
recovery's `:survey` and `:repair` history records. A repeated standalone survey
needs a matching `survey-completed` event by Cy. Repeated recovery needs both
records, with a Cy survey followed at the next tick by `generator-repaired`.
The repair actor is its historical spender; a later treasurer can differ.
An ID belonging to a message, loss, another operation, or an incomplete/conflicting
recovery pair returns 2 without a new output. These are local naming and history
rules, not a universal policy for game state transfer.

The saved event format is unchanged, so the earlier `recovery-1` and
`expedition-2` saves remain readable and repeatable. Once an operation really
completed, later changes to stock, source yield, generator condition or active
participants do not undo that history. Replaying it preserves the *current*
state without paying again or repairing a later loss. A fresh operation still
checks the current source and participant conditions.

The related [systems paper study](../systems-studies/README.md) deliberately has
a different revision: a working generator adds a two-piece bonus to a base
two-piece survey, and repeated v2 migration is rejected. This digital fixture
has a two-piece total resumed source and idempotent migration. They share a
design question, not identical rules or transferable execution evidence.

## Observer-specific views

Projection and choice are separate command invocations. The choice command
receives a serialized permitted view and the content repertoire; it does not
receive the global save.

```bash
"$PYTHON" examples/analysis-lab/consumer.py view \
  --save "$OUT/save-v2.json" --actor bo --output "$OUT/bo-view.json"
"$PYTHON" examples/analysis-lab/consumer.py view \
  --save "$OUT/save-v2.json" --actor cy --output "$OUT/cy-view.json"
"$PYTHON" examples/analysis-lab/consumer.py choose \
  --view "$OUT/bo-view.json" --content examples/analysis-lab/fixtures/content.json \
  --stage salvage --output "$OUT/bo-choice.json"
"$PYTHON" examples/analysis-lab/consumer.py choose \
  --view "$OUT/cy-view.json" --content examples/analysis-lab/fixtures/content.json \
  --stage salvage --output "$OUT/cy-choice.json"
```

Bo's view contains his winch knowledge, permitted rights, own/shared scrap and
public facts. Cy's contains the public map without the winch procedure or archive
code. Bo's deterministic policy chooses `operate-winch`; Cy's chooses
`chart-route`. Changing the global archive code leaves Bo's view and decision
unchanged. Each operation has a different contributor; no model role-playing
or actual human agreement is inferred from that arrangement.

The selected repertoire contains distinct actions and prerequisites. The
already-emitted archive message is excluded. An unavailable archive choice is
a **refuted selection claim**, while an unknown stage contains no inspected
population and is **missing evidence**:

```bash
"$PYTHON" examples/analysis-lab/consumer.py choose \
  --view "$OUT/bo-view.json" --content examples/analysis-lab/fixtures/content.json \
  --stage archive --output "$OUT/zero-selected.json"
# Expected exit 1: one relevant item inspected, zero selected.
"$PYTHON" examples/analysis-lab/consumer.py choose \
  --view "$OUT/bo-view.json" --content examples/analysis-lab/fixtures/content.json \
  --stage absent-stage --output "$OUT/empty-inspected.json"
# Expected exit 2: no relevant items inspected.
```

An accepted delegation can enable Bo to host before expiry while Ava retains
ownership. It does not automatically teach the archive code. At the exact
expiry instant the hosted right is unavailable. Permanent assistance and a
deliberately inaccessible archive can both be legitimate designs; the local
test asks what the declared contract permits.

## Telemetry by build, cohort and missingness

```bash
"$PYTHON" examples/analysis-lab/lab.py telemetry \
  --sessions examples/analysis-lab/fixtures/sessions.csv \
  --events examples/analysis-lab/fixtures/events.csv \
  --dictionary examples/analysis-lab/fixtures/event-dictionary.json \
  --build gate-episode-2 --cohort new \
  --database "$OUT/telemetry.sqlite" --output "$OUT/telemetry.json"
```

The CSV parser imports eight synthetic sessions and eighteen events into real
SQLite tables. Composite foreign keys protect session/build agreement and
sequence constraints detect duplicates. `outcome-query.sql` selects one named
build and cohort and is executed by SQLite; the database is written, reopened
and counted through its native API. The implementation uses documented
[Python SQLite operations](https://docs.python.org/3.12/library/sqlite3.html) and
explicitly enabled [foreign-key enforcement](https://sqlite.org/foreignkeys.html).

For build 2's five new-cohort sessions, the result is:

| Classification | Count | Reason |
| --- | ---: | --- |
| Success | 1 | An accepted action and crossing before resolution, with complete capture |
| Failure | 1 | Accepted action; complete capture through resolution; no timely crossing |
| Unknown | 2 | One incomplete capture; one missing sequence number despite a nominal complete flag |
| Not attempted | 1 | Complete capture but no accepted action |

The reported success fraction is 1/2 among known attempted outcomes. Missing
events are not silently converted into failure. The old build's `episode_complete`
means being alive at episode end; build 2's `gate_crossed` has a spatial deadline.
Those definitions must not be pooled as the same outcome. A deliberately late
crossing event in the semantic controls fails the deadline despite its event name.
These rows demonstrate query semantics, not player frequencies or treatment effects.

## Observation and material evidence route

```bash
"$PYTHON" skills/game-design/scripts/observe_evidence.py \
  --csv examples/analysis-lab/fixtures/observations.csv \
  --manifest examples/analysis-lab/fixtures/observation-manifest.json \
  --output "$OUT/observations.json"
```

The four rows are explicitly fabricated format examples. They exercise an
unaided recorded outcome, an assisted attempt, an unknown outcome after lost
recording, and a declined attempt. The importer preserves the rows, source hashes,
question and missingness. It reports `human_claim: not_established`.

For real evidence, use the [collection and interpretation route](OBSERVATIONS.md).
Importing real records would still require inspection of their provenance,
conditions and relevance before making a human or material claim. This package
has not collected people, device recordings, cultural judgments or physical
tabletop observations. It does not create them by assigning a model a role.

## Tests, source identity and limits

```bash
"$PYTHON" -m unittest discover -s examples/analysis-lab -p 'test_*.py' -v
```

Twenty-three public semantic tests cover an
equal-total but wrong-owner save that still passes the schema, an absent
authority, lost winch, altered private fact, expired delegation, repeated reward,
empty selection, late crossing, missing telemetry, empty observation set and
an unavailable validator dependency with a distinct exit status. The added
numerical regression compares tiny-probability capped waiting with an independent
high-precision finite sum and checks the representable-range rejection.
A nearby valid delegation and an alternate pair of transfer owner names are
accepted. These are public example controls, not independent model trials.
The input/replay regressions additionally exercise malformed roots and nested
records, non-finite JSON, message/loss ID conflicts, partial recovery history,
reserved subevent IDs, true repeats after later world changes, and a missing
route participant. They inspect the CLI status and absence of a forbidden output.
Earlier full and numerical-repair records remain historical evidence; the
current examples incorporate the relevant corrections.

Each command receipt records its source fields. The formal scope is this finite synthetic
campaign and these event definitions. It does not establish market stability,
matchmaking quality, real cooperation, learning, comfort or the quality of a
whole encountered content distribution. The companion
[native Godot episode](../godot-episode/README.md) supplies actual engine input,
collision and save/load observations under a separate episode build identity.
