"""Independent reference checks for Section 10.4."""
import math
from section_10_04 import (finite, exponential_growth_integral, discount_integral,
                           time_weighted_discount_integral, linear_cashflow_pv,
                           midpoint_reference, phi, assessment)

def close(a,b,rel_tol=1e-8,abs_tol=1e-8):
    assert math.isclose(a,b,rel_tol=rel_tol,abs_tol=abs_tol),(a,b)

def rejects(exc,fn,*args):
    try:
        fn(*args)
    except exc:
        return
    raise AssertionError("expected "+exc.__name__)

def run():
    close(exponential_growth_integral(500,0,2),1000)
    close(exponential_growth_integral(500,0.02,2),500*math.expm1(0.04)/0.02)
    close(discount_integral(0,2),2)
    close(time_weighted_discount_integral(0,2),2)
    close(phi(0),0.5)
    close(phi(0.04),midpoint_reference(lambda s:s*math.exp(-0.04*s),0,1,10000),
          rel_tol=1e-8)
    for rate in (-0.05,-0.01,0,1e-12,1e-7,0.01,0.04,0.1):
        t=2
        exact=linear_cashflow_pv(1000,100,rate,t)
        numeric=midpoint_reference(lambda x:(1000+100*x)*math.exp(-rate*x),0,t,5000)
        close(exact,numeric,rel_tol=2e-8)
        close(discount_integral(rate,t),
              midpoint_reference(lambda x:math.exp(-rate*x),0,t,5000),
              rel_tol=2e-8)
        close(time_weighted_discount_integral(rate,t),
              midpoint_reference(lambda x:x*math.exp(-rate*x),0,t,5000),
              rel_tol=2e-8)
    close(linear_cashflow_pv(1000,100,0,2),2200)
    close(linear_cashflow_pv(1000,100,0.04,0),0)
    report=assessment()
    assert len(report["scenarios"])==5
    assert not report["runtime_certified"]
    assert not report["independent_review_completed"]
    rejects(ValueError,discount_integral,0.04,-1)
    rejects(ValueError,midpoint_reference,lambda t:t,0,1,0)
    rejects(TypeError,finite,True,"value")
    rejects(ValueError,finite,float("nan"),"value")
    print("PASS: Section 10.4 independent reference checks")

if __name__=="__main__":
    run()
