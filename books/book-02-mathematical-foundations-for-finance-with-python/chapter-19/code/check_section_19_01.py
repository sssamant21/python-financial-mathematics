"""Independent analytic reference checks for Book 02 Section 19.1."""
import math
from section_19_01 import (assessment,finite,growth,account,
                            continuous_from_effective,effective_from_continuous,
                            euler_account)

def near(a,b,rel=1e-11,abs_=1e-10):
    assert math.isclose(a,b,rel_tol=rel,abs_tol=abs_),(a,b)

def rejects(exc,fn,*args):
    try:
        fn(*args)
    except exc:
        return
    raise AssertionError("expected "+exc.__name__)

def run():
    near(account(0,5e-324,100,0.5),50)
    a=assessment()
    exact=1000*math.exp(0.1)
    near(a["growth_2_years"],exact)
    near(growth(1000,0,2),1000)
    near(growth(0,0.05,2),0)
    near(growth(1000,-0.05,2),1000*math.exp(-0.1))
    near(a["zero_rate_account"],2000)
    near(a["account_with_flow"],1000*math.exp(0.2)+200*math.expm1(0.2)/0.04)
    near(account(1000,0,-100,10),0)
    near(continuous_from_effective(0.05),math.log(1.05))
    near(effective_from_continuous(0.05),math.exp(0.05)-1)
    near(continuous_from_effective(effective_from_continuous(0.05)),0.05)
    errors=[abs(a[f"growth_euler_{n}"]-exact) for n in (10,20,40)]
    assert errors[2]<errors[1]<errors[0]
    near(euler_account(1000,0,-100,10,40),0,abs_=1e-8)
    rejects(ValueError,growth,1000,0.05,-1)
    rejects(ValueError,account,1000,0,100,-1)
    rejects(ValueError,continuous_from_effective,-1)
    rejects(ValueError,euler_account,1000,0.05,0,2,0)
    rejects(ValueError,euler_account,1000,0.05,0,2,True)
    rejects(ValueError,finite,float("nan"),"value")
    rejects(TypeError,finite,True,"value")
    assert a["runtime_certified"] is False
    assert a["independent_review_completed"] is False
    print("PASS: Section 19.1 independent analytic reference checks")

if __name__=="__main__":
    run()
