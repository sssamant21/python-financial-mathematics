"""Independent analytical reference checks for Book 02 Section 19.4."""
import math
from section_19_04 import (assessment,finite,classify_derivative,
                            mean_reversion,half_life,account_equilibrium,
                            logistic_equilibria,logistic,phase_direction)

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
    near(a["mean_reverting_balance"],1000+200/math.e)
    near(a["mean_reversion_half_life"],math.log(2)/0.5)
    near(mean_reversion(1200,1000,0.5,0),1200)
    near(mean_reversion(1000,1000,0.5,2),1000)
    near(account_equilibrium(0.04,-100),2500)
    near(account_equilibrium(-0.04,100),2500)
    assert account_equilibrium(0,100) is None
    assert account_equilibrium(0,0)=="all_states"
    assert classify_derivative(-1)=="locally_asymptotically_stable"
    assert classify_derivative(1)=="unstable"
    assert classify_derivative(0)=="inconclusive"
    eq=logistic_equilibria(0.4,1000)
    assert [e["state"] for e in eq]==[0,1000]
    assert [e["classification"] for e in eq]==["unstable","locally_asymptotically_stable"]
    near(a["logistic_balance"],1000/(1+4*math.exp(-2)))
    near(logistic(0,0.4,1000,5),0)
    near(logistic(1000,0.4,1000,5),1000)
    assert phase_direction(-1)=="left"
    assert phase_direction(1)=="right"
    assert phase_direction(0)=="equilibrium"
    # Independently differentiate mean-reverting exact solution.
    t=2
    derivative=-0.5*200*math.exp(-0.5*t)
    near(derivative,0.5*(1000-mean_reversion(1200,1000,0.5,t)))
    # Nonhyperbolic phase signs are decisive, not f'(0)=0.
    assert phase_direction(-(-1)**3)=="right"
    assert phase_direction(-(1)**3)=="left"
    assert phase_direction((-1)**2)=="right"
    assert phase_direction((1)**2)=="right"
    rejects(ValueError,half_life,0)
    rejects(ValueError,mean_reversion,1000,1000,-0.5,2)
    rejects(ValueError,logistic_equilibria,0,1000)
    rejects(ValueError,logistic,-1,0.4,1000,5)
    rejects(ValueError,finite,float("nan"),"value")
    rejects(TypeError,finite,True,"value")
    assert a["runtime_certified"] is False
    assert a["independent_review_completed"] is False
    print("PASS: Section 19.4 independent analytical reference checks")

if __name__=="__main__":
    run()
