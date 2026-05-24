# Hermes for Geothermal Engineering

Hermes Agent course for **geothermal reservoir engineering**, adapted from the `hermes-reservoir-engineering` workflow framework.  Every exercise maps the same AI-assisted guardrail (explore-plan-code-verify-review) to real geothermal workflows: enthalpy balance, thermodynamic state validation, wellbore deliverability, tracer interpretation, scaling/precipitation screening, sustainability analysis, and parallel sensitivity studies.

The goal: teach geothermal engineers to direct AI like a disciplined technical assistant — context, constraints, units in SI, verification with tests, proven thermo libraries over hand-rolled formulas.

## Why This Course Exists

Geothermal engineering has its own set of high-consequence small details:

- thermodynamic properties: enthalpy, entropy, density, viscosity as functions of T and P
- phase changes: liquid, two-phase, vapor, and transitions across the saturation dome
- unit discipline: SI (kPa, C, kg/s) vs legacy (psia, degF, lb/hr)
- wellbore deliverability: IPR + TPR (wellbore flowing)
- chemistry: silica saturation, scaling indices, CO2/H2S degassing
- sustainability: reservoir pressure drawdown vs recharge, temperature decline
- simulation: mass/energy balance, boundary conditions, mesh, timestep stability
- uncertainty: natural state calibration vs production forecasting, parameter correlations

AI tools accelerate this work only when engineers demand domain context, SI units, known-value checks, and physical-bounds verification.  This course teaches that workflow concretely.

## What You Will Learn

By the end:

- use Hermes explore-plan-code-verify on geothermal scripts
- write prompts with file, function, SI units, and expected T-P-h relationship
- ask Hermes for tests: known IFE-97 values, monotonicity, physical bounds
- create `CLAUDE.md` / `AGENTS.md` with geothermal standards
- package repeatable workflows as Hermes skills
- run a reviewer subagent for unit consistency, correlation range, nonphysical output
- combine shell + Python for CSV/datalog QA before analysis
- use thermodynamic tools (CoolProp, iapws, geochem) via MCP or direct Python
- parallelize independent sensitivity cases (injectivity, drawdown, sustainability)

## Who This Is For

- geothermal reservoir engineers
- production engineers managing wellbore deliverability and scaling
- geothermal drilling / well-test engineers
- renewable energy data scientists in subsurface
- technical managers evaluating AI for geothermal workflows
- students / researchers in geothermal systems, volcanology, hydrogeology

No software engineering background needed.  Basic Python + terminal comfort is enough.

## Source Inspiration

