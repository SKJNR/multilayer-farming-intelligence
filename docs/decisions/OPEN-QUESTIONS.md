# Open Questions and Blockers

## P0 — source reproducibility

- [ ] Obtain `agrisim_core.py`, `mr_tests.py`, `run_sprint1.py`, benchmark scripts, raw JSON/CSV logs and all data-generating code cited in the supplied reports.
- [ ] Reconcile hashes against the actual files.
- [ ] Pin Python and package versions; commit environment instructions.
- [ ] Re-run sampler + simulator + metamorphic tests from a clean checkout.
- [ ] Reconcile the reported runtimes (including 28.8/35.6/19.71 microseconds per step) using one workload and timing method.

## P1 — generator quality

- [ ] Specify joint/derived soil parameterization and physical meanings/units.
- [ ] Validate PAW sampling bounds, not just theta ordering; ensure derived field capacity stays below saturation.
- [ ] Confirm runoff-producing valid scenarios under a well-defined scenario family, including their count among independent trajectories.
- [ ] Adequately sample near the aeration threshold in a held-out test set and report denominators.
- [ ] Preserve representative scenarios separately from intentionally stress-enriched scenarios.
- [ ] Validate weather sequence generation and correlation assumptions.

## P1 — physical model specification

- [ ] State flux equations, root allocation and water-limiting behavior.
- [ ] Verify shared water extraction, per-layer and total-profile mass balance, storage bounds and zero hardpan flux.
- [ ] Check that stress equations and reported state variables use the same explicit time-step convention.
- [ ] Compare against suitable reference implementations or analytic cases.

## P2 — real-world calibration

- [ ] Inspect potential dataset metadata and raw fields before deciding suitability.
- [ ] Determine which model parameters can be identified from available observed variables/depths.
- [ ] Separate parameter calibration from independent evaluation.
- [ ] Plan local measurements (soil texture/hydraulic measurements, profile moisture/tension at depth, rainfall, crop stage, irrigation/abstraction and management records as relevant).
- [ ] Record domain mismatch and limitations; a site-specific calibration does not automatically generalize to other farms/seasons.

## P2 — further architecture

- [ ] Draft knowledge-graph schema for claims, entities, evidence, applicability, contradictions and temporal validity.
- [ ] Draft farmer action/compliance event model after core interaction requirements are clear.
- [ ] Define what tasks truly need ML instead of deterministic rules/simulation.
