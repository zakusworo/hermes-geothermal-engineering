# Exercise 9: Parallel Sensitivity Studies

## Goal
Teach Hermes to parallelize independent sensitivity scenarios via `delegate_task`.

## Engineering Focus
Three independent cases:
1. Reservoir pressure drawdown over 10 years
2. Injectivity time to fill X % of reservoir
3. Temperature decline trajectory with reinjection

## Before Prompt (vague)
```
Run sensitivity analysis.
```

## After Prompt (precise)
```
Use delegate_task with three parallel tasks:
1. scenario_drawdown(4000 kPa initial, J=0.5, 10 years, 5 kPa/year decline)
2. scenario_injectivity(well_count=5, injectivity_index=0.3, make
 up_fraction=0.1)
3. scenario_temperature_decline(initial=250 C, reinjection=80 C, lifetime=30 years, decline=0.5 C/year)

Each task should return a dict with:
- scenario name
- inputs
- outputs
- one sanity check
Aggregate the results and compare:
- which scenario reaches critical limit first?
- is reinjection enough to offset drawdown?
```

## Checklist
- [ ] Three subagents spawned
- [ ] Each returned structured dict
- [ ] Aggregation performed
- [ ] Physical comparison made
