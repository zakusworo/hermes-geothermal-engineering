# Exercise 2: Specific Context

## Goal
Teach Hermes that precise context (failing test, exact file, formula) produces correct fixes faster than vague prompts.

## Engineering Focus
Thermodynamic state bug: a fake `PropsSI` wrapper ignores pressure and returns physics-wrong enthalpy.  Fixing this requires naming the failing test and the expected IAPWS-IF91 formula.

## Before Prompt (vague)
```
Fix the thermo bug.
```

## After Prompt (precise)
```
The test test_known_value_200C_2MPa in 02_specific_context/test_thermo_properties.py fails.
Current PropsSI is a dummy that ignores pressure and returns h = 4.18*T + 50.
Replace with real CoolProp PropsSI('H', 'T', T_K, 'P', P_Pa, 'Water') and check that at 200 C (473.15 K), 2000 kPa:
  - enthalpy is ~852 kJ/kg
  - density is ~865 kg/m3
Also add a monotonicity test: at 1500 kPa, enthalpy must increase with temperature from 120 C to 180 C.
Run pytest 02_specific_context/.
```

## Checklist
- [ ] Failing test named
- [ ] Expected reference values given
- [ ] Monotonicity test added
- [ ] Invalid inputs rejected
- [ ] All tests pass
