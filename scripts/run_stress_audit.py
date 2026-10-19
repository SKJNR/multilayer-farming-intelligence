"""Reproducible randomized stress test for the synthetic two-layer candidate.

This checks bookkeeping, finite outputs, and configured storage bounds only.
It does not validate the physical accuracy of the flux laws.
"""
from __future__ import annotations
import json
import sys
from pathlib import Path
import numpy as np
ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
from simulation.agrisim_core import SoilParameters, TwoLayerSoilWaterModel
from simulation.soil_generator import generate_soil_priors


def main() -> None:
    seed = 20261015
    n_profiles, days = 2_000, 30
    rng = np.random.default_rng(seed)
    priors = generate_soil_priors(n_profiles, seed=seed)
    max_residual = 0.0
    checks = 0
    failure = None
    max_flux = {"runoff_mm": 0.0, "drainage_l1_l2_mm": 0.0, "deep_drainage_mm": 0.0}

    for index, p in enumerate(priors):
        # Same prior is mapped to both layers for this software stress test.
        # This intentionally does not assert realistic vertical stratification.
        soil = SoilParameters(
            z1_mm=p["z1_mm"], z2_mm=p["z2_mm"],
            theta_sat1=p["theta_sat"], theta_sat2=p["theta_sat"],
            theta_fc1=p["theta_fc"], theta_fc2=p["theta_fc"],
            theta_wp1=p["theta_wp"], theta_wp2=p["theta_wp"],
            theta_aer1=p["theta_aer"], theta_aer2=p["theta_aer"],
            ksat1_mm_day=p["ksat1_mm_day"], ksat2_mm_day=p["ksat2_mm_day"],
            hardpan_factor=p["hardpan_factor"],
        )
        model = TwoLayerSoilWaterModel(soil)
        for day in range(days):
            rain = float(rng.choice([0, 0, 0, 1, 5, 15, 40, 80, 120]))
            irrigation = float(rng.choice([0, 0, 0, 5, 10, 20]))
            evaporation = float(rng.uniform(0, 10))
            groundnut_demand = float(rng.uniform(0, 12))
            papaya_demand = float(rng.uniform(0, 15))
            roots = tuple(rng.uniform(0, 1, size=2))
            out = model.step(rain, evaporation, groundnut_demand, papaya_demand,
                             roots, irrigation_mm=irrigation)
            residual = abs(out["mass_balance_residual_mm"])
            max_residual = max(max_residual, residual)
            theta = model.get_theta()
            fluxes = [out[k] for k in ("runoff_mm", "evaporation_actual_mm",
                      "groundnut_uptake_l1_mm", "papaya_uptake_l1_mm",
                      "papaya_uptake_l2_mm", "drainage_l1_l2_mm", "deep_drainage_mm")]
            for key in max_flux:
                max_flux[key] = max(max_flux[key], float(out[key]))
            if (not np.isfinite(theta).all() or not np.all(np.isfinite(fluxes))
                    or min(fluxes) < -1e-10
                    or np.any(theta < model.wp - 1e-9)
                    or np.any(theta > model.sat + 1e-9)
                    or residual > 1e-8):
                failure = {"profile_index": index, "day_index": day,
                           "residual_mm": residual, "theta": theta.tolist(),
                           "rainfall_mm": rain, "irrigation_mm": irrigation,
                           "fluxes": fluxes}
                break
            checks += 1
        if failure:
            break

    report = {
        "status": "PASS" if failure is None else "FAIL",
        "evidence_class": "Synthetic_Software_Stress_Test_Not_Field_Validation",
        "seed": seed, "profiles_requested": n_profiles, "days_per_profile": days,
        "steps_checked": checks, "failure": failure,
        "max_abs_profile_mass_residual_mm": max_residual,
        "max_observed_flux_mm_per_day": max_flux,
        "design_note": "Each generated prior is applied identically to both layers; this tests software bounds/accounting, not vertical soil-profile realism.",
        "limitations": ["illustrative priors", "no field observations", "no calibrated hydraulic curves", "not an agronomic validation"],
    }
    root = Path(__file__).resolve().parents[1]
    out = root / "artifacts" / "stress_audit.json"
    out.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(report, indent=2))
    if failure:
        raise SystemExit(1)

if __name__ == "__main__":
    main()
