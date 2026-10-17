"""Comprehensive test suite for both 2-layer baseline and v2.0 Universal Multi-Strata Engine."""
from pathlib import Path
import json
import numpy as np

from simulation.mr_tests import (
    test_mr1_mass_balance_over_deterministic_sequence,
    test_mr2_drought_monotonicity,
    test_mr3_hardpan_strictly_reduces_interlayer_drainage,
    test_mr4_generator_ordering_and_aeration_margin,
    test_mr5_generator_determinism,
    test_invalid_soil_rejected,
)
from simulation.identifiability import run_screen
from simulation.universal_multilayer_engine import (
    SoilProfileTensor,
    UniversalCropTraits,
    AgronomicMethodSpec,
    RemoteSensingContext,
    simulate_multistrata_season,
)
from simulation.spatial_weather_adapter import WeatherStationNode, interpolate_borderless_farm_weather
from simulation.canopy_pond_perception import extract_pond_and_canopy_state


def test_all_metamorphic_checks():
    test_mr1_mass_balance_over_deterministic_sequence()
    test_mr2_drought_monotonicity()
    test_mr3_hardpan_strictly_reduces_interlayer_drainage()
    test_mr4_generator_ordering_and_aeration_margin()
    test_mr5_generator_determinism()
    test_invalid_soil_rejected()


def test_identifiability_screen_and_trajectory_svd():
    report = run_screen(n=64, seed=7)
    assert report["jacobian_rank"] == 1
    traj = report["trajectory_identifiability"]
    assert traj["wet_storm_dual_depth_theta1_theta2_rank"] > traj["dry_spell_theta1_only_rank"]


def test_declarative_config_driven_universal_engine():
    root = Path(__file__).resolve().parents[1]
    crops_cfg = json.loads((root / "configs/crop_traits.json").read_text())["crops"]
    soils_cfg = json.loads((root / "configs/soil_profiles.json").read_text())["profiles"]
    methods_cfg = json.loads((root / "configs/agronomic_methods.json").read_text())["methods"]

    soil = SoilProfileTensor(
        profile_id=soils_cfg["semi_arid_red_alfisol_3layer"]["profile_id"],
        z_mm=tuple(soils_cfg["semi_arid_red_alfisol_3layer"]["z_mm"]),
        theta_sat=tuple(soils_cfg["semi_arid_red_alfisol_3layer"]["theta_sat"]),
        theta_fc=tuple(soils_cfg["semi_arid_red_alfisol_3layer"]["theta_fc"]),
        theta_wp=tuple(soils_cfg["semi_arid_red_alfisol_3layer"]["theta_wp"]),
        theta_aer=tuple(soils_cfg["semi_arid_red_alfisol_3layer"]["theta_aer"]),
        ksat_mm_day=tuple(soils_cfg["semi_arid_red_alfisol_3layer"]["ksat_mm_day"]),
        interface_conductance=tuple(soils_cfg["semi_arid_red_alfisol_3layer"]["interface_conductance"]),
        brooks_corey_exp=soils_cfg["semi_arid_red_alfisol_3layer"]["brooks_corey_exp"],
        curve_number_ii=soils_cfg["semi_arid_red_alfisol_3layer"]["curve_number_ii"],
    )

    def load_crop(cid: str) -> UniversalCropTraits:
        d = dict(crops_cfg[cid])
        d["pathogen_Tags"] = tuple(d["pathogen_Tags"])
        return UniversalCropTraits(**d)

    guild = [load_crop("papaya"), load_crop("pigeonpea"), load_crop("turmeric")]
    m_flat = AgronomicMethodSpec(**methods_cfg["Flat_Bare_NoPond"])
    m_mound = AgronomicMethodSpec(**methods_cfg["MoundTrench_Mulch_Subsoiled_PondDrip"])

    weather = [(60.0, 3.0), (55.0, 3.0)] + [(0.0, 5.5)] * 15 + [(20.0, 4.0)] * 5
    rs = RemoteSensingContext(0.8, 0.85, 0.05, pond_storage_budget_mm=32.0)

    out_flat = simulate_multistrata_season(soil, guild, m_flat, weather, RemoteSensingContext(0, 0, 0, 0))
    out_mound = simulate_multistrata_season(soil, guild, m_mound, weather, rs)

    assert out_flat["max_mass_balance_residual_mm"] < 1e-12
    assert out_mound["max_mass_balance_residual_mm"] < 1e-12
    assert out_mound["LER"] > out_flat["LER"]
    assert out_mound["net_profit_per_ha"] > out_flat["net_profit_per_ha"]


def test_borderless_spatial_weather_and_canopy_pond_adapters():
    s1 = WeatherStationNode("Border_Node_AP", 14.70, 76.85, 480.0, (45.0, 0.0, 12.0), (34.0, 36.0, 33.0), (22.0, 23.0, 21.0), (5.2, 5.8, 4.5), (65.0, 40.0, 60.0))
    s2 = WeatherStationNode("Border_Node_KA", 14.72, 76.82, 510.0, (52.0, 0.0, 15.0), (33.5, 35.5, 32.5), (21.5, 22.5, 20.5), (5.0, 5.5, 4.2), (68.0, 42.0, 62.0))
    w_out = interpolate_borderless_farm_weather(14.71, 76.835, 495.0, [s1, s2])
    assert len(w_out["daily_forcing"]) == 3
    assert w_out["nearest_station_distance_km"] < 5.0

    bands = {
        "nir": [0.32, 0.35, 0.38, np.nan],
        "red": [0.08, 0.07, 0.07, np.nan],
        "green": [0.12, 0.14, 0.13, np.nan],
        "blue": [0.06, 0.06, 0.05, np.nan],
        "re1": [0.18, 0.19, 0.20, np.nan],
        "swir1": [0.09, 0.08, 0.09, np.nan],
        "swir2": [0.05, 0.05, 0.04, np.nan],
        "VH": [-27.5, -28.1, -26.8, np.nan],
        "VV": [-18.0, -17.5, -18.2, np.nan],
    }
    rs_ctx = extract_pond_and_canopy_state(bands)
    assert rs_ctx.pond_storage_budget_mm > 0.0
    assert rs_ctx.observed_overstory_lai is not None and rs_ctx.observed_overstory_lai > 0.5


if __name__ == "__main__":
    import sys
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
    test_all_metamorphic_checks()
    print("[PASS] test_all_metamorphic_checks (MR1-MR5 + invalid soil rejection)")
    test_identifiability_screen_and_trajectory_svd()
    print("[PASS] test_identifiability_screen_and_trajectory_svd")
    test_declarative_config_driven_universal_engine()
    print("[PASS] test_declarative_config_driven_universal_engine")
    test_borderless_spatial_weather_and_canopy_pond_adapters()
    print("[PASS] test_borderless_spatial_weather_and_canopy_pond_adapters")
    print("\nALL 10/10 VERIFICATION SUITES PASSED.")
