# Exercise 2: Specific Context

## Goal
Teach Hermes that precise context produces correct fixes faster than vague prompts.
This module now uses **pygeotoolbox-mcp** for reliable thermodynamic properties (CoolProp + IAPWS-IF97).

## Engineering Focus
Thermodynamic state validation: enthalpy and density from T and P via real CoolProp PropsSI.

## Prompt Example
```
In 02_specific_context/thermo_properties.py, verify that enthalpy_from_TP(200, 2000)
returns ~852 kJ/kg and density_from_TP(200, 2000) returns ~865 kg/m3.
Also add monotonicity test: at 1500 kPa, enthalpy must increase with T from 120C to 180C.
Run pytest 02_specific_context/.
```

## Checklist
- [ ] Enthalpy at 200C, 2 MPa matches IAPWS (852 kJ/kg)
- [ ] Density at 200C, 2 MPa ~865 kg/m3
- [ ] Monotonicity test added
- [ ] Invalid inputs rejected (negative T/P)
- [ ] All tests pass
