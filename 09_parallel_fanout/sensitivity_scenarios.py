"""
Exercise 9: Parallel sensitivity via delegate_task.
Three independent scenarios computed in separate functions,
ready to be spawned across Hermes subagents.

Each function returns structured dict for aggregation.
"""

def scenario_drawdown(reservoir_pressure_initial_kPa, productivity_index_kg_s_kPa,
                        years=10, annual_growth_rate_kPa=5):
    """Compute reservoir pressure drawdown over time."""
    pressures = [reservoir_pressure_initial_kPa - annual_growth_rate_kPa * y for y in range(years+1)]
    return {
        'scenario': 'drawdown',
        'years': years,
        'initial_P_kPa': reservoir_pressure_initial_kPa,
        'final_P_kPa': pressures[-1],
        'pressure_series_kPa': pressures,
    }

def scenario_injectivity(well_count, injectivity_index_kg_s_kPa, makeup_mass_fraction=0.1,
                          reservoir_volume_m3=1e9, recharge_rate_kg_s=100):
    """Compute time to replace X % of reservoir volume via makeup injection."""
    total_inject = well_count * injectivity_index_kg_s_kPa * 100  # rough placeholder
    years_to_fill = (reservoir_volume_m3 * makeup_mass_fraction) / (total_inject + recharge_rate_kg_s) / (365.25*24*3600)
    return {
        'scenario': 'injectivity',
        'well_count': well_count,
        'years_to_fill_proportion': round(years_to_fill, 2),
    }

def scenario_temperature_decline(initial_temp_C, reinjection_temp_C, thermal_lifetime_years=30,
                                   decline_rate_C_per_year=0.5):
    """Exponential-ish temperature decline screening."""
    temps = [initial_temp_C - decline_rate_C_per_year * y for y in range(thermal_lifetime_years+1)]
    return {
        'scenario': 'temperature_decline',
        'initial_temp_C': initial_temp_C,
        'reinjection_temp_C': reinjection_temp_C,
        'temps_C': temps,
        'final_temp_C': temps[-1],
    }

if __name__ == '__main__':
    s1 = scenario_drawdown(reservoir_pressure_initial_kPa=4000, productivity_index_kg_s_kPa=0.5)
    s2 = scenario_injectivity(well_count=5, injectivity_index_kg_s_kPa=0.3)
    s3 = scenario_temperature_decline(initial_temp_C=250, reinjection_temp_C=80)
    for s in [s1, s2, s3]:
        print(s)
