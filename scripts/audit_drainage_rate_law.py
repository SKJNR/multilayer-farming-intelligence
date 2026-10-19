"""Adversarial diagnostic for daily drainage relative to its Ksat scale.

A flux/Ksat ratio above one is not universally impossible: Darcy flux depends
on hydraulic gradient. This script flags a specification question because the
bucket implementation does not explicitly calculate/report a hydraulic-head
gradient while naming parameters Ksat (mm/day).
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
    seed, n_profiles, days = 20261015, 2_000, 30
    rng = np.random.default_rng(seed)
    priors = generate_soil_priors(n_profiles, seed=seed)
    count_d12_over = count_d2_over = steps = 0
    max_d12 = {"ratio_to_ksat": 0.0}
    max_d2 = {"ratio_to_ksat": 0.0}
    for index, p in enumerate(priors):
        # Same generated prior mapped to both layers: an intentional software
        # stress fixture, not a realistic vertical-profile generator.
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
            evap = float(rng.uniform(0, 10))
            groundnut = float(rng.uniform(0, 12))
            papaya = float(rng.uniform(0, 15))
            roots = tuple(rng.uniform(0, 1, size=2))
            out = model.step(rain, evap, groundnut, papaya, roots,
                             irrigation_mm=irrigation)
            if soil.ksat1_mm_day > 0:
                ratio = out["drainage_l1_l2_mm"] / soil.ksat1_mm_day
                count_d12_over += ratio > 1.0
                if ratio > max_d12["ratio_to_ksat"]:
                    max_d12 = {"ratio_to_ksat": float(ratio), "profile_index": index,
                               "day_index": day, "flux_mm_day": out["drainage_l1_l2_mm"],
                               "ksat_mm_day": soil.ksat1_mm_day,
                               "theta_after_step": out["theta1"]}
            if soil.ksat2_mm_day > 0:
                ratio = out["deep_drainage_mm"] / soil.ksat2_mm_day
                count_d2_over += ratio > 1.0
                if ratio > max_d2["ratio_to_ksat"]:
                    max_d2 = {"ratio_to_ksat": float(ratio), "profile_index": index,
                              "day_index": day, "flux_mm_day": out["deep_drainage_mm"],
                              "ksat_mm_day": soil.ksat2_mm_day,
                              "theta_after_step": out["theta2"]}
            steps += 1
    report = {
        "status": "REVIEW_REQUIRED",
        "evidence_class": "Reproduced_Synthetic_Code_Diagnostic_Not_Field_Evidence",
        "source": "simulation/agrisim_core.py + simulation/soil_generator.py",
        "seed": seed, "profiles": n_profiles, "days_per_profile": days,
        "steps": steps,
        "steps_d12_flux_above_ksat_scale": int(count_d12_over),
        "steps_d2_flux_above_ksat_scale": int(count_d2_over),
        "fraction_d12_steps_above_ksat_scale": float(count_d12_over / steps),
        "fraction_d2_steps_above_ksat_scale": float(count_d2_over / steps),
        "max_d12_ratio_example": max_d12, "max_d2_ratio_example": max_d2,
        "interpretation": (
            "The exponential drainage multiplier can produce daily flux greater than the numeric Ksat parameter. "
            "This is not, alone, proof of physical impossibility because Darcy flux depends on hydraulic gradient; "
            "however, the bucket code does not explicitly calculate or report that gradient. The rate law, units, "
            "intended meaning, and plausible domain require a domain-reviewed equation before field use."
        ),
        "limitations": ["illustrative priors only", "same prior mapped to both layers",
                        "no observed hydraulic-head gradient", "not field validation"],
    }
    out = ROOT / "artifacts" / "drainage_rate_law_audit.json"
    out.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(report, indent=2))
    print(f"Saved {out.relative_to(ROOT)}")

if __name__ == "__main__":
    main()
