"""Deterministic texture-coupled soil parameter prior generator.

This module is deliberately not labelled a full implementation of a published
pedotransfer function (PTF). It samples texture on a simplex, uses transparent
texture/organic-matter-informed retention priors, enforces water-content order
and air-filled-porosity margin, and couples Ksat monotonically to sand content.
It is a prior generator for stress-testing, not a substitute for measured soil
hydraulic properties or a validated Saxton-Rawls/Rosetta implementation.
"""
from __future__ import annotations
import numpy as np
from scipy.stats import qmc


def generate_soil_priors(n: int, seed: int = 42) -> list[dict[str, float]]:
    if n < 1:
        raise ValueError("n must be >= 1")
    # Sobol samples in [0,1]^6: texture split, OM, depths, hardpan.
    sampler = qmc.Sobol(d=6, scramble=True, seed=seed)
    unit = sampler.random_base2(m=int(np.ceil(np.log2(n))))[:n]
    soils = []
    for u in unit:
        # Dirichlet-like simplex construction from two uniforms.
        a, b = sorted((float(u[0]), float(u[1])))
        sand, clay, silt = a, b - a, 1.0 - b
        # Keep meaningful, non-zero fractions; renormalize onto simplex.
        tex = np.maximum([sand, silt, clay], 0.03)
        sand, silt, clay = (tex / tex.sum()).tolist()
        om_pct = 0.5 + 4.0 * float(u[2])
        z1 = 200.0 + 200.0 * float(u[3])
        z2 = 300.0 + 500.0 * float(u[4])
        hardpan = 0.05 + 0.95 * float(u[5])

        # Transparent broad priors (illustrative): finer texture tends to hold
        # more water; organic matter reduces bulk density/increases retention.
        theta_wp = float(np.clip(0.035 + 0.30 * clay + 0.0015 * om_pct, 0.05, 0.25))
        theta_fc = float(np.clip(theta_wp + 0.10 + 0.12 * clay + 0.002 * om_pct, theta_wp + 0.10, 0.42))
        theta_sat = max(theta_fc + 0.08, float(np.clip(0.48 - 0.12 * clay + 0.002 * om_pct, 0.38, 0.58)))
        theta_sat = min(theta_sat, 0.62)
        # Ensure aeration threshold is 5-10 percentage points above FC and below SAT.
        theta_aer = min(theta_fc + 0.06, theta_sat - 0.02)
        # Texture-coupled log-scale Ksat prior; broad enough for sensitivity tests.
        ksat1 = float(np.exp(np.log(2.0) + sand * (np.log(180.0) - np.log(2.0))))
        ksat2 = float(np.exp(np.log(0.5) + sand * (np.log(60.0) - np.log(0.5))))
        soils.append({"sand_fraction": sand, "silt_fraction": silt, "clay_fraction": clay,
                      "organic_matter_pct": om_pct, "z1_mm": z1, "z2_mm": z2,
                      "theta_wp": theta_wp, "theta_fc": theta_fc, "theta_sat": theta_sat,
                      "theta_aer": theta_aer, "ksat1_mm_day": ksat1,
                      "ksat2_mm_day": ksat2, "hardpan_factor": hardpan,
                      "evidence_class": "Illustrative_Prior_Not_Field_Measured"})
    return soils
