"""Sobol simplex texture + Saxton-Rawls PTF coupled soil prior generator."""
from __future__ import annotations
from scipy.stats import qmc
import numpy as np


def generate_soil_priors(n: int = 1000, seed: int = 42) -> list[dict[str, float]]:
    sampler = qmc.Sobol(d=6, scramble=True, seed=seed)
    u = sampler.random(n)
    rows: list[dict[str, float]] = []
    for row in u:
        a, b = sorted([float(row[0]), float(row[1])])
        sand, clay, silt = max(0.05, a), max(0.05, b - a), max(0.05, 1.0 - b)
        tot = sand + silt + clay
        sand, silt, clay = sand / tot, silt / tot, clay / tot
        om_pct = 0.5 + 3.5 * float(row[2])
        z1 = 200.0 + 200.0 * float(row[3])
        z2 = 300.0 + 500.0 * float(row[4])
        hardpan = 0.05 + 0.95 * float(row[5])

        # Saxton-Rawls (2006) / texture-coupled retention and conductivity priors
        wp = float(np.clip(0.035 + 0.30 * clay + 0.0015 * om_pct, 0.05, 0.25))
        fc = float(np.clip(wp + 0.10 + 0.12 * clay + 0.002 * om_pct, wp + 0.10, 0.42))
        sat = float(np.clip(max(fc + 0.08, 0.48 - 0.12 * clay + 0.002 * om_pct), fc + 0.08, 0.60))
        aer = float(min(fc + 0.06, sat - 0.02))
        ksat1 = float(2.0 * (90.0 ** sand))
        ksat2 = float(0.5 * (120.0 ** sand))

        rows.append({
            "sand_fraction": sand,
            "silt_fraction": silt,
            "clay_fraction": clay,
            "om_pct": om_pct,
            "z1_mm": z1,
            "z2_mm": z2,
            "theta_wp": wp,
            "theta_fc": fc,
            "theta_aer": aer,
            "theta_sat": sat,
            "ksat1_mm_day": ksat1,
            "ksat2_mm_day": ksat2,
            "hardpan_factor": hardpan,
        })
    return rows
