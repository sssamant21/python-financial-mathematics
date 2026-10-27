"""Independent analytic reference checks for Book 02 Section 18.7."""
import math
from section_18_07 import (assessment,finite,forward_difference,central_difference,
                           second_difference,zero_price,trapezoid,simpson,
                           continuous_cashflow_pv)

def near(a,b,rel=1e-6,abs_=1e-8):
    assert math.isclose(a,b,rel_tol=rel,abs_tol=abs_),(a,b)

def rejects(exc,fn,*args):
    try:
        fn(*args)
    except exc:
        return
    raise AssertionError("expected "+exc.__name__)

def run():
    a=assessment()
    r=0.05
    p=1000/(1+r)**2
    near(a["price"],p,rel=1e-12)
    d1=-2000/(1+r)**3
    d2=6000/(1+r)**4
    near(a["forward_derivative"],d1,rel=3e-4)
    near(a["central_derivative"],d1,rel=1e-7)
    near(a["second_derivative"],d2,rel=1e-6)
    near(a["numerical_duration"],2/(1+r),rel=1e-7)
    near(a["numerical_convexity"],6/(1+r)**2,rel=1e-6)
    near(forward_difference(lambda x:x*x,2,1e-4),4,rel=3e-5)
    near(central_difference(lambda x:x*x,2,1e-4),4,rel=1e-10)
    near(second_difference(lambda x:x*x,2,1e-3),2,rel=1e-8)
    near(trapezoid(lambda x:2*x,0,3,8),9,rel=1e-12)
    near(simpson(lambda x:x**3,0,2,8),4,rel=1e-12)
    exact=100*(-math.expm1(-0.15))/0.03
    near(a["analytic_continuous_pv"],exact,rel=1e-12)
    assert abs(a["trapezoid_40"]-exact)<abs(a["trapezoid_20"]-exact)
    assert abs(a["simpson_40"]-exact)<abs(a["simpson_20"]-exact)
    assert abs(a["simpson_40"]-exact)<abs(a["trapezoid_40"]-exact)
    near(continuous_cashflow_pv(100,0,5),500,rel=1e-12)
    rejects(ValueError,zero_price,-1)
    rejects(ValueError,forward_difference,lambda x:x,1,0)
    rejects(ValueError,central_difference,lambda x:x,1,1e-30)
    rejects(ValueError,simpson,lambda x:x,0,1,3)
    rejects(ValueError,trapezoid,lambda x:x,1,0,10)
    rejects(ValueError,trapezoid,lambda x:float("nan"),0,1,4)
    rejects(ValueError,continuous_cashflow_pv,-1,0.03,5)
    rejects(TypeError,finite,True,"value")
    assert a["runtime_certified"] is False
    assert a["independent_review_completed"] is False
    print("PASS: Section 18.7 independent analytic reference checks")

if __name__=="__main__":
    run()
