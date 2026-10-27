"""Independent reference-check source for Book 02 Section 20.2."""
import math
from section_20_02 import (assessment,present_value,nominal_to_continuous,
                           annuity_explicit,annuity_closed,account,
                           depletion_time,solve_two_by_two)

def near(a,b,rel=1e-10,abs_=1e-8):
    assert math.isclose(a,b,rel_tol=rel,abs_tol=abs_),(a,b)

def rejects(exc,fn,*args):
    try:
        fn(*args)
    except exc:
        return
    raise AssertionError("expected "+exc.__name__)

def run():
    data=assessment()
    near(data["present_value"],1000/math.exp(0.1))
    near(present_value(1000,0,5),1000)
    near(present_value(1000,0.05,0),1000)
    near(nominal_to_continuous(0.06,12),12*math.log(1+0.06/12))
    near(data["nominal_one_year_growth"],data["continuous_one_year_growth"])
    near(annuity_explicit(100,0,24),2400)
    near(annuity_closed(100,0,24),2400)
    near(annuity_closed(100,0.005,24),sum(100/(1.005)**k for k in range(1,25)))
    near(data["annuity_explicit"],data["annuity_closed"])
    near(annuity_closed(100,0.005,0),0)
    near(data["continuous_account"],1000*math.exp(0.2)+200*(math.exp(0.2)-1)/0.04)
    near(account(1000,0,200,5),2000)
    near(data["depletion_time"],-math.log(0.6)/0.04)
    assert depletion_time(1000,0.04,40) is None
    near(depletion_time(1000,0,100),10)
    x,y=data["linear_system_solution"]
    near(x,1.6)
    near(y,1.8)
    near(2*x+y,5)
    near(x+3*y,7)
    rejects(ValueError,solve_two_by_two,1,2,2,4,5,7)
    rejects(ValueError,annuity_closed,100,-1,10)
    rejects(ValueError,annuity_explicit,100,0.01,-1)
    rejects(ValueError,nominal_to_continuous,-12,12)
    rejects(ValueError,present_value,1000,0.05,-1)
    rejects(TypeError,present_value,True,0.05,2)
    assert data["runtime_certified"] is False
    assert data["independent_review_completed"] is False
    print("PASS: Section 20.2 independent reference checks")

if __name__=="__main__":
    run()
