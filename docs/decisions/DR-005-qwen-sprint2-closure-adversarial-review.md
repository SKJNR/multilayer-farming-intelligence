# Decision Record 005 — Adversarial Review of Qwen's Sprint 2 Closure

- **Recorded:** 2026-10-14
- **Source:** User-pasted Qwen report archived in `source-drops/qwen-sprint2-closure-generator-repair-and-calibration-gate.md`
- **Status:** Conditional acceptance of direction; execution claims remain unverified in this repository
- **Review mode:** Multi-perspective desk review. The role labels below are structured review hats, not evidence that independent agents or external experts were actually invoked.

## 1. Problem and objective

Determine what the Sprint 2 closure report supports, what it does not support, and what evidence is required before calling the two-layer simulator frozen, physically valid, or ready for real-world calibration.

## 2. Competing proposals

- **A — Accept the report as verified and proceed:** rejected. The narrative and short logs are not accompanied by source code, environment, scenario definitions, or raw outputs in this repository.
- **B — Reject the architecture entirely:** not justified by the supplied evidence. A small explicit simulator remains a sensible baseline to reproduce and test.
- **C — Accept the engineering direction conditionally, preserve claim provenance, and reproduce the artifacts:** accepted.

## 3. Specialist review hats

### Agro-hydrology / crop systems hat (Aris)

- Deriving `theta_fc = theta_wp + PAW` can guarantee the ordering `theta_wp < theta_fc < theta_sat` when bounds are correctly enforced.
- That ordering alone does **not** guarantee a soil hydraulic parameter set is consistent with a van Genuchten or Brooks–Corey retention/conductivity curve. The joint distribution, texture, bulk density, organic matter, hydraulic curve parameters and conductivity relationships still need defensible constraints or measured calibration.
- A named `Storm` or `Aeration_Test` family is not evidence of adequate regime coverage by itself. Define the target physical state, forcing, expected response and assertions for each family.
- A two-layer bucket model can be an MVP, but it should not be described as physically validated or agronomically safe solely because accounting checks pass.

### Numerical methods / software architecture hat (Turing)

- The arithmetic in the reported timing is internally consistent: 0.1971 seconds / 10,000 steps = 19.71 microseconds per step; the reciprocal is about 50,736 steps/second.
- The report does not define what one “step” includes, hardware/runtime environment, warm-up, timer placement, repetitions' distribution, or whether I/O and scenario setup are included. The figure is a reported microbenchmark, not yet an independently reproducible performance claim.
- The comparison between 5.3 seconds to simulate 150,000 steps and a roughly 6-second model-training time is directionally useful but not a complete workload analysis. Training time is a one-time cost; inference may matter for much larger batches, repeated optimization, ensembles, interactive use, or expensive future physics. Keep the surrogate deferred until a representative end-to-end workload demonstrates a need, rather than declaring it permanently unnecessary.
- A freeze label such as `v1.0.0-ref` requires a tagged source commit, dependency lockfile, deterministic seeds, tests, and a release artifact. The label in prose does not itself establish a frozen implementation.

### Adversarial verification hat (Murphy)

- `1000 / 1000` valid soils demonstrates only that 1,000 generated samples passed the specific validity predicate used. The predicate and parameter bounds are not supplied in the log.
- `Normal: Runoff days=0, Aeration days=0; Storm: 1,1; Aeration_Test: 1,1` is too underspecified to audit. It is unclear whether these are counts over one trajectory, all generated samples, or aggregate test cases. The test could pass by construction while missing important boundary conditions.
- Timing variation attributed to garbage collection and cold-start effects is plausible but not established without raw timings and the benchmark harness.
- Reported mass-balance closure is not evidence that runoff, infiltration, drainage, crop uptake, evaporation, or stress functions are physically correct. Verify both the independent water-accounting identity and flux-specific invariants.

### Statistics / experimental design hat

