"""Auditable two-layer soil-water balance prototype.

This is a new audit candidate, not a reconstruction of the missing historical
``agrisim_core.py``. Units: depths and water fluxes are mm per daily step;
volumetric water contents are m3/m3; Ksat is mm/day. Fluxes are evaluated in
an explicitly documented sequence to avoid ambiguous operator splitting.

This model is a research prototype, not a field-calibrated crop recommendation
engine. It omits lateral flow, capillary rise, preferential flow, dynamic roots,
and a mechanistic hydraulic conductivity curve.
"""
from __future__ import annotations
from dataclasses import dataclass, asdict
from typing import Any
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
    drainage_shape: float = 5.0

    def validate(self) -> None:
        if self.z1_mm <= 0 or self.z2_mm <= 0:
            raise ValueError("Layer depths must be positive")
        for i in (1, 2):
            sat = getattr(self, f"theta_sat{i}")
            fc = getattr(self, f"theta_fc{i}")
            wp = getattr(self, f"theta_wp{i}")
            aer = getattr(self, f"theta_aer{i}")
            if not (0 <= wp < fc < sat <= 1):
                raise ValueError(f"Layer {i} must satisfy 0 <= theta_wp < theta_fc < theta_sat <= 1")
            if not (wp < aer < sat):
                raise ValueError(f"Layer {i} theta_aer must be between theta_wp and theta_sat")
        if self.ksat1_mm_day < 0 or self.ksat2_mm_day < 0:
            raise ValueError("Ksat cannot be negative")
        if not 0 <= self.hardpan_factor <= 1:
            raise ValueError("hardpan_factor must be in [0, 1]")
        if self.drainage_shape < 0:
            raise ValueError("drainage_shape must be non-negative")


