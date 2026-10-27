"""Independent analytic reference checks for Book 02 Section 18.4."""
import math
from section_18_04 import (assessment,finite,safeguarded_newton,
                           zero_coupon,zero_coupon_derivative,npv,npv_derivative)

def near(a,b,tol=1e-9):
    assert math.isclose(a,b,rel_tol=1e-10,abs_tol=tol),(a,b)

def rejects(exc,fn,*args):
    try:
        fn(*args)
    except exc:
        return
    raise AssertionError("expected "+exc.__name__)

def run():
    a=assessment()
    expected=(10/9)**0.5-1
    y=a["zero_coupon"]
    assert y["status"] in ("converged","exact_root")
    near(y["root"],expected)
    assert y["bracket"][0]-1e-12<=expected<=y["bracket"][1]+1e-12
    assert y["width"]<1e-9
    near(zero_coupon(0),100)
    near(zero_coupon(0.2),1000/1.44-900)
    near(zero_coupon_derivative(0),-2000)
    n=a["npv"]
    assert n["status"] in ("converged","exact_root")
    near(n["root"],0.1)
    near(npv(0.1),0)
    near(npv_derivative(0.1),-1100/1.21)
    # A zero derivative must trigger a safe midpoint fallback.
    fallback=safeguarded_newton(lambda x:x*x-2,lambda x:0.0,1,2)
    assert fallback["status"] in ("converged","exact_root")
    near(fallback["root"],math.sqrt(2))
    assert fallback["bisection_steps"]>0
    # Endpoint root, invalid bracket, nonfinite derivative, and exhaustion.
    endpoint=safeguarded_newton(lambda x:x-1,lambda x:1,1,2)
    assert endpoint["status"]=="endpoint_root"
    rejects(ValueError,safeguarded_newton,lambda x:x*x+1,lambda x:2*x,-1,1)
    rejects(ValueError,safeguarded_newton,lambda x:x,lambda x:1,2,1)
    rejects(ValueError,safeguarded_newton,lambda x:x-0.25,lambda x:float("nan"),-1,1)
    rejects(ValueError,zero_coupon,-1)
    rejects(TypeError,finite,True,"value")
    exhausted=safeguarded_newton(lambda x:x*x-2,lambda x:0,1,2,1e-15,0,1)
    assert exhausted["status"]=="max_iter"
    assert a["runtime_certified"] is False
    assert a["independent_review_completed"] is False
    print("PASS: Section 18.4 independent analytic reference checks")

if __name__=="__main__":
    run()
