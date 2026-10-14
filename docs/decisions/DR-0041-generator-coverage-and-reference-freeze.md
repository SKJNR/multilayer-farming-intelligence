# DR-004.1 — Reference Freeze and Generator Coverage

**Status:** reference-freeze intent recorded; latest repair metrics remain AI-reported and are not independently verified in this repository.

## Decision intent

Use the explicit soil-water simulator as the reference implementation, defer a surrogate unless a real workload justifies it, and improve scenario generation before further model benchmarking. Distinguish a reproducible software reference from an agronomically validated recommendation engine.

## Latest submitted claims (2026-10-14)

The latest Qwen response claims:

- a timing audit of 10,000 steps repeated 10 times, with mean 0.1971 s (19.71 microseconds/step);
- 1,000/1,000 PAW-derived soil records respecting θ_wp < θ_fc < θ_sat;
- Normal, Storm and Aeration_Test scenario families producing distinct runoff/aeration outcomes;
- the simulator frozen as `v1.0.0-ref`;
- the ML surrogate deferred indefinitely for the current workload; and
- a real-world calibration gate as the next milestone.

The complete submitted response is preserved in `source-drops/qwen-sprint2-closure-generator-repair-and-calibration-gate.md`.

## Evidence status and conditions

The metrics and outcomes above are **reported, not independently verified here**. The actual simulator source, sampler, scenario configurations, timing script, raw logs, and data used for the execution were not attached with the report. The timing also differs from earlier reported figures; a reproducible run must reconcile this.

To call the engine a frozen release, commit the actual source and dependencies, establish the version-to-commit mapping, and run the complete test suite against that revision. To call it agriculturally valid, calibrate only against suitable measured data and evaluate on independent observations. Passing water-accounting tests does not prove that the physical model or crop-specific parameters are correct.

## Next gate

1. Acquire and commit the actual simulator, parameter registry, sampler, scenario definitions, tests and raw logs.
2. Independently rerun all claims, including timing and runoff/aeration coverage.
3. Inspect the Berambadi dataset metadata and variables to establish which model quantities it can validate; seek local multi-depth measurements if necessary.
4. Define calibration, holdout, error metrics and acceptance thresholds before fitting parameters.

Knowledge-graph ontology design may proceed in parallel as low-risk architecture work, provided synthetic or uncalibrated simulation outputs are clearly labelled and not promoted to verified agricultural facts.
