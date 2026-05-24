"""
Exercise 8: MCP-backed thermodynamic tool usage.
This file bridges Hermes terminal() tool to CoolProp / IAPWS live calls.
When Hermes uses a configured MCP geochem/thermo server, this module acts
as the client-side agent logic.
"""

from CoolProp.CoolProp import PropsSI, PhaseSI
from iapws import IAPWS97

def get_water_properties(T_C, P_kPa):
    """Returns dict with phase, enthalpy (kJ/kg), density (kg/m3), and sanity checks."""
    T_K = T_C + 273.15
    P_Pa = P_kPa * 1000.0
    phase = PhaseSI('T', T_K, 'P', P_Pa, 'Water')
    h_J = PropsSI('H', 'T', T_K, 'P', P_Pa, 'Water')
    rho = PropsSI('D', 'T', T_K, 'P', P_Pa, 'Water')
    sat = IAPWS97(P=P_kPa/1000.0)  # IAPWS97 expects P in MPa
    T_sat_C = sat.T - 273.15
    h = h_J / 1000.0
    checks = [
        'Temperature is within 0-374 C',
        f'Saturation temperature at {P_kPa} kPa is ~{T_sat_C:.1f} C',
        f'Given T={T_C} C is {"saturated" if abs(T_C - T_sat_C) < 0.5 else ("subcooled" if T_C < T_sat_C else "superheated")}',
        'Density positive' if rho > 0 else 'FAIL: density nonpositive',
        'Enthalpy between h_f and h_g' if h > sat.hf and h < sat.hg else 'FAIL: enthalpy outside saturation bounds',
    ]
    return {
        'T_C': T_C,
        'P_kPa': P_kPa,
        'phase': phase,
        'enthalpy_kJ_kg': round(h, 2),
        'density_kg_m3': round(rho, 2),
        'saturation_T_C': round(T_sat_C, 2),
        'sanity_checks': checks,
    }

if __name__ == '__main__':
    result = get_water_properties(200, 2000)
    for k, v in result.items():
        print(f'{k}: {v}')
