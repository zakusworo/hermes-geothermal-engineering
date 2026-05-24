"""Two-phase wellbore flow model using pygeotoolbox IAPWS saturation."""
try:
    from pygeotoolbox import siapws_saturation, thermo
except ImportError:
    siapws_saturation = None
    thermo = None


def check_flow_regime(T_res_C, P_wf_kPa, P_wh_kPa):
    """
    Determine if wellbore flow is single-phase or two-phase.
    Returns dict with regime, P_sat_kPa, and steam fraction estimate.
    """
    if siapws_saturation is None or thermo is None:
        return {"status": "error", "message": "pygeotoolbox not available"}
    
    P_sat = siapws_saturation.saturation_pressure(T_res_C)
    if P_sat is None:
        return {"status": "error", "message": "T out of IAPWS range"}
    
    # P_wh is passed as argument but needs to be compared to saturation pressure at reservoir T
    if P_wh_kPa > P_sat:
        # Wellhead pressure above saturation: single-phase
        return {
            "status": "ok",
            "regime": "single_phase_liquid",
            "P_sat_at_T_res_kPa": round(P_sat, 3),
            "steam_fraction": 0.0,
        }
    else:
        # Two-phase: estimate steam fraction using enthalpy
        h_res = thermo.enthalpy_from_TP(T_res_C, P_wf_kPa)
        # Simplified: at wellhead, flash to saturation
        T_sat = siapws_saturation.saturation_temperature(P_wh_kPa)
        if T_sat:
            h_l = thermo.enthalpy_from_TP(T_sat, P_wh_kPa)  # approx liquid
            # Very rough steam fraction
            h_v = 2.8e6  # J/kg, rough steam enthalpy
            if h_v > h_l:
                x_est = max(0, min(1, (h_res - h_l) / (h_v - h_l)))
            else:
                x_est = 0
            return {
                "status": "ok",
                "regime": "two_phase",
                "P_sat_at_T_res_kPa": round(P_sat, 3),
                "T_sat_at_P_wh_C": round(T_sat, 2),
                "steam_fraction_estimate": round(x_est, 4),
            }
        return {"status": "error", "message": "Cannot determine saturation at wellhead"}


if __name__ == "__main__":
    # Demo: typical geothermal well
    print(check_flow_regime(200, 8000, 1500))   # likely two-phase
    print(check_flow_regime(150, 5000, 3000))   # likely single-phase
