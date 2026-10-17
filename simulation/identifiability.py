"""Structural and practical trajectory identifiability diagnostics (DR-006 / DR-007)."""
from __future__ import annotations
import numpy as np
from scipy.stats import qmc
from .agrisim_core import SoilParameters, TwoLayerSoilWaterModel


def product_drainage(ksat: float, hardpan: float, excess: float = 1000.0) -> float:
    return float(min(ksat * hardpan, excess))


def local_jacobian_product(ksat: float = 40.0, hardpan: float = 0.5, eps: float = 1e-5) -> np.ndarray:
    dk = (product_drainage(ksat + eps, hardpan) - product_drainage(ksat - eps, hardpan)) / (2.0 * eps)
    dh = (product_drainage(ksat, hardpan + eps) - product_drainage(ksat, hardpan - eps)) / (2.0 * eps)
    return np.array([[dk, dh]], dtype=float)


def trajectory_jacobian_screen() -> dict[str, object]:
    """Evaluate 7-parameter Jacobian SVD of TwoLayerSoilWaterModel across dry vs wet regimes."""
    base = np.array([300.0, 500.0, 0.10, 0.25, 0.45, 50.0, 0.5], dtype=float)
    dry_w = [(2.0 if i % 5 == 0 else 0.0, 4.0) for i in range(30)]
    wet_w = [(55.0 if i % 6 == 0 else 3.0, 3.5) for i in range(30)]

    def sim_traj(vec: np.ndarray, weather: list[tuple[float, float]], observe_both_layers: bool) -> np.ndarray:
        z1, z2, wp1, fc1, sat1, ksat1, hp = vec
        p = SoilParameters(z1_mm=z1, z2_mm=z2, theta_wp1=wp1, theta_fc1=fc1, theta_sat1=sat1,
                           ksat1_mm_day=ksat1, hardpan_factor=hp)
        m = TwoLayerSoilWaterModel(p, initial_theta=(0.24, 0.24))
        out = []
        for r, ep in weather:
            m.step(r, ep, 4.0, 6.0)
            out.append(m.storage[0] / m.z[0])
            if observe_both_layers:
                out.append(m.storage[1] / m.z[1])
        return np.array(out, dtype=float)

    def svd_rank(weather: list[tuple[float, float]], both: bool) -> tuple[int, list[float]]:
        y0 = sim_traj(base, weather, both)
        J = np.zeros((len(y0), len(base)), dtype=float)
        for j in range(len(base)):
            h = max(1e-6, abs(base[j]) * 1e-5)
            vp, vm = base.copy(), base.copy()
            vp[j] += h
            vm[j] -= h
            J[:, j] = (sim_traj(vp, weather, both) - sim_traj(vm, weather, both)) / (2.0 * h)
        sv = np.linalg.svd(J, compute_uv=False)
        return int(np.sum(sv > 1e-6)), [round(float(x), 6) for x in sv]

    rank_dry_l1, sv_dry_l1 = svd_rank(dry_w, False)
    rank_wet_l1, sv_wet_l1 = svd_rank(wet_w, False)
    rank_wet_l12, sv_wet_l12 = svd_rank(wet_w, True)
    return {
        "dry_spell_theta1_only_rank": rank_dry_l1,
        "dry_spell_singular_values": sv_dry_l1,
        "wet_storm_theta1_only_rank": rank_wet_l1,
        "wet_storm_theta1_singular_values": sv_wet_l1,
        "wet_storm_dual_depth_theta1_theta2_rank": rank_wet_l12,
        "wet_storm_dual_depth_singular_values": sv_wet_l12,
    }


def run_screen(n: int = 256, seed: int = 42) -> dict[str, object]:
    sampler = qmc.Sobol(d=2, scramble=True, seed=seed)
    u = sampler.random(n)
    ksat = 5.0 + 95.0 * u[:, 0]
    hp = 0.05 + 0.95 * u[:, 1]
    prod = ksat * hp
    J = local_jacobian_product()
    sv = np.linalg.svd(J, compute_uv=False)
    return {
        "n": n,
        "seed": seed,
        "design": "scrambled Sobol + full 30-day trajectory SVD",
        "ksat_range_mm_day": [5.0, 100.0],
        "hardpan_range": [0.05, 1.0],
        "product_range_observed": [float(np.min(prod)), float(np.max(prod))],
        "local_jacobian": J.tolist(),
        "jacobian_rank": int(np.linalg.matrix_rank(J)),
        "singular_values": sv.tolist(),
        "trajectory_identifiability": trajectory_jacobian_screen(),
        "interpretation": "One product observation cannot separately identify Ksat and hardpan. Dual-depth wet-storm + dry-down windows with fixed horizon depths are required.",
        "evidence_class": "Synthetic_Identifiability_Diagnostic",
    }
