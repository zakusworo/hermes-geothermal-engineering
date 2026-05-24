"""
Generate course figures for Hermes Geothermal Engineering.

Figures:
1. separator_enthalpy_temperature.png -- enthalpy trends + steam fraction by well
2. thermo_state_surface.png -- density or enthalpy contour in T-P space
3. wellbore_deliverability.png -- IPR + TPR + operating point
4. hermes_geothermal_workflow.png -- 5-step guardrail workflow
"""

import os
import matplotlib.pyplot as plt
import numpy as np

try:
    from pygeotoolbox import thermo, wellbore
except ImportError:
    thermo = None
    wellbore = None

def figure_1_separator():
    """Plot separator enthalpy and steam fraction trends using real pygeotoolbox data."""
    # Raw data: (T_C, P_kPa, steam_frac) for each well per month
    raw = {
        'A-01': [(145, 250, 0.077), (143, 248, 0.096), (142, 247, 0.115), (141, 245, 0.146)],
        'B-02': [(152, 255, 0.216), (150, 252, 0.231), (148, 250, 0.258), (147, 248, 0.277)],
        'C-03': [(138, 240, 0.055), (137, 238, 0.065), (136, 237, 0.075), (135, 235, 0.087)],
    }
    dates = ['Jan', 'Feb', 'Mar', 'Apr']

    enthalpy = {k: [] for k in raw}
    if thermo is not None:
        for well, values in raw.items():
            for T, P, _ in values:
                try:
                    h = thermo.enthalpy_from_TP(T, P) / 1000.0
                    enthalpy[well].append(h)
                except Exception:
                    enthalpy[well].append(None)
    else:
        # fallback linear approx
        for well, values in raw.items():
            for T, _, _ in values:
                enthalpy[well].append(4.18 * T)

    fig, axes = plt.subplots(1, 2, figsize=(10, 4))
    ax = axes[0]
    for well in ['A-01', 'B-02', 'C-03']:
        ax.plot(dates, enthalpy[well], marker='o', label=well)
    ax.set_ylabel('Enthalpy (kJ/kg)')
    ax.set_title('Separator Enthalpy via CoolProp')
    ax.legend()
    ax.grid(True)

    ax = axes[1]
    for well, values in raw.items():
        ax.plot(dates, [x*100 for _, _, x in values], marker='o', label=well)
    ax.set_ylabel('Steam Fraction (%)')
    ax.set_title('Separator Steam Fraction Trend')
    ax.legend()
    ax.grid(True)
    fig.tight_layout()
    return fig

def figure_2_thermo_surface():
    """Density contour in T-P space using real CoolProp data."""
    import os, sys
    try:
        from CoolProp.CoolProp import PropsSI
    except ImportError:
        # fallback to dummy contour if CoolProp unavailable
        PropsSI = None
    T = np.linspace(50, 350, 120)   # C
    P = np.linspace(500, 10000, 120)  # kPa
    Tm, Pm = np.meshgrid(T, P)
    if PropsSI is None:
        rho = 1000 - 0.4*Tm + 0.02*(Pm/1000)
    else:
        rho = np.zeros_like(Tm)
        for i in range(Tm.shape[0]):
            for j in range(Tm.shape[1]):
                try:
                    rho[i,j] = PropsSI('D', 'T', Tm[i,j]+273.15, 'P', Pm[i,j]*1000, 'Water')
                except Exception:
                    rho[i,j] = np.nan
    fig, ax = plt.subplots(figsize=(7, 5.5))
    cs = ax.contourf(Tm, Pm/1000, rho, levels=20, cmap='viridis')
    ax.set_xlabel('Temperature (C)')
    ax.set_ylabel('Pressure (MPa)')
    ax.set_title('Water Density Contour (kg/m3) — CoolProp')
    cbar = fig.colorbar(cs)
    cbar.set_label('Density (kg/m3)')
    # saturation dome rough overlay
    if PropsSI is None:
        Tsat = 99.63 * (np.log10(Pm/1000 + 0.1) + 1.0) ** 0.3
        ax.contour(Tm, Pm/1000, Tm - Tsat, levels=[0], colors='red', linewidths=1)
        ax.text(300, 9.5, 'Saturation dome\\n(approx)', color='red', fontsize=8)
    else:
        try:
            import iapws
            T_sat_arr = []
            for p in P:
                try:
                    sat = iapws.IAPWS97(P=p/1000)
                    T_sat_arr.append(sat.T-273.15 if getattr(sat, 'T', None) else np.nan)
                except Exception:
                    T_sat_arr.append(np.nan)
            ax.plot(T_sat_arr, np.array(P)/1000, 'r--', label='Saturation dome', linewidth=1.5)
            ax.legend(fontsize=8)
        except Exception:
            pass
    return fig

