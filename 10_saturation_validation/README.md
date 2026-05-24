# Exercise 10: Saturation Property Validation

## Goal
Validate IAPWS saturation properties against known reference values.

## Background
IAPWS-IF97 defines the saturation curve between triple point (0.611657 kPa, 0.01 C)
and critical point (22.064 MPa, 373.946 C). This exercise tests the pygeotoolbox
siapws_saturation module against these standard values.

## Tasks
1. Test T_sat(P) at known reference points.
2. Test P_sat(T) at same points.
3. Verify roundtrip error < 1%.
4. Test steam quality calculation at 1 MPa, 200 C.

## Run
```bash
python3 -m pytest 10_saturation_validation/ -v
```
