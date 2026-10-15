from simulation.mr_tests import (
    test_mr1_mass_balance_over_deterministic_sequence,
    test_mr2_drought_monotonicity,
    test_mr3_hardpan_reduces_interlayer_drainage,
    test_mr4_generator_ordering_and_aeration_margin,
    test_mr5_generator_determinism,
    test_invalid_soil_rejected,
)
from simulation.identifiability import run_screen


def test_all_metamorphic_checks():
    test_mr1_mass_balance_over_deterministic_sequence()
    test_mr2_drought_monotonicity()
    test_mr3_hardpan_reduces_interlayer_drainage()
    test_mr4_generator_ordering_and_aeration_margin()
    test_mr5_generator_determinism()
    test_invalid_soil_rejected()


def test_identifiability_screen_is_explicitly_rank_deficient():
    report = run_screen(n=64, seed=7)
    assert report["jacobian_rank"] == 1
    assert "cannot separately identify" in report["interpretation"]
