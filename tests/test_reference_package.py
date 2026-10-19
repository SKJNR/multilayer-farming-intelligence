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


def test_agronomic_sat_solver_and_soft_sensor():
    from simulation.realtime_sat_edge_advisor import AgronomicSATSolver, parse_farmer_text_zero_llm_cost
    from simulation.multimodal_video_soft_sensor import verify_youtube_yield_claim_against_physics

    root = Path(__file__).resolve().parents[1]
    crops_cfg = json.loads((root / "configs/crop_traits.json").read_text())["crops"]
    methods_cfg = json.loads((root / "configs/agronomic_methods.json").read_text())["methods"]

    def load_crop(cid: str) -> UniversalCropTraits:
        d = dict(crops_cfg[cid])
        d["pathogen_Tags"] = tuple(d["pathogen_Tags"])
        return UniversalCropTraits(**d)

    traits_map = {cid: load_crop(cid) for cid in crops_cfg}
    methods_map = {mid: AgronomicMethodSpec(**methods_cfg[mid]) for mid in methods_cfg}
    solver = AgronomicSATSolver(traits_map, methods_map)

    # 1. Unviable: Papaya + Chilli on Flat land with storm ponding (shares Phytophthora and violates mound implication)
    res_bad = solver.verify_assignment(
        ("papaya", "chilli"), "Flat_Bare_NoPond", waterlogging_hours=30.0, require_legume=False, max_budget_per_ha=200000.0
    )
    assert not res_bad.satisfiable
    assert any("C2_PATHOGEN_CLAUSE" in v for v in res_bad.violated_clauses)
    assert any("C4_HYPOXIA_IMPLICATION" in v for v in res_bad.violated_clauses)

    # 2. Viable: Papaya + Pigeonpea + Turmeric on Mound+Trench
    res_good = solver.verify_assignment(
        ("papaya", "pigeonpea", "turmeric"),
        "MoundTrench_Mulch_Subsoiled_PondDrip",
        waterlogging_hours=30.0,
        require_legume=True,
        max_budget_per_ha=250000.0,
    )
    assert res_good.satisfiable
    assert any("IMP_MOUND_TRENCH" in imp for imp in res_good.active_implications)

    # 3. Physics hype filter test: 45 t/ha biomass on 350 mm transpiration exceeds water ceiling
    claim = verify_youtube_yield_claim_against_physics(45000.0, 350.0)
    assert not claim["physically_plausible"]
    assert claim["assigned_evidence_class"] == "REJECTED_PROMOTIONAL_OUTLIER"

    # 4. Zero-LLM-cost text parser test with explicit crop detection
    ctx = parse_farmer_text_zero_llm_cost("I have papaya and groundnut on flat land, water stands 24 hours after rain")
    assert "papaya" in ctx.detected_existing_crops
    assert ctx.reported_waterlogging_hours_after_storm == 24.0


def test_negation_and_unknown_slot_handling():
    from simulation.realtime_sat_edge_advisor import parse_farmer_text_zero_llm_cost

    # A. Negation: "no pond" must NOT evaluate to True
    ctx_neg = parse_farmer_text_zero_llm_cost("I have red sandy soil, no pond, rainfed only, what can I grow?")
    assert ctx_neg.has_farm_pond_or_borewell is False
    assert len(ctx_neg.detected_existing_crops) == 0
    assert "current_crops_or_varieties" in ctx_neg.unknown_critical_slots

    # B. Explicit pond/borewell with budget parsing
    ctx_pos = parse_farmer_text_zero_llm_cost("I grow pigeonpea with borewell and drip irrigation, budget: Rs. 150,000")
    assert ctx_pos.has_farm_pond_or_borewell is True
    assert "pigeonpea" in ctx_pos.detected_existing_crops
    assert ctx_pos.max_budget_per_ha == 150000.0

    # C. Ambiguous / Unknown: missing pond remains None (unknown)
    ctx_unk = parse_farmer_text_zero_llm_cost("I have flat 3 acres of land, recommend crops")
    assert ctx_unk.has_farm_pond_or_borewell is None
    assert "irrigation_or_pond_access" in ctx_unk.unknown_critical_slots