- Original reservoir course: `Claude-for-reservoir-engineering` by Gabriel Serrao  
- Hermes port: `hermes-reservoir-engineering` by Zulfikar Aji Kusworo
- Companion toolbox: [pygeotoolbox-mcp](https://github.com/zakusworo/pygeotoolbox-mcp) — Geothermal engineering MCP server with 15+ tools (thermo, wellbore, scaling, decline, heat balance, sensitivity) using CoolProp + IAPWS-IF97
- Waiwera simulator (Fortran/PETSc): insight into geothermal flow simulation structure  
- CoolProp and IAPWS-IF97 for reliable thermodynamic properties  
- Geochemist's Workbench / PHREEQC for geochemical calculations  

## Repository Structure

```text
.
|-- 01_explore_plan_code/           # Production enthalpy analysis: explore, plan, implement
|-- 02_specific_context/            # Thermodynamic state bug: precise context beats vague prompts
|-- 03_verify_your_work/            # Wellbore deliverability checks: tests and sanity checks
|-- 04_init_project_memory/           # Geothermal project memory (CLAUDE.md + AGENTS.md)
|-- 05_skills/                      # Reusable Hermes geothermal skills
|-- 06_subagent_review/             # Reviewer subagent for units & thermodynamic consistency
|-- 07_cli_workflow/                # Shell + Python QA for timeseries data
|-- 08_mcp_geochem_thermo/          # CoolProp / IAPWS / geochem via MCP
|-- 09_parallel_fanout/             # Parallel sustainability / drawdown studies
|-- assets/                          # Generated plots + result tables
|-- scripts/generate_course_figures.py
|-- .hermes/skills/geothermal-engineering/  # Hermes geothermal skill (CoolProp, IPR, scaling)
|-- .hermes/skills/run-tests/              # Test skill
|-- AGENTS.md                        # Reviewer subagent prompt
|-- CLAUDE.md                        # Project rules
|-- BEGINNERS_GUIDE.txt             # Panduan awam (Bahasa Indonesia)
|-- requirements.txt
|-- LICENSE
|-- README.md
```

## Prerequisites

- Hermes Agent: https://hermes-agent.nousresearch.com/docs/
- Python 3.10+ and `pip`
- `coolprop`, `iapws`, `matplotlib`, `numpy`, `pandas`, `pytest`
- Optional: `phreeqpy` or `geochem` for Module 8
- Optional: WSL or Linux for shell workflows

## Quick Start

```bash
git clone https://github.com/zakusworo/hermes-geothermal-engineering.git
cd hermes-geothermal-engineering
python3 -m pip install -r requirements.txt
python3 scripts/generate_course_figures.py
hermes
```

Navigate to Exercise 1:

```bash
cd 01_explore_plan_code
```

Read README, try vague prompt first, /clear, then improved prompt.  Contrast is the point.

## Hermes vs Claude Code

| Feature | Claude Code | Hermes Agent |
|---------|-------------|--------------|
| Explore/plan/code/verify | Yes | Yes, plus `/skill` preloading |
| Project memory | `CLAUDE.md` | `CLAUDE.md` + `AGENTS.md` + `.hermes/skills/` |
| Skills | `.claude/skills/` | `.hermes/skills/` — loaded with `/skill` |
| Subagent review | Reviewer agent | `delegate_task` — isolated subagent |
| Cron/scheduled tasks | Not built-in | `/cron` — recurring analysis |
| Web search | Not built-in | `/web_search` built-in |
| Memory across sessions | Manual | Persistent via `/memory` |
| CLI approvals | `--yolo` | `hermes config set approvals.mode manual` (default) |
| WSL/Windows native | Yes | Yes, with `/mnt/c/` paths |

All exercises mapped to Hermes tool model: `terminal()`, `browser_navigate()`, `delegate_task()`, `cronjob()`, `web_search()`, `skill_view()`.

## Course Modules

| # | Folder | Hermes Practice | Geothermal Engineering Focus |
|---|--------|-----------------|------------------------------|
| 1 | `01_explore_plan_code/` | Explore->Plan->Code | Separator enthalpy analysis and temperature trend |
| 2 | `02_specific_context/` | Exact file/function/unit context | Fixing thermodynamic state (h, rho, s from T,P) |
| 3 | `03_verify_your_work/` | Test as quality gate | Wellbore deliverability: IPR + TPR, physical bounds |
| 4 | `04_init_project_memory/` | `CLAUDE.md`/`AGENTS.md` | Geothermal standards (SI, saturation checks, mesh rules) |
| 5 | `05_skills/` | Reusable domain skills | Geothermal-engineering skill (IAPWS, IPR, scaling) |
| 6 | `06_subagent_review/` | `delegate_task` reviewer | Unit consistency, IAPWS range, nonphysical output |
| 7 | `07_cli_workflow/` | Shell + Python QA | Timeseries CSV QA: NaN, out-of-range T/P, duplicates |
| 8 | `08_mcp_geochem_thermo/` | MCP tools (CoolProp, IAPWS) | Live thermodynamic calls + geochemical checks |
| 9 | `09_parallel_fanout/` | Parallel sensitivity | Sustainability, drawdown, injectivity scenarios |

## Illustrated Outputs

Run `python3 scripts/generate_course_figures.py` to regenerate.

| Graph | File | Description |
|-------|------|-------------|
| Separator Enthalpy & Temperature | `separator_enthalpy_temperature.png` | Steam/water enthalpy fractions and separator temperature trend |
| Thermodynamic State Surface | `thermo_state_surface.png` | Density and enthalpy contours in T-P space (IAPWS-IF97) |
| Wellbore Deliverability | `wellbore_deliverability.png` | IPR + TPR intersection; mass flow vs wellhead pressure |
| Geothermal Workflow Map | `hermes_geothermal_workflow.png` | 5-step guardrail applied to geothermal |

### Separator Enthalpy Diagnostic

![Separator enthalpy](assets/separator_enthalpy_temperature.png)

- Well A: higher enthalpy, lower mass fraction increase (7% to 12%)
- Well B: lower enthalpy, wetter trend, fraction increase (21% to 28%)
- A good prompt: "compute enthalpy from T,P; is separator temperature stable, monotonically decreasing, or oscillating?"

### Thermodynamic State Surface

![Thermodynamic state](assets/thermo_state_surface.png)

- Density drops sharply near boiling point at each pressure level.
- Enthalpy increases with temperature but bends approaching saturation.
- Phase-transition boundary visible as kink.  Any tool that produces a smooth surface crossing the saturation line without discontinuity is suspect.

### Wellbore Deliverability

![Wellbore deliverability](assets/wellbore_deliverability.png)

- IPR (Inflow Performance Relationship): mass flow vs flowing pressure
- TPR (Tubing Performance Relationship): mass flow vs wellhead pressure (includes friction, elevation)
- Operating point: IPR = TPR, within physical bounds (flow > 0, P_wf < P_res)

## Key Hermes Commands

```text
hermes                              # start session
hermes -w                           # isolated worktree
hermes -s geothermal-engineering    # preload skill
/skill geothermal-engineering         # load within session
/skill run-tests                    # load test skill
/init                               # reload CLAUDE.md rules
/delegate_task                      # spawn reviewer subagent
/cron                               # schedule recurring analysis
/agents                             # list subagents
/memory add                         # save note across sessions
/web_search                         # search web for latest references
```

## Running Tests

```bash
python3 -m pytest -v
python3 -m pytest 01_explore_plan_code/ -v
```

Tests are teaching tools.  Add real-edge cases and known IAPWS-IF97 reference values for production use.

## Using CoolProp / IAPWS-IF97

```python
from CoolProp.CoolProp import PropsSI

h = PropsSI('H', 'T', 473.15, 'P', 2.0e6, 'Water')  # J/kg
rho = PropsSI('D', 'T', 473.15, 'P', 2.0e6, 'Water')  # kg/m3
```

Always capture: inputs T [K] or [C], P [Pa] or [kPa], phase expectation, output units, sanity check (rho > 0, h > h_f at that P).

## Using IAPWS directly

```python
from iapws import IAPWS97

sat = IAPWS97(T=473.15, x=0.5)   # two-phase at 200 C
h = sat.h                          # kJ/kg
rho = sat.rho                      # kg/m3
```

- IAPWS97 expects T in K and P in MPa
- Always verify input is within valid range (T < 1273 K, P < 100 MPa)
- Never silently assume single phase if T,P is near saturation dome

## Using pyrestoolbox-mcp (if configured)

For Hermes with MCP, `pyrestoolbox-mcp` can expose PVT functions; geothermal adaptation uses IAPWS / CoolProp MCP equivalents.

Recommended response format for any calculation:

```text
Inputs:
- Temperature: 200 C (473.15 K)
- Pressure: 2000 kPa (2.0 MPa)

Method:
- IAPWS-IF97 / CoolProp / correlation

Result:
- Enthalpy: 852.3 kJ/kg
- Density: 862.1 kg/m3

Sanity check:
- 200 C, 2 MPa is single-phase liquid (saturated T at 2 MPa = 212.4 C, so subcooled)
- Density positive, enthalpy between h_f and h_g at that pressure
- Not crossing saturation dome

Assumptions:
- Pure water, not brine
- No dissolved gas effect on density
- Single phase (subcooled liquid)
```

## Security Note

```bash
hermes config set approvals.mode manual   # default
# CI/batch: --yolo
```

Hermes runs shell via `terminal()`.  Exercises intentionally allow `python`, `pytest`, `uv run`.

## Contributing

Pattern:

1. Add numbered exercise folder.
2. Include README.md with before/after prompts.
3. Include Python file + tests.
4. Keep sample data fictional or openly licensed.
5. Add figure generation to `scripts/generate_course_figures.py`.

## License

MIT License. See `LICENSE`.

- Copyright (c) 2025 Gabriel Serrao (original petroleum reservoir course)
- Copyright (c) 2026 Zulfikar Aji Kusworo — Hermes port, rewrite, figures, packaging, and geothermal adaptation.

## Acknowledgements

- Claude Code ecosystem + `claude-code-for-hydrology`
- pyResToolbox / pyrestoolbox-mcp (Mark Burgoyne)
- Waiwera geothermal simulator (University of Auckland)
- IAPWS-IF97 formulation and CoolProp
- Nous Research Hermes Agent
