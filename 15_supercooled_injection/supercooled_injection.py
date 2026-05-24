"""Supercooled injection modeling for EGS."""
try:
    from pygeotoolbox import thermo_supercooled
except ImportError:
    thermo_supercooled = None


def cold_reinjection_energy_sink(T_injection_C, T_reservoir_C, mass_flow_kg_s):
    """
    Calculate available heat sink for reinjection.
    Assumes injection T is below reservoir T.
    Returns dict with delta_h, heat sink MW.
    """
    if thermo_supercooled is None:
        return {"status": "error", "message": "pygeotoolbox not available"}
    
    if T_injection_C > 0:
        return {"status": "error", "message": "T_injection must be ≤ 0 C for supercooled zone"}
    
    # Injection enthalpy (supercooled)
    h_inj = thermo_supercooled.enthalpy(T_injection_C, 5.0)  # MPa
    
    # Reservoir liquid enthalpy (use 0 C reference for comparison)
    # Approximate using cp=4180 J/kg/K
    h_res = 4180.0 * T_reservoir_C
    
    delta_h = h_res - h_inj
    Q_MW = (mass_flow_kg_s * delta_h) / 1e6
    
    return {
        "status": "ok",
        "T_injection_C": T_injection_C,
        "T_reservoir_C": T_reservoir_C,
        "h_inj_J_kg": round(h_inj, 1),
        "h_res_J_kg": round(h_res, 1),
        "delta_h_J_kg": round(delta_h, 1),
        "heat_sink_MW": round(Q_MW, 2),
    }


if __name__ == "__main__":
    result = cold_reinjection_energy_sink(-5, 120, 50)
    print(result)
