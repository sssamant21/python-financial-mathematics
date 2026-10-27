"""Independent analytic reference checks for Book 02 Section 19.7."""
import math
from section_19_07 import (assessment,finite,account,depletion_time,
                            linear_crossing,simulate_jumps)

def near(a,b,rel=1e-10,abs_=1e-8):
    assert math.isclose(a,b,rel_tol=rel,abs_tol=abs_),(a,b)

def rejects(exc,fn,*args,**kwargs):
    try:
        fn(*args,**kwargs)
    except exc:
        return
    raise AssertionError("expected "+exc.__name__)

def run():
    near(account(100,5e-324,100,0.5),50)
    near(depletion_time(0.5,5e-324,1),0.5)
    simultaneous=simulate_jumps(100,0,50,2,[(2,1000)])
    assert simultaneous["status"]=="completed" and simultaneous["final_balance"]==1000
    a=assessment()
    t=-math.log(0.6)/0.04
    near(a["depletion_positive_rate"],t)
    near(account(1000,0.04,100,t),0)
    near(a["depletion_zero_rate"],10)
    near(a["depletion_negative_rate"],-math.log1p(0.4)/(-0.02))
    assert a["no_depletion"] is None
    assert depletion_time(1000,0.04,39) is None
    assert depletion_time(1000,0.04,40) is None
    assert depletion_time(1000,0.04,41)>0
    assert depletion_time(1000,0,0) is None
    near(depletion_time(0,0.04,100),0)
    near(linear_crossing(2,4,10,-10),3)
    near(linear_crossing(2,4,10,0),4)
    jump=1000*math.exp(0.05*5)+200*math.exp(0.05*3)
    assert a["jump_balance"]["status"]=="completed"
    near(a["jump_balance"]["final_balance"],jump)
    terminal=a["terminal_depletion"]
    assert terminal["status"]=="depleted"
    near(terminal["event_time"],t)
    near(terminal["final_balance"],0)
    # Scheduled deposit at t=0 is applied before depletion evaluation.
    near(simulate_jumps(0,0,0,2,[(0,100)])["final_balance"],100)
    assert simulate_jumps(1000,0,100,20,[])["status"]=="depleted"
    assert simulate_jumps(1000,0,100,5,[])["status"]=="completed"
    rejects(ValueError,linear_crossing,2,1,10,-10)
    rejects(ValueError,linear_crossing,2,4,-10,10)
    rejects(ValueError,simulate_jumps,1000,0.04,100,5,[(2,10),(1,20)])
    rejects(ValueError,simulate_jumps,1000,0.04,100,5,[(2,10),(2,20)])
    rejects(ValueError,simulate_jumps,1000,0.04,100,5,[(6,10)])
    rejects(ValueError,depletion_time,-1,0.04,100)
    rejects(ValueError,finite,float("nan"),"value")
    rejects(TypeError,finite,True,"value")
    assert a["runtime_certified"] is False
    assert a["independent_review_completed"] is False
    print("PASS: Section 19.7 independent analytic reference checks")

if __name__=="__main__":
    run()
