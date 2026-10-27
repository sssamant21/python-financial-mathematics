"""Independent analytical reference checks for Book 02 Section 19.10."""
import math
from section_19_10 import (assessment,finite,exact_account,classify_equilibrium,
                            euler,rk4,depletion_time,deposit_at)

def near(a,b,rel=1e-10,abs_=1e-8):
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
    near(a["exact_growth"],exact)
    near(a["contributions"],1000*math.exp(0.2)+200*math.expm1(0.2)/0.04)
    near(exact_account(1000,0,200,5),2000)
    assert classify_equilibrium(-1)=="asymptotically_stable"
    assert classify_equilibrium(1)=="unstable"
    assert classify_equilibrium(0)=="inconclusive"
    near(a["withdrawal_equilibrium"],100/0.04)
    near(a["mean_reversion_half_life"],math.log(2)/0.5)
    near(a["depletion_time"],-math.log(0.6)/0.04)
    assert depletion_time(1000,0.04,40) is None
    near(depletion_time(1000,0,100),10)
    near(a["deposit_at_year_two"],1000*math.exp(0.25)+200*math.exp(0.15))
    e_errors=[]
    r_errors=[]
    for n in (10,20,40):
        row=a["convergence"][str(n)]
        near(row["euler"],1000*(1+0.1/n)**n)
        e_errors.append(row["euler_absolute_error"])
        r_errors.append(row["rk4_absolute_error"])
    assert e_errors[2]<e_errors[1]<e_errors[0]
    assert r_errors[2]<r_errors[1]<r_errors[0]
    assert r_errors[0]<e_errors[0]
    assert 1.8<e_errors[0]/e_errors[1]<2.2
    assert 12<r_errors[0]/r_errors[1]<20
    rejects(ValueError,euler,1000,0.05,0,2,0)
    rejects(ValueError,rk4,1000,0.05,0,2,0)
    rejects(ValueError,exact_account,1000,0.05,0,-1)
    rejects(ValueError,deposit_at,1000,0.05,200,6,5)
    rejects(ValueError,finite,float("nan"),"value")
    rejects(TypeError,finite,True,"value")
    assert a["runtime_certified"] is False
    assert a["independent_review_completed"] is False
    print("PASS: Section 19.10 independent analytical reference checks")

if __name__=="__main__":
    run()
