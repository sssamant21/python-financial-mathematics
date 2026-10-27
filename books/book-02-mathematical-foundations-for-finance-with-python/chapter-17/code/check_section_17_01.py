"""Independent analytic reference checks for Book 02 Section 17.1."""
import math
from section_17_01 import (assessment,finite,variance,feasibility,
                           minimum_variance_full_investment)

def near(a,b):
    assert math.isclose(a,b,rel_tol=1e-10,abs_tol=1e-10),(a,b)

def rejects(exc,fn,*args,**kwargs):
    try:
        fn(*args,**kwargs)
    except exc:
        return
    raise AssertionError("expected "+exc.__name__)

def run():
    a=assessment()
    near(variance(0.6,0.4),0.0336)
    near(variance(0,0),0)
    near(a["full_investment"]["w1"],8/11)
    near(a["full_investment"]["w2"],3/11)
    near(a["capped"]["w1"],0.6)
    near(a["capped"]["w2"],0.4)
    assert a["full_investment"]["feasibility"]["feasible"]
    assert a["capped"]["feasibility"]["feasible"]
    assert a["example"]["feasible"]
    assert "w1_cap" in a["example"]["active_inequalities"]
    assert not a["infeasible_example"]["feasible"]
    near(a["infeasible_example"]["maximum_inequality_violation"],0.2)
    assert not feasibility(0,0)["feasible"]
    assert "w2_lower" in feasibility(1,0)["active_inequalities"]
    rejects(TypeError,finite,True,"x")
    rejects(ValueError,feasibility,0.5,0.5,cap1=1.2)
    rejects(ValueError,minimum_variance_full_investment,0.4,0.4)
    assert a["runtime_certified"] is False
    assert a["independent_review_completed"] is False
    print("PASS: Section 17.1 independent analytic reference checks")

if __name__=="__main__":
    run()
