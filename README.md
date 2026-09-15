# CartPole-v1 & 2048 — Reinforcement Learning and Game-Tree Search Agents

Two from-scratch AI agents built for a university AI course: a tabular Q-Learning agent that learns to balance a pole through state-space discretization, and an Expectimax/Minimax game-tree agent that plays 2048 using weighted heuristic board evaluation.

## Overview

This repository contains two independent modules that tackle two classic AI control problems with two different families of techniques. The first, the "Dynamic Balance" module, solves Gymnasium's `CartPole-v1` with **Q-Learning** and a **Stochastic Q-Learning** variant (approximate max over a random action subset, per the referenced paper), comparing three different state-discretization granularities (64, 324 and 5,184 states) across a combined grid search of 1,080 hyperparameter configurations. The second, the "Cognitive Strategy" module, solves the 2048 game with depth-limited **Expectimax** and **Minimax + alpha-beta pruning** agents driven by a hand-designed heuristic (empty cells, monotonicity, smoothness, corner concentration, mergeability, positional weighting), benchmarked over multiple weight presets and search depths.

What makes this interesting technically is that both problems require modeling uncertainty explicitly rather than avoiding it: CartPole's continuous state has to be discretized in a way that preserves the signal that actually predicts failure (pole angle/angular velocity), and 2048's random tile spawn has to be represented as a genuine probability distribution (a Expectimax "chance" node) rather than folded into a simple heuristic. Both modules were driven by systematic experimentation — grid search with quantitative evaluation for CartPole, and a parametrized benchmark harness (`bench.py`) with CSV exports for 2048 — rather than manual tuning, so every claim below is backed by a logged result, not a guess.

The full write-up (in Spanish), including all plots referenced below, is in [`Documentación.pdf`](Documentación.pdf).

## Architecture / Approach

**CartPole-v1 — Q-Learning module** (`Cartpole/cartpole_env.ipynb`):
- Exploratory analysis of the 4 continuous observation variables (100 random episodes) to define discretization ranges.
- Three discretization strategies: Ultra Coarse (2×2×4×4 = 64 states), Coarse (3×3×6×6 = 324 states), Fine (6×6×12×12 = 5,184 states).
- Classic Q-Learning: ε-greedy policy over a discretized state, tabular update `Q(s,a) ← Q(s,a) + α[r + γ·maxₐ'Q(s',a') − Q(s,a)]`.
- Stochastic Q-Learning: same update rule but the max is approximated over a random subset `A_k` of size `k` (1 or 2), optionally seeded with the last known-good action (`use_memory`).
- Grid search over α, γ, ε decay strategy/end-value (and k, use_memory for the stochastic variant) — 72 configs per discretization for Q-Learning, 288 for Stochastic Q-Learning (1,080 total), each evaluated over 200 greedy episodes.
- Best model per grid search exported to `Cartpole/models/*.pkl` (backed up in `models_backup/`).

