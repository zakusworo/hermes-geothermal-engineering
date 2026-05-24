"""Geophysical integration: resistivity to salinity via pygeotoolbox."""
try:
    from pygeotoolbox import geophysics
except ImportError:
    geophysics = None


def resistivity_profile_to_salinity(depths_m, resistivities, T_C_profile):
    """
    Convert resistivity log to estimated salinity profile.
    Args:
        depths_m: list of depths
        resistivities: list of resistivity values (ohm·m)
        T_C_profile: list of temperatures at each depth
    Returns:
        list of dict with depth, resistivity, estimated salinity
    """
    if geophysics is None:
        return [{"depth": d, "status": "error"} for d in depths_m]
    
    results = []
    for d, rho, T in zip(depths_m, resistivities, T_C_profile):
        sal = geophysics.salinity_from_resistivity(rho, T)
        results.append({
            "depth_m": d,
            "resistivity_ohm_m": rho,
            "temperature_C": T,
            "estimated_salinity_psu": sal.get("salinity_estimated_psu") if sal.get("status") == "ok" else None,
            "conductivity_S_m": round(geophysics.resistivity_from_conductivity(rho) if rho > 0 else float('inf'), 6),
        })
    return results


def identify_anomalous_zones(results, threshold_salinity_psu=30):
    """Identify zones with salinity above threshold."""
    anomalous = []
    for r in results:
        s = r.get("estimated_salinity_psu")
        if s and s > threshold_salinity_psu:
            anomalous.append(r)
    return anomalous


if __name__ == "__main__":
    # Demo: resistivity log for typical coastal geothermal
    depths = [100, 200, 300, 400, 500, 600]
    res = [5.0, 4.5, 1.2, 0.8, 2.0, 5.5]  # ohm·m — low at 300-400 m = saline
    temps = [40, 60, 80, 100, 120, 140]
    
    profile = resistivity_profile_to_salinity(depths, res, temps)
    for p in profile:
        print(f"{p['depth_m']}m: rho={p['resistivity_ohm_m']}, S_est={p['estimated_salinity_psu']}")
    
    anomalies = identify_anomalous_zones(profile, 25)
    print(f"Anomalous zones (S > 25 psu): {len(anomalies)}")
    for a in anomalies:
        print(f"  {a['depth_m']} m: S~{a['estimated_salinity_psu']:.1f} psu")
