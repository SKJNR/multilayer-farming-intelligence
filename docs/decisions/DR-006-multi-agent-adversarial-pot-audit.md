# DR-006 — Adversarial audit of archived simulator claims and new candidate package

- **Status:** Accepted as an audit agenda; not a claim that historical results have been reproduced
- **Date:** 2026-10-14
- **Scope:** Argon's supplied repository/PoT audit summary, Qwen's supplied code snippets and execution log, and the locally run candidate package included with this record
- **Evidence classes:** `Archived_Claim`, `Analytical_Check`, `Locally_Reproduced_Candidate`, `Unverified_External_Claim`

## Decision

1. Do not label the historical `v1.0.0-ref` independently reproduced. The original `agrisim_core.py`, original generator, exact benchmark harness, environment lock, and raw timing samples were not present in the local source bundle available for this work.
2. Keep the explicit simulator as the preferred model class for current farm-scale exploratory sweeps, but do not freeze its physics or use its outputs for farmer-facing prescriptions.
3. Accept a new, clearly labelled **audit candidate** package for reproducible testing. It is not byte-for-byte equivalent to the historical code and its timing is not a reproduction of Qwen's reported timing.
4. Continue KG/provenance work in parallel. Every parameter and output must carry a provenance/evidence class; synthetic prior values must never be presented as measured soil data.
5. Treat soil hydraulic parameterization and calibration as unresolved. The included generator is a transparent texture-coupled illustrative prior, **not a validated full implementation of Saxton–Rawls or Rosetta**.

## Findings from the supplied Argon audit — not independently reproduced here

- Argon reports a mismatch between a historical source-file hash and a later hash in archived reports. This is a legitimate provenance issue to resolve by recovering the exact files and recomputing SHA-256; the historical file bytes were not available to compare in this session.
- Argon reports an independent scalar timing of `0.0245 s ± 0.0014 s` for 10,000 steps × 10 repetitions. Because the harness, exact implementation, runtime metadata, and raw timing samples were not supplied as files, this is recorded as an `Unverified_External_Claim`, not a verified performance comparison. Different implementations cannot establish an apples-to-apples speed ratio.
- The product `Ksat × hardpan` is confounded in a regime where the only observable is that product. This supports a *conditional* identifiability warning, not a universal proof that every time-series calibration of the full model is structurally unidentifiable under all possible observations and forcings.
- **Newly checked LHS mismatch:** running the exact `custom_lhs(7, 100, seed=42)` function shown in the archived Sprint 1 report yields `15 valid / 85 rejected` when the raw `[0,1]` values are checked without scaling. Applying the displayed affine `problem_bounds` yields `100 valid / 0 rejected`, because the theta intervals are disjoint. Neither result reproduces the archived `86 valid / 14 rejected`; some omitted/different code must have been used, or the log is wrong.
- **Newly checked PAW arithmetic:** the exact area where `theta_fc - theta_wp < 0.10` over the stated independent bounds is `5/28 = 17.857%`. The archived `223/1200` count is `18.583%`, not the report's associated `20.1%`. Finite-sample counts can differ from the theoretical rate, but the percentage/count pairing needs correction and the source run must be reproduced.
- Argon reports that Fix B emitted a sample `theta_wp=0.070`, outside the earlier `[0.08, 0.15]` registry range. Its reported 16.4% aeration-margin violations and 10.2% texture/Ksat mismatch rate are not reproducible from the archived sample lines alone; the displayed sample itself has `theta_fc + 0.05 < theta_sat`.
- Argon's scalar timing, greater-than-15% operator-splitting sensitivity, broad seven-parameter unidentifiability claim, and three-ply papaya/waterlogging failure remain hypotheses or external claims until their exact code, environment, definitions, and raw results are preserved. Product confounding is exact when the only observable is `Ksat × hardpan`; this is a conditional result, not a universal proof about every possible time-series experiment.
- Argon's suggestion to begin KG/provenance work in parallel is accepted as project sequencing: ontology and evidence types do not require the simulator to be field-calibrated first, provided synthetic priors remain labelled as such.
- These detailed claims and their evidence dispositions are preserved in `source-drops/argon-pot-audit-submitted-2026-10-14.md`.

## Local candidate package

Files added with this decision:

- `simulation/agrisim_core.py`
- `simulation/soil_generator.py`
- `simulation/identifiability.py`
- `simulation/mr_tests.py`
- `tests/test_reference_package.py`
- `scripts/run_audit.py`
- `scripts/write_sha256_manifest.py`
- `artifacts/candidate_audit.json`
- `README-SIMULATION-PACKAGE.md`
- `requirements.txt`
- `SHA256SUMS.txt`

The candidate uses an explicit sequence: rainfall/infiltration and runoff → inter-layer drainage → deep drainage → stress and uptake. It emits a per-step water balance residual. The candidate tests exercise bookkeeping closure, demand monotonicity, hardpan drainage monotonicity, sampled hydraulic ordering, generator determinism, invalid parameter rejection, and a small product-confounding diagnostic.

### Local verification result

- `python -m pytest -q`: **8 passed** in the available sandbox.
- `python scripts/run_audit.py`: executed and wrote `artifacts/candidate_audit.json`.
- `python scripts/write_sha256_manifest.py`: wrote a SHA-256 manifest.
- The timing result in `candidate_audit.json` is machine/environment-specific and must not be compared directly with the archived historical numbers without matching code, Python/NumPy/SciPy versions, and methodology.

These checks establish only that this candidate package's tests passed in this environment. They do not establish real-world accuracy, calibration, hydraulic realism, or validation of the missing historical reference implementation.

## Required next evidence

1. Recover the original `agrisim_core.py`, `mr_tests.py`, `run_sprint1.py`, generator, benchmark scripts, and any intervening versions from the environment where Qwen ran them.
2. Recompute SHA-256 for every recovered file and reconcile the reported hash discrepancy.
3. Re-run LHS/PAW generation from the exact source and explicitly reconcile `86/14`, `223/1200`, and `20.1%`; save all samples/counts and the exact affine-scaling code.
4. Supply a pinned environment (`requirements-lock.txt` or equivalent), OS/Python metadata, exact command, raw per-repetition timing values, and test output.
5. Run the historical and candidate implementations side by side with identical initial states, weather, flux order, and units; compare state trajectories and every flux, not just mass residuals. Separately test whether alternative operator-splitting orders materially change storm outcomes.
6. Replace the illustrative texture prior with a cited, tested PTF implementation or measured retention/conductivity data before attempting calibration.
7. For calibration, predefine observables, forcing regimes, parameter bounds/priors, identifiability diagnostics, and an independent holdout. Fix rooting depths from measurements where possible and avoid interpreting `Ksat` and hardpan independently when the observations only constrain their product.

## Non-goals

This decision does not certify a soil hydraulic model, select field parameters for Anantapur, validate any crop-disease outcome, or authorize farmer-facing recommendations. Mass conservation is necessary bookkeeping evidence, not proof that the flux laws are physically correct.
