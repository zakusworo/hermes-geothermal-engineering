---
description: Geothermal reservoir engineering skill for Hermes Agent.  Covers thermodynamic property lookup (IAPWS-IF97 / CoolProp), wellbore deliverability (IPR/TPR), separator enthalpy balance, scaling screening, and sustainability analysis.
category: geothermal-engineering
tags: [geothermal, reservoir, thermodynamics, wellbore, scaling, sustainability, IAPWS, CoolProp]
requires_tools: [terminal, web, browser, delegate_task, cronjob]
requires_env_vars: [PYTHONPATH]
python_dependencies:
  - CoolProp
  - iapws
  - numpy
  - pandas
  - matplotlib
  - pytest
---

# Geothermal Engineering Skill

Use this skill for geothermal subsurface engineering: wells, heat extraction, thermodynamic state, chemistry, and sustainability.  It ensures SI units, physical bounds checks, and phase awareness in every calculation.

## 1. Thermodynamic Properties

For a given temperature and pressure, always ask for:
- Phase (subcooled liquid, saturated, two-phase, superheated vapor)
- Density (kg/m³)
- Enthalpy (kJ/kg)
- Entropy (kJ/kg·K) if analyzing cycles
- Dynamic viscosity (Pa·s) if wellbore friction matters

```python
from CoolProp.CoolProp import PropsSI, PhaseSI

T_K = 473.15        # K
P_Pa = 2.0e6        # Pa

phase = PhaseSI('T', T_K, 'P', P_Pa, 'Water')
h = PropsSI('H', 'T', T_K, 'P', P_Pa, 'Water') / 1000  # --> kJ/kg
rho = PropsSI('D', 'T', T_K, 'P', P_Pa, 'Water')       # --> kg/m3
```

Guardrails:
- T < 1273 K and P < 100 MPa for IAPWS-IF97
- Phase must be stated explicitly; never silently assume single phase
- If x (quality) requested, saturation properties must be computed first

## 2. Separator Enthalpy Balance

Flash separator: total enthalpy in = steam enthalpy out + liquid enthalpy out.

```python
from CoolProp.CoolProp import PropsSI

def separator_quality(h_total, P_sep, T_sat=None):
    P = P_sep
    hf = PropsSI('H', 'P', P, 'Q', 0, 'Water')
    hg = PropsSI('H', 'P', P, 'Q', 1, 'Water')
    x = (h_total - hf) / (hg - hf)
    return x
```

Guardrails:
- x must be between 0 and 1; reject otherwise
- h_total must be between hf and hg at separator pressure
- If using T_sat instead of P_sep, verify against saturation table

## 3. Wellbore Deliverability

### Inflow Performance Relationship (IPR)

Linear productivity index model for liquid-dominated geothermal reservoir:

```text
q = J * (P_res - P_wf)
```

where:
- q = mass flow rate (kg/s)
- J = productivity index (kg/s / kPa)
- P_res = static reservoir pressure (kPa)
- P_wf = bottomhole flowing pressure (kPa)

### Tubing Performance Relationship (TPR)

Wellhead pressure vs mass flow, accounting for hydrostatic head and friction:

```text
P_wh = P_wf - rho_avg * g * TVD - f * (L/D) * (rho_avg * v^2) / 2
```

where:
- rho_avg = average density in wellbore (kg/m³)
- g = 9.81 m/s²
- TVD = true vertical depth (m)
- f = friction factor
- L = measured depth (m), D = inner diameter (m)

Operating point: solve for q where IPR = TPR.

Guardrails:
- q > 0
- P_wf < P_res
- P_wh > 0 (or > atmospheric for atmospheric well)
- rho_avg must be based on actual wellbore T,P profile, not constant

## 4. Geochemistry / Scaling (Optional Module)

Use PHREEQC or `geochem` library for saturation indices (SI):

- amorphous silica: SI > 0 means supersaturated, potential scaling
- calcite: temperature-dependent, watch cooling during flashing
- H2S / CO2 degassing: non-condensable gas affects separator vents

## 5. Sustainability

Key metrics:

- Pressure drawdown rate (kPa/year)
- Temperature decline rate (C/year)
- Mass extraction vs recharge ratio
- Reservoir lifespan estimate with decline assumptions

## 6. Tests

Every calculation requires:

1. Known-value check at reference state (e.g., 200 C, 2 MPa)
2. Monotonicity check where expected (h increases with T at fixed P in single-phase)
3. Physical bounds (rho > 0, finite enthalpy)
4. Invalid-input rejection (T < 0 K, P < 0)

## 7. Hermes Tool Calls

- `terminal()` — run QA on well-test CSV, N, P, T, NaN checks
- `browser_navigate()` — fetch IAPWS-IF97 formulation or CoolProp docs
- `delegate_task()` — reviewer subagent for phase-change or unit conversion code
- `cronjob()` — schedule recurring wellhead pressure monitoring
- `web_search()` — search for latest geothermal IPR correlations or scaling indices