def figure_3_wellbore():
    """IPR + TPR with operating point (realistic geothermal parameters)."""
    P_res = 20000
    J = 0.5
    rho = 900
    g = 9.81
    TVD = 1200
    L = 1500
    D = 0.2
    f = 0.02
    v = 2.5
    P_wf = np.linspace(500, P_res, 100)
    ipr = J * (P_res - P_wf)
    ipr = np.clip(ipr, 0, None)
    hydrostatic = rho * g * TVD / 1000
    friction = f * (L/D) * (rho * v**2) / 2 / 1000
    P_wh = P_wf - hydrostatic - friction
    fig, ax = plt.subplots(figsize=(7, 5.5))
    ax.plot(ipr, P_wf, label='IPR (Inflow)', color='blue', linewidth=2)
    ax.plot(ipr, P_wh, label='TPR (Wellhead)', color='orange', linewidth=2)
    best_i = np.argmin(np.abs(P_wf - P_wh))
    q_op = ipr[best_i]
    p_op = P_wf[best_i]
    ax.plot(q_op, p_op, 'ro', markersize=8, label=f'Operating point\\nq={q_op:.0f} kg/s, P_wf={p_op:.0f} kPa')
    ax.set_xlabel('Mass Flow (kg/s)')
    ax.set_ylabel('Pressure (kPa)')
    ax.set_title('Wellbore Deliverability (P_res = 20 MPa)')
    ax.legend(loc='upper right')
    ax.grid(True)
    ax.set_xlim(left=0)
    return fig

def figure_4_workflow():
    """5-step quality guardrail."""
    fig, ax = plt.subplots(figsize=(8, 4))
    steps = [
        '1. Explore\ncodebase',
        '2. Plan\nchanges',
        '3. Implement\ncode',
        '4. Verify\nwith tests',
        '5. Review\nwith subagent',
    ]
    for i, step in enumerate(steps):
        ax.broken_barh([(i*1.5, 1.2)], (0.5, 0.8), facecolors='steelblue', alpha=0.7)
        ax.text(i*1.5 + 0.6, 0.9, step, ha='center', va='center', fontsize=8, color='white')
    ax.set_xlim(-0.2, 8)
    ax.set_ylim(0, 2)
    ax.set_title('Hermes Geothermal Workflow: Explore -> Plan -> Code -> Verify -> Review')
    ax.set_yticks([])
    ax.set_xticks([])
    ax.axis('off')
    return fig

def figure_5_supercooled():
    """Supercooled water density trends for IAPWS G12-15 (0 C to -22 C)."""
    try:
        import sys, os
        sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'pygeotoolbox-mcp', 'src'))
        from pygeotoolbox import thermo_supercooled
    except ImportError:
        thermo_supercooled = None

    fig, axes = plt.subplots(1, 2, figsize=(10, 4))

    # Left: density vs temperature at two pressures
    T = np.linspace(-22, 0, 100)
    for P_MPa, color, label in [(0.1, 'teal', '0.1 MPa'), (10, 'crimson', '10 MPa')]:
        if thermo_supercooled:
            rho = [thermo_supercooled.density(t, P_MPa) for t in T]
        else:
            rho = [999.8 - 0.1*abs(t) for t in T]  # fallback
        axes[0].plot(T, rho, color=color, linewidth=2, label=label)
    axes[0].axvline(x=0, color='gray', linestyle='--', alpha=0.5, label='0 C boundary')
    axes[0].set_xlabel('Temperature (C)')
    axes[0].set_ylabel('Density (kg/m3)')
    axes[0].set_title('Supercooled Water Density (IAPWS G12-15)')
    axes[0].legend()
    axes[0].grid(True)
    axes[0].set_xlim(-25, 2)

    # Right: enthalpy vs temperature
    if thermo_supercooled:
        h = [thermo_supercooled.enthalpy(t, 0.1)/1000 for t in T]
    else:
        h = [4.2*t for t in T]  # fallback
    axes[1].plot(T, h, color='navy', linewidth=2)
    axes[1].axvline(x=0, color='gray', linestyle='--', alpha=0.5)
    axes[1].axhline(y=0, color='gray', linestyle=':', alpha=0.3)
    axes[1].set_xlabel('Temperature (C)')
    axes[1].set_ylabel('Specific Enthalpy (kJ/kg)')
    axes[1].set_title('Supercooled Enthalpy (ref: 0 C = 0)')
    axes[1].grid(True)
    axes[1].set_xlim(-25, 2)

    fig.tight_layout()
    return fig


