"""Independent reference checks for Section 10.5."""
import math
from section_10_05 import (
    finite,constant_pv,growing_pv,linear_pv,midpoint_integral,
    variable_curve_pv,growing_pv_rate_derivative,assessment)

def close(a,b,rel_tol=2e-8,abs_tol=1e-8):
    assert math.isclose(a,b,rel_tol=rel_tol,abs_tol=abs_tol),(a,b)

def rejects(exc,fn,*args):
    try:
        fn(*args)
    except exc:
        return
    raise AssertionError("expected "+exc.__name__)

def run():
    close(constant_pv(1000,0,2),2000)
    close(constant_pv(1200,0.05,3),1200*(-math.expm1(-0.15))/0.05)
    close(growing_pv(1000,0.02,0.02,4),4000)
    close(linear_pv(1000,100,0,2),2200)
    close(constant_pv(1000,0.04,0),0)
    for rate in (-0.01,0,0.02,0.05,0.08):
        exact=growing_pv(1000,0.02,rate,4)
        numeric=midpoint_integral(lambda t:1000*math.exp((0.02-rate)*t),4,4000)
        close(exact,numeric)
    for rate in (-0.03,0,0.01,0.04):
        exact=linear_pv(1000,100,rate,2)
        numeric=midpoint_integral(lambda t:(1000+100*t)*math.exp(-rate*t),2,4000)
        close(exact,numeric)
    c,g,r,T=1000,0.02,0.05,4
    h=1e-5
    numeric=(growing_pv(c,g,r+h,T)-growing_pv(c,g,r-h,T))/(2*h)
    close(growing_pv_rate_derivative(c,g,r,T),numeric,rel_tol=1e-7)
    assert growing_pv(c,g,0.08,T)<growing_pv(c,g,0.05,T)<growing_pv(c,g,0,T)
    variable=variable_curve_pv(lambda t:1000*math.exp(0.02*t),0.03,0.005,4,4000)
    reference=midpoint_integral(lambda t:1000*math.exp(-0.01*t-0.0025*t*t),4,4000)
    close(variable,reference)
    report=assessment()
    assert len(report["scenarios"])==5
    assert report["runtime_certified"] is False
    rejects(ValueError,constant_pv,1000,0.04,-1)
    rejects(ValueError,midpoint_integral,lambda t:t,1,0)
    rejects(TypeError,finite,True,"value")
    rejects(ValueError,finite,float("inf"),"value")
    print("PASS: Section 10.5 independent reference checks")

if __name__=="__main__":
    run()
