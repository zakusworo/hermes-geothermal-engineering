# Exercise 8: MCP Thermo + Geochem

## Goal
Install and use pygeotoolbox-mcp as MCP server for Hermes Agent. All thermo, wellbore, and scaling functions exposed as tools.

## Install pygeotoolbox-mcp

```bash
pip install git+https://github.com/zakusworo/pygeotoolbox-mcp.git
```

## Register as MCP Server in Hermes

Add to your Hermes config (e.g., `~/.hermes/config.yaml`):

```yaml
mcp_servers:
  pygeotoolbox:
    command: fastmcp run /path/to/pygeotoolbox-mcp/src/pygeotoolbox/mcp_server.py
    transport: stdio
```

Or run directly:
```bash
fastmcp run src/pygeotoolbox/mcp_server.py --transport stdio
```

## Available Tools (15+)

| Tool | Description | Module |
|------|-------------|--------|
| `get_enthalpy` | Enthalpy (kJ/kg) at T, P | thermo |
| `get_density` | Density (kg/m3) at T, P | thermo |
| `get_saturation_temperature` | Tsat for pressure | thermo |
| `get_batch_properties` | Batch compute H, D, V, cp, k | thermo |
| `calculate_ipr` | Mass flow from IPR | wellbore |
| `calculate_tpr` | Wellhead pressure from TPR | wellbore |
| `find_operating_point` | IPR-TPR intersection | wellbore |
| `check_caco3_scaling` | Ryznar Index + risk | scaling |
| `check_sio2_scaling` | SiO2 scaling risk | scaling |
| `check_corrosivity` | Brine corrosivity score | scaling |
| `simulate_decline` | Exponential/hyperbolic decline | decline |
| `simulate_reinjection_temperature` | Temp decline from reinjection | decline |
| `calculate_heat_in_reservoir` | Sensible heat (MJ) | heat_balance |
| `calculate_power_output` | Gross power (MW) | heat_balance |
| `run_monte_carlo` | Monte Carlo on any function | sensitivity |

## Prompt Example

```
Use MCP tool get_enthalpy with T=200C, P=2000kPa.
Then calculate operating point for P_res=20000kPa, J=0.5, rho=900, TVD=1200m.
Then check SiO2 scaling risk for SiO2=200mg/L at T=200C.
```

## Checklist
- [ ] pygeotoolbox-mcp installed
- [ ] MCP server registered in Hermes config
- [ ] `hermes tools` lists pygeotoolbox tools
- [ ] Enthalpy lookup matches IAPWS
- [ ] Operating point physically feasible
- [ ] Scaling risk classified correctly
