# Evidence, Provenance, and Reproducibility

## Evidence classes for agricultural knowledge

- **Officially reported:** identified official source and date.
- **Research-derived:** identified paper/dataset and relevant conditions.
- **Measured:** recorded observation with method, location/time precision appropriate to the project, units and quality flags.
- **Simulation-generated:** output from identified model version and parameter set.
- **Synthetic-test:** artificial case made to test software or scenarios.
- **Estimated:** calculated from explicit assumptions or incomplete inputs.
- **Inferred:** conclusion derived from other evidence; the inference rule must be documented.
- **Unknown:** evidence does not currently establish the claim.

Record contradictory evidence rather than silently flattening it.

## Minimum experiment artifact bundle

Every run should archive:

1. Source code for simulator, scenario generator, and tests.
2. Git commit SHA and checksums for source and input artifacts.
3. Environment: operating system, Python version, pinned dependencies, hardware if timing matters.
4. Exact command to reproduce the run.
5. Random seeds and sampler settings.
6. Parameter registry with units, source/assumption and allowed ranges.
7. Scenario-level inputs/outputs or deterministic instructions to regenerate them.
8. Raw logs and machine-readable summary (`JSON`/`CSV`).
9. Failures, skips, invalid fixtures and acceptance thresholds.
10. Independent rerun notes and reviewer.

## Claim levels

### INDEPENDENTLY VERIFIED

An available source artifact is executed with documented inputs, environment and command; the output is inspected and the result is repeatable. The scope of what was tested is stated narrowly.

### REPRODUCIBLE CLAIM — NOT YET RE-RUN HERE

The source producer supplied enough artifacts and instructions for a repeat, but this repository's reviewers have not rerun it yet.

### REPORTED, ARTIFACTS MISSING

Narrative, tables, hashes or screenshots are present, but sufficient underlying code/logs/data are absent.

### FIELD-VALIDATED

Performance is evaluated against independent real observations using a documented protocol that matches the intended domain. Synthetic data and simulator cross-checks alone never qualify.

## Minimum numerical checks for the water model

- All terms use compatible dimensions and units.
- Layer storage bounds are enforced by model design, and violations fail tests rather than being silently clipped.
- Each layer has an explicit budget, and the total profile balance treats inter-layer flows as internal transfers.
- Flux calculations are independently checked against state transitions where feasible.
- Hardpan zero-flux, saturation/overflow, drought shutdown, stress-boundary and shared-uptake cases are tested with explicit fixtures.
- Metamorphic relations state preconditions; e.g. reducing rainfall does not universally reduce uptake if it also relieves waterlogging.
- Test reports include pass/fail/skip counts and scenario denominators.

## ML surrogate evaluation

Separate scenario families between training and test data; do not split daily rows from the same trajectory across both. Report per-output MAE/RMSE, tail error, errors near regime boundaries, raw and post-constraint violation rates, rollout drift, runtime, training overhead, speedup and baseline performance. Use a surrogate only if it improves the actual workload sufficiently to justify added risk and maintenance.
