# Exercise 8: MCP-Backed Thermodynamic Tool

## Goal
Teach Hermes to use external MCP tools (CoolProp / IAPWS / geochem) for live calculations rather than inventing formulas.

## Engineering Focus
Live enthalpy-density lookup from CoolProp, plus sanity checks:
- Is point inside saturation dome?
- Does density match single-phase expectation?
- Is enthalpy between h_f and h_g at that pressure?

## Activity
1. Read `mcp_thermo_client.py`.
2. Compute water properties at:
   - 150 C, 1500 kPa (subcooled liquid)
   - 250 C, 2500 kPa (two-phase)
   - 300 C, 500 kPa (superheated vapor)
3. Verify phases match expectations.
4. Document recommended response format:
   - Inputs, Method, Result, Sanity check, Assumptions.

## Checklist
- [ ] Three states computed and verified
- [ ] Response format documented
- [ ] Assumptions listed
