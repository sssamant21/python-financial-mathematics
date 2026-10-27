"""Independent analytic reference checks for Book 02 Section 15.10."""
import math
from section_15_10 import assessment,finite

def close(a,b):
    assert math.isclose(a,b,rel_tol=1e-9,abs_tol=1e-8),(a,b)

def rejects(exc,fn,*args):
    try:
        fn(*args)
    except exc:
        return
    raise AssertionError("expected "+exc.__name__)

def run():
    a=assessment()
    assert a["worked_exercises"]==50
    assert a["hands_on_steps"]==12
    close(a["polynomial_base"],15)
    close(a["polynomial_gradient"][0],8)
    close(a["polynomial_gradient"][1],11)
    assert a["polynomial_hessian"]==((2.0,3.0),(3.0,4.0))
    close(a["polynomial_exact_change"],-1.37)
    e=math.exp(0.1)
    d=math.exp(-0.1)
    close(a["engine_base_values"][0],1000*e)
    close(a["engine_base_values"][1],500*d)
    close(a["engine_exact_changes"][0],1100*math.exp(0.15)-1000*e)
    close(a["engine_exact_changes"][1],550*math.exp(-0.15)-500*d)
    close(a["engine_first_order_changes"][0],145*e)
    close(a["engine_first_order_changes"][1],27.5*d)
    close(a["engine_portfolio_exact_change"],sum(a["engine_exact_changes"]))
    close(a["iso_value_slope"],-40)
    close(a["iso_variance_slope"],-2/3)
    close(a["feasible_variance_derivative"],-0.028)
    close(a["future_value_taylor_change"],0.0510125*1000*e)
    rejects(ValueError,finite,{"bad":float("nan")})
    assert a["runtime_certified"] is False
    assert a["independent_review_completed"] is False
    print("PASS: Section 15.10 independent reference checks")

if __name__=="__main__":
    run()
