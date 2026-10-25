"""Independent reference checks for Section 10.8."""
import math
from section_10_08 import (
    finite,continuous_pv,schedule_pv,equal_payment_pv,timing_ratio,comparison)

def close(a,b,rel_tol=1e-10,abs_tol=1e-9):
    assert math.isclose(a,b,rel_tol=rel_tol,abs_tol=abs_tol),(a,b)

def rejects(exc,fn,*args):
    try:
        fn(*args)
    except exc:
        return
    raise AssertionError("expected "+exc.__name__)

def run():
    c,T=1200,2
    close(continuous_pv(c,0,T),2400)
    close(schedule_pv([(0,100),(1,100)],0),200)
    close(schedule_pv([(0,100),(1,100)],math.log(2)),150)
    for rate in (-0.02,0,0.06):
        continuous=continuous_pv(c,rate,T)
        for n in (2,8,24,730):
            for timing in ("begin","mid","end"):
                exact=equal_payment_pv(c,rate,T,n,timing)
                offset={"begin":0,"mid":0.5,"end":1}[timing]
                explicit=math.fsum((c*T/n)*math.exp(-rate*(i+offset)*T/n)
                                   for i in range(n))
                close(exact,explicit)
                close(exact,continuous*timing_ratio(rate,T,n,timing))
            start=equal_payment_pv(c,rate,T,n,"begin")
            middle=equal_payment_pv(c,rate,T,n,"mid")
            end=equal_payment_pv(c,rate,T,n,"end")
            if rate>0:
                assert start>middle>end
            elif rate<0:
                assert start<middle<end
            else:
                close(start,middle)
                close(middle,end)
        for timing in ("begin","mid","end"):
            assert abs(equal_payment_pv(c,rate,T,730,timing)-continuous)<abs(
                equal_payment_pv(c,rate,T,2,timing)-continuous)+1e-9
    close(equal_payment_pv(1000,0,2,4),2000)
    close(equal_payment_pv(0,0.06,2,4),0)
    rejects(ValueError,equal_payment_pv,1000,0.06,2,0)
    rejects(ValueError,equal_payment_pv,1000,0.06,2,2,"other")
    rejects(ValueError,continuous_pv,1000,0.06,-1)
    rejects(TypeError,finite,True,"value")
    rejects(ValueError,finite,float("nan"),"value")
    report=comparison()
    assert len(report["scenarios"])==4 and report["runtime_certified"] is False
    print("PASS: Section 10.8 independent reference checks")

if __name__=="__main__":
    run()
