# DR-007 — Candidate Code Audit and Real-World Readiness Gate

- **Recorded:** 2026-10-15
- **Baseline:** GitHub `main` commit `a6b3f45e77aa36c6748271858178522070be61a7`
- **Review artifact:** local branch `review/real-world-readiness-gates` (not merged into GitHub `main`)
- **Status:** Conditional acceptance for research/synthetic testing only; field-readiness blocked
- **Review type:** repository inspection, reproduced code checks, and structured specialist/adversarial desk review; not independent external-agent consensus

## 1. Decision question

Does the committed simulation candidate provide sufficient evidence for real farm use, and what must happen next?

## 2. Findings from the `a6b3f45` baseline

- GitHub `main` contains the candidate simulator, illustrative soil generator, tests, audit scripts/artifacts, DR-006 and a checksum manifest.
- The complete-repository archive used for execution had local Git `HEAD` exactly matching `a6b3f45e77aa36c6748271858178522070be61a7`.
- Before hardening, `python -m pytest -q` passed 8 tests. The benchmark was environment-specific.
- **Finite-state defect reproduced:** `initial_theta=(NaN, 0.25)` was accepted and propagated a NaN state.
- **Manifest defect reproduced:** the manifest generator included `.pytest_cache` and `__pycache__`; ordinary test/audit runs changed these files and caused checksum verification to fail.

## 3. Review-branch changes and verification

The local review branch adds:

- finite-value checks for soil parameters and initial moisture;
- the configured relationship `theta_fc < theta_aer < theta_sat`;
- explicit non-negative `irrigation_mm` input included in the water ledger, without changing existing positional calls;
- separate regression tests for the existing metamorphic checks and the new guardrails;
- a checksum generator that excludes `.git`, Python bytecode and pytest/build caches;
- a deterministic randomized software stress script and machine-readable report;
- a field-readiness roadmap, field-measurement protocol, CSV templates, CI workflow, and explicit adversarial-pairing rule for high-risk reviews.

Results after these local changes:

- `python -m pytest -q`: **13 passed**.
- `python scripts/run_audit.py`: executed on Python 3.13.5, Linux x86_64/glibc 2.41, NumPy 2.3.5, SciPy 1.17.0. Latest recorded five 10,000-step repetitions were 0.54527, 0.58600, 0.47763, 0.49180, 0.48091 seconds; mean 0.51632 s (51.632 µs/step), population standard deviation 0.04253 s. Timing is run- and environment-specific. Environment-specific; not comparable with historical runs without matched methodology.
- `python scripts/run_stress_audit.py`: **60,000 synthetic steps checked**, zero detected software/storage-bound/mass-ledger failures, maximum absolute profile residual `1.4211e-13 mm`, seed `20261015`.
- `sha256sum -c SHA256SUMS.txt`: **52/52 entries passed** after regenerating the manifest with cache exclusions. The manifest is regenerated after all source and generated outputs are final.

The stress fixture maps each generated illustrative hydraulic parameter set identically to both layers. It checks finite output, flux sign, storage bounds and bookkeeping only; it does not establish vertical stratification realism, physical correctness, calibration, or field performance.

## 4. Specialist and adversarial assessment

### Soil physics / agro-hydrology

The candidate is a simplified bucket model with an explicit flux sequence. It omits rainfall-intensity infiltration limits, lateral/preferential flow, capillary rise, mechanistic hydraulic curves, dynamic rooting, and other processes named in the source comments. Its water-content thresholds and conductivity priors need sourced definitions and field/lab or validated-PTF provenance. Mass closure is necessary, not sufficient.

**Adversarial counterexample:** a restrictive subsoil after an intense storm may produce real ponding/back-up that a simplified drainage law misses while the model still closes its mass balance.

### Crop physiology

Potential evaporation, groundnut transpiration, papaya transpiration, and papaya root fractions are inputs; the code does not derive them from weather, crop stage, or measured root profiles. The candidate does not predict yield, infection, root disease, or mortality. A simulated wetness period cannot be labeled a *Phytophthora* event without separate disease evidence.

### Statistics / identifiability

`simulation/identifiability.py` illustrates non-identifiability for one scalar product of two parameters. It is not a full sensitivity/calibration analysis of the dynamic simulator. Fix measurable profile depths and known inputs; evaluate whether observations identify each remaining parameter; retain uncertainty for confounded values.

### Software / reproducibility

The baseline accepted NaN initial states and generated volatile checksum entries. Both defects are addressed and tested on the review branch. The branch has not been merged into `main`; repository tests and local metrics should not be described as a GitHub CI result.

## 5. Decision

- **Accepted:** candidate for transparent software development, controlled synthetic fixtures, sensitivity exploration, and field-measurement planning.
- **Conditional:** offline comparison against observations only after inputs, units, data provenance, and the forcing adapter are documented.
- **Not accepted:** calling this the recovered historical `v1.0.0-ref`; claiming field validation or production readiness; or issuing farmer-facing crop, disease, irrigation, trenching, or yield recommendations.

## 6. Required next evidence

1. Review and merge the hardening/tests/checksum/CI changes only after normal repository review.
2. Recover historical source/scripts and reconcile the original hash mismatch; preserve historical and candidate results separately.
3. Freeze and review governing equations, units, flux order, state timing, supported domain, and known omissions.
4. Replace illustrative priors with a documented PTF/measurement workflow, including uncertainty and applicability limits.
5. Specify/version the adapter that turns weather, crop stage and root evidence into potential evaporation/transpiration and root fractions; preserve rainfall and irrigation as separate inputs.
6. Run a measurement-feasibility pilot, calibrate only identifiable parameters, and evaluate on independent complete plots/seasons/events.
7. Define acceptance criteria before scoring a held-out set; only after passing the relevant gates consider prospective shadow mode and human safety review.

## 7. Related files

- `docs/validation/real-world-readiness-roadmap.md`
- `docs/validation/field-data-protocol.md`
- `templates/field-pilot/`
- `docs/protocol/agent-hats-and-debate-template.md`
- `docs/protocol/evidence-and-reproducibility.md`
