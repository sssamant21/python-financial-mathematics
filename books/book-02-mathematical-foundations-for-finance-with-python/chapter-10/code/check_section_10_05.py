"""Independent reference checks for Section 10.5."""
import math
from section_10_05 import (
    finite,exponential_integral,time_weighted_factor,constant_pv,growing_pv,linear_pv,midpoint_integral,
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
    # Selected complete-expression regressions; detailed independent oracle
    # and pre-correction failures are retained in validation/ch10-payment-kernel.
    assert exponential_integral(0,1e308,1e308)==0
    close(exponential_integral(1e308,-1,2),8.646647167633873e307,rel_tol=1e-14,abs_tol=0)
    close(exponential_integral(1e-300,1,1000),1.970071114017047e134,rel_tol=1e-14,abs_tol=0)
    close(constant_pv(1,1e308,1e308),1e-308,rel_tol=1e-14,abs_tol=0)
    close(growing_pv(1,-1e308,1e308,1),5e-309,rel_tol=1e-14,abs_tol=0)
    close(growing_pv(1e-300,1,-1e-16,700),10142.320547350755,rel_tol=1e-14,abs_tol=0)
    rejects(ValueError,exponential_integral,1,1,1000)
    assert growing_pv(0,1e308,-1e308,1)==0
    assert linear_pv(-1e308,1e308,0,2)==0
    close(linear_pv(1e-308,0,0,1e308),1,rel_tol=1e-14,abs_tol=0)
    close(linear_pv(0,1e-308,0,1e200),5e91,rel_tol=1e-14,abs_tol=0)
    assert linear_pv(-11999,2,-2,6000)==6000
    assert linear_pv(0,0,-1e308,1e308)==0
    close(time_weighted_factor(1,1e200),1,rel_tol=1e-14,abs_tol=0)
    close(time_weighted_factor(0,1.5e154),1.125e308,rel_tol=1e-14,abs_tol=0)
    close(time_weighted_factor(-1,700),7.089482062597681e306,rel_tol=1e-14,abs_tol=0)
    rejects(ValueError,time_weighted_factor,-1,720)
    calls=[]
    assert midpoint_integral(lambda t:calls.append(t),0,4)==0
    assert calls==[]
    assert midpoint_integral(lambda t:1e308 if t<2 else -1e308,4,2)==0
    rejects(ValueError,midpoint_integral,lambda t:1e308,4,4)
    calls=[]
    rejects(ValueError,midpoint_integral,lambda t:calls.append(t) or 1,math.ulp(0.),2)
    assert calls==[]
    assert midpoint_integral(lambda t:math.ulp(0.),1,2)==math.ulp(0.)
    assert growing_pv_rate_derivative(0,1,0,1000)==0
    close(growing_pv_rate_derivative(1e-308,0,0,1e200),-5e91,rel_tol=1e-14,abs_tol=0)
    close(growing_pv_rate_derivative(1e308,0,1e308,1e308),-1e-308,rel_tol=1e-14,abs_tol=0)
    close(growing_pv_rate_derivative(1e308,-1e308,1e308,1),-2.5e-309,rel_tol=1e-14,abs_tol=0)
    rejects(ValueError,growing_pv_rate_derivative,1e308,0,0,2)
    assert growing_pv_rate_derivative(1e308,1e308,-1e308,0)==0
    assert variable_curve_pv(lambda t:0,-1e308,0,4,2)==0
    close(variable_curve_pv(lambda t:1e-300,-1000,0,2,1),3.940142228034094e134,rel_tol=1e-14,abs_tol=0)
    close(variable_curve_pv(lambda t:1e308,1000,0,2,1),1.0151917795098914e-126,rel_tol=1e-14,abs_tol=0)
    assert variable_curve_pv(lambda t:1,1e308,-1e308,4,1)==4
    assert variable_curve_pv(lambda t:1 if t<2 else -1,-2000,1000,4,2)==0
    rejects(ValueError,variable_curve_pv,lambda t:1,-20000,0,2,1)
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
