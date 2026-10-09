# Optional zero-sum analysis

Use this operation when a finite **two-player zero-sum expected-utility model**
already represents the decision being examined. It calculates candidate mixed
strategies, a utility interval and the gain available from a best response.
It can answer whether a price or payoff change alters that model's incentives.
It does not decide which player experiences, costs or consequences belong in
the model.

A paper calculation remains sufficient when it answers the question. This
optional numerical dependency is unnecessary for an ordinary resource transfer,
an expressive scene or a question about observed player understanding.

## State the model that the numbers mean

Give each player a name and an ordered, nonempty list of available actions.
Rows belong to the maximizing player; columns belong to the minimizing player.
An entry is the row player's cardinal utility for that action pair. The column
player's utility is exactly its negative. The declared objective is expected
utility under independent mixed choices, not an observed action frequency.

Record the applicable situation, action availability and time horizon. Explain
the utility unit, what higher utility means, and how costs enter the entries.
“No additional cost within this model” is a valid statement. If choosing an
action consumes scarce equipment, closes a later route or changes exposure to
risk, account for that consequence before claiming that a raw damage or score
table expresses preference. The command accepts declared utility values; it
does not perform a score-to-utility conversion or verify the declaration against
the implemented game.

The JSON contract is specific to this optional command:

| Field | Required content |
| --- | --- |
| `schema_version` | Integer `1`, not a boolean |
| `model_id` | Nonempty name identifying this stated model or revision |
| `model_type` | Exactly `two-player-zero-sum` |
| `context` | Object containing nonempty `situation`, `availability`, `horizon` strings |
| `row_player`, `column_player` | Each has a distinct player `name` and an `actions` list; action names are unique within their own axis |
| `utility` | Nonempty `meaning`, `unit`, `costs`; `row_objective` is `maximize-expected-utility`; `column_utility` is `negative-of-row` |
| `payoffs` | Nonempty rectangular numeric matrix aligned to the two action lists |

All listed fields are required. Unsupported fields and duplicate JSON keys are
rejected, including a second payoff matrix. Numeric strings, booleans, NaN,
infinity and values outside finite binary64 range are invalid. Ordinary JSON
numbers are evaluated in binary64 arithmetic. The two axes can have different
lengths; neither antisymmetry nor entries restricted to `-1`, `0`, `1` are
required.

One available action is a valid limited case. An empty action set is invalid.
A model may intentionally contain a dominant action or an inferior authored
choice; neither is a failure of the calculation. A cooperative or general-sum
game is also a legitimate design, but requires a model and method outside this
command's contract. Do not erase its second player's preferences to make it fit.

## Run the optional operation

The runtime entry is [`../scripts/solve_zero_sum.py`](../scripts/solve_zero_sum.py).
It uses Python 3.11+ and the optional
[`../scripts/requirements.txt`](../scripts/requirements.txt), which pins
`scipy==1.17.0`. Install that dependency in a disposable or project virtual
environment only when this operation is needed. SciPy supplies optimization;
NumPy supplies its array operations. SciPy 1.17.0 declares NumPy
`>=1.26.4,<2.7`; actual versions are recorded in every solved report. [S1] [S2]

From a checkout, with `python` resolving to that environment:

```sh
python -m pip install -r skills/game-systems-design/scripts/requirements.txt
python -B skills/game-systems-design/scripts/solve_zero_sum.py \
  --model examples/strategy-matrix/fixtures/channel-signals.json \
  --output /path/to/new/channel-signals-report.json
```

For an installed skill, use its `scripts/solve_zero_sum.py` and supply your own
model file. The runtime does not depend on checkout examples or maintenance
tests. The output's parent directory must exist; use a new output path for each
inspection. Existing files, directories and symlinks are never overwritten.

This small dense adapter accepts at most 256 actions per player and a model
file up to 4 MiB. Each of the two linear programs receives a default 10-second
HiGHS time limit; `--time-limit SECONDS` changes that limit per program. This is
a solver time limit, not a wall-clock promise for imports and file operations.
Other SciPy versions produce `dependency_mismatch` until that boundary is
qualified and the pin is deliberately revised.

## Read the numerical claim

Let `A` be the row-utility matrix, `p` the row mixture and `q` the column
mixture. The two linear programs are:

$$
\max_{p,v} v\quad\text{subject to}\quad
A^\mathsf{T}p\ge v\mathbf{1},\quad p\ge0,\quad\sum_i p_i=1;
$$

$$
\min_{q,w} w\quad\text{subject to}\quad
Aq\le w\mathbf{1},\quad q\ge0,\quad\sum_j q_j=1.
$$

