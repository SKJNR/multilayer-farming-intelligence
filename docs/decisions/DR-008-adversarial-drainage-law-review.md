# DR-008 — Adversarial Drainage-Law and Field-Readiness Review

- **Recorded:** 2026-10-15
- **Reviewed source commit:** `9e84ec4698c9136b4051d19f6b903a33c3239b49`
- **Branch:** `review/real-world-readiness-gates`; do not merge this branch automatically
- **Status:** Research prototype only; field readiness blocked
- **Review mode:** Direct source inspection, clean-archive test rerun, deterministic synthetic diagnostic, and structured specialist/adversarial review. No independent external expert panel was invoked.

## Decision

Keep the candidate for software testing, sensitivity exploration, and measurement planning. Do not calibrate the empirical drainage multiplier or use predictions for farmer-facing decisions until the flux law's units, meaning, and physical interpretation are written down and reviewed.

## Reproducibility status

- Live GitHub `main`: `a6b3f45e77aa36c6748271858178522070be61a7`.
- Review branch: `9e84ec4698c9136b4051d19f6b903a33c3239b49`; not merged into `main`.
- GitHub Actions run [38763681646](https://github.com/SKJNR/multilayer-farming-intelligence/actions/runs/38763681646) passed the branch's test and synthetic-stress job.
- Independent clean-archive rerun: **13 tests passed**; **60,000 synthetic steps** checked; maximum absolute profile mass residual `1.4211e-13 mm`; **52/52** source-snapshot checksum entries verified.
- None of these checks is field calibration or validation.

## New executable finding: drainage law requires physical review

The implementation calculates:

```python
raw_d12 = Ksat1 * exp(drainage_shape * max(0, theta1 - theta_fc1))
raw_d2  = Ksat2 * exp(drainage_shape * max(0, theta2 - theta_fc2))
```

The daily flux can exceed the numeric `Ksat_mm_day` parameter because the exponential factor can be greater than one. The model does not explicitly compute or report hydraulic head gradient, so the intended relationship between that factor, saturated conductivity, and daily drainage is unspecified.

A deterministic diagnostic on the illustrative soil priors and seeded forcing sequence (seed `20261015`, 2,000 profiles × 30 days) found:

- Inter-layer flux greater than the `Ksat1` numerical scale in **17,073 / 60,000 steps (28.455%)**.
- Deep drainage greater than the `Ksat2` numerical scale in **26,804 / 60,000 steps (44.673%)**.
- Maximum sampled ratios: **4.737×** (inter-layer) and **5.028×** (deep drainage).

Reproduce with `python scripts/audit_drainage_rate_law.py`; machine-readable output is `artifacts/drainage_rate_law_audit.json`.

**Interpretation must remain narrow:** a flux-to-conductivity ratio above one is not automatically physically impossible because Darcy flux depends on hydraulic gradient. The concern is that this bucket implementation does not explicitly model that gradient while labelling the parameters as Ksat and using an exponential empirical multiplier. This is a model-specification ambiguity that requires domain review, not proof of physical impossibility. Do not silently cap flux or merely rename the parameter without defining and validating the law.

## Specialist and adversarial review

These are analytical review hats, not claims that separately invoked experts independently agreed.

### Soil physicist / agro-hydrologist
Write the inter-layer and deep-drainage equations with units, operating domain, hardpan representation, receiving-layer effects, and the physical basis of the multiplier. Compare with hand-calculable cases, a documented hydraulic function, or observed drainage trajectories.

### Numerical-methods reviewer
Profile-level conservation passed the synthetic fixtures. Add explicit per-layer water-budget calculations so the transfer enters layer 1 and layer 2 with opposite signs; verify internal transfers cancel at profile scale. Ensure storage clipping cannot conceal an unexplained correction.

### Crop physiologist / agronomist
Potential evaporation, groundnut transpiration, papaya transpiration, and papaya root fractions are supplied inputs, not derived by the simulator. The forcing adapter needs its own versioned equations and provenance. Soil-water fit does not validate yield, disease, crop death, or intervention efficacy.

### Statistician / calibration designer
The existing product example only illustrates rank deficiency for one scalar response. It is not a global identifiability analysis of the dynamic model. Fix measured depths and known inputs where possible; assess sensitivity/correlation under the actual observation design and retain ranges for confounded parameters.

### Data / knowledge-graph steward
Retain horizon, method, date, units, uncertainty, and evidence class for every parameter. The stress test applies the same illustrative prior to both layers; it does not test realistic vertical stratification.

### Adversarial reviewer (Murphy; chess-move challenge)

- **Ply 1:** choose a low-conductivity generated soil with layer 1 above field capacity.
- **Ply 2:** apply repeated heavy rain/irrigation while the lower layer is near saturation or the profile has a restrictive boundary.
- **Ply 3:** check whether the multiplier creates fast drainage without a specified gradient and whether the resulting trajectory remains plausible despite an excellent mass residual.

A suitable falsifier is a domain-reviewed, fully specified law with units, independent hand-checkable fixtures, and acceptable agreement against measured wetting/drainage observations over the declared operating domain.

## G2 exit criteria before calibration

1. Decide whether each parameter denotes saturated hydraulic conductivity, effective conductivity, or an empirical drainage-rate coefficient, and make variable names/units consistent.
2. Specify all inter-layer/deep-drainage equations and time-step integration.
3. Add per-layer budgets and tests; unexplained storage correction must fail loudly.
4. Compare hand-calculable fixtures and an independent reference case; test alternative operator-splitting order under storm conditions.
5. Keep the current run labelled synthetic software evidence; do not tune the multiplier to field moisture before the law and forcing pipeline are specified.

## Go / no-go

- **GO:** software/source control, synthetic tests, sensitivity exploration, knowledge-graph/provenance work, measurement feasibility.
- **CONDITIONAL:** replay measured moisture after the input adapter, equation specification and data-QA rules are reviewed.
- **NO-GO:** farmer-facing irrigation/trenching advice, field-validation claims, or yield/disease predictions from this soil-water prototype.

## Reference

The [Rosetta soil hydraulic PTF implementation](https://github.com/usda-ars-ussl/rosetta-soil) documents a van Genuchten parameter set and distinguishes saturated conductivity from unsaturated-conductivity behavior. Apply a published hydraulic function only after checking its inputs, units, and applicability; it is not an automatic drop-in replacement for this bucket law.
