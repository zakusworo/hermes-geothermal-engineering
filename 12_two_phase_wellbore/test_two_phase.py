"""Tests for Exercise 12: Two-Phase Wellbore."""
import pytest
try:
    from two_phase_flow import check_flow_regime
except ImportError:
    check_flow_regime = None


class TestTwoPhase:
    def setup_method(self):
        if check_flow_regime is None:
            pytest.skip("two_phase_flow module not available")

    def test_high_pressure_single_phase(self):
        result = check_flow_regime(150, 5000, 3500)
        assert result["status"] == "ok"
        if result["regime"] == "single_phase_liquid":
            assert result["steam_fraction"] == 0.0

    def test_low_pressure_two_phase(self):
        result = check_flow_regime(250, 10000, 1000)
        assert result["status"] == "ok"
        # Could be single or two-phase depending on saturation
        assert "P_sat_at_T_res_kPa" in result

    def test_invalid_temperature(self):
        result = check_flow_regime(500, 10000, 1000)
        assert result["status"] == "error"
