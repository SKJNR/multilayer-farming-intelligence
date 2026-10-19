# Candidate audit execution log

- **Status:** locally executed candidate package; not reproduction of historical `v1.0.0-ref`
- **Python:** 3.13.5
- **Platform:** Linux x86_64, glibc 2.41
- **NumPy:** 2.3.5
- **SciPy:** 1.17.0
- **Test command:** `python -m pytest -q`
- **Latest test result:** `8 passed in 0.89s`
- **Audit command:** `python scripts/run_audit.py`
- **Steps/repetition:** 10,000
- **Repetitions:** 5
- **Latest observed elapsed times (seconds):** 0.4669576070, 0.4905091080, 0.4938067380, 0.5383608650, 0.4932347830
- **Mean:** 0.4965738202 s per 10,000 steps
- **Population standard deviation:** 0.0231467658 s
- **Mean per step:** 49.6574 microseconds
- **Generated prior rows:** 1,000; basic hydraulic ordering and FC-to-saturation margin checks passed
- **Identifiability screen:** rank 1 for the one-output, two-parameter product example

These numbers characterize only this candidate implementation in this environment and run. Timing varies by run and environment; it must not be compared directly to archived Qwen/Argon values without identical code, environment, workload, and measurement method. Passing mass-balance tests confirms accounting closure for tested sequences, not physical validity or field calibration. For full structured output, see `artifacts/candidate_audit.json`.


## Review-branch hardening rerun — 2026-10-15

- `python -m pytest -q`: **13 passed** in 1.25 s (latest local rerun).
- `python scripts/run_audit.py`: executed on Python 3.13.5, Linux x86_64/glibc 2.41, NumPy 2.3.5, SciPy 1.17.0. Five 10,000-step repetitions were 0.54527, 0.58600, 0.47763, 0.49180, 0.48091 seconds; mean 0.51632 s (51.632 µs/step), population standard deviation 0.04253 s. Environment-specific; not comparable with historical runs without matched methodology.
- `python scripts/run_stress_audit.py`: **60,000 synthetic steps checked**, zero detected failures, maximum absolute profile residual `1.4211e-13 mm`; seed `20261015`. Each generated illustrative parameter set was applied identically to both layers, so this does not establish vertical profile realism or field validity. Full result: `artifacts/stress_audit.json`.
- Regression hardening: non-finite soil parameters and initial moisture rejected; aeration threshold must lie above field capacity and below saturation; explicit irrigation is included in the input ledger and tested.
- Checksum workflow revised to exclude `.git`, `__pycache__`, `.pytest_cache`, and other volatile build/cache directories. Regenerate `SHA256SUMS.txt` only after finalizing run artifacts.
- No field observations used; no calibration, independent validation, disease prediction, yield prediction, or farmer recommendation is claimed.
- `sha256sum -c SHA256SUMS.txt`: **52/52 entries passed** after the final manifest was regenerated with cache exclusions.
