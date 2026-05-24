# Exercise 3: Verify Your Work

## Goal
Teach Hermes to use tests as quality gate.  Wellbore deliverability calculation is only trustworthy when bounded by known physics.

## Use a different model to verify
Run this verification with a different LLM or agent than the one that wrote the code. A model is weak at catching its own mistakes, so self-review misses errors that an independent model finds. In this course, code authored with Hermes + Kimi-2.6 was verified by a separate agent (Claude Code, Opus 4.7), which caught errors the authoring model had missed. Treat VERIFY as a cross-model second opinion, and note which model authored and which verified.

## Engineering Focus
Inflow Performance Relationship (IPR) + Tubing Performance Relationship (TPR).  Operating point intersection must yield positive mass flow, flowing pressure below reservoir pressure, and wellhead pressure above atmospheric.

## Before Prompt (vague)
```
Calculate the operating point of a geothermal well.
```

## After Prompt (precise)
```
Read 03_verify_your_work/wellbore_deliverability.py.
Add tests:
1. IPR at P_res=3000 kPa, P_wf=2500 kPa, J=0.5 kg/s/kPa must return 250.0 kg/s.
2. When P_wf equals P_res, q must be 0.
3. When P_wf > P_res, q must also be 0 (no backflow).
4. TPR must return wellhead < bottomhole.
5. Operating point must be physically feasible: q > 0, 0 < P_wf < P_res, P_wh > 0.
6. Monotonic: lower P_wf should yield higher q at same P_res and J.
Run pytest 03_verify_your_work/.
```

## Checklist
- [ ] Known-value IPR test
- [ ] Physical bounds enforced
- [ ] Monotonicity test
- [ ] All tests pass
