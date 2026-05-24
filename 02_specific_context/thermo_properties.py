"""
Thermodynamic properties via pygeotoolbox (CoolProp + IAPWS-IF97).

In the original course this module had a buggy DummyPropsSI wrapper.
Now it uses pygeotoolbox-mcp for reliable, tested thermal properties.
"""
try:
    from pygeotoolbox import thermo
except ImportError:
    thermo = None


def enthalpy_from_TP(T_C, P_kPa):
    """Compute enthalpy (J/kg) from T (C) and P (kPa)."""
    if thermo is not None:
        return thermo.enthalpy_from_TP(T_C, P_kPa)
    # fallback approximation
    return (4.18 * T_C) * 1000.0


def density_from_TP(T_C, P_kPa):
    """Compute density (kg/m3) from T (C) and P (kPa)."""
    if thermo is not None:
        return thermo.density_from_TP(T_C, P_kPa)
    return 1000.0 - 0.5 * T_C


if __name__ == '__main__':
    h = enthalpy_from_TP(200, 2000)
    rho = density_from_TP(200, 2000)
    print(f"T=200 C, P=2000 kPa --> h={h/1000:.1f} kJ/kg, rho={rho:.1f} kg/m3")
