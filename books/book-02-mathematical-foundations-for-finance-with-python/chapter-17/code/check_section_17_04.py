"""Independent analytic reference checks for Book 02 Section 17.4."""
import math
from section_17_04 import (TRANSITION,assessment,finite,variance,
                           optimal_portfolio,kkt_report,value_function,shadow_price)

def near(a,b):
    assert math.isclose(a,b,rel_tol=1e-10,abs_tol=1e-9),(a,b)

def rejects(exc,fn,*args):
    try:
        fn(*args)
    except exc:
        return
    raise AssertionError("expected "+exc.__name__)

def run():
    a=assessment()
    near(a["transition"],8/11)
    assert len(a["cases"])==4
    assert all(c["kkt"]["passes"] for c in a["cases"])
    binding=optimal_portfolio(0.6)
    assert binding["regime"]=="binding"
    near(binding["weights"][0],0.6)
    near(binding["weights"][1],0.4)
    near(binding["variance"],0.0336)
    near(binding["lambda"],-0.084)
    near(shadow_price(0.6),0.028)
    assert 2 in kkt_report(binding)["active"]
    transition=optimal_portfolio(TRANSITION)
    assert transition["regime"]=="weakly_active_transition"
    near(transition["multipliers"][2],0)
    assert 2 in kkt_report(transition)["active"]
    inactive=optimal_portfolio(0.9)
    assert inactive["regime"]=="inactive"
    near(inactive["weights"][0],8/11)
    near(inactive["weights"][1],3/11)
    near(inactive["multipliers"][2],0)
    assert 2 not in kkt_report(inactive)["active"]
    endpoint=optimal_portfolio(0)
    assert endpoint["regime"]=="degenerate_endpoint"
    assert 0 in kkt_report(endpoint)["active"]
    assert 2 in kkt_report(endpoint)["active"]
    eps=1e-5
    derivative=(value_function(0.6+eps)-value_function(0.6-eps))/(2*eps)
    near(derivative,-shadow_price(0.6))
    near(variance(0.6,0.4),0.0336)
    rejects(TypeError,finite,True,"value")
    rejects(ValueError,optimal_portfolio,-0.1)
    rejects(ValueError,optimal_portfolio,1.1)
    rejects(ValueError,kkt_report,binding,-1)
    assert a["runtime_certified"] is False
    assert a["independent_review_completed"] is False
    print("PASS: Section 17.4 independent analytic reference checks")

if __name__=="__main__":
    run()
