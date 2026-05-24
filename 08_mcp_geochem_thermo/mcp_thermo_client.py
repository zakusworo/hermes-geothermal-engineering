"""
Exercise 8: MCP-backed thermodynamic tool usage.
This file bridges Hermes terminal() tool to CoolProp / IAPWS live calls.
"""

from CoolProp.CoolProp import PropsSI, PhaseSI
from iapws import IAPWS97


def get_water_properties(T_C, P_kPa):
    """Returns dict with phase, enthalpy (kJ/kg), density (kg/m3), and sanity checks."""
    T_K = T_C + 273.15
    P_Pa = P_kPa * 1000.0
    P_MPa = P_kPa / 1000.0
    phase = PhaseSI('T', T_K,              'P', P_Pa, 'Water')
    h_J   = PropsSI('H', 'T', T_K,  'P', P_Pa, 'Water')
    rho   = PropsSI('D', 'T', T_K, 'P', P_Pa, 'Water')
    h = h_J / 1000.0

    # Saturation properties at this pressure
    try:
        sat = IAPWS97(P=P_MPa)
        if sat is None or getattr(sat, 'T', None) is None:
            raise ValueError("IAPWS97 returned None for this pressure")
        T_sat_C = sat.T - 273.15
        h_f = sat.hf
        h_g = sat.hg
        is_saturated = abs(T_C - T_sat_C) < 0.5
        phase_desc = (
            'saturated'
            if is_saturated
            else ('subcooled' if T_C < T_sat_C else 'superheated')
        )
        h_check = (
            'Enthalpy between h_f and h_g'
            if h_f < h < h_g
            else f'Enthalpy {h:.1f} outside [{h_f:.1f}, {h_g:.1f}]'
        )
    except (ValueError, Exception):
        T_sat_C = None
        phase_desc = 'single-phase (IAPWS97 saturation infeasible at this P)'
        h_check = 'N/A'

    checks = [
        f'Temperature in range: {0 <= T_C <= 374}',
        (
            f'Saturation T at {P_kPa} kPa: ~{T_sat_C:.1f} C'
            if T_sat_C is not None
            else f'Saturation not defined at {P_kPa} kPa'
        ),
        f'T={T_C} C is {phase_desc}',
        'Density positive' if rho > 0 else 'FAIL: density nonpositive',
        h_check,
    ]

    return {
        'T_C': T_C,
        'P_kPa': P_kPa,
        'phase': phase,
        'enthalpy_kJ_kg': round(h, 2),
        'density_kg_m3': round(rho, 2),
        'saturation_T_C': round(T_sat_C, 2) if T_sat_C is not None else 'N/A',
        'sanity_checks': checks,
    }


if __name__ == '__main__':
    scenarios = [
        (200, 2000),   # subcooled liquid
        (250, 2500),   # two-phase
        (300, 500),    # superheated vapor
    ]
    for T_C, P_kPa in scenarios:
        print(f'\n--- T={T_C} C, P={P_kPa} kPa ---')
        result = get_water_properties(T_C, P_kPa)
        for k, v in result.items():
            print(f'  {k}: {v}')
