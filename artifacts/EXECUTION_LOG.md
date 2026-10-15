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
