# Strategy matrix example

These original synthetic paper games exercise the optional
[zero-sum utility calculation](../../skills/game-systems-design/references/zero-sum-analysis.md).
They provide declared model consequences, not observations of player behavior.

## Run with the optional numerical environment

Use Python 3.11+ in a disposable or project virtual environment. From the
repository root, with `python` resolving to that environment:

```sh
python -m pip install -r skills/game-systems-design/scripts/requirements.txt
python -B skills/game-systems-design/scripts/solve_zero_sum.py \
  --model examples/strategy-matrix/fixtures/channel-signals.json \
  --output /path/to/new/channel-signals-report.json
python -B -m unittest discover -s examples/strategy-matrix -p 'test_*.py' -v
```

Choose an existing output directory and a new report filename. The command
never overwrites a path. Dependencies are optional outside this operation;
this suite intentionally requires actual SciPy `1.17.0` and does not skip the
calculation when it is missing. The tests call the delivered CLI, read its
persisted JSON output, and check its exact input digest.

## Channel Signals: unequal stakes

In [channel-signals.json](fixtures/channel-signals.json), Harbour and Channel
choose a signal simultaneously. A positive entry is a utility-credit transfer
to Harbour; a negative entry reverses that transfer. All signals are available
and free. The paper game's stated preferences are linear in those credits.
The scope is one clash, without later state or learning effects.

| Harbour \ Channel | Anchor | Lantern | Sail |
| --- | ---: | ---: | ---: |
| Anchor | 0 | -1 | 2 |
| Lantern | 1 | 0 | -3 |
| Sail | -2 | 3 | 0 |

The exact oracle is the mixture `(1/2, 1/3, 1/6)` for **each** player and value
zero. Against that mixture every pure opponent response yields zero. Solving
the indifference equations gives `q0 = 3*q2`, `q1 = 2*q2`, and the sum is one;
skew symmetry gives the same row result. Equal probability for all three
signals would instead leave a profitable opponent response.

Positive affine utility changes preserve this mixture. Adding five to every
entry changes the value to five; multiplying all entries by four and then
subtracting seven changes it to minus seven. The column player's utility
continues to be the negative of the row player's. Tests also retain the mixture
under a large common offset and a small positive scale. These are checks of
the stated mathematical relation, not recommended game tuning operations.

## Intended Hierarchy: a valid dominant choice

In [intended-hierarchy.json](fixtures/intended-hierarchy.json), `Complete`
returns `[2, 2]` and `Incomplete` returns `[1, 0]` against the two column
actions. The teacher intentionally offers an inferior demonstration choice.
The solution selects `Complete` and guarantees utility two. This is a valid
calculation; it does not order removal of `Incomplete` or evaluate the later
teaching conversation, which is explicitly outside the model.

## What the tests protect

| Case | Independent expectation |
| --- | --- |
| Unequal cycle | Exact rational mixtures and value zero |
| Positive scaling, utility shifts and named-axis permutations | Preserve the corresponding action probabilities and change values as specified |
| Negative 2-by-3 matrix | Value minus 2.5, with the minimizing third column selected |
| Rectangular game with several optima | Correct value and best responses; no demand for one arbitrary optimal column mixture |
| Intended dominant action | Valid result with guaranteed utility two |
| Singleton and one-sided choice | Valid limited result with the corresponding maximum/minimum entry; no diversity claim |
| Empty/misaligned matrix, booleans, NaN/infinity, malformed JSON | Invalid model and no result file |
| General-sum or undeclared utility | No silent conversion to this model |
| Missing or unqualified numerical dependency | Unavailable evidence and no result file |
| Dense action limit | 256 row actions are accepted; 257 exceed this adapter's declared bound |
| Existing output | Preserve its exact bytes |
| Corrupted successful solver candidates | Independent probability and best-response checks reject them |
| Failed solver status | Preserve the actual failure; no game-design verdict |

Valid calculations use real `scipy.optimize.linprog`. Error-boundary tests run
that same CLI and solver but deliberately corrupt returned candidates or a
status before the adapter consumes them. Those injected cases establish the
adapter's refusal to trust an unverified result, not the real solver's failure
rate. Temporary test files and subprocesses are isolated per test.

For sources, dependency licenses, numerical tolerances, report fields and
failure statuses, read the owning
[zero-sum reference](../../skills/game-systems-design/references/zero-sum-analysis.md).
