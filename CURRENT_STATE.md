# Current State

**Last summarized:** 2026-10-14  
**Status:** architecture and review protocol established; reference simulator and generator claims still need artifact-level verification.

## What we are building

A multilayer farming intelligence system combining:

1. A provenance-aware agricultural knowledge base / graph.
2. Explicit rules and feasibility constraints.
3. Reusable process-based simulation primitives (starting with soil-water balance and crop-specific root uptake).
4. Synthetic scenario generation for test coverage, sensitivity analysis, and simulator-emulation experiments.
5. ML models only for tasks with a demonstrated need and adequate evaluation.
6. A decision engine that compares trade-offs and uncertainty.
7. A field-feedback pipeline to evaluate predictions and interventions against measured outcomes.

## Current decisions

- **Soil-water primitive:** a two-layer water-balance model is a candidate MVP. Shared soil water, crop-specific root distributions, separate drought and aeration stress, explicit inter-layer drainage, hardpan boundary cases, and complete water accounting are required concepts.
- **Numerical code status:** source files and logs mentioned in AI-submitted reports are not included in this package. Their checksums, reported metrics, and pass counts are therefore recorded as claims, not as independently verified facts.
- **Synthetic generation:** use bounded, reproducible sampling and scenario families. Sample linked soil hydraulic properties consistently; preserve rare-but-valid weather cases; separate valid scenarios from invalid input fixtures.
- **Surrogate:** do not build/deploy a Random Forest, Extra Trees, PINN, or other surrogate unless a real workload and benchmark show the benefit outweighs error and maintenance costs.
- **Production terminology:** the model may be called a *frozen reference prototype* only after source freeze/versioning. Do not call it agronomically validated or safe for farmer recommendations without relevant field evaluation.
- **Calibration:** real-world calibration/evaluation is the gate for agricultural validity, not a reason to block documentation and unrelated architecture work entirely.
- **Next engineering step:** obtain and commit `agrisim_core.py`, the parameter registry, test harness, scenario generator, raw logs and run instructions from the authors of the claimed execution; rerun them independently; then repair coverage and parameter sampling where tests show defects.

## Open questions

1. What exact version of the simulator source corresponds to each reported log/hash?
2. What are the full equations, units, time-step convention, boundary conditions and flux allocation implementation?
3. Can the reported run be reproduced from committed source, pinned dependencies, seeds and input data?
4. How should soil profiles and weather trajectories be sampled for the intended area and use cases?
5. Which public measured dataset is suitable for which subset of the model, and what does it not identify?
6. What is the minimum field measurement plan for local calibration and independent evaluation?

## Evidence status at a glance

| Claim | Status here | What would upgrade it |
|---|---|---|
| Layered simulator is the right MVP direction | PROPOSED / ARCHITECTURE DECISION | More complete requirements and comparison against fit-for-purpose reference models |
| Water-balance residuals near floating-point tolerance | REPORTED, ARTIFACTS MISSING | Actual source, logs, independent residual calculation and reproducible run |
| 100-scenario LHS / metamorphic tests passed | REPORTED, ARTIFACTS MISSING | Sampler, simulator, test functions, outputs and repeatable run |
| Random Forest/Extra Trees results and constraint violations | REPORTED, ARTIFACTS MISSING | Training/evaluation code, datasets or deterministic generation, dependency versions and logs |
| Simulator runs around 19.71 microseconds per step | REPORTED, NEEDS REPRODUCTION | Timing script, environment details, workload definition, repeated results |
| Synthetic data is locally representative of Anantapur | NOT ESTABLISHED | Suitable local soil/weather distributions and real observations |
| Simulator predicts actual farm outcomes correctly | NOT ESTABLISHED | Calibration plus independent real-world evaluation |

## Next action

Ask the source AI/user to export the actual source artifacts cited in `source-drops/qwen-sprint1-reexecution-and-sprint2-benchmark-report.txt`. Do not recreate missing code from narrative descriptions and claim it is the original implementation.