SciPy's `linprog` minimizes a linear objective. The row program therefore
minimizes `-v`; the column program minimizes `w`. Both value variables have
unbounded sign, so negative-utility games remain valid. The API's default
nonnegative bound must not be applied to these value variables. [S1] The
zero-sum model and minimax interpretation also appear in Nashpy's documented
derivation. [N1]

After optimization, the adapter recomputes the following from the payoff matrix
and the **reported** mixtures, independently of the LP constraint arrays and
the solver's success flag:

$$
L=\min_j\sum_i p_i A_{ij},\qquad
U=\max_i\sum_j A_{ij}q_j,\qquad E=p^\mathsf{T}Aq.
$$

`L` is the row mixture's guaranteed utility against any column response; `U`
is the most row utility available against the column mixture. `U-E` is the
row player's possible gain from a best response; `E-L` is the column player's
corresponding gain in its own utility. A sufficiently small `U-L` certifies an
approximate solution of this stated model. These are numerical bounds, not
claims that participants choose these probabilities or find the game enjoyable.

To preserve useful differences in shifted utilities, the adapter solves
`B = (A - offset) / scale`. `offset` is the midpoint of the extreme payoffs;
`scale` is their greatest distance from that midpoint, or `1` for a constant
matrix. The positive affine transformation preserves preferences. Both the
normalization and the restored utility-unit quantities appear in the report.

The adapter checks raw probability sum error, negative mass and violation of
the upper bound against `1e-8`. Only drift inside that allowance is clipped to
nonnegative values and normalized. The raw and reported residuals and greatest
adjustment are retained. Best responses are then calculated for the reported
mixtures. The normalized gap and the disagreement between LP values and those
independent bounds must each be at most `1e-7`; nonfinite quantities fail.
HiGHS primal, dual and IPM tolerances are set to `1e-9`. These are this adapter's
explicit numerical choices, not thresholds for acceptable game design. [S1]
Tiny negative gaps or regrets inside the allowance remain visible as signed
floating-point residuals; they are not exact negative gains.

The report retains the exact inspected input's SHA-256, byte length, parsed
model, adapter SHA-256, Python/SciPy/NumPy versions, solver method, options,
statuses and residuals. The arrays `row_against_columns` and
`rows_against_column` follow the named input axes. A degenerate game can have
several optimal mixtures: another certified mixture is not evidence of a
regression by itself. The reported tolerance is in normalized utility; its
scaled equivalent is a comparison threshold, not an error bound on decimal
output. Restored utility values also round to binary64. Inspect the normalized
quantities when a large common offset hides a smaller difference in the printed
bounds, and decide whether that precision answers the game question.

## Use a worked result without enlarging its scope

The original synthetic **Channel Signals** example can be saved as a complete
input for the installed script, without a checkout fixture:

```json
{
  "schema_version": 1,
  "model_id": "channel-signals-1",
  "model_type": "two-player-zero-sum",
  "context": {
    "situation": "Harbour and Channel choose a signal simultaneously without seeing the other's choice.",
    "availability": "Both players can choose every named signal; none has a prerequisite.",
    "horizon": "One clash, settled immediately. Later state, learning and repeated-game incentives are excluded."
  },
  "row_player": {"name": "Harbour", "actions": ["Anchor", "Lantern", "Sail"]},
  "column_player": {"name": "Channel", "actions": ["Anchor", "Lantern", "Sail"]},
  "utility": {
    "meaning": "Positive entries transfer credits from Channel to Harbour; negative entries reverse that transfer. Declared preferences are linear in utility credits.",
    "unit": "net utility credits to Harbour per clash",
    "costs": "Signals are free to choose. No additional cost or later consequence is included in this one-clash model.",
    "row_objective": "maximize-expected-utility",
    "column_utility": "negative-of-row"
  },
  "payoffs": [[0, -1, 2], [1, 0, -3], [-2, 3, 0]]
}
```

Both players' mixture is `(1/2, 1/3, 1/6)` and the value is zero. The equations
for an indifferent opponent give `p0 = 3*p2` and `p1 = 2*p2`; normalization
then gives the fractions. Equal use of all three actions is not the answer to
this unequal-stakes model. Adding five to every row payoff preserves both
mixtures and moves the value to five. It simultaneously subtracts five from
the column player's utility, as the model requires.

