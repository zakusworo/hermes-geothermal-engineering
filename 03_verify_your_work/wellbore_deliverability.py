"""
Wellbore deliverability: IPR + TPR for geothermal well.
Uses pygeotoolbox-mcp wellbore module for tested, SI-unit calculations.
"""
try:
    from pygeotoolbox import wellbore as _wellbore
    ipr_mass_flow = _wellbore.ipr_mass_flow
    tpr_wellhead_pressure = _wellbore.tpr_wellhead_pressure
    operating_point = _wellbore.operating_point
except ImportError:
    # Inline fallback if pygeotoolbox not installed
    def ipr_mass_flow(P_res_kPa, P_wf_kPa, J_kg_s_kPa):
        q = J_kg_s_kPa * max(P_res_kPa - P_wf_kPa, 0.0)
        return q

    def tpr_wellhead_pressure(P_wf_kPa, rho_avg_kg_m3, TVD_m, L_m, D_m, f_Darcy, v_ms, g=9.81):
        hydrostatic_Pa = rho_avg_kg_m3 * g * TVD_m
        friction_Pa = f_Darcy * (L_m / max(D_m, 1e-6)) * (rho_avg_kg_m3 * v_ms ** 2) / 2.0
        return P_wf_kPa - (hydrostatic_Pa + friction_Pa) / 1000.0

    def operating_point(P_res_kPa, J_kg_s_kPa, rho_avg_kg_m3, TVD_m, L_m, D_m, f_Darcy, v_ms, num_points=200):
        ipr_curve = []
        tpr_curve = []
        best = (0.0, P_res_kPa, P_res_kPa)
        best_err = float('inf')
        for i in range(1, num_points):
            frac = i / num_points
            P_wf = P_res_kPa * (1.0 - frac)
            q = ipr_mass_flow(P_res_kPa, P_wf, J_kg_s_kPa)
            P_wh = tpr_wellhead_pressure(P_wf, rho_avg_kg_m3, TVD_m, L_m, D_m, f_Darcy, v_ms)
            ipr_curve.append((P_wf, q))
            tpr_curve.append((P_wf, P_wh))
            err = abs(P_wf - P_wh)
            if err < best_err:
                best_err = err
                best = (q, P_wf, P_wh)
        return (*best, ipr_curve, tpr_curve)
