# Exercise 15: Supercooled Injection Modeling

## Goal
Model cold water injection below 0 °C for EGS (Enhanced Geothermal Systems)
and low-enthalpy reinjection using pygeotoolbox IAPWS G12-15 properties.

## Context
In deep wells and winter operations, injected water can remain liquid
below 0 °C due to pressure (0.1–50 MPa).  Standard IAPWS-IF97 does not
cover this region; use IAPWS G12-15 (supercooled water) instead.

## Tasks
1. Calculate density at −10 °C, 5 MPa — should be higher than at 0 °C
2. Calculate enthalpy at −15 °C — should be negative (below reference)
3. Compute heat sink: extracting energy from cold fluid
4. Compare reinjection strategy: cold liquid vs near-freezing

## Run
```bash
python3 -m pytest 15_supercooled_injection/ -v
```
