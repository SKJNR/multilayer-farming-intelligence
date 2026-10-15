"""Small reproducible sensitivity/identifiability screen; not a full calibration.

Demonstrates exact confounding for the product Ksat * hardpan in a regime where
D12 is limited by that product, and provides a Sobol design for later model runs.
"""
from __future__ import annotations
import numpy as np
from scipy.stats import qmc


def product_drainage(ksat: float, hardpan: float, excess: float = 1000.0) -> float:
    return min(ksat * hardpan, excess)


def local_jacobian_product(ksat: float = 40.0, hardpan: float = 0.5, eps: float = 1e-5) -> np.ndarray:
    base = np.array([ksat, hardpan], dtype=float)
    y0 = product_drainage(*base)
    jac = np.empty((1, 2), dtype=float)
    for j in range(2):
        plus, minus = base.copy(), base.copy()
        plus[j] += eps
        minus[j] -= eps
        jac[0, j] = (product_drainage(*plus) - product_drainage(*minus)) / (2 * eps)
    return jac


def run_screen(n: int = 256, seed: int = 42) -> dict[str, object]:
    if n < 2:
        raise ValueError("n must be >= 2")
    points = qmc.Sobol(d=2, scramble=True, seed=seed).random(n)
    # Bounds are design ranges, not calibrated physical truth.
    ksat = 5.0 + 95.0 * points[:, 0]
    hardpan = 0.05 + 0.95 * points[:, 1]
    y = ksat * hardpan
    jac = local_jacobian_product()
    singular_values = np.linalg.svd(jac, compute_uv=False)
    # For one scalar observation and two parameters, rank is necessarily <= 1.
    return {"n": n, "seed": seed, "design": "scrambled Sobol; illustrative bounds",
            "ksat_range_mm_day": [5.0, 100.0], "hardpan_range": [0.05, 1.0],
            "product_range_observed": [float(y.min()), float(y.max())],
            "local_jacobian": jac.tolist(), "jacobian_rank": int(np.linalg.matrix_rank(jac)),
            "singular_values": singular_values.tolist(),
            "interpretation": "One product observation cannot separately identify Ksat and hardpan. More independent observables or priors are required.",
            "evidence_class": "Synthetic_Identifiability_Diagnostic"}


if __name__ == "__main__":
    import json
    print(json.dumps(run_screen(), indent=2))