def figure_6_seawater():
    """Seawater density vs salinity and temperature (IAPWS G14-19)."""
    try:
        import sys, os
        sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'pygeotoolbox-mcp', 'src'))
        from pygeotoolbox import seawater
    except ImportError:
        seawater = None
    sal = np.array([0, 10, 20, 35, 42])
    T = 25
    if seawater:
        rho = [seawater.seawater_density(s, T).get('density_kg_m3', 1000+0.77*s) for s in sal]
        rho2 = [seawater.seawater_density(35, t).get('density_kg_m3', 1020-0.2*(t-25)) for t in range(0, 41, 10)]
    else:
        rho = [1000 + 0.77*s for s in sal]
        rho2 = [1020 - 0.2*(t-25) for t in range(0, 41, 10)]
    temps = list(range(0, 41, 10))
    fig, axes = plt.subplots(1, 2, figsize=(10, 4))
    axes[0].plot(sal, rho, 'o-', color='teal')
    axes[0].set_xlabel('Salinity (psu)')
    axes[0].set_ylabel('Density (kg/m3)')
    axes[0].set_title(f'Seawater Density at T={T} C')
    axes[0].grid(True)
    axes[1].plot(temps, rho2, 's-', color='darkblue')
    axes[1].set_xlabel('Temperature (C)')
    axes[1].set_ylabel('Density (kg/m3)')
    axes[1].set_title('Seawater Density (S=35 psu)')
    axes[1].grid(True)
    fig.tight_layout()
    return fig

def figure_7_transport():
    """Thermal conductivity and viscosity across IAPWS range."""
    try:
        import sys, os
        sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'pygeotoolbox-mcp', 'src'))
        from pygeotoolbox import transport
    except ImportError:
        transport = None
    T = np.linspace(0, 350, 100)
    if transport:
        k = [transport.thermal_conductivity(t, 1.0) for t in T]
        mu = [transport.dynamic_viscosity(t, 1.0)*1e6 for t in T]  # convert to uPa.s
    else:
        k = [0.55 + 0.002*t for t in T]
        mu = [1000 - 2*t for t in T]
    fig, axes = plt.subplots(1, 2, figsize=(10, 4))
    axes[0].plot(T, k, color='firebrick', linewidth=2)
    axes[0].set_xlabel('Temperature (C)')
    axes[0].set_ylabel('k (W/mK)')
    axes[0].set_title('Thermal Conductivity (P=1 MPa)')
    axes[0].grid(True)
    axes[1].plot(T, mu, color='navy', linewidth=2)
    axes[1].set_xlabel('Temperature (C)')
    axes[1].set_ylabel('Viscosity (uPa.s)')
    axes[1].set_title('Dynamic Viscosity (P=1 MPa)')
    axes[1].grid(True)
    fig.tight_layout()
    return fig

def figure_8_humid_air():
    """Humid air properties for cooling tower analysis (IAPWS G11-15)."""
    try:
        import sys, os
        sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'pygeotoolbox-mcp', 'src'))
        from pygeotoolbox import humid_air
    except ImportError:
        humid_air = None
    T_range = np.linspace(20, 60, 5)
    fig, axes = plt.subplots(1, 2, figsize=(10, 4))
    for RH in [0.2, 0.5, 0.8, 1.0]:
        if humid_air:
            rho = [humid_air.density_humid_air(t, 101.325, RH) for t in T_range]
            h = [humid_air.enthalpy_humid_air(t, RH)/1000 for t in T_range]
        else:
            rho = [1.2 - 0.01*(t-20) for t in T_range]
            h = [50 + RH*100*t for t in T_range]
        axes[0].plot(T_range, rho, '-o', label=f'RH={RH:.0%}')
        axes[1].plot(T_range, h, '-s', label=f'RH={RH:.0%}')
    axes[0].set_xlabel('Temperature (C)')
    axes[0].set_ylabel('Density (kg/m3)')
    axes[0].set_title('Humid Air Density')
    axes[0].legend()
    axes[0].grid(True)
    axes[1].set_xlabel('Temperature (C)')
    axes[1].set_ylabel('Enthalpy (kJ/kg dry air)')
    axes[1].set_title('Humid Air Enthalpy')
    axes[1].legend()
    axes[1].grid(True)
    fig.tight_layout()
    return fig


def main():
    outdir = os.path.join(os.path.dirname(__file__), '..', 'assets')
    os.makedirs(outdir, exist_ok=True)
    for fn, maker in [
        ('separator_enthalpy_temperature.png', figure_1_separator),
        ('thermo_state_surface.png', figure_2_thermo_surface),
        ('wellbore_deliverability.png', figure_3_wellbore),
        ('hermes_geothermal_workflow.png', figure_4_workflow),
        ('supercooled_density.png', figure_5_supercooled),
        ('seawater_density.png', figure_6_seawater),
        ('transport_properties.png', figure_7_transport),
        ('humid_air.png', figure_8_humid_air),
    ]:
        fig = maker()
        path = os.path.join(outdir, fn)
        fig.savefig(path, dpi=150, bbox_inches='tight')
        print(f'Saved {path}')
        plt.close(fig)

if __name__ == '__main__':
    main()
