# Exercise 4: Project Memory (`CLAUDE.md` + `AGENTS.md`)

## Goal
Teach Hermes to use persistent project memory, not one-off instructions, for geothermal-domain constraints.

## Engineering Focus
Reservoir standards saved in `CLAUDE.md` and reviewer in `AGENTS.md`:
- SI units (kPa, C, kJ/kg)
- Thermo validity (IAPWS range, phase awareness, no smooth crossing of saturation dome)
- Wellbore bounds (q > 0, P_wf < P_res)
- Test expectations (known-value, monotonicity, physical bounds)
- Geochemistry mention (scaling indices from documented tools, not invented curves)
- Simulation discipline (natural-state calibration before production forecast)

## Activity
1. Edit root CLAUDE.md to add a new rule: "When using IAPWS-IF97, always state whether the point is single-phase liquid, saturated, two-phase, or superheated vapor."
2. Edit AGENTS.md to add a new checkpoint: "If mesh or simulation is mentioned, verify natural-state calibration is discussed before production forecasting."
3. Run `/init` to reload.

## Checklist
- [ ] New rule in CLAUDE.md
- [ ] New checkpoint in AGENTS.md
- [ ] `/init` executed successfully