def test_ler_scientific_soundness_and_monocrop_identity():
    root = Path(__file__).resolve().parents[1]
    crops_cfg = json.loads((root / "configs/crop_traits.json").read_text())["crops"]
    soils_cfg = json.loads((root / "configs/soil_profiles.json").read_text())["profiles"]
    methods_cfg = json.loads((root / "configs/agronomic_methods.json").read_text())["methods"]

    soil = SoilProfileTensor(
        profile_id="test",
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
    c_gn = UniversalCropTraits(**crops_cfg["groundnut"])
    method_flat = AgronomicMethodSpec(**methods_cfg["Flat_Bare_NoPond"])
    weather = [(0.0, 5.0)] * 30 + [(25.0, 4.0)] + [(0.0, 5.5)] * 29

    # 1. Monocrop Identity: Unstressed sole crop LER equals 1.000 (potential baseline)
    weather_ideal = [(8.0, 3.5)] * 60
    res_mono = simulate_multistrata_season(soil, [c_gn], method_flat, weather_ideal)
    assert abs(res_mono["LER"] - 1.0) < 1e-3
    assert res_mono["per_crop_breakdown"][0]["partial_ler"] <= 1.0
    assert res_mono["ler_evidence_class"] == "ILLUSTRATIVE_SIMULATION_CALIBRATION_PENDING"

    # 2. Multicrop LER must strictly equal sum of individual partial LERs
    c_pp = UniversalCropTraits(**crops_cfg["pigeonpea"])
    res_multi = simulate_multistrata_season(soil, [c_gn, c_pp], method_flat, weather)
    sum_partials = sum(p["partial_ler"] for p in res_multi["per_crop_breakdown"])
    assert abs(res_multi["LER"] - round(sum_partials, 3)) < 1e-4


def test_particle_filter_joint_likelihood_and_state_alignment():
    from simulation.multimodal_video_soft_sensor import VideoFrameBioAssay, ZeroHardwareSoftSensorAssimilator

    assimilator = ZeroHardwareSoftSensorAssimilator(n_particles=60, seed=123)
    bio = VideoFrameBioAssay(
        visual_topsoil_wetness_theta1=0.22,
        topsoil_obs_std=0.03,
        visual_canopy_turgor_score=0.75,
        turgor_obs_std=0.08,
    )
    # Joint assimilation of both SAR and video bio-assay
    out = assimilator.step_and_assimilate(
        rain_mm=10.0,
        et0_mm=5.0,
        sar_surface_theta1_obs=0.20,
        video_bio_assay=bio,
    )
    assert 0.10 <= out["theta1_mean"] <= 0.44
    assert 0.10 <= out["theta2_mean"] <= 0.44
    assert 2.0 <= out["ksat_hardpan_mean"] <= 80.0


def test_zero_pond_perception_and_evidence_tag():
    from simulation.canopy_pond_perception import extract_pond_and_canopy_state

    dummy_bands = {
        "nir": [0.35] * 12, "red": [0.12] * 12, "green": [0.15] * 12,
        "blue": [0.08] * 12, "re1": [0.22] * 12, "swir1": [0.18] * 12,
        "swir2": [0.10] * 12, "VH": [-18.0] * 12, "VV": [-12.0] * 12,
    }
    # Case with zero pond area must strictly return 0.0 budget
    rs_no_pond = extract_pond_and_canopy_state(dummy_bands, pond_area_m2=0.0)
    assert rs_no_pond.pond_storage_budget_mm == 0.0
    assert rs_no_pond.evidence_status == "NO_POND_ZERO_STORAGE"


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
    test_agronomic_sat_solver_and_soft_sensor()
    print("[PASS] test_agronomic_sat_solver_and_soft_sensor")
    test_negation_and_unknown_slot_handling()
    print("[PASS] test_negation_and_unknown_slot_handling")
    test_ler_scientific_soundness_and_monocrop_identity()
    print("[PASS] test_ler_scientific_soundness_and_monocrop_identity")
    test_particle_filter_joint_likelihood_and_state_alignment()
    print("[PASS] test_particle_filter_joint_likelihood_and_state_alignment")
    test_zero_pond_perception_and_evidence_tag()
    print("[PASS] test_zero_pond_perception_and_evidence_tag")
    print("\nALL 15/15 VERIFICATION SUITES PASSED.")
