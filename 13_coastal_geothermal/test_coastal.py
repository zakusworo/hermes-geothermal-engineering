"""Tests for Exercise 13: Coastal Geothermal."""
import pytest
try:
    from coastal_evaluation import evaluate_seawater_geothermal
except ImportError:
    evaluate_seawater_geothermal = None


class TestCoastal:
    def setup_method(self):
        if evaluate_seawater_geothermal is None:
            pytest.skip("coastal_evaluation not available")

    def test_seawater_higher_density(self):
        r_sw = evaluate_seawater_geothermal(15, 120, 35, 100)
        assert r_sw["status"] == "ok"
        assert r_sw["rho_kg_m3"] > 1020

    def test_heat_increases_with_flow(self):
        r1 = evaluate_seawater_geothermal(15, 120, 35, 50)
        r2 = evaluate_seawater_geothermal(15, 120, 35, 100)
        assert r2["heat_extraction_MW"] > r1["heat_extraction_MW"]

    def test_invalid_salinity(self):
        r = evaluate_seawater_geothermal(15, 120, 50, 100)
        assert r["status"] == "error"
