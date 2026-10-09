# Adjacent class: computational game and multi-agent environments

**Decision: retain OpenSpiel and PettingZoo as conditional, project-owned
integrations.** They add an executable game representation and algorithm-facing
interfaces beyond a collection of design instructions. The present paper, Ink,
glTF and finite-matrix operations do not demonstrate a need for another framework
dependency or a new general method.

This supplement inspected exact primary source on **2026-10-08**. Neither
framework was installed or executed. No upstream implementation, tests, examples
or assets are transferred to Game Design. The [source record](simulation-source-identities.json)
gives the inspected commits, Git blob identities, reading scope and execution
limits. These are Git snapshots, not asserted published-package identities.

## OpenSpiel: an executable state and information model

Inspected `google-deepmind/open_spiel@48401890ee9857e611678302371378175a8e4c6b`.
The selected [core header](https://github.com/google-deepmind/open_spiel/blob/48401890ee9857e611678302371378175a8e4c6b/open_spiel/spiel.h)
defines sequential/simultaneous dynamics, chance modes and utility categories;
`State` exposes legal actions, transitions, per-step rewards, cumulative returns,
cloning, child states and serialization. Its player information state represents
remembered information; the observation may contain less, provided the player's
action/observation history can reconstruct that information state. Those are
consequential modeling contracts. Their presence in a header does not establish
that every game implements each optional representation correctly.

There is an actual algorithm consumer. The complete
[Python CFR implementation](https://github.com/google-deepmind/open_spiel/blob/48401890ee9857e611678302371378175a8e4c6b/open_spiel/python/algorithms/cfr.py)
keys policy/regret records by player information state, traverses chance outcomes
and child states, and evaluates terminal returns. It asserts sequential dynamics;
its Nash-policy interpretation is described for two-player zero-sum games.
Supporting more utility categories in `GameType` does not make that guarantee
universal. The inspected [CFR test section](https://github.com/google-deepmind/open_spiel/blob/48401890ee9857e611678302371378175a8e4c6b/open_spiel/python/algorithms/cfr_test.py#L75-L130)
includes initial-policy checks and Kuhn poker value/best-response checks. Their
presence supplies intended checks, not an observed convergence result here.

The selected [basic test helpers](https://github.com/google-deepmind/open_spiel/blob/48401890ee9857e611678302371378175a8e4c6b/open_spiel/tests/basic_tests.cc)
compare clone/history results, optionally compare serialized/restored string
representations, check observable tensor size/finiteness and inspect legal
actions and reward/return relationships during random simulations. These
checks have bounded meanings: finite observation tensors do not establish
faithful information hiding, and serialization comparisons do not establish a
production save migration. The core header also explicitly limits its default
action-history serialization for sampled-stochastic games.

The complete [LP solver](https://github.com/google-deepmind/open_spiel/blob/48401890ee9857e611678302371378175a8e4c6b/open_spiel/python/algorithms/lp_solver.py)
is a real alternative for matrix work: `solve_zero_sum_matrix_game` asserts a
one-shot, zero-sum `pyspiel.MatrixGame`, constructs both players' LPs, and returns
mixtures and values. Its implementation uses CVXPY, NumPy and pyspiel, with ECOS
as the default solver; retained CVXOPT comments are not its current call path.
Its [tests](https://github.com/google-deepmind/open_spiel/blob/48401890ee9857e611678302371378175a8e4c6b/open_spiel/python/algorithms/lp_solver_test.py)
cover biased rock-paper-scissors, rectangular utilities, Blotto and dominance
distinctions.

**Disposition:** direct SciPy remains sufficient for the existing declared finite
matrix operation. Its [local adapter](../../../skills/game-systems-design/references/zero-sum-analysis.md)
already supplies model semantics, source identity and independently recomputed
probability/best-response bounds. Moving that task into `MatrixGame` and another
solver stack has no demonstrated benefit. Reconsider OpenSpiel when a concrete
game already has, or actually needs, a faithful multi-step/information-state
model and a selected algorithm consumer. No performance or reliability ranking
between these solver stacks was established.

## PettingZoo: agent turns, observations and episode lifecycle

Inspected `Farama-Foundation/PettingZoo@c88bed4324a9021fa6fdd938bc66b6d1d020ac3b`.
The complete [base environment file](https://github.com/Farama-Foundation/PettingZoo/blob/c88bed4324a9021fa6fdd938bc66b6d1d020ac3b/pettingzoo/utils/env.py)
distinguishes AEC's one-agent-at-a-time stepping from ParallelEnv's action
dictionary for live agents. AEC `last()` returns the current agent's observation,
accumulated reward, termination, truncation and info. Its final `step(None)`
retires a completed agent after the consumer can read the final transition.
Parallel `step()` returns five dictionaries. Optional global `state()` and an
agent's `observe()` are separate interfaces; a global training input is not
automatically a permitted player observation.

The ordinary [AEC-to-parallel wrapper](https://github.com/Farama-Foundation/PettingZoo/blob/c88bed4324a9021fa6fdd938bc66b6d1d020ac3b/pettingzoo/utils/conversions.py#L110-L241)
requires `is_parallelizable`, documents end-of-cycle updates, and checks some
cycle-order and mid-cycle completion violations. Its step accumulates rewards
across the component AEC steps. This is a semantic precondition, not just a
change in dictionary shape. For example, if a later actor originally observes
an earlier actor's choice before deciding, replacing that sequence with jointly
submitted choices can change the game. That is a local inference from the
interface contract, not an executed conversion experiment. The metadata flag
does not itself verify equivalence.

The complete [parallel API test](https://github.com/Farama-Foundation/PettingZoo/blob/c88bed4324a9021fa6fdd938bc66b6d1d020ac3b/pettingzoo/test/parallel_test.py)
checks reset arguments, dictionary returns, active-agent lifecycle and stable
space-object identity; it samples masked actions when an observation includes
`action_mask`. Some step dictionary-key differences issue warnings, while
other lifecycle conditions assert; later indexing/checks may still fail.
It does not directly validate observation tensor shapes or prove that a reward
measures the intended game quality. Its finished-identity tracking, populated
when `possible_agents` exists, constrains an environment episode. It does not
forbid a real participant from leaving and returning: the project must represent
that participation without silently redefining it as permanent termination.

**Disposition:** a useful project integration when an actual multi-agent
simulation or RL task calls for this interface. The inspected
[package metadata](https://github.com/Farama-Foundation/PettingZoo/blob/c88bed4324a9021fa6fdd938bc66b6d1d020ac3b/pyproject.toml)
declares Gymnasium, NumPy and typing-extensions, with additional dependencies for
selected environment families. Translation of game state, reward, timing,
observations and episode identity remains project work. No automatic training
loop, reward metric or agent-lifecycle rule is adopted here.

## Ownership and reconsideration

| Existing owner | What a selected environment can supply | What remains with the owner |
| --- | --- | --- |
| [Systems design](../../../skills/game-systems-design/SKILL.md) | Executable transitions, resource/reward calculations and strategy experiments | Meaning of utility, resources, rights, loss and continuation |
| [Actor knowledge](../../../skills/gameplay-design/references/entities.md) and the [observer-view consumer](../../../examples/analysis-lab/consumer.py) | Per-agent observations and policy inputs | Permitted acquisition, memory and disclosure; actual context isolation where needed |
| [Environment contract](../../../skills/game-design/references/environment-contracts.md) | A concrete native consumer and its API tests | Artifact identity, faithful mapping and the distinction between source reading, execution and the checked property |
| [Assay binding](../../../skills/game-design/references/consumer-and-assay-contract.md) | Framework-specific operations used by a selected project | General research, implementation, testing and interpretation methods |

A future selection should resolve a concrete missing operation, then compare
the native model and original game on relevant action/observation traces,
algorithm assumptions and returned artifacts. A deliberate absence, return,
hidden fact or chance event is a useful neighboring case where it affects that
game. These are conditions for deciding a future integration, not new mandatory
gates for every design task. No such integration is qualified by this supplement.

The inspected OpenSpiel [root license](https://github.com/google-deepmind/open_spiel/blob/48401890ee9857e611678302371378175a8e4c6b/LICENSE)
is Apache-2.0; the LP/CFR files carry DeepMind's 2019 notice and the selected
core/header test files carry its 2021 notice. PettingZoo's
[root license](https://github.com/Farama-Foundation/PettingZoo/blob/c88bed4324a9021fa6fdd938bc66b6d1d020ac3b/LICENSE)
is MIT with Farama Foundation's copyright. Study of these interfaces transfers
no source bytes into the product. If a later project redistributes selected
source or packages, inspect that exact distribution and preserve its applicable
license, modification and attribution notices. This bounded reading does not
establish rights to every bundled game asset or third-party dependency.
