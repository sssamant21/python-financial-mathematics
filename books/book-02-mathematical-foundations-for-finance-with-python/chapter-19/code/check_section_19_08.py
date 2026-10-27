"""Independent analytic reference checks for Book 02 Section 19.8."""
import math
from section_19_08 import (assessment,finite,nominal_to_continuous,
    continuous_to_nominal,continuous_growth,discrete_growth,
    continuous_contributions,end_period_contributions,euler_account,
    rk4_account,depletion_time)

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
    r=12*math.log(1+0.06/12)
    near(a["equivalent_continuous_rate"],r)
    near(continuous_to_nominal(r,12),0.06)
    near(a["nominal_annual_balance"],1000*(1+0.06/12)**12)
    near(a["continuous_annual_balance"],a["nominal_annual_balance"])
    near(continuous_growth(1000,0,1),1000)
    near(discrete_growth(1000,0,12,12),1000)
    exact=1000*math.exp(0.2)+200*math.expm1(0.2)/0.04
    near(a["continuous_flow_balance"],exact)
    near(continuous_contributions(1000,0,200,5),2000)
    near(end_period_contributions(1000,0,200,5,60),2000)
    assert a["monthly_end_period_balance"]<exact
    near(a["monthly_end_period_balance"],
         1000*math.exp(0.2)+(200*5/60)*sum(math.exp(0.04*(5-k*5/60)) for k in range(1,61)))
    errors_e=[a["convergence"][str(n)]["euler_absolute_error"] for n in (10,20,40)]
    errors_r=[a["convergence"][str(n)]["rk4_absolute_error"] for n in (10,20,40)]
    assert errors_e[2]<errors_e[1]<errors_e[0]
    assert errors_r[2]<errors_r[1]<errors_r[0]
    assert errors_r[0]<errors_e[0]
    near(a["depletion_time"],-math.log(0.6)/0.04)
    assert depletion_time(1000,0.04,40) is None
    near(depletion_time(1000,0,100),10)
    rejects(ValueError,nominal_to_continuous,-12,12)
    rejects(ValueError,discrete_growth,1000,0.06,12,-1)
    rejects(ValueError,end_period_contributions,1000,0.04,200,5,0)
    rejects(ValueError,euler_account,1000,0.04,200,5,0)
    rejects(ValueError,rk4_account,1000,0.04,200,5,0)
    rejects(ValueError,finite,float("nan"),"value")
    rejects(TypeError,finite,True,"value")
    assert a["runtime_certified"] is False
    assert a["independent_review_completed"] is False
    print("PASS: Section 19.8 independent analytic reference checks")

if __name__=="__main__":
    run()
