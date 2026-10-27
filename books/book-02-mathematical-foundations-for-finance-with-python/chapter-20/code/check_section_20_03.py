"""Independent reference checks for Book 02 Section 20.3."""
import math
from section_20_03 import (
    assessment,discount_factor,present_value,future_value,
    account_transition,cash_flow_pv,portfolio_feasible,covariance_quadratic_2x2)

def near(a,b,rel=1e-11,abs_=1e-9):
    assert math.isclose(a,b,rel_tol=rel,abs_tol=abs_),(a,b)

def rejects(exc,fn,*args):
    try:
        fn(*args)
    except exc:
        return
    raise AssertionError("expected "+exc.__name__)

def run():
    a=assessment()
    near(a["discount_zero_horizon"],1)
    near(discount_factor(0,5),1)
    near(a["discount_composition_left"],a["discount_composition_right"])
    near(a["discount_composition_left"],math.exp(-0.2))
    near(a["pv_split_left"],a["pv_split_right"])
    near(a["pv_split_left"],100*math.exp(-0.08))
    near(cash_flow_pv([(40,2),(60,2)],0.04),100*math.exp(-0.08))
    near(a["pv_future_round_trip"],1000)
    near(present_value(future_value(250,0.03,3),0.03,3),250)
    near(a["account_composition_left"],a["account_composition_right"])
    near(a["account_composition_left"],1000*math.exp(0.2)+200*math.expm1(0.2)/0.04)
    near(account_transition(1000,0,200,5)-1000,1000)
    assert a["portfolio_feasible"] is True
    assert portfolio_feasible([0.4,0.6])
    assert not portfolio_feasible([-0.1,1.1])
    assert not portfolio_feasible([0.4,0.5])
    near(covariance_quadratic_2x2(1,2,2,1,1,-1),-2)
    near(covariance_quadratic_2x2(2,1,1,2,1,-1),2)
    rejects(ValueError,discount_factor,0.04,-1)
    rejects(ValueError,account_transition,1000,0.04,200,-1)
    rejects(ValueError,portfolio_feasible,[0.4,0.6],-1)
    rejects(ValueError,portfolio_feasible,[])
    rejects(TypeError,present_value,True,0.04,2)
    assert a["runtime_certified"] is False
    assert a["independent_review_completed"] is False
    print("PASS: Section 20.3 independent reference checks")

if __name__=="__main__":
    run()
