"""Independent analytic reference checks for Book 02 Section 18.6."""
import math
from section_18_06 import (assessment,finite,nodes,piecewise_linear,
                           lagrange,discount_factor,financial_comparison)

def near(a,b):
    assert math.isclose(a,b,rel_tol=1e-11,abs_tol=1e-12),(a,b)

def rejects(exc,fn,*args):
    try:
        fn(*args)
    except exc:
        return
    raise AssertionError("expected "+exc.__name__)

def run():
    a=assessment()
    near(a["linear_midpoint"],0.045)
    near(a["quadratic_interpolated"],1+1.5**2)
    near(a["extrapolated_rate"],0.055)
    for x,y in ((1,0.04),(3,0.05)):
        near(piecewise_linear((1,3),(0.04,0.05),x),y)
    for x in (0,1,2):
        near(lagrange((0,1,2),(1,2,5),x),1+x*x)
    f=a["financial"]
    d1=1/1.04
    d3=1/(1.05**3)
    near(f["discount_endpoints"][0],d1)
    near(f["discount_endpoints"][1],d3)
    near(f["discount_from_rate"],1/(1.045**2))
    near(f["discount_linear"],(d1+d3)/2)
    near(f["discount_log_linear"],math.sqrt(d1*d3))
    assert abs(f["discount_from_rate"]-f["discount_linear"])>1e-6
    assert abs(f["discount_log_linear"]-f["discount_linear"])>1e-6
    rejects(ValueError,piecewise_linear,(1,3),(0.04,0.05),4)
    rejects(ValueError,nodes,(1,1),(2,3))
    rejects(ValueError,nodes,(3,1),(2,3))
    rejects(ValueError,discount_factor,-1,2)
    rejects(ValueError,discount_factor,0.05,-1)
    rejects(TypeError,finite,True,"value")
    assert a["runtime_certified"] is False
    assert a["independent_review_completed"] is False
    print("PASS: Section 18.6 independent analytic reference checks")

if __name__=="__main__":
    run()
