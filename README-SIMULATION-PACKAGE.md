# Auditable simulation candidate package

## Status and important distinction

This is a **new, locally testable audit candidate**, not a reconstruction or verification of the historical `v1.0.0-ref` claimed in archived chat reports. The original `agrisim_core.py`, exact historical generator, and original benchmark harness were not present in the repository when this package was prepared. Do not attribute this candidate's test or timing results to that missing code.

The soil generator is texture-coupled and enforces basic hydraulic ordering and an air-filled-porosity margin, but it is **not a complete implementation of Saxton–Rawls or Rosetta**. Its retention and conductivity relationships are transparent illustrative priors. Replace them with a validated PTF implementation and local soil data before calibration or farmer-facing use.

## Files

- `simulation/agrisim_core.py`: two-layer daily water balance with explicit operator order and per-step mass residual.
- `simulation/soil_generator.py`: deterministic texture-simplex prior generator.
- `simulation/identifiability.py`: Sobol design and exact product-confounding diagnostic for `Ksat × hardpan`.
- `simulation/mr_tests.py`: metamorphic checks MR1–MR5.
- `scripts/run_audit.py` and `scripts/run_stress_audit.py`: timing, prior validity and identifiability report.
- `scripts/write_sha256_manifest.py`: writes `SHA256SUMS.txt` for repository files while excluding volatile caches.

## Run

```bash
python -m pip install -r requirements-lock.txt
python -m pytest -q
python scripts/run_audit.py
python scripts/run_stress_audit.py
python scripts/write_sha256_manifest.py
```

The generated `artifacts/candidate_audit.json` captures the local runtime environment and results. Timing is hardware/runtime dependent and is not a portable performance guarantee.

## Evidence labels

All generated soil parameters and simulator states are synthetic. Mass-balance closure checks bookkeeping; it does not validate the physical correctness of the flux laws. No field validation, parameter calibration, or suitability for crop-management decisions is claimed.


The `step()` method accepts `rainfall_mm` and keyword-only `irrigation_mm` separately. It still does not model event-intensity infiltration limits or derive evaporation/transpiration demands from meteorology/crop phenology. Read `docs/validation/real-world-readiness-roadmap.md` before connecting field observations.
