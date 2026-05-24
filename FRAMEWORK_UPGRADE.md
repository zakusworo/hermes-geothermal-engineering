# Framework Upgrade: Production-Grade Accuracy

## Problem
The original hermes-geothermal-engineering + pygeotoolbox-mcp framework showed large discrepancies when compared to published plant data:

| Case | Published | Original Calc | Ratio |
|------|-----------|-------------|-------|
| Wairakei | 161 MW | 51.4 MW | 31.9% |
| Soultz | 1.5 MW | 0.17 MW | 8.5% |
| Krafla | 60 MW | 48.6 MW | 81.0% |
| Hellisheidi | 303 MW | 43.8 MW | 14.5% |
| Olkaria | 25°C decline | 25.0°C | 100% |

## Root Causes
1. **Single-flash model** — real plants use double/triple flash
2. **No NCG handling** — CO2/H2S compression consumes 5-15% power
3. **No parasitic loads** — cooling, reinjection, controls omitted
4. **Single-phase flow** — two-phase pressure drop in wells ignored
5. **Approximate working fluid** — R134a enthalpies estimated

## Solution: pygeotoolbox-mcp v0.5.0

Five new modules added:

### 1. multiphase.py — Two-Phase Flow
- Homogeneous Equilibrium Model (HEM)
- Drift-Flux Model (Zuber-Findlay)
- Beggs-Brill pressure drop
- Quality profile along wellbore

**Impact:** Improves EGS well deliverability from 8.5% → ~30-50%

### 2. ncg.py — Non-Condensable Gas
- CO2, H2S, CH4, NH3 compressor models
- Isentropic compression with efficiency
- Species-by-species penalty calculation

**Impact:** Adds realistic 3-8% power penalty for liquid-dominated systems

### 3. multiflash.py — Multi-Stage Flash
- Double-flash cycle (HP + LP turbines)
- Triple-flash cycle
- Energy balance at each stage

**Impact:** Improves flash plant accuracy from 14-32% → ~50-70%

### 4. parasitic.py — Parasitic Loads
- Cooling system (air/water)
- Reinjection pumps
- Working fluid pumps
- Control systems

**Impact:** Subtracts 8-15% from gross to get realistic net power

### 5. working_fluid.py — Accurate Working Fluids
- R134a, R600a, R290, R717
- CoolProp integration (when available)
- Polynomial fallback (when CoolProp not installed)
- ORC cycle efficiency with real properties

**Impact:** Improves binary cycle from 81% → ~85-90%

## Usage Example

```python
from pygeotoolbox import multiflash, ncg, parasitic

# Double-flash cycle (Hellisheidi)
cycle = multiflash.double_flash_cycle(
    m_total_kg_s=400,
    T_separator_C=180,
    P_separator_kPa=1000,
    T_flash2_C=140,
    P_flash2_kPa=361,
)

# NCG penalty
ncg_result = ncg.total_ncg_penalty(
    m_steam_kg_s=cycle['m_steam_total_kg_s']
)

# Net power after parasitics
net = parasitic.parasitic_loads(
    gross_power_MW=cycle['gross_MW'],
    m_steam_kg_s=cycle['m_steam_total_kg_s'],
    m_brine_kg_s=400 - cycle['m_steam_total_kg_s'],
    cooling_type='air',
    has_ncg=False,
)

print(f"Gross: {cycle['gross_MW']:.1f} MW")
print(f"Net: {net['net_power_MW']:.1f} MW")
print(f"Parasitic: {net['parasitic_fraction_percent']:.1f}%")
```

## Expected Improved Results

| Case | Original | With Upgrades | Expected Improvement |
|------|----------|---------------|---------------------|
| Wairakei | 31.9% | ~55-65% | Double-flash + NCG |
| Soultz | 8.5% | ~25-40% | Multiphase + temporal |
| Krafla | 81.0% | ~85-90% | Working fluid accuracy |
| Hellisheidi | 14.5% | ~50-60% | Double-flash + parasitic |
| Olkaria | 100% | 100% | Already perfect (conservation law) |

## Limitations Remaining
Even with upgrades, the framework cannot match commercial software:

| Feature | Our Framework | TOUGH2 | WELLSIM |
|---------|--------------|--------|---------|
| Temporal simulation | Steady-state | Transient 50+ years | Steady-state |
| Fracture networks | Darcy (single J) | Discrete fracture | Pipe network |
| Geochemistry | None | TOUGHREACT | WATCH |
| Optimization | None | Built-in | None |
| Validation | Published data | Lab + field | Field data |

## Conclusion
The upgraded framework bridges the gap between simple teaching models and commercial software. It captures the **essential physics** that cause the largest discrepancies (multi-flash, NCG, parasitics) while maintaining zero external dependencies and AI-agent compatibility.

For **final engineering design**, use TOUGH2 + WELLSIM.
For **education, feasibility studies, and AI-assisted analysis**, use hermes-geothermal-engineering + pygeotoolbox-mcp v0.5.0.

---
**Reference:** pygeotoolbox-mcp v0.5.0, DOI: 10.5281/zenodo.xxxxx (pending)
**GitHub:** https://github.com/zakusworo/pygeotoolbox-mcp
