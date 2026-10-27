"""Independent analytic reference checks for Book 02 Section 19.6."""
import math
from section_19_06 import (assessment,finite,rk4_step,fixed_rk4,
                            exact_account,adaptive_rk4)

def near(a,b,rel=1e-10,abs_=1e-8):
    assert math.isclose(a,b,rel_tol=rel,abs_tol=abs_),(a,b)

def rejects(exc,fn,*args,**kwargs):
    try:
        fn(*args,**kwargs)
    except exc:
        return
    raise AssertionError("expected "+exc.__name__)

def run():
    a=assessment()
    exact=1000*math.exp(0.1)
    near(a["growth_reference"],exact)
    errors=[]
    for n in (4,8,16):
        result=a["fixed_rk4"][str(n)]
        assert result["status"]=="completed"
        assert result["evaluations"]==4*n
        errors.append(result["absolute_error"])
    assert errors[2]<errors[1]<errors[0]
    assert 12<errors[0]/errors[1]<20
    assert 12<errors[1]/errors[2]<20
    near(rk4_step(lambda t,y:2,3,10,0.5),11)
    near(fixed_rk4(lambda t,y:0,123,0,10)["final_state"],123)
    near(exact_account(1000,0,200,5),2000)
    near(a["account_reference"],1000*math.exp(0.2)+200*math.expm1(0.2)/0.04)
    adaptive=a["adaptive_growth"]
    assert adaptive["status"]=="completed"
    near(adaptive["final_time"],2)
    assert adaptive["accepted_steps"]>0
    assert adaptive["evaluations"]==12*(adaptive["accepted_steps"]+adaptive["rejected_steps"])
    assert adaptive["absolute_error"]<1e-5
    account=a["adaptive_account"]
    assert account["status"]=="completed"
    near(account["final_state"],a["account_reference"],rel=1e-7,abs_=1e-4)
    exhausted=adaptive_rk4(lambda t,y:y,1000,2,max_attempts=1)
    assert exhausted["status"]=="attempt_budget_exhausted"
    too_small=adaptive_rk4(lambda t,y:y,1000,2,initial_step=0.01,min_step=0.1)
    assert too_small["status"]=="step_too_small"
    rejects(ValueError,rk4_step,lambda t,y:y,0,1,0)
    rejects(ValueError,fixed_rk4,lambda t,y:y,1000,2,0)
    rejects(ValueError,adaptive_rk4,lambda t,y:y,1000,2,atol=0)
    rejects(ValueError,adaptive_rk4,lambda t,y:y,1000,2,rtol=-1)
    rejects(ValueError,adaptive_rk4,lambda t,y:y,1000,2,max_attempts=0)
    rejects(ValueError,adaptive_rk4,lambda t,y:float("nan"),1000,2)
    rejects(ValueError,finite,float("nan"),"value")
    rejects(TypeError,finite,True,"value")
    assert a["runtime_certified"] is False
    assert a["independent_review_completed"] is False
    print("PASS: Section 19.6 independent analytic reference checks")

if __name__=="__main__":
    run()
