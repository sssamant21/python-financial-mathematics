"""Independent analytic reference checks for Book 02 Section 18.9."""
import math
from section_18_09 import assessment,solve,finite,zero_coupon,one_period_npv

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
    for key,expected in (("zero_coupon",math.sqrt(10/9)-1),
                         ("one_period_npv",0.1)):
        result=a[key]
        assert result["status"] in ("converged","exact_root")
        near(result["root"],expected)
        lo,hi=result["bracket"]
        assert lo-1e-12<=expected<=hi+1e-12
        assert result["width"]<=result["tolerances"]["atol"]+result["tolerances"]["rtol"]*max(abs(lo),abs(hi))
        assert result["function_evaluations"]>=2
        assert result["iterations"]==len(result["trace"])
        assert result["newton_steps"]+result["bisection_steps"]==len(result["trace"])
        assert result["runtime_certified"] is False
    near(zero_coupon(0),100)
    near(zero_coupon(0.2),1000/1.44-900)
    near(one_period_npv(0.1),0)
    endpoint=solve(lambda x:x-1,lambda x:1,1,2)
    assert endpoint["status"]=="endpoint_root"
    fallback=solve(lambda x:x*x-2,lambda x:0,1,2)
    assert fallback["bisection_steps"]>0
    near(fallback["root"],math.sqrt(2))
    exhausted=solve(lambda x:x*x-2,lambda x:0,1,2,1e-16,0,1)
    assert exhausted["status"]=="max_iter"
    x=1.0
    y=math.nextafter(x,2.0)
    stagnated=solve(lambda z:-1 if z==x else 1,lambda z:0,x,y,1e-20,0,5)
    assert stagnated["status"]=="stagnation"
    rejects(ValueError,solve,lambda x:x*x+1,lambda x:2*x,-1,1)
    rejects(ValueError,solve,lambda x:float("nan"),lambda x:1,-1,1)
    rejects(ValueError,solve,lambda x:x,lambda x:1,2,1)
    rejects(ValueError,solve,lambda x:x,lambda x:1,-1,1,0)
    rejects(TypeError,finite,True,"value")
    assert a["runtime_certified"] is False
    assert a["independent_review_completed"] is False
    print("PASS: Section 18.9 independent analytic reference checks")

if __name__=="__main__":
    run()
