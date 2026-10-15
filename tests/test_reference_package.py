from simulation import mr_tests
from simulation.identifiability import run_screen
from simulation.agrisim_core import TwoLayerSoilWaterModel


def test_mr1_mass_balance_over_deterministic_sequence():
    mr_tests.test_mr1_mass_balance_over_deterministic_sequence()


def test_mr2_drought_monotonicity():
    mr_tests.test_mr2_drought_monotonicity()


def test_mr3_hardpan_reduces_interlayer_drainage():
    mr_tests.test_mr3_hardpan_reduces_interlayer_drainage()


def test_mr4_generator_ordering_and_aeration_margin():
    mr_tests.test_mr4_generator_ordering_and_aeration_margin()


def test_mr5_generator_determinism():
    mr_tests.test_mr5_generator_determinism()


def test_invalid_soil_rejected():
    mr_tests.test_invalid_soil_rejected()


def test_nonfinite_initial_theta_rejected():
    mr_tests.test_nonfinite_initial_theta_rejected()


def test_nonfinite_soil_parameter_rejected():
    mr_tests.test_nonfinite_soil_parameter_rejected()


def test_aeration_threshold_must_exceed_field_capacity():
    mr_tests.test_aeration_threshold_must_exceed_field_capacity()


def test_identifiability_screen_is_explicitly_rank_deficient():
    report = run_screen(n=64, seed=7)
    assert report["jacobian_rank"] == 1
    assert "cannot separately identify" in report["interpretation"]


def test_irrigation_is_explicit_and_conserves_water():
    mr_tests.test_irrigation_is_explicit_and_conserves_water()


def test_negative_irrigation_rejected():
    mr_tests.test_negative_irrigation_rejected()


def test_high_rainfall_and_irrigation_stays_bounded():
    model = TwoLayerSoilWaterModel()
    out = model.step(120, 0, 0, 0, irrigation_mm=20)
    assert abs(out["mass_balance_residual_mm"]) < 1e-8
    assert out["runoff_mm"] >= 0
    assert (model.get_theta() <= model.sat + 1e-9).all()
