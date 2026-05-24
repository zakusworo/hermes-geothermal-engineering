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
    """Density contour in T-P space (placeholder).
    In real work, compute via CoolProp."""
    T = np.linspace(50, 350, 200)   # C
    P = np.linspace(500, 10000, 200)  # kPa
    Tm, Pm = np.meshgrid(T, P)
    # Placeholder: approximate single-phase liquid density decreasing with T and P
    rho = 1000 - 0.4 * Tm + 0.02 * (Pm / 1000)
    fig, ax = plt.subplots(figsize=(6, 5))
    cs = ax.contourf(Tm, Pm/1000, rho, levels=20, cmap='viridis')
    ax.set_xlabel('Temperature (C)')
    ax.set_ylabel('Pressure (MPa)')
    ax.set_title('Approximate Density Contour (kg/m3)')
    cbar = fig.colorbar(cs)
    cbar.set_label('Density (kg/m3)')
    # Annotate boiling curve (very rough Tsat approximation)
    Tsat = 99.63 * (np.log10(Pm/1000 + 0.1) + 1.0) ** 0.3
    ax.contour(Tm, Pm/1000, Tm - Tsat, levels=[0], colors='red', linewidths=1)
    ax.text(300, 9.5, 'Saturation dome\n(approx)', color='red', fontsize=8)
    return fig

def figure_3_wellbore():
    """IPR + TPR with operating point."""
    P_wf = np.linspace(500, 3000, 100)
    P_res = 3000
    J = 0.5
    ipr = J * (P_res - P_wf)
    ipr = np.clip(ipr, 0, None)
    # TPR (simplified)
    rho = 900
    g = 9.81
    TVD = 800
    f = 0.02
    L = 1000
    D = 0.2
    v = 2.5
    hydrostatic = rho * g * TVD / 1000
    friction = f * (L/D) * (rho * v**2) / 2 / 1000
    P_wh = P_wf - hydrostatic - friction
    # Only plot region where IPR = TPR approximate intersection
    fig, ax = plt.subplots(figsize=(6, 5))
    ax.plot(ipr, P_wf, label='IPR (Inflow)', color='blue')
    ax.plot(ipr, P_wh, label='TPR (Wellhead)', color='orange')
    # Find approximate intersection by brute force
    best_i = np.argmin(np.abs(P_wf - P_wh))
    q_op = ipr[best_i]
    p_op = P_wf[best_i]
    ax.plot(q_op, p_op, 'ro', label=f'Operating point\nq={q_op:.0f} kg/s, P_wf={p_op:.0f} kPa')
    ax.set_xlabel('Mass Flow (kg/s)')
    ax.set_ylabel('Pressure (kPa)')
    ax.set_title('Wellbore Deliverability')
    ax.legend()
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
