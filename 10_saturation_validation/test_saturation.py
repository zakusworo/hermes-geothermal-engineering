"""Tests for Exercise 10: IAPWS Saturation Validation."""
import pytest
try:
    from pygeotoolbox import siapws_saturation
except ImportError:
    siapws_saturation = None


class TestSaturationValidation:
    def setup_method(self):
        if siapws_saturation is None:
            pytest.skip("pygeotoolbox not available")

    def test_triple_point(self):
        T = siapws_saturation.saturation_temperature(0.611657)
        assert T is not None
        assert abs(T - 0.01) < 0.001

    def test_one_atm(self):
        T = siapws_saturation.saturation_temperature(101.325)
        assert T is not None
        assert 99.9 < T < 100.1

    def test_critical_point(self):
        T = siapws_saturation.saturation_temperature(22064.0)
        assert abs(T - 373.946) < 0.01

    def test_roundtrip(self):
        for P in [500, 5000, 15000]:
            T = siapws_saturation.saturation_temperature(P)
            if T:
                P_back = siapws_saturation.saturation_pressure(T)
                rel_err = abs(P_back - P) / P
                assert rel_err < 0.01

    def test_steam_quality_liquid(self):
        try:
            from pygeotoolbox import thermo
            x = thermo.steam_quality_from_enthalpy(
                thermo.enthalpy_from_TP(200, 1000), 1000
            )
            assert x == 0.0
        except ImportError:
            pytest.skip()
