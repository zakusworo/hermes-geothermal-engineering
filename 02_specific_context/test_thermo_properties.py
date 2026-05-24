"""Tests for Exercise 2: thermodynamic state (IAPWS/enthalpy)."""
try:
    from pygeotoolbox import thermo
    PropsSI = thermo.PropsSI if hasattr(thermo, 'PropsSI') else None
except ImportError:
    thermo = None
    PropsSI = None

from thermo_properties import enthalpy_from_TP, density_from_TP

def test_density_positive():
    rho = density_from_TP(150, 2000)
    assert rho > 0, f"Density negative: {rho}"

def test_known_value_200C_2MPa():
    """
    At 200 C (473.15 K) and 2 MPa (2000 kPa), IAPWS-IF97 gives:
    h ~ 852.4 kJ/kg, rho ~ 864.7 kg/m3 (single-phase liquid, Tsat at 2 MPa ~ 212.4 C).
    This test WILL FAIL with the current buggy DummyPropsSI implementation,
    and should pass after replacing DummyPropsSI with real CoolProp.
    """
    h = enthalpy_from_TP(200, 2000)
    rho = density_from_TP(200, 2000)
    # Known reference values (rounded)
    assert abs(h / 1000.0 - 852.4) < 5.0, f"Enthalpy {h/1000:.1f} kJ/kg far from expected 852.4 kJ/kg"
    assert abs(rho - 864.7) < 10.0, f"Density {rho:.1f} far from expected 864.7 kg/m3"

def test_monotonic_enthalpy_increases_with_T():
    """At constant pressure, enthalpy must increase with temperature in single-phase region."""
    P = 1500  # kPa
    T_values = [120, 140, 160, 180]
    h_values = [enthalpy_from_TP(T, P) for T in T_values]
    for i in range(len(h_values) - 1):
        assert h_values[i+1] > h_values[i], "Enthalpy did not monotonically increase with T"

def test_invalid_input_rejected():
    """Negative temperature must be rejected."""
    try:
        enthalpy_from_TP(-5, 2000)
        assert False, "Should have raised ValueError for negative temperature"
    except (ValueError, AssertionError):
        pass

    try:
        enthalpy_from_TP(100, -100)
        assert False, "Should have raised ValueError for negative pressure"
    except (ValueError, AssertionError):
        pass
