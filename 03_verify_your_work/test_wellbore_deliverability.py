"""Tests for Exercise 3: wellbore deliverability."""
from wellbore_deliverability import ipr_mass_flow, tpr_wellhead_pressure, operating_point

def test_ipr_positive():
    q = ipr_mass_flow(P_res_kPa=20000, P_wf_kPa=19000, J_kg_s_kPa=0.5)
    assert q == 500.0
    assert q > 0

def test_ipr_zero_at_equal_pressure():
    q = ipr_mass_flow(20000, 20000, 0.5)
    assert q == 0.0

def test_ipr_zero_when_pwf_above_pres():
    q = ipr_mass_flow(20000, 21000, 0.5)
    assert q == 0.0, "IPR must not return negative flow"

def test_tpr_wellhead_less_than_bottomhole():
    wh = tpr_wellhead_pressure(18000, rho_avg_kg_m3=900, TVD_m=1200, L_m=1500, D_m=0.2, f_Darcy=0.02, v_ms=2.5)
    assert wh < 18000, "Wellhead must be lower than bottomhole"
    assert wh > 0, "Wellhead must be positive"

def test_operating_point_found():
    q_op, p_wf_op, p_wh_op, ipr, tpr = operating_point(
        P_res_kPa=20000, J_kg_s_kPa=0.5, rho_avg_kg_m3=900,
        TVD_m=1200, L_m=1500, D_m=0.2, f_Darcy=0.02, v_ms=2.5)
    assert q_op > 0, f"Operating flow must be positive, got {q_op}"
    assert 0 < p_wf_op < 20000, f"Operating P_wf out of range: {p_wf_op}"
    assert p_wh_op > 0, f"Operating P_wh must be positive, got {p_wh_op}"

def test_ipr_monotonic_with_pressure():
    P_res = 20000
    J = 0.5
    q_low = ipr_mass_flow(P_res, 5000, J)
    q_high = ipr_mass_flow(P_res, 15000, J)
    assert q_low > q_high, "Lower flowing pressure should yield higher flow"
