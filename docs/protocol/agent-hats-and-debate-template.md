# Agent Hats and Adversarial Debate Template

Use this template for architecture, simulation, synthetic-data, ML, calibration, and farmer-decision reviews. Use only the hats relevant to the decision; do not add roles for decoration.

## Operating rule

The goal is not artificial agreement or simulated “consciousness.” The goal is a decision that survives independent-looking challenge, executable checks, domain constraints, and explicit uncertainty. If multiple AI systems are actually consulted, identify them and preserve their outputs separately. Otherwise call these **review hats/perspectives**, not independent agents.

Do not request or publish hidden private chain-of-thought. Ask each reviewer for concise conclusions, assumptions, evidence, counterexamples, calculations, and reproducible tests. A debate transcript is not a substitute for evidence.

## Role roster

1. **Domain scientist / practitioner:** agronomy, soil physics, crop physiology, farm operations, and applicability limits.
2. **Systems architect:** interfaces, state variables, modularity, computational complexity, operational constraints and versioning.
3. **Numerical methods reviewer:** equations, units, discretization, stability, conservation, boundary conditions and error propagation.
4. **Statistician / experimental designer:** sampling distributions, confounding, identifiability, uncertainty, validation splits, power and calibration metrics.
5. **Data provenance / knowledge-graph steward:** evidence source, claim scope, citations, licensing, time/location/crop context, and data lineage.
6. **ML evaluator (only if ML is proposed):** baselines, leakage, OOD performance, calibration, constraint violations and whether ML adds measurable value.
7. **Farmer / deployment / economics reviewer:** affordability, labor, feasibility, adoption friction, risk tolerance, equity and reversibility.
8. **Adversarial reviewer (Murphy):** strongest counterexample, boundary case, failure injection, alternative explanation and evidence that would falsify the proposal.
9. **Test engineer / reproducibility reviewer:** executable commands, fixtures, deterministic seeds, environment, independent assertions and artifact completeness.
10. **Decision moderator:** separates facts from assumptions, preserves unresolved disagreement, chooses the smallest decisive next experiment, and records acceptance criteria.

## Review sequence

1. **Step back:** state the actual decision, intended user, operating domain, costs of false positives/negatives, and invariants.
2. **Branch:** compare at least two genuinely different options; use a decision tree when choices depend on conditions.
3. **Independent first pass:** each selected hat writes its verdict, key assumptions, evidence and strongest concern before reading the others' conclusions where feasible.
4. **Adversarial turn:** Murphy constructs a counterexample and tries to falsify the leading option. Use chess-move analysis for second-order consequences when relevant.
5. **Evidence / tool turn (ReAct):** identify what must be looked up, measured, calculated, or executed; run it when tools and artifacts are available. Label anything not run.
6. **Quantitative turn (Program of Thoughts):** show equations, units, intermediate numeric results, code/tests and outputs sufficient for reproduction—not hidden reasoning traces.
7. **Cross-check:** compare candidate answers, test self-consistency, and explain disagreements. Consensus increases confidence only when the evidence independently supports it.
8. **Decision record:** problem; options; specialist review; adversarial findings; verification; decision; uncertainty; next experiment.
9. **Commit:** update `CURRENT_STATE.md`, decision record, source archive, tests/artifacts, and changelog; commit only what actually changed.

## Adversarial pairing rule

For every **high-risk or decision-critical subtask**, the task owner must name a counter-reviewer before accepting its result. A shared red-team role (for example, Murphy) may challenge several workstreams, but each one needs its own concrete counterexample, disconfirming test, or evidence gap. At minimum assign a counter-reviewer for: model equations/flux order; soil and crop parameter priors; measurement/data QA; calibration/identifiability; validation metrics/split design; and any farmer-facing action. Low-risk clerical tasks may use a checklist instead of a separate adversarial pass. Record the paired reviewers and their conclusions in the decision record.

Do not assume a role is an independent agent. Independent review requires genuinely separate reviewer work (such as different people or separately invoked model/tool sessions); identify the actual source. Consensus is recorded only after the evidence review and never replaces passing tests or field evaluation.

## Required output from every review

- **Decision:** accept / reject / conditional / defer.
- **Confidence and why:** evidence-backed, not a numerical confidence score without calibration.
- **Known facts vs reported claims vs assumptions vs inferences.**
- **Top three failure modes** and one explicit counterexample.
- **Executable verification:** command, fixture, expected result, actual result, environment, seed and artifact path—or say `NOT RUN` and why.
- **Unresolved disagreements:** no forced consensus.
- **Smallest next experiment** with measurable pass/fail criteria.
- **Repository changes proposed** and exact paths.

## Domain-specific adversarial prompts

- **Soil-water model:** Can any flux make storage negative? Is every flux in the balance? Are units and time indices consistent? Are root fractions normalized? Does a shared-water limiter preserve fair/defined allocation? Do aeration and drought responses behave correctly in controlled paired cases? Are hydraulic parameters jointly plausible?
- **Synthetic generator:** Which physical combinations are excluded? Are rare extremes deliberately covered? Is the joint distribution defensible? Can seeds reproduce the dataset? Are invalid fixtures separated from valid scenarios?
- **ML surrogate:** Does it beat the explicit baseline on the real workload? Does it violate constraints? Is test data grouped by scenario/time/location to avoid leakage? Are tail errors and OOD behavior measured?
- **Calibration:** Which parameters are identifiable from the actual observations? Are measurement error and missingness modeled? Is evaluation independent of calibration? Is performance compared with a simple baseline?
- **Knowledge graph:** Can every consequential claim be traced to a source, context, date, and uncertainty? Are contradictory findings preserved? Are synthetic labels impossible to confuse with observations?
- **Farmer decision engine:** Is the recommendation feasible, affordable, reversible, robust to uncertainty, and explicit about risk? What happens when a farmer does not or cannot follow the recommendation?
