# DR-004 — ML Surrogate Benchmark

**Status:** decision to defer production surrogates is accepted provisionally; all numerical benchmark results remain reported, artifacts missing, until independently reproduced.

## 1. Objective

Determine whether a machine-learning surrogate provides enough inference speedup over the explicit soil-water simulator to justify added complexity and constraint risk.

## 2. Proposals considered

- Random Forest flux regression plus deterministic physics/state update.
- Extra Trees flux regression plus deterministic update.
- Direct state regression.
- No surrogate; use the explicit simulator.

## 3. Reported benchmark

The supplied report initially cited 1,000 training scenarios and 200 test scenarios but later provided a reduced-scale pilot with 959 training scenarios/7,672 rows and 293 held-out scenarios/2,344 rows. The report gave these later results:

- uptake/ET MAE around 0.1465 mm (RF) and 0.1585 mm (ET);
- drainage MAE around 0.0825 mm (RF) and 0.0867 mm (ET);
- runoff MAE around 0.0007–0.0009 mm, acknowledged as vacuous because the generated data almost never contained positive runoff;
- raw constraint violation rates around 31.6% (RF) and 40.9% (ET);
- approximate speedup around 5x in the later report;
- direct state regression had much worse reported state drift and bound violations than flux-plus-update.

Earlier messages reported different timings and metrics. See the raw source drops. The source code, raw datasets, complete logs and pinned execution environment needed to reconcile these values are not currently present.

## 4. Adversarial interpretation

- Near-zero average runoff error is not meaningful when positive-runoff cases are absent or extremely rare.
- A small global RMSE can obscure severe errors at threshold/boundary conditions.
- Any post-prediction repair must be reported separately from raw constraint violations.
- Held-out splitting must group complete trajectories/scenarios, not random daily rows.
- Speedup claims need a matching workload, warm-up/timing method, repeated samples, hardware/environment and simulator baseline.
- Low surrogate-to-simulator error does not imply field accuracy.

## 5. Decision

Do not use a surrogate in production at this stage. Preserve the exact reference simulator as the default calculation path. A surrogate is optional and should be reconsidered only if a measured workload proves a meaningful speed or deployment benefit and it meets predeclared error/constraint thresholds.

## 6. Next experiment

Repair scenario coverage for runoff, drought, hardpan and aeration. Design adequate evaluation cases near thresholds. Fix any inconsistent PAW/hydraulic parameter sampling, then rerun the benchmark only after source and test artifacts are reproducible. The exact simulator may already be fast enough, so training a surrogate is not a required milestone.
