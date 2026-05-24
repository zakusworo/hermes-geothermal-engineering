"""Tests for Exercise 15: Supercooled Injection."""
import pytest
try:
    from supercooled_injection import cold_reinjection_energy_sink
except ImportError:
    cold_reinjection_energy_sink = None


class TestSupercooledInjection:
    def setup_method(self):
        if cold_reinjection_energy_sink is None:
            pytest.skip("supercooled_injection not available")

    def test_colder_injection_greater_sink(self):
        """Colder injection T = larger heat sink."""
        r1 = cold_reinjection_energy_sink(-5, 120, 50)
        r2 = cold_reinjection_energy_sink(-10, 120, 50)
        assert r1["status"] == "ok"
        assert r2["status"] == "ok"
        assert r2["heat_sink_MW"] > r1["heat_sink_MW"]

    def test_error_above_zero(self):
        result = cold_reinjection_energy_sink(5, 120, 50)
        assert result["status"] == "error"

    def test_negative_enthalpy(self):
        result = cold_reinjection_energy_sink(-10, 120, 50)
        assert result["h_inj_J_kg"] < 0

    def test_heat_increases_with_flow(self):
        r1 = cold_reinjection_energy_sink(-10, 120, 20)
        r2 = cold_reinjection_energy_sink(-10, 120, 40)
        assert r2["heat_sink_MW"] > r1["heat_sink_MW"]