class TwoLayerSoilWaterModel:
    """Daily two-layer bucket model with explicit flux order.

    Sequence per step: (1) add rainfall to layer 1 up to saturation and assign
    overflow to runoff; (2) drain layer 1 above field capacity to layer 2,
    limited by Ksat/hardpan and receiver capacity; (3) drain layer 2 above FC;
    (4) compute stress from the post-rain/post-drain state; (5) allocate layer-1
    available water proportionally across E, groundnut uptake and papaya uptake;
    (6) allocate layer-2 water to papaya. Lower bounds are protected by capping
    uptake to water above wilting point. Each step returns a mass-balance residual.
    """
    def __init__(self, soil: SoilParameters | None = None, initial_theta: tuple[float, float] | None = None):
        self.soil = soil or SoilParameters()
        self.soil.validate()
        self.z = np.array([self.soil.z1_mm, self.soil.z2_mm], dtype=float)
        self.wp = np.array([self.soil.theta_wp1, self.soil.theta_wp2], dtype=float)
        self.fc = np.array([self.soil.theta_fc1, self.soil.theta_fc2], dtype=float)
        self.sat = np.array([self.soil.theta_sat1, self.soil.theta_sat2], dtype=float)
        self.aer = np.array([self.soil.theta_aer1, self.soil.theta_aer2], dtype=float)
        self.ksat = np.array([self.soil.ksat1_mm_day, self.soil.ksat2_mm_day], dtype=float)
        theta = np.array(initial_theta if initial_theta is not None else self.fc, dtype=float)
        if theta.shape != (2,) or np.any(theta < self.wp) or np.any(theta > self.sat):
            raise ValueError("initial_theta must be two values within [theta_wp, theta_sat]")
        self.storage = theta * self.z

    def get_theta(self) -> np.ndarray:
        return self.storage / self.z

    @staticmethod
    def _stress(theta: float, wp: float, fc: float, aer: float, sat: float) -> tuple[float, float]:
        fw = 1.0 if theta >= fc else (0.0 if theta <= wp else (theta - wp) / (fc - wp))
        fa = 1.0 if theta <= aer else (0.0 if theta >= sat else (sat - theta) / (sat - aer))
        return float(np.clip(fw, 0, 1)), float(np.clip(fa, 0, 1))

    def step(self, rainfall_mm: float, evaporation_potential_mm: float,
             groundnut_transpiration_potential_mm: float,
             papaya_transpiration_potential_mm: float,
             papaya_root_fraction: tuple[float, float] = (0.3, 0.7)) -> dict[str, Any]:
        inputs = [rainfall_mm, evaporation_potential_mm, groundnut_transpiration_potential_mm,
                  papaya_transpiration_potential_mm, *papaya_root_fraction]
        if not all(np.isfinite(x) for x in inputs):
            raise ValueError("All inputs must be finite")
        if min(inputs[:4]) < 0:
            raise ValueError("Rainfall and potential demands must be non-negative")
        roots = np.asarray(papaya_root_fraction, dtype=float)
        if roots.shape != (2,) or np.any(roots < 0) or roots.sum() <= 0:
            raise ValueError("papaya_root_fraction must contain two non-negative values with positive sum")
        roots = roots / roots.sum()
        old_total = float(self.storage.sum())
        smax = self.sat * self.z
        smin = self.wp * self.z

        # 1. Infiltration and runoff.
        infil = min(float(rainfall_mm), max(0.0, smax[0] - self.storage[0]))
        runoff = float(rainfall_mm) - infil
        self.storage[0] += infil

        # 2. Drainage from layer 1 to layer 2; receiver capacity is explicit.
        theta = self.get_theta()
        excess1 = max(0.0, self.storage[0] - self.fc[0] * self.z[0])
        raw_d12 = self.ksat[0] * np.exp(self.soil.drainage_shape * max(0.0, theta[0] - self.fc[0]))
        d12 = min(float(raw_d12 * self.soil.hardpan_factor), excess1,
                   max(0.0, smax[1] - self.storage[1]))
        self.storage[0] -= d12
        self.storage[1] += d12

        # 3. Deep drainage from layer 2.
        theta = self.get_theta()
        excess2 = max(0.0, self.storage[1] - self.fc[1] * self.z[1])
        raw_d2 = self.ksat[1] * np.exp(self.soil.drainage_shape * max(0.0, theta[1] - self.fc[1]))
        d2 = min(float(raw_d2), excess2)
        self.storage[1] -= d2

        # 4. Stress modifiers and demand; 5. shared layer-1 water pool.
        theta = self.get_theta()
        fw1, fa1 = self._stress(theta[0], self.wp[0], self.fc[0], self.aer[0], self.sat[0])
        fw2, fa2 = self._stress(theta[1], self.wp[1], self.fc[1], self.aer[1], self.sat[1])
        qg1 = float(groundnut_transpiration_potential_mm) * fw1 * fa1
        qp1 = float(papaya_transpiration_potential_mm) * roots[0] * fw1 * fa1
        qp2 = float(papaya_transpiration_potential_mm) * roots[1] * fw2 * fa2
        ep = float(evaporation_potential_mm)
        available1 = max(0.0, self.storage[0] - smin[0])
        demand1 = ep + qg1 + qp1
        alpha1 = min(1.0, available1 / demand1) if demand1 > 0 else 1.0
        e_actual, ug1, up1 = ep * alpha1, qg1 * alpha1, qp1 * alpha1
        self.storage[0] -= e_actual + ug1 + up1

        # 6. Layer-2 papaya uptake, capped to water above wilting point.
        available2 = max(0.0, self.storage[1] - smin[1])
        up2 = min(qp2, available2)
        self.storage[1] -= up2
        self.storage = np.clip(self.storage, smin, smax)
        new_total = float(self.storage.sum())
        outputs = e_actual + ug1 + up1 + up2 + d2 + runoff
        residual = old_total + float(rainfall_mm) - new_total - outputs
        return {
            "runoff_mm": runoff, "evaporation_actual_mm": e_actual,
            "groundnut_uptake_l1_mm": ug1, "papaya_uptake_l1_mm": up1,
            "papaya_uptake_l2_mm": up2, "drainage_l1_l2_mm": d12,
            "deep_drainage_mm": d2, "theta1": float(self.get_theta()[0]),
            "theta2": float(self.get_theta()[1]), "storage_mm": self.storage.copy(),
            "mass_balance_residual_mm": float(residual),
            "evidence_class": "Synthetic_Model_Output",
        }

    def state(self) -> dict[str, Any]:
        return {"soil": asdict(self.soil), "storage_mm": self.storage.tolist(),
                "theta": self.get_theta().tolist(), "evidence_class": "Synthetic_Model_State"}