**2048 — Game-tree search module** (`2048/*.py`):
- `GameBoard.py`: 4x4 board mechanics (slide/merge, random tile spawn at 0.9/0.1 for 2/4).
- `Agent.py`: shared interface (`play`, `heuristic_utility`) plus `safe_clone`/`safe_get_available_moves`, which snapshot and restore `np.random`'s state so that an agent's internal search does not consume randomness the real game would otherwise use.
- `heuristics.py`: `evaluate(board, weights)` — linear combination of 6 heuristics (empty cells, monotonicity, max-tile-in-corner, smoothness, possible merges, snake positional weights), configurable via named presets (`baseline`, `tuned`, `corner_heavy`, `smooth_heavy`, `snake`).
- `Expectimax_Agent.py`: alternates MAX nodes (agent's move) and CHANCE nodes (weighted 0.9/0.1 over all empty cells) down to a fixed depth.
- `Minimax_AlphaBeta_Agent.py`: models the tile spawn as an adversarial MIN node instead, with optional alpha-beta pruning (`use_pruning`).
- `bench.py`: CLI benchmark harness — agent, depth, weight preset/custom weights, pruning on/off, seed, episode count — exporting per-episode CSVs to `2048/results/`.
- `summarize_results.py`: aggregates the raw CSVs into `results/summary.csv` / `summary.md` / `summary_agg.md`.

## Key results

### CartPole-v1 (200 greedy evaluation episodes per config, max reward = 500)

**Best Q-Learning configuration per discretization:**

| Discretization | States | α | γ | ε_end | Decay | Eval mean ± std | Success rate | Grid search time |
|---|---:|---:|---:|---:|---|---|---:|---:|
| Ultra coarse | 64 | 0.10 | 0.95 | 0.10 | linear | 493.83 ± 49.25 | 98.0% | 8.3 s |
| Coarse | 324 | 0.10 | 0.95 | 0.05 | exponential | 498.38 ± 13.63 | 96.0% | 48.7 s |
| Fine | 5,184 | 0.10 | 0.99 | 0.05 | linear | 500.00 ± 0.00 | 100.0% | 66.5 s |

**Best Stochastic Q-Learning configuration per discretization:**

| Discretization | States | α | γ | ε_end | Decay | k | Memory | Eval mean ± std | Success rate | Time |
|---|---:|---:|---:|---:|---|---:|---|---|---:|---:|
| Ultra coarse | 64 | 0.10 | 0.99 | 0.05 | linear | 1 | Yes | 500.00 ± 0.00 | 100.0% | 27.4 s |
| Coarse | 324 | 0.20 | 0.99 | 0.01 | exponential | 2 | No | 497.74 ± 16.97 | 96.0% | 92.4 s |
| Fine | 5,184 | 0.10 | 0.99 | 0.01 | exponential | 2 | Yes | 500.00 ± 0.00 | 100.0% | 375.1 s |

The 1,080-configuration grid search (Q-Learning: 72 configs × 3 discretizations; Stochastic Q-Learning: 288 configs × 3 discretizations) ran in roughly 16–402 minutes per grid depending on discretization and algorithm.

### 2048 (agreed configurations, `e10` seeds, from `2048/results/summary_agg.md`)

| Agent | Preset | Depth | Pruning | Episodes | Win % | Max tile (avg) | Time (avg s) |
|---|---|---:|---|---:|---:|---:|---:|
| Expectimax | smooth_heavy | 2 | – | 30 | 16.7 | 998.4 | 37.2 |
| Expectimax | snake | 3 | – | 30 | 16.7 | 968.5 | 112.9 |
| Expectimax | baseline | 2 | – | 30 | 6.7 | 887.5 | 34.3 |
| Minimax | snake | 3 | on | 30 | 3.3 | 759.5 | 17.8 |
| Minimax | snake | 3 | off | 10 | 0.0 | 691.2 | 45.2 |
| Minimax | smooth_heavy | 3 | on | 30 | 0.0 | 546.1 | 21.5 |
| Minimax | smooth_heavy | 3 | off | 10 | 0.0 | 512.0 | 42.2 |
| Random | – | – | – | 10 | 0.0 | 112.0 | 0.2 |

Expectimax outperformed Minimax on every metric that matters for play quality (best win rate 16.7% vs. 3.3%, best avg. max tile 998.4 vs. 759.5), consistent with it correctly modeling the game's real, non-adversarial randomness. Alpha-beta pruning did not change Minimax's decisions but cut its runtime substantially (17.8s vs. 45.2s for `snake`; 21.5s vs. 42.2s for `smooth_heavy`).

## Design decisions

**1. Non-uniform, criticality-based state discretization for CartPole, instead of equal bins per variable.**
The 4 observation variables were split into "critical" (pole angle, pole angular velocity — the two variables whose thresholds directly cause episode termination) and "non-critical" (cart position, cart velocity), and each discretization strategy allocates more bins to the critical pair (e.g., 6×6 vs. 3×3 in the coarse setup). The alternative — giving all 4 variables the same number of bins — was discarded because it would either waste states resolving cart position/velocity ranges that rarely affect failure, or under-resolve pole angle/angular velocity where fine distinctions actually separate "recoverable" from "about-to-fall" states. This paid off empirically: even the 64-state Ultra Coarse discretization reached a 98–100% success rate, meaning the critical variables were the actual leverage point, not the total state count.

**2. Implementing Minimax (an intentionally wrong model) alongside Expectimax for 2048, instead of only building the theoretically correct agent.**
2048's tile spawn is genuine randomness (0.9/0.1 over 2/4, uniform over empty cells), not an adversary — so Expectimax, which takes an expectation over that distribution, is the model that matches reality. The team built Minimax with alpha-beta pruning anyway, deliberately treating the spawn as a worst-case adversarial choice. This wasn't a naïve alternative: it gave a controlled way to measure the cost of a wrong assumption (Minimax's best win rate was 3.3% vs. Expectimax's 16.7%) and to isolate the effect of alpha-beta pruning in a setting where its correctness guarantee (same decision, less work) could be verified directly — pruning cut Minimax's runtime by ~55–60% without changing which move it picked. Pure Expectimax would not have produced either of those comparisons.

## Tech stack

- **Language:** Python 3.10
- **RL / environment:** [Gymnasium](https://gymnasium.farama.org/) (`CartPole-v1`), pygame (rendering)
- **Numerics / data:** NumPy, pandas
- **Visualization:** Matplotlib, Seaborn
- **Performance:** Numba (`@jit`, used in the 2048 board/heuristic hot paths)
- **Tooling:** Jupyter (`ipykernel`), Poetry (per-module dependency management)

## How to run

Each module was developed as an independent [Poetry](https://python-poetry.org/) project (`Cartpole/pyproject.toml`, `2048/pyproject.toml`). A consolidated [`requirements.txt`](requirements.txt) is also provided at the repo root for a single-environment `pip` setup covering everything actually imported by the code.

```bash
# from the repo root, Python 3.10
python -m venv .venv
source .venv/bin/activate          # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

**Run the CartPole notebook:**
```bash
jupyter notebook Cartpole/cartpole_env.ipynb
# run all cells top to bottom — the full grid search (1,080 configs) takes on the order of hours;
# trained models are already exported to Cartpole/models/*.pkl if you just want to inspect results
```

**Run 2048:**
```bash
cd 2048
python Main.py                                             # single game, Expectimax depth 3, "smooth_heavy" preset

python bench.py --agent expectimax --preset snake --depth 3 --episodes 30 --seed 0 --output results/my_run.csv
python bench.py --agent minimax --preset snake --depth 3 --no-pruning --episodes 10

python summarize_results.py                                # rebuild results/summary.csv, summary.md, summary_agg.md
```

## Team & authorship

This was a two-person team project for the "Inteligencia Artificial" course at Universidad ORT Uruguay (group M7A, 2025), by Juan Diego Fagnoni and Francisco Baraibar. The two modules were split between us: **I (Juan Diego Fagnoni) was primarily responsible for the CartPole-v1 / Q-Learning module** (`Cartpole/`) — the discretization strategies, both Q-Learning variants, the hyperparameter grid search and its analysis. My teammate Francisco Baraibar was primarily responsible for the 2048 / game-tree search module (`2048/`) — the board mechanics, the Expectimax/Minimax agents, the heuristic weight presets and the benchmark harness. The final documentation (`Documentación.pdf`) and repository integration were done jointly.
