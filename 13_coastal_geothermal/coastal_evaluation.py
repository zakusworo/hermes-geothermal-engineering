"""Seawater geothermal evaluation using pygeotoolbox."""
try:
    from pygeotoolbox import seawater
except ImportError:
    seawater = None


def evaluate_seawater_geothermal(T_surface_C, T_reservoir_C, salinity_psu, mass_flow_kg_s):
    """
    Evaluate seawater geothermal potential.
    Returns dict with density, delta_T, heat extraction estimate.
    """
    if seawater is None:
        return {"status": "error", "message": "pygeotoolbox not available"}
    
    dens = seawater.seawater_density(T_surface_C, salinity_psu)
    if dens.get("status") != "ok":
        return {"status": "error", "message": "Density calculation failed"}
    
    rho = dens["rho_kg_m3"]
    delta_T = T_reservoir_C - T_surface_C

    # Heat extraction ~ m_dot * cp * delta_T
    cp = 4000.0  # J/kg/K (approx for seawater, slightly lower than freshwater)
    Q_MW = (mass_flow_kg_s * cp * delta_T) / 1e6
    
    return {
        "status": "ok",
        "T_surface_C": T_surface_C,
        "T_reservoir_C": T_reservoir_C,
        "salinity_psu": salinity_psu,
        "rho_kg_m3": rho,
        "delta_T_C": delta_T,
        "heat_extraction_MW": round(Q_MW, 3),
    }


if __name__ == "__main__":
    result = evaluate_seawater_geothermal(15, 120, 35, 100)
    print(result)