The adjacent **Intended Hierarchy** example gives `Complete` payoffs `[2, 2]`
and `Incomplete` payoffs `[1, 0]`. The guaranteed row utility is two and the
row solution chooses `Complete`. Keeping that intentional teaching hierarchy
is a valid design choice. The calculation cannot value the later teaching
conversation, which the example expressly excludes.

The checkout examples include both complete inputs and mathematical-oracle
tests. Their interpretation belongs to the stated model. They are original
synthetic artifacts, not measured playtest evidence.

## Distinguish an unavailable result

| Status | Exit | Meaning |
| --- | ---: | --- |
| `solved` | 0 | Both LPs succeeded and the independent numerical checks passed; JSON is written to the new file and stdout |
| `invalid_model` | 2 | Missing, malformed, nonfinite, ambiguous or out-of-contract model; no report file is created |
| `input_unavailable` | 2 | Required input bytes could not be read |
| `dependency_unavailable`, `dependency_mismatch` | 2 | The optional numerical runtime is unavailable or outside the qualified version |
| `solver_failure` | 2 | An LP did not return an optimum; its actual status and message are retained |
| `numerical_failure` | 2 | Candidates or restored quantities fail finite/simplex/best-response checks |
| `output_unavailable` | 2 | The chosen report path cannot be created exclusively or written |

Failures emit diagnostic JSON on stderr; malformed command-line arguments use
the ordinary argparse usage error. Model/dependency/solver failures do not
create a result file. A file-write failure must not be treated as a stored
result. An unavailable calculation neither supports nor refutes a claim about
the game's quality. A singleton result explicitly records its lack of strategic
choice; it does not certify diversity from an empty comparison.

## Source and reuse boundary

The comparison that prompted this optional capability inspected
[`apetrovCode/game-design-skills` matrix analysis at
`b8bc2c4d99ccd6e8b2fb3a5fed63fec66dfce35c`](https://github.com/apetrovCode/game-design-skills/blob/b8bc2c4d99ccd6e8b2fb3a5fed63fec66dfce35c/game-analysis/scripts/matrix_analysis.py),
under its root [MIT license](https://github.com/apetrovCode/game-design-skills/blob/b8bc2c4d99ccd6e8b2fb3a5fed63fec66dfce35c/LICENSE).
That script's ordinal interaction analysis and eigenvector heuristic are not
this operation's minimax solver. **No code, skill text, fixtures or tests from
that package are copied here.** This repository owns the original model
adapter, certificate and examples; it calls the maintained SciPy API for the
optimization mechanism. General research, implementation and testing methods
remain with the consumer's Assay binding.

- **[S1] SciPy 1.17.0 API:**
  [`linprog(method='highs')`](https://docs.scipy.org/doc/scipy-1.17.0/reference/optimize.linprog-highs.html).
  The inspected release tag resolves to SciPy commit
  `8c75ae75176236f233824e9a0483c26a69e6dfec`.
- **[S2] SciPy dependency and license:**
  [package metadata](https://github.com/scipy/scipy/blob/8c75ae75176236f233824e9a0483c26a69e6dfec/pyproject.toml),
  [BSD-3-Clause license](https://github.com/scipy/scipy/blob/8c75ae75176236f233824e9a0483c26a69e6dfec/LICENSE.txt),
  [bundled-license index](https://github.com/scipy/scipy/blob/8c75ae75176236f233824e9a0483c26a69e6dfec/LICENSES_bundled.txt).
  Its HiGHS submodule is `scipy/HiGHS` commit
  `222cce79a2bca866dbfbcd91b55da11336ae88f4`, with an
  [MIT license](https://github.com/scipy/HiGHS/blob/222cce79a2bca866dbfbcd91b55da11336ae88f4/LICENSE.txt).
  These are external runtime dependencies; their source is not vendored here.
- **NumPy runtime inspected:** `2.3.5`, release commit
  `c3d60fc8393f3ca3306b8ce8b6453d43737e3d90`, under its
  [BSD-3-Clause license](https://github.com/numpy/numpy/blob/c3d60fc8393f3ca3306b8ce8b6453d43737e3d90/LICENSE.txt).
  SciPy's compatibility range is the dependency requirement; the exact installed
  NumPy version remains part of each report's identity.
- **[N1] Alternative examined:** Nashpy's
  [zero-sum derivation](https://nashpy.readthedocs.io/en/stable/text-book/zero-sum-games.html)
  and [minimax API](https://nashpy.readthedocs.io/en/stable/how-to/use-minimax.html).
  Direct SciPy exposes the needed statuses without another wrapper dependency.
  A broader bimatrix requirement would warrant a fresh solver choice rather
  than extending this zero-sum contract by implication.
