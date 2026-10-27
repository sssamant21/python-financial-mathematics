"""Independent analytical reference checks for Book 02 Section 18.10."""
import math
from section_18_10 import assessment,finite,zero_price,npv,bisect,interpolate,central_derivative,simpson

def near(a,b,tol=1e-9):
    assert math.isclose(a,b,rel_tol=1e-9,abs_tol=tol),(a,b)

def rejects(exc,fn,*args):
    try:
        fn(*args)
    except exc:
        return
    raise AssertionError("expected "+exc.__name__)

def run():
    a=assessment()
    near(a["yield_reference"],math.sqrt(10/9)-1)
    y=a["yield_solution"]
    assert y["status"] in ("converged","exact_root")
    near(y["root"],math.sqrt(10/9)-1)
    assert y["bracket"][0]-1e-12<=a["yield_reference"]<=y["bracket"][1]+1e-12
    roots=a["multiple_irr_solutions"]
    near(roots[0]["root"],0.1)
    near(roots[1]["root"],0.2)
    near(npv(0,(-100,230,-132)),-2)
    near(npv(0.1,(-100,230,-132)),0)
    near(npv(0.2,(-100,230,-132)),0)
    near(a["rate_interpolation"],0.045)
    near(a["discount_interpolation"],(1/1.04+1/(1.05**3))/2)
    near(a["duration_estimate"],2/1.05,tol=1e-7)
    near(a["continuous_pv_reference"],100*(-math.expm1(-0.15))/0.03)
    near(a["simpson_continuous_pv"],a["continuous_pv_reference"],tol=1e-8)
    near(central_derivative(lambda x:x*x,2,0.01),4)
    near(simpson(lambda x:x**3,0,2,2),4)
    rejects(ValueError,zero_price,-1)
    rejects(ValueError,npv,-1,(-100,110))
    rejects(ValueError,bisect,lambda x:x*x+1,-1,1)
    rejects(ValueError,interpolate,1,2,1,3,1)
    rejects(ValueError,simpson,lambda x:x,0,1,3)
    rejects(TypeError,finite,True,"value")
    assert a["runtime_certified"] is False
    assert a["independent_review_completed"] is False
    print("PASS: Section 18.10 independent analytical reference checks")

if __name__=="__main__":
    run()
