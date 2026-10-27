"""Independent analytic reference checks for Book 02 Section 19.9."""
import math
from section_19_09 import (assessment,finite,transition,depletion_time,simulate)

def near(a,b,rel=1e-10,abs_=1e-8):
    assert math.isclose(a,b,rel_tol=rel,abs_tol=abs_),(a,b)

def rejects(exc,fn,*args):
    try:
        fn(*args)
    except exc:
        return
    raise AssertionError("expected "+exc.__name__)

def run():
    near(transition(0,5e-324,100,0.5),50)
    near(depletion_time(0.5,5e-324,-1),0.5)
    a=assessment()
    growth=a["growth"]
    assert growth["status"]=="completed"
    near(growth["final_balance"],1000*math.exp(0.2))
    contribution=a["contributions"]
    near(contribution["final_balance"],1000*math.exp(0.2)+200*math.expm1(0.2)/0.04)
    depleted=a["depletion"]
    assert depleted["status"]=="depleted"
    near(depleted["depletion_time"],-math.log(0.6)/0.04)
    near(depleted["final_balance"],0)
    jump=a["scheduled_deposit"]
    near(jump["final_balance"],1000*math.exp(0.25)+200*math.exp(0.15))
    assert jump["applied_jumps"]==1
    late=a["late_deposit"]
    assert late["status"]=="depleted"
    near(late["depletion_time"],2)
    assert late["applied_jumps"]==0
    near(transition(1000,0,200,5),2000)
    near(depletion_time(1000,0,-100),10)
    assert depletion_time(1000,0.04,-40) is None
    assert depletion_time(1000,0.04,-30) is None
    assert depletion_time(1000,0.04,0) is None
    near(simulate(0,0,0,2,[(0,100)])["final_balance"],100)
    assert simulate(0,0,0,2)["status"]=="depleted"
    assert simulate(100,0,-50,2,[(2,1000)])["applied_jumps"]==0
    assert simulate(100,0,-50,2,[(1,100)])["status"]=="completed"
    assert simulate(100,0,-50,2,[(1,100)])["applied_jumps"]==1
    assert simulate(100,0,0,1,[(1,10)])["applied_jumps"]==1
    rejects(ValueError,simulate,-1,0,0,1)
    rejects(ValueError,simulate,100,0,0,-1)
    rejects(ValueError,simulate,100,0,0,5,[(2,10),(1,20)])
    rejects(ValueError,simulate,100,0,0,5,[(2,10),(2,20)])
    rejects(ValueError,simulate,100,0,0,5,[(6,10)])
    rejects(ValueError,transition,100,0,0,-1)
    rejects(ValueError,finite,float("nan"),"value")
    rejects(TypeError,finite,True,"value")
    assert a["runtime_certified"] is False
    assert a["independent_review_completed"] is False
    print("PASS: Section 19.9 independent analytic reference checks")

if __name__=="__main__":
    run()
