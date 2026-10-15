# Argon PoT / PAL audit — submitted summary (2026-10-14)

- **Record type:** preserved external AI review summary supplied by the project owner
- **Evidence status:** mixed. Some arithmetic and one archived code snippet were independently checked in this working session; other findings remain claims from Argon's report because the exact source, generator, harness, environment, and raw logs were not supplied.
- **Important:** role names such as Aris, Turing, and Murphy are review perspectives reported by Argon, not proof that independent agent processes were actually run.

## Repository/provenance findings reported by Argon

Argon reported that the GitHub repository was at commit `2fa6f1f` on `main`, with six commits, and that the core project records and protocol docs were present. It reported that the historical executable artifacts (`agrisim_core.py`, `mr_tests.py`, `run_sprint1.py`, benchmark scripts, JSON/CSV run outputs) were not committed; only report text and reported hashes were available.

The archived Qwen report `qwen-sprint1-reexecution-and-sprint2-benchmark-report.txt` contains two different core hashes:

- Sprint 1 log: `d05fbd3156cd76a60388f07b5e2cfe2a4ffc49e93668ffd1ff235ed7231ac906`
- Sprint 2 decision: `5ec4698a29f060d3...` (truncated)

This is a provenance discrepancy to resolve by recovering the exact file versions and recomputing complete hashes. The text alone does not establish whether the source changed, whether the hash belongs to a different version, or whether a reporting error occurred.

## Quantitative findings and reconciliation status

| Audit target | Argon's finding | Reconciliation in this package |
|---|---|---|
| Sprint 1 LHS code/log | The exact displayed `custom_lhs(7, 100, seed=42)` snippet, without affine scaling, gives 15 ordered theta triples and 85 rejected. If the shown `problem_bounds` are applied, all 100 satisfy `theta_wp < theta_fc < theta_sat`, because the intervals are disjoint. Neither path gives the report's `86 valid / 14 rejected`. | **Independently reproduced here** by running the exact archived snippet and its stated affine scaling in Python: unscaled `15/85`, scaled `100/0`. The displayed source and the `86/14` output are inconsistent unless omitted/different code was used. |
| PAW rejection geometry | For independent uniform draws `theta_fc ∈ [0.20, 0.30]` and `theta_wp ∈ [0.08, 0.15]`, the area with `PAW = theta_fc - theta_wp < 0.10` is `0.5 × 0.05² / (0.07 × 0.10) = 5/28 ≈ 17.857%`. | **Analytically verified here.** This is the theoretical probability under those bounds, not an exact expected count in any finite seeded sample. The archived statement `223/1200` equals **18.583%**, not `20.1%`; that percentage/count pair is arithmetically inconsistent. Raw generator output is needed to evaluate the observed count. |
| Fix B PAW sample | Argon flags sample `theta_wp = 0.070` as outside the older `theta_wp ∈ [0.08, 0.15]` registry bound and reports that some generated draws violate `theta_aer = theta_fc + 0.05 < theta_sat`. | The sample value `0.070` is visible in the archived report and lies outside that older bound. Its sample `theta_fc = 0.257`, `theta_sat = 0.440` gives `theta_aer = 0.307 < 0.440`, so the shown example itself passes the aeration-margin test. Argon's reported 16.4% violation rate and 10.2% texture/conductivity mismatch rate remain **unverified** without the full sampler and generated rows. |
| Independent scalar timing | Argon reports `0.0245 s ± 0.0014 s` for 10,000 steps × 10 repetitions (`2.45 µs/step`, about 408k steps/s), compared with Qwen's `0.1971 s ± 0.0048 s`. | **Unverified external timing claim.** The scalar implementation, exact workload, environment, warm-up policy, and raw repetitions are not preserved as files. It cannot establish an apples-to-apples speed ratio. The new candidate has its own logged timing, explicitly not comparable absent matched code and method. |
| Operator-splitting sensitivity | Argon reports that different within-step flux orders moved storm runoff / inter-layer drainage by more than 15%, despite mass balance holding. | A useful hypothesis and priority experiment, but the quoted percentage is **not independently reproduced** here. The candidate locks one explicit sequence and logs residuals; this does not prove that sequence is the most physically appropriate. |

## Structural / agronomic risks raised

### Soil hydraulic parameter generation

Argon recommends sampling soil texture fractions on a simplex and deriving hydraulic properties with a cited pedotransfer function (PTF), such as Saxton–Rawls or Rosetta, rather than independently sampling hydraulic variables. It stresses that `theta_wp < theta_fc < theta_sat` alone is necessary but not sufficient for joint hydraulic consistency, that drainable/air-filled porosity needs an explicit constraint, and that conductivity should be coupled to texture/structure.

This is a sound design direction, but the exact reported percentage of incompatible draws and any field representativeness claim need the actual sampler, parameter definitions, bounds, and validation target. The simulation candidate's generator is deliberately labelled **illustrative texture-coupled priors**, not a full or validated implementation of either named PTF.

### Identifiability and calibration

Argon highlights conditional confounding between `Ksat` and `hardpan` when an observable depends only on their product, and between layer depths and storage/uptake under limited moisture observations. These are important warnings. A one-output/two-parameter product model is rank-deficient by construction; extending that conclusion to every full-model time series requires specifying observables, forcings, regimes, priors, and sensitivities. The broad assertion that the full seven-parameter model is always structurally unidentifiable is not established by the submitted summary alone.

The claim that Anantapur dry spells leave certain parameters insensitive on more than 85% of days needs a local forcing dataset and a defined sensitivity calculation. Rooting depths should be measured/fixed where feasible, and storm/wet-drainage and dry-down regimes should be analyzed separately.

### Three-ply adverse scenario

Argon proposes a test in which mild-rainfall calibration equifinality (`Ksat` high, hardpan factor low) looks acceptable, then a two-day 110 mm storm exposes deep-drainage failure and top-layer waterlogging in papaya. Preserve this as an **adversarial test hypothesis**, not a demonstrated crop-loss, disease, or trenching result. The model would need a reproducible scenario, explicit drainage law, calibrated soil profile, and appropriate agronomic evidence before such an outcome could support a recommendation.

### Knowledge-graph parallel track

Argon argues that ontology/provenance work need not wait for calibration. This aligns with the project plan: ontology types for `SoilHorizon`, `CropGuild`, `HydraulicParameterPrior`, and `EvidenceRecord` can be built now, as long as prior values are clearly distinguished from measured data and source provenance is retained.

## Recommended follow-up

1. Recover the exact historical source files and all Fix A–D benchmark scripts, JSON/CSV logs, dependency versions, and environment metadata.
2. Recompute all complete SHA-256 hashes and tie each report/log to a source version.
3. Re-run LHS and PAW counts from one committed script, using explicit affine scaling, bounds, seed, and raw output; resolve the `86/14`, `223/1200` and `20.1%` inconsistencies.
4. Test alternative operator-splitting orders on identical storm/dry scenarios; compare every flux and state trajectory, not mass residual alone.
5. Replace illustrative parameter priors with a cited PTF or measured hydraulic data before calibration; do not claim Anantapur-local realism without local evidence.
6. Run sensitivity / identifiability analysis against predeclared observations and wet-storm plus dry-down regimes, with measured layer depths where possible.
7. Continue KG/provenance work in parallel and keep farmer-facing advice gated on independent field evaluation.
