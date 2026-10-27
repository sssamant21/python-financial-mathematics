"""Independent analytic reference checks for Book 02 Section 18.8."""
import math
from section_18_08 import assessment,audited_bisection,finite,zero_coupon_residual

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
    d=a["result"]
    exact=math.sqrt(10/9)-1
    assert d["status"] in ("converged","exact_root")
    near(d["root"],exact)
    assert d["bracket"][0]-1e-12<=exact<=d["bracket"][1]+1e-12
    assert d["width"]<=d["atol"]+d["rtol"]*max(abs(x) for x in d["bracket"])
    assert d["evaluations"]>=d["iterations"]+2
    assert d["bracket_invariant"] is True
    near(zero_coupon_residual(0),100)
    near(zero_coupon_residual(0.2),1000/1.44-900)
    for prev,curr in zip(d["trace"],d["trace"][1:]):
        assert curr["width"]<=prev["width"]
    endpoint=audited_bisection(lambda x:x-1,1,2)
    assert endpoint["status"]=="endpoint_root"
    exhausted=audited_bisection(lambda x:x*x-2,1,2,1e-16,0,1)
    assert exhausted["status"]=="max_iter"
    assert exhausted["bracket_invariant"]
    # Adjacent floating-point numbers cannot be bisected.
    x=1.0
    y=math.nextafter(x,2.0)
    stagnant=audited_bisection(lambda z:-1 if z==x else 1,x,y,1e-20,0,5)
    assert stagnant["status"]=="stagnation"
    rejects(ValueError,audited_bisection,lambda x:x*x+1,-1,1)
    rejects(ValueError,audited_bisection,lambda x:float("nan"),-1,1)
    rejects(ValueError,audited_bisection,lambda x:x,2,1)
    rejects(TypeError,finite,True,"value")
    assert a["runtime_certified"] is False
    assert a["independent_review_completed"] is False
    print("PASS: Section 18.8 independent analytic reference checks")

if __name__=="__main__":
    run()
