"""Deterministic metamorphic/regression tests (MR1-MR5)."""
from __future__ import annotations
import numpy as np
from .agrisim_core import SoilParameters, TwoLayerSoilWaterModel
from .soil_generator import generate_soil_priors


def test_mr1_mass_balance_over_deterministic_sequence() -> None:
    model = TwoLayerSoilWaterModel()
    weather = [(0, 4), (10, 4), (120, 2), (0, 5), (0, 5), (15, 3)]
    for p, e in weather:
        out = model.step(p, e, 5, 8, (0.3, 0.7))
        assert abs(out["mass_balance_residual_mm"]) < 1e-12
        assert np.all(model.storage >= model.wp * model.z - 1e-9)
        assert np.all(model.storage <= model.sat * model.z + 1e-9)


def test_mr2_drought_monotonicity() -> None:
    low_demand = TwoLayerSoilWaterModel(initial_theta=(0.30, 0.30))
    high_demand = TwoLayerSoilWaterModel(initial_theta=(0.30, 0.30))
    for _ in range(5):
        low_demand.step(0, 0, 0, 0)
        high_demand.step(0, 10, 10, 10)
    assert np.all(high_demand.storage <= low_demand.storage + 1e-9)


def test_mr3_hardpan_strictly_reduces_interlayer_drainage() -> None:
    base = dict(z1_mm=300, z2_mm=500, theta_sat1=.45, theta_sat2=.45,
                theta_fc1=.25, theta_fc2=.25, theta_wp1=.10, theta_wp2=.10,
                theta_aer1=.35, theta_aer2=.35, ksat1_mm_day=50,
                ksat2_mm_day=20)
    low = TwoLayerSoilWaterModel(SoilParameters(**base, hardpan_factor=.2), initial_theta=(.42, .25))
    high = TwoLayerSoilWaterModel(SoilParameters(**base, hardpan_factor=.9), initial_theta=(.42, .25))
    out_low = low.step(0, 0, 0, 0)
    out_high = high.step(0, 0, 0, 0)
    assert out_low["drainage_l1_l2_mm"] < out_high["drainage_l1_l2_mm"]


def test_mr4_generator_ordering_and_aeration_margin() -> None:
    soils = generate_soil_priors(512, seed=123)
    for s in soils:
        assert abs(s["sand_fraction"] + s["silt_fraction"] + s["clay_fraction"] - 1) < 1e-12
        assert 0 < s["theta_wp"] < s["theta_fc"] < s["theta_aer"] < s["theta_sat"] <= 1
        assert s["theta_sat"] - s["theta_fc"] >= 0.08 - 1e-12


def test_mr5_generator_determinism() -> None:
    assert generate_soil_priors(10, seed=42) == generate_soil_priors(10, seed=42)


def test_invalid_soil_rejected() -> None:
    try:
        TwoLayerSoilWaterModel(SoilParameters(theta_fc1=.50))
    except ValueError:
        return
    raise AssertionError("invalid hydraulic ordering should fail")
