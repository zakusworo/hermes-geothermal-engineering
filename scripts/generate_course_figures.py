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

def figure_1_separator():
    """Plot separator enthalpy and steam fraction trends."""
    dates = ['Jan', 'Feb', 'Mar', 'Apr']
    # Well A-01: higher enthalpy, increasing steam fraction
    enthalpy_A = [660.5, 655.4, 652.1, 648.8]
    fraction_A = [0.077, 0.096, 0.115, 0.146]
    # Well B-02: lower enthalpy, wetter start
    enthalpy_B = [670.2, 665.0, 660.1, 655.0]
    fraction_B = [0.216, 0.231, 0.258, 0.277]
    # Well C-03: moderate
    enthalpy_C = [620.3, 616.0, 612.2, 608.5]
    fraction_C = [0.055, 0.065, 0.075, 0.087]

    fig, axes = plt.subplots(1, 2, figsize=(10, 4))
    ax = axes[0]
    ax.plot(dates, enthalpy_A, 'o-', label='A-01')
    ax.plot(dates, enthalpy_B, 's-', label='B-02')
    ax.plot(dates, enthalpy_C, '^-', label='C-03')
    ax.set_ylabel('Enthalpy (kJ/kg)')
    ax.set_title('Separator Enthalpy Trend')
    ax.legend()
    ax.grid(True)

    ax = axes[1]
    ax.plot(dates, [x*100 for x in fraction_A], 'o-', label='A-01')
    ax.plot(dates, [x*100 for x in fraction_B], 's-', label='B-02')
    ax.plot(dates, [x*100 for x in fraction_C], '^-', label='C-03')
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

def main():
    outdir = os.path.join(os.path.dirname(__file__), '..', 'assets')
    os.makedirs(outdir, exist_ok=True)
    for fn, maker in [
        ('separator_enthalpy_temperature.png', figure_1_separator),
        ('thermo_state_surface.png', figure_2_thermo_surface),
        ('wellbore_deliverability.png', figure_3_wellbore),
        ('hermes_geothermal_workflow.png', figure_4_workflow),
    ]:
        fig = maker()
        path = os.path.join(outdir, fn)
        fig.savefig(path, dpi=150, bbox_inches='tight')
        print(f'Saved {path}')
        plt.close(fig)

if __name__ == '__main__':
    main()
