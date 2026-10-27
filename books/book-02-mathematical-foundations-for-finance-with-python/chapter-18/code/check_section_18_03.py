"""Independent analytic reference checks for Book 02 Section 18.3."""
import math
from section_18_03 import (assessment,finite,bisection,opposite_signs,
                           zero_coupon_residual,npv_residual)

def near(a,b,abs_=1e-10):
    assert math.isclose(a,b,rel_tol=1e-10,abs_tol=abs_),(a,b)

def rejects(exc,fn,*args):
    try:
        fn(*args)
    except exc:
        return
    raise AssertionError("expected "+exc.__name__)

def run():
    a=assessment()
    expected=math.sqrt(10/9)-1
    near(a["yield_analytical"],expected)
    y=a["yield_solution"]
    assert y["status"] in ("converged","exact_root")
    near(y["root"],expected)
    assert y["bracket"][0]-1e-12<=expected<=y["bracket"][1]+1e-12
    assert y["width"]<=1e-9
    near(zero_coupon_residual(0),100)
    near(zero_coupon_residual(0.2),1000/1.44-900)
    assert opposite_signs(*a["yield_initial_signs"])
    n=a["npv_solution"]
    assert n["status"] in ("converged","exact_root")
    near(n["root"],0.1)
    near(npv_residual(0.1),0)
    assert opposite_signs(-1,2)
    assert not opposite_signs(0,1)
    # Endpoints, invalid brackets, nonfinite evaluations, and exhaustion.
    end=bisection(lambda x:x-1,1,2)
    assert end["status"]=="endpoint_root" and end["root"]==1
    rejects(ValueError,bisection,lambda x:x*x+1,-1,1)
    rejects(ValueError,bisection,lambda x:x,2,1)
    rejects(ValueError,bisection,lambda x:float("nan"),-1,1)
    rejects(ValueError,zero_coupon_residual,-1)
    rejects(TypeError,finite,True,"value")
    short=bisection(lambda x:x*x-2,1,2,1e-15,0,1)
    assert short["status"]=="max_iter"
    assert a["runtime_certified"] is False
    assert a["independent_review_completed"] is False
    print("PASS: Section 18.3 independent analytic reference checks")

if __name__=="__main__":
    run()
