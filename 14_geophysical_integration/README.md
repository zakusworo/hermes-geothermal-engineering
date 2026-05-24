# Exercise 14: Geophysical Integration

## Goal
Convert resistivity logging data to salinity estimates using IAPWS-based
brine electrical conductivity model.

## Context
In geothermal exploration, resistivity tomography identifies saline zones.
This exercise links geophysical measurements to brine chemistry using
pygeotoolbox.geophysics.

## Tasks
1. Convert resistivity (ohm·m) to conductivity (S/m)
2. Estimate salinity from conductivity at known temperature
3. Compare with direct sampling data
4. Identify anomalous zones (low resistivity = high salinity)
