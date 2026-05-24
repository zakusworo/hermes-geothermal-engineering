"""Tests for Exercise 14: Geophysical Integration."""
import pytest
try:
    from geophysical_analysis import resistivity_profile_to_salinity, identify_anomalous_zones
except ImportError:
    resistivity_profile_to_salinity = None
    identify_anomalous_zones = None


class TestGeophysical:
    def setup_method(self):
        if resistivity_profile_to_salinity is None:
            pytest.skip("geophysical_analysis not available")

    def test_resistivity_profile_length(self):
        depths = [100, 200, 300]
        res = [5.0, 2.0, 1.0]
        temps = [50, 80, 120]
        profile = resistivity_profile_to_salinity(depths, res, temps)
        assert len(profile) == 3
        assert "depth_m" in profile[0]

    def test_low_resistivity_high_salinity(self):
        depths = [100, 200]
        res = [10.0, 0.5]
        temps = [50, 50]
        profile = resistivity_profile_to_salinity(depths, res, temps)
        assert profile[1].get("estimated_salinity_psu", 0) > profile[0].get("estimated_salinity_psu", 0)

    def test_anomalous_zones_filter(self):
        profile = [
            {"depth_m": 100, "estimated_salinity_psu": 10},
            {"depth_m": 200, "estimated_salinity_psu": 35},
            {"depth_m": 300, "estimated_salinity_psu": 5},
        ]
        zones = identify_anomalous_zones(profile, 25)
        assert len(zones) == 1
        assert zones[0]["depth_m"] == 200
