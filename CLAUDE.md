# Geothermal Engineering Standards

This is a Hermes course for geothermal reservoir engineering.  All code, analysis, and figures follow these rules.

## Units

- Always use SI units internally:  
  - Temperature: K (Kelvin) or C (Celsius) — state which  
  - Pressure: Pa or kPa — state which  
  - Enthalpy: J/kg or kJ/kg — state which  
  - Density: kg/m³  
  - Mass flow: kg/s  
  - Time: s or year — state which
- If converting from legacy units (psia, degF, lb/hr), document the conversion factor explicitly.

## Thermodynamic Properties

- Prefer CoolProp or IAPWS-IF97 standard libraries for water/steam properties.
- Use pygeotoolbox-mcp (`pygeotoolbox.thermo`) for batch properties, saturation curves, and steam quality.
- Never silently hand-roll water properties.  If using a correlation, document it and state applicability range.
- Always verify T and P are within valid range:
  - IAPWS-IF97: 0 < T < 1273 K, 0 < P < 100 MPa
  - CoolProp: similar, but check PhaseSI for phase before trusting density/enthalpy
- Always state phase assumption (subcooled liquid, saturated, two-phase, superheated vapor).
- Never produce a smooth curve crossing the saturation dome without phase change discontinuity; that is a clear bug.

## Wellbore Deliverability

- Inflow Performance Relationship (IPR): relate bottomhole flowing pressure to mass flow.
- Tubing Performance Relationship (TPR): relate wellhead pressure to mass flow (includes friction + elevation).
- Operating point: IPR = TPR intersection.
- Use pygeotoolbox-mcp (`pygeotoolbox.wellbore`) for operating point and productivity index.
- Always check physical bounds:
  - mass flow > 0, flowing pressure < reservoir pressure, wellhead pressure > atmospheric.
- Prefer known geothermal IPR models (linear, quadratic, or productivity index) over generic oil-gas models.

## Chemistry and Scaling

- When discussing scaling, always include:
  - saturation index (e.g., amorphous silica, calcite)
  - temperature at which saturation is reached
  - whether the fluid is single-phase or two-phase during cooling
- Use pygeotoolbox-mcp (`pygeotoolbox.scaling`) for RSI, SiO2 risk, and brine density.
- Use PHREEQC-style or geochem library results; do not invent solubility curves.

## Decline and Sustainability

- Use pygeotoolbox-mcp (`pygeotoolbox.decline`) for pressure/temperature decline and reinjection models.
- Use `pygeotoolbox.heat_balance` for reservoir heat, thermal recovery, power output, and NPV.
- Use `pygeotoolbox.sensitivity` for one-factor sweeps, tornado charts, and Monte Carlo.

## MCP Integration

- Install pygeotoolbox-mcp as MCP server: `fastmcp run src/pygeotoolbox/mcp_server.py`
- Exposes 15 tools to Hermes Agent: get_enthalpy, get_density, calculate_ipr, calculate_tpr, check_caco3_scaling, simulate_decline, etc.
- Prefer MCP tools over raw CoolProp when working iteratively with Hermes.

## Simulation Mesh and Timestep

- If discussing numerical simulation (inspired by Waiwera), include:
  - mesh type (structured / unstructured)
  - boundary conditions (mass flow, heat flux, fixed pressure, fixed temperature)
  - timestep stability criteria (CFL, Newton tolerance)
  - natural state calibration before production forecasting

## Testing Expectations

- Every engineering function must have:
  - known-value check against IAPWS-IF97 or CoolProp reference
  - monotonicity where expected (enthalpy increases with T at fixed P)
  - physical bounds (density > 0, enthalpy finite)
  - rejected invalid inputs (T < 0 K, P < 0)
- Plot as second verification surface: if the table says one thing and the plot contradicts it, investigate.

## Hermes Tool Usage

- Use `terminal()` for shell QA on CSV datalogs.
- Use `browser_navigate()` for fetching IAPWS docs or CoolProp reference tables.
- Use `delegate_task()` for reviewer subagent on any calculation involving phase change or unit conversion.
- Use `cronjob()` for recurring monitoring of separator temperature trends or wellhead pressure decline.
