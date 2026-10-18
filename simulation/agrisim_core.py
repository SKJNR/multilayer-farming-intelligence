"""Physically bounded two-layer soil-water model with midpoint stress evaluation (DR-007)."""
from __future__ import annotations
from dataclasses import dataclass
import numpy as np


@dataclass(frozen=True)
class SoilParameters:
    z1_mm: float = 300.0
    z2_mm: float = 500.0
    theta_sat1: float = 0.45
    theta_sat2: float = 0.45
    theta_fc1: float = 0.25
    theta_fc2: float = 0.25
    theta_wp1: float = 0.10
    theta_wp2: float = 0.10
    theta_aer1: float = 0.35
    theta_aer2: float = 0.35
    ksat1_mm_day: float = 50.0
    ksat2_mm_day: float = 20.0
    hardpan_factor: float = 0.5
    drainage_shape: float = 3.0


def _stress(theta: float, wp: float, fc: float, aer: float, sat: float) -> tuple[float, float, float]:
    fw = float(np.clip((theta - wp) / (fc - wp), 0.0, 1.0))
    fa = float(np.clip((sat - theta) / (sat - aer), 0.0, 1.0))
    return fw, fa, fw * fa


class TwoLayerSoilWaterModel:
    def __init__(
        self,
        params: SoilParameters = SoilParameters(),
        initial_theta: tuple[float, float] = (0.25, 0.25),
    ) -> None:
        if not (0.0 < params.theta_wp1 < params.theta_fc1 < params.theta_aer1 < params.theta_sat1 <= 1.0):
            raise ValueError("Invalid Layer 1 hydraulic ordering.")
        if not (0.0 < params.theta_wp2 < params.theta_fc2 < params.theta_aer2 < params.theta_sat2 <= 1.0):
            raise ValueError("Invalid Layer 2 hydraulic ordering.")
        self.params = params
        self.z = np.array([params.z1_mm, params.z2_mm], dtype=float)
        self.sat = np.array([params.theta_sat1, params.theta_sat2], dtype=float)
        self.fc = np.array([params.theta_fc1, params.theta_fc2], dtype=float)
        self.wp = np.array([params.theta_wp1, params.theta_wp2], dtype=float)
        self.aer = np.array([params.theta_aer1, params.theta_aer2], dtype=float)
        self.storage = np.array(initial_theta, dtype=float) * self.z

    def get_theta(self) -> np.ndarray:
        return self.storage / self.z

    def step(
        self,
        rainfall_mm: float,
        evaporation_potential_mm: float,
        guild1_transpiration_potential_mm: float = 5.0,
        guild2_transpiration_potential_mm: float = 8.0,
        roots: tuple[float, float] = (0.3, 0.7),
        irrigation_mm: float = 0.0,
    ) -> dict[str, float]:
        p = self.params
        s_max = self.sat * self.z
        s_min = self.wp * self.z
        s0 = self.storage.copy()

        # 1. Surface infiltration and saturation-excess runoff
        water_input = float(rainfall_mm) + float(irrigation_mm)
        infil = min(water_input, max(0.0, s_max[0] - self.storage[0]))
        runoff = water_input - infil
        self.storage[0] += infil
        theta1_pre = self.storage[0] / self.z[0]
        theta2_pre = self.storage[1] / self.z[1]

        # 2. Normalized Brooks-Corey gravity drainage L1 -> L2 (0 at FC, Ksat*hardpan at Sat)
        excess1 = max(0.0, self.storage[0] - self.fc[0] * self.z[0])
        se1 = float(np.clip((theta1_pre - self.fc[0]) / (self.sat[0] - self.fc[0]), 0.0, 1.0))
        raw_d12 = p.ksat1_mm_day * (se1 ** p.drainage_shape)
        d12 = min(raw_d12 * p.hardpan_factor, excess1, max(0.0, s_max[1] - self.storage[1]))
        self.storage[0] -= d12
        self.storage[1] += d12

        # 3. Normalized Brooks-Corey deep drainage from L2
        theta2_mid = self.storage[1] / self.z[1]
        excess2 = max(0.0, self.storage[1] - self.fc[1] * self.z[1])
        se2 = float(np.clip((theta2_mid - self.fc[1]) / (self.sat[1] - self.fc[1]), 0.0, 1.0))
        raw_d2 = p.ksat2_mm_day * (se2 ** p.drainage_shape)
        d2 = min(raw_d2, excess2)
        self.storage[1] -= d2

        # 4. Midpoint moisture evaluation for stress & FAO-56 Stage 2 evaporation reduction
        theta1_eff = 0.5 * (theta1_pre + self.storage[0] / self.z[0])
        theta2_eff = 0.5 * (theta2_pre + self.storage[1] / self.z[1])
        fw1, fa1, m1 = _stress(theta1_eff, self.wp[0], self.fc[0], self.aer[0], self.sat[0])
        fw2, fa2, m2 = _stress(theta2_eff, self.wp[1], self.fc[1], self.aer[1], self.sat[1])

        qg1 = guild1_transpiration_potential_mm * m1
        qp1 = guild2_transpiration_potential_mm * roots[0] * m1
        qp2 = guild2_transpiration_potential_mm * roots[1] * m2
        ep = evaporation_potential_mm * fw1

        avail1 = max(0.0, self.storage[0] - s_min[0])
        demand1 = ep + qg1 + qp1
        alpha1 = min(1.0, avail1 / demand1) if demand1 > 0.0 else 1.0
        e_act = ep * alpha1
        ug1 = qg1 * alpha1
        up1 = qp1 * alpha1
        self.storage[0] -= (e_act + ug1 + up1)

        avail2 = max(0.0, self.storage[1] - s_min[1])
        up2 = min(qp2, avail2)
        self.storage[1] -= up2

        assert np.all(self.storage >= s_min - 1e-9), f"Storage below wilting point: {self.storage}"
        assert np.all(self.storage <= s_max + 1e-9), f"Storage above saturation: {self.storage}"

        ds = float(np.sum(self.storage - s0))
        net = water_input - runoff - d2 - e_act - ug1 - up1 - up2
        return {
            "rainfall_mm": float(rainfall_mm),
            "irrigation_mm": float(irrigation_mm),
            "runoff_mm": float(runoff),
            "drainage_l1_l2_mm": float(d12),
            "deep_drainage_mm": float(d2),
            "evaporation_mm": float(e_act),
            "evaporation_actual_mm": float(e_act),
            "guild1_uptake_mm": float(ug1),
            "groundnut_uptake_l1_mm": float(ug1),
            "guild2_uptake_l1_mm": float(up1),
            "papaya_uptake_l1_mm": float(up1),
            "guild2_uptake_l2_mm": float(up2),
            "papaya_uptake_l2_mm": float(up2),
            "fw1": fw1,
            "fa1": fa1,
            "fw2": fw2,
            "fa2": fa2,
            "mass_balance_residual_mm": float(ds - net),
        }
