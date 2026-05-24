"""Tests for Exercise 11: Transport Property Verification."""
import pytest
try:
    from pygeotoolbox import transport
except ImportError:
    transport = None


class TestTransportVerification:
    def setup_method(self):
        if transport is None:
            pytest.skip("pygeotoolbox not available")

    def test_thermal_conductivity_ambient(self):
        k = transport.thermal_conductivity(25, 101.325)
        assert k is not None
        assert 0.55 < k < 0.65

    def test_viscosity_liquid_order(self):
        mu_25 = transport.dynamic_viscosity(25, 101.325)
        mu_80 = transport.dynamic_viscosity(80, 101.325)
        assert mu_80 < mu_25

    def test_prandtl_decreases_with_temp(self):
        props_50 = transport.transport_properties(50, 500)
        props_150 = transport.transport_properties(150, 500)
        assert props_150["Pr"] < props_50["Pr"]

    def test_steam_properties_range(self):
        k = transport.thermal_conductivity(500, 10000)
        mu = transport.dynamic_viscosity(500, 10000)
        assert 0.02 < k < 0.15
        assert mu < 5e-5

    def test_liquid_vs_gas(self):
        k_liq = transport.thermal_conductivity(200, 2000)
        k_gas = transport.thermal_conductivity(500, 2000)
        assert k_liq > k_gas
