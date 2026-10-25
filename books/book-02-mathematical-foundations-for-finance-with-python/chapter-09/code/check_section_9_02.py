"""Independent reference checks for Section 9.2."""
import math
from section_9_02 import (
    finite, point_elasticity, arc_elasticity, constant_elasticity_demand,
    linear_demand, income_elasticity, discounted_rate_elasticity,
    centered_elasticity)

def close(actual,expected,rel_tol=1e-7,abs_tol=1e-8):
    assert math.isclose(actual,expected,rel_tol=rel_tol,abs_tol=abs_tol),(actual,expected)

def rejects(exc,fn,*args):
    try:
        fn(*args)
    except exc:
        return
    raise AssertionError("expected "+exc.__name__)

def run():
    close(point_elasticity(2,8,12),3)
    for p in (1,5,10,20,100):
        result=constant_elasticity_demand(p)
        close(result["quantity"],400*p**-1.5)
        close(result["elasticity"],-1.5)
        close(centered_elasticity(lambda z:400*z**-1.5,p,1e-4),-1.5,rel_tol=1e-7)
    for p,expected in ((10,-0.25),(25,-1),(40,-4)):
        result=linear_demand(p)
        close(result["elasticity"],expected)
        close(result["revenue_derivative"],100-4*p)
    assert linear_demand(10)["revenue_derivative"]>0
    close(linear_demand(25)["revenue_derivative"],0)
    assert linear_demand(40)["revenue_derivative"]<0
    close(income_elasticity(50000),0.7)
    close(discounted_rate_elasticity(0.04,5),-0.2)
    close(arc_elasticity(10,12,80,70),-11/15)
    close(arc_elasticity(12,10,70,80),-11/15)
    rejects(ValueError,point_elasticity,0,10,1)
    rejects(ValueError,point_elasticity,1,0,1)
    rejects(ValueError,arc_elasticity,10,10,80,70)
    rejects(ValueError,arc_elasticity,10,12,-10,10)
    rejects(ValueError,linear_demand,50)
    rejects(ValueError,constant_elasticity_demand,0)
    rejects(ValueError,discounted_rate_elasticity,0,5)
    rejects(ValueError,centered_elasticity,lambda x:x*x,1,0)
    rejects(TypeError,finite,True,"value")
    rejects(ValueError,finite,float("nan"),"value")
    print("PASS: Section 9.2 reference checks")

if __name__=="__main__":
    run()
