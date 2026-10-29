"""Independent analytic reference checks for Book 02 Section 19.6."""
import math
from fractions import Fraction
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

def stability(z):
    # Exact RK4 stability polynomial for y'=y, separate from stage code.
    return 1+z+z*z/2+z**3/6+z**4/24

def traced_run(**controls):
    calls=[]
    def rhs(time,state):
        calls.append((time,state))
        return state
    result=adaptive_rk4(rhs,1,2,**controls)
    assert len(calls)==result["evaluations"]
    return result,calls

def check_adaptive_policy():
    full=stability(Fraction(1))
    half=stability(Fraction(1,2))**2
    error=float((half-full)/15)
    # max(|old|,|two-half|) matters: old-state-only scaling would reject.
    accepted,calls=traced_run(initial_step=1,atol=1e-5,rtol=0.00025,max_attempts=1)
    assert 1e-5+0.00025 < error < 1e-5+0.00025*float(half)
    assert (accepted["accepted_steps"],accepted["rejected_steps"])==(1,0)
    near(accepted["final_time"],1,abs_=1e-14)
    near(accepted["final_state"],float(half),abs_=1e-14)
    # Actual stages discriminate time locations and state weights.
    assert calls[:4]==[(0.0,1.0),(0.5,1.5),(0.5,1.75),(1.0,2.75)]

    rejected,calls=traced_run(initial_step=1,atol=1e-5,rtol=0,max_attempts=1)
    assert rejected["status"]=="attempt_budget_exhausted"
    assert (rejected["accepted_steps"],rejected["rejected_steps"])==(0,1)
    assert rejected["final_time"]==0 and rejected["final_state"]==1
    assert rejected["evaluations"]==12

    factor=0.9*(1e-5/error)**0.2
    retried,calls=traced_run(initial_step=1,atol=1e-5,rtol=0,max_attempts=2)
    assert 0.2<factor<5
    assert calls[12]==(0.0,1.0)  # rejected attempt advanced neither coordinate
    near(calls[15][0],factor,rel=1e-12,abs_=1e-14)
    assert (retried["accepted_steps"],retried["rejected_steps"])==(1,1)
    near(retried["final_time"],factor,rel=1e-12,abs_=1e-14)
    expected=stability(Fraction.from_float(factor)/2)**2
    near(retried["final_state"],float(expected),rel=1e-12,abs_=1e-14)

    # Controller lower clipping and upper clipping with nonzero error.
    low,calls=traced_run(initial_step=1,atol=1e-12,rtol=0,max_attempts=2)
    assert calls[12]==(0.0,1.0)
    near(calls[15][0],0.2,abs_=1e-14)
    high,calls=traced_run(initial_step=0.1,atol=1,rtol=0,max_attempts=2)
    near(calls[15][0]-calls[12][0],0.5,abs_=1e-14)
    assert high["accepted_steps"]==2

    tiny,calls=traced_run(initial_step=1,atol=1e-12,rtol=0,min_step=0.3,max_attempts=2)
    assert tiny["status"]=="step_too_small"
    assert tiny["final_time"]==0 and tiny["final_state"]==1
    assert tiny["evaluations"]==12 and tiny["rejected_steps"]==1

    # Zero estimator branch, fivefold growth and final-horizon clipping.
    times=[]
    def constant(time,state):
        times.append(time)
        return 0
    zero=adaptive_rk4(constant,1,0.7,initial_step=0.1,atol=1e-8,rtol=0)
    assert zero["status"]=="completed" and zero["rejected_steps"]==0
    assert zero["accepted_steps"]==3 and len(times)==36
    for index,step in ((0,0.1),(12,0.5),(24,0.1)):
        near(times[index+3]-times[index],step,abs_=1e-14)
    near(zero["final_time"],0.7,abs_=1e-14)
    near(zero["final_state"],1,abs_=1e-14)

def run():
    check_adaptive_policy()
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