- Publish parameter bounds and joint distributions; distinguish independent parameter draws from correlated soil-profile properties.
- Separate routine, boundary, and deliberately invalid-input fixtures. Record seeds and scenario IDs.
- Add sensitivity and identifiability analysis before calibration. Sparse moisture observations may not identify all hydraulic, root-uptake, drainage and stress parameters simultaneously.
- Use calibration observations and held-out evaluation observations that are separated in time, location, or profile as appropriate. Do not tune and evaluate on the same observations.

## 4. Adversarial findings and disposition

| Claim in submitted report | Review disposition | Evidence required |
|---|---|---|
| 19.71 microseconds per step | Arithmetic checks out; benchmark not reproduced here | Timing script, source commit, environment, warm-up policy, raw repeated timings and workload definition |
| PAW sampling guarantees physically consistent soils | Overstated | Exact sampler, hydraulic parameterization, joint constraints and validity tests beyond simple theta ordering |
| 1,000 of 1,000 profiles valid | Reported, not independently verified | Generator source, seed, validity predicate, complete output summary and test command |
| Storm and aeration cases are covered | Reported, insufficiently specified | Scenario definitions, expected outcomes, per-scenario assertions and coverage matrix |
| Simulator is frozen as `v1.0.0-ref` | Not established by report alone | Version tag, source, lockfile, changelog, test results and immutable release artifact |
| Simulator is mathematically verified and biologically constrained | Too broad for evidence shown | Independent numerical tests plus empirical comparison against relevant observations |
| Surrogate is unnecessary | Reasonable current default, not universal conclusion | Representative end-to-end workload; revisit if scale, latency, or optimization use changes |
| Calibration must precede all knowledge-graph work | Overly restrictive as a project-wide dependency | Calibration gates model-dependent recommendations; ontology/provenance and data-ingestion work can proceed in parallel |

## 5. Verification plan / acceptance criteria

1. Commit the exact simulator, generator, test harness, benchmark script, parameter registry, dependency lockfile, and README commands.
2. Run tests from a clean environment and capture command, exit code, commit SHA, seed, versions, and raw logs.
3. Independently recompute daily and cumulative water balance from recorded states and fluxes. Define units and sign conventions explicitly.
4. Test invariants including non-negative storage and fluxes, runoff not exceeding available rainfall/run-on under the defined boundary model, no inter-layer drainage when the relevant transfer coefficient is exactly zero, and uptake bounded by available water and root access.
5. Test monotonic relations only under controlled conditions where the relation is actually expected; document counterexamples and domain assumptions.
6. Validate PAW sampling against a stated soil parameterization and empirical parameter ranges; do not equate a valid theta ordering with a fully consistent hydraulic profile.
7. Define a scenario matrix for dry spell, ordinary rainfall, extreme storm, waterlogging/aeration stress, hardpan, deep drainage, near-wilting conditions, and combined stress. Report both case-level results and aggregate coverage.
8. Benchmark the simulator with a representative workload and report median, spread, warm-up, hardware/software and whether setup/I/O are included. Keep the surrogate deferred unless an explicit performance requirement is missed.
9. For calibration, specify the observation dataset, depth/time resolution, missingness, measurement uncertainty, parameter priors/bounds, objective function, identifiability checks, and independent holdout evaluation.
10. Do not claim field validation or deploy farmer-facing recommendations until independent observations show acceptable predictive performance for the intended crop, soil, climate and management domain.

## 6. Decision

**Conditionally accept** the decision to keep the explicit simulator as the reference implementation and defer the ML surrogate for now. **Do not mark the reported execution, soil validity, simulator freeze, or agricultural validity as independently verified** until the artifacts and rerun evidence are committed.

The calibration gate should block claims of local predictive validity and field-facing recommendations. It should not block parallel development of the knowledge-graph ontology, provenance model, data inventory, experiment registry, or field-measurement plan.

## 7. Uncertainty

The report does not include code, raw logs, parameter bounds, full scenario definitions, hardware/software details, or measured field observations. This review therefore evaluates the claims and internal consistency of the report, not the unseen implementation.

## 8. Next experiment

Request and commit the exact code and run artifacts. Reproduce the timing, PAW sampler and scenario-family tests from a clean environment. Then build a calibration plan around an actual candidate dataset and explicitly state which model parameters that dataset can and cannot identify.
