"""Independent checks for Chapter 10 integrated assessment."""
import math
from section_10_10 import assessment
from section_10_09 import Stream,Curve,analytic_pv,numerical_pv,discrete_pv
from section_10_07 import integrate
from section_10_06 import perpetuity_pv,tail_value

def close(a,b,rel_tol=1e-9,abs_tol=1e-7):
    assert math.isclose(a,b,rel_tol=rel_tol,abs_tol=abs_tol),(a,b)

def rejects(exc,fn,*args):
    try:
        fn(*args)
    except exc:
        return
    raise AssertionError("expected "+exc.__name__)

def run():
    report=assessment()
    e=report["examples"]
    close(e["accumulation_linear"],1470)
    close(e["fundamental_theorem_at_2"],1280/3)
    close(e["substitution_integral"],1-math.exp(-4))
    close(e["level_stream_pv"],analytic_pv(Stream("constant",1500),Curve(0.04),4))
    close(e["growing_stream_pv"],analytic_pv(Stream("exponential",800,0.025),Curve(0.05),5))
    close(e["growth_matches_discount_pv"],analytic_pv(Stream("exponential",800,0.05),Curve(0.05),5))
    close(e["zero_rate_linear_pv"],analytic_pv(Stream("linear",1000,100),Curve(0),2))
    close(e["level_perpetuity_pv"],perpetuity_pv(900,0,0.045))
    close(e["growing_perpetuity_pv"],perpetuity_pv(1200,0.02,0.06))
    close(e["tail_one_percent_years"],math.log(100)/0.04)
    close(e["discrete_two_payments_pv"],discrete_pv([(1,500),(2,500)],Curve(0.05)))
    close(e["quadrature_midpoint"],0.3125)
    close(e["quadrature_trapezoid"],0.375)
    close(e["quadrature_simpson"],1/3)
    case=report["integrated_case"]
    grids=case["simpson_reconciliation"]
    assert len(grids)==3
    assert grids[-1]["absolute_error"]<1e-6
    assert grids[-1]["absolute_error"]<=grids[0]["absolute_error"]+1e-10
    assert case["flat_rate_derivative_1bp_bump"]<0
    assert case["affine_rate_derivative_1bp_bump"]<0
    assert case["affine_numerical_total"]>0
    rejects(ValueError,perpetuity_pv,1000,0.05,0.05)
    rejects(ValueError,integrate,lambda t:t,0,1,3,"simpson")
    rejects(ValueError,analytic_pv,Stream("constant",1000),Curve(0.03,0.005),4)
    assert report["runtime_certified"] is False
    assert report["independent_review_completed"] is False
    print("PASS: Section 10.10 independent reference checks")

if __name__=="__main__":
    run()
