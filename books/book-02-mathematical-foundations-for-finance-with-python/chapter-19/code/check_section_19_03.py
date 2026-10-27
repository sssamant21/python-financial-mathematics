"""Independent analytic reference checks for Book 02 Section 19.3."""
import math
from section_19_03 import (assessment,finite,account,depletion_time,
                            variable_rate_no_flow,piecewise_account,euler_account)

def near(a,b,rel=1e-11,abs_=1e-9):
    assert math.isclose(a,b,rel_tol=rel,abs_tol=abs_),(a,b)

def rejects(exc,fn,*args):
    try:
        fn(*args)
    except exc:
        return
    raise AssertionError("expected "+exc.__name__)

def run():
    a=assessment()
    exact=1000*math.exp(0.2)+200*math.expm1(0.2)/0.04
    near(a["constant_flow_balance"],exact)
    near(a["zero_rate_balance"],2000)
    near(account(1000,0.04,200,0),1000)
    near(account(1000,0,0,5),1000)
    near(a["small_rate_balance"],1000*math.exp(5e-8)+200*math.expm1(5e-8)/1e-8)
    t=a["depletion_time"]
    near(t,math.log(100/(100-0.04*1000))/0.04)
    near(account(1000,0.04,-100,t),0,abs_=1e-8)
    assert depletion_time(1000,0.04,40) is None
    assert depletion_time(1000,0.04,30) is None
    near(depletion_time(1000,0,100),10)
    near(a["time_varying_rate_balance"],1000*math.exp(0.03*5+0.001*25))
    piece=account(account(1000,0.04,100,2),0.04,200,3)
    near(a["piecewise_balance"],piece)
    errors=[abs(a[f"euler_{n}"]-exact) for n in (10,20,40)]
    assert errors[2]<errors[1]<errors[0]
    # Independent differential identity at a sample time.
    t=2
    balance=account(1000,0.04,200,t)
    derivative=0.04*1000*math.exp(0.04*t)+200*math.exp(0.04*t)
    near(derivative,0.04*balance+200)
    rejects(ValueError,account,1000,0.04,200,-1)
    rejects(ValueError,depletion_time,0,0.04,100)
    rejects(ValueError,depletion_time,1000,-0.04,100)
    rejects(ValueError,euler_account,1000,0.04,200,5,0)
    rejects(ValueError,piecewise_account,1000,0.04,[(100,-1)])
    rejects(ValueError,finite,float("nan"),"value")
    rejects(TypeError,finite,True,"value")
    assert a["runtime_certified"] is False
    assert a["independent_review_completed"] is False
    print("PASS: Section 19.3 independent analytic reference checks")

if __name__=="__main__":
    run()
