# Exercise 6: Subagent Review

## Goal
Teach Hermes to delegate engineering-risky code to a reviewer subagent.

## Engineering Focus
Reviewer checks: unit consistency, thermodynamic range, physical bounds, wellbore bounds, geochemistry validity, simulation structure.

## Before Prompt (vague)
```
Is this code correct?
```

## After Prompt (precise)
```
Use /delegate_task with the reviewer context from AGENTS.md.
Ask the reviewer to check the wellbore_deliverability.py and mcp_thermo_client.py for:
1. SI units only
2. IAPWS-IF97 range (T < 1273 K, P < 100 MPa)
3. Phase stated explicitly
4. Wellbore: q > 0, P_wf < P_res, P_wh > 0
5. Tests present
Return findings first, not summaries.
```

## Checklist
- [ ] Subagent spawned
- [ ] Findings received
- [ ] Any issues fixed
- [ ] Tests re-run
