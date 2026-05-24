# Exercise 5: Reusable Hermes Skills

## Goal
Teach Hermes to load domain-specific skills instead of pasting boilerplate into every prompt.

## Engineering Focus
Geothermal engineering skill covers:
- Thermodynamic properties (CoolProp / IAPWS-IF97)
- Separator enthalpy balance and quality
- Wellbore deliverability (IPR + TPR)
- Geochemistry / scaling indices
- Sustainability metrics
- Testing requirements (known-value, monotonicity, physical bounds)

## Activity
1. Run `/skill view geothermal-engineering` to inspect the skill.
2. Create a new exercise script that loads the skill via `/skill geothermal-engineering` and computes separator quality at 2500 kPa for a total enthalpy of 850 kJ/kg.
3. Verify the result: quality must be between 0 and 1.
4. Add a test.

## Checklist
- [ ] Skill loaded
- [ ] separator_quality computed
- [ ] Quality bounded
- [ ] Test passes
