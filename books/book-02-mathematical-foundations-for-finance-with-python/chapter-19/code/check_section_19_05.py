"""Independent analytic reference checks for Book 02 Section 19.5."""
import math
from section_19_05 import (assessment,finite,euler,exact_account,
                            linear_amplification,stable_linear_decay)

def near(a,b,rel=1e-11,abs_=1e-10):
    assert math.isclose(a,b,rel_tol=rel,abs_tol=abs_),(a,b)

def rejects(exc,fn,*args):
    try:
        fn(*args)
    except exc:
        return
    raise AssertionError("expected "+exc.__name__)

def run():
    a=assessment()
    exact=1000*math.exp(0.1)
    near(a["growth_reference"],exact)
    errors=[]
    for n in (10,20,40):
        result=a["growth_euler"][str(n)]
        near(result["final_state"],1000*(1+0.1/n)**n)
        near(result["step_size"],2/n)
        assert result["status"]=="completed"
        errors.append(result["absolute_error"])
    assert errors[2]<errors[1]<errors[0]
    assert 1.8<errors[0]/errors[1]<2.2
    near(a["account_reference"],1000*math.exp(0.2)+200*math.expm1(0.2)/0.04)
    assert a["account_euler_40"]["final_state"]<a["account_reference"]
    near(exact_account(1000,0,200,5),2000)
    near(euler(lambda t,y:0,123,2,10)["final_state"],123)
    near(euler(lambda t,y:2*t,0,0,10)["final_state"],0)
    near(linear_amplification(-2,0.25),0.5)
    near(linear_amplification(-2,0.75),-0.5)
    near(linear_amplification(-2,1.25),-1.5)
    assert stable_linear_decay(-2,0.25)
    assert stable_linear_decay(-2,0.75)
    assert not stable_linear_decay(-2,1)
    assert not stable_linear_decay(-2,1.25)
    rejects(ValueError,euler,lambda t,y:y,100,-1,10)
    rejects(ValueError,euler,lambda t,y:y,100,1,0)
    rejects(ValueError,euler,lambda t,y:y,100,1,True)
    rejects(ValueError,euler,lambda t,y:float("nan"),100,1,10)
    rejects(ValueError,stable_linear_decay,2,0.5)
    rejects(ValueError,linear_amplification,-2,0)
    rejects(ValueError,finite,float("nan"),"value")
    rejects(TypeError,finite,True,"value")
    assert a["runtime_certified"] is False
    assert a["independent_review_completed"] is False
    print("PASS: Section 19.5 independent analytic reference checks")

if __name__=="__main__":
    run()
