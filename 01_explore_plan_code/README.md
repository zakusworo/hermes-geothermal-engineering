# Exercise 1: Explore, Plan, Then Code

## Goal
Teach Hermes to explore the codebase first before editing.  Hermes reads the separator analysis script, sample CSV, and existing tests before adding enthalpy trend analysis.

## Engineering Focus
Geothermal separator data: temperature, pressure, mass flow, steam fraction.  Engineers need to know if separator temperature is declining (indicates reservoir cooling or scaling).  Steam fraction increases with enthalpy — a useful screening metric for well performance.

## Hermes Commands
```text
/hermes -w  # isolated worktree
/skill geothermal-engineering
/init       # reload CLAUDE.md
```

## Before Prompt (vague)
```
Add enthalpy analysis to the production script.
```

## After Prompt (precise)
```
Read 01_explore_plan_code/separator_analysis.py and 01_explore_plan_code/sample_separator.csv.
The script currently adds enthalpy and steam fraction but the enthalpy is a placeholder formula.
Replace it with a call to CoolProp PropsSI('H', 'T', T_K, 'P', P_Pa, 'Water').
Add a test to verify enthalpy increases monotonically with temperature at fixed pressure.
Plot separator temperature trend and steam fraction trend per well.
Run pytest 01_explore_plan_code/.
```

## Checklist
- [ ] Hermes explored files before editing
- [ ] Enthalpy uses CoolProp rather than placeholder
- [ ] Monotonicity test exists
- [ ] Plot regenerated and committed
- [ ] All tests pass
