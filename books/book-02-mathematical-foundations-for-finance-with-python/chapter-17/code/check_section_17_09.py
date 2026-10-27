"""Independent analytic reference checks for Book 02 Section 17.9."""
import math
from section_17_09 import (assessment,finite,validate_caps,objective,
                           gradient,verify_candidate,optimize,financial_report)

def near(a,b):
    assert math.isclose(a,b,rel_tol=1e-10,abs_tol=1e-9),(a,b)

def rejects(exc,fn,*args):
    try:
        fn(*args)
    except exc:
        return
    raise AssertionError("expected "+exc.__name__)

def run():
    a=assessment()
    s=a["allocation"]
    assert s["certificate"]["passes"]
    near(s["weights"][0],0.6)
    near(s["weights"][1],0.4)
    near(s["variance"],0.0336)
    near(s["lambda"],-0.084)
    near(s["multipliers"][2],0.028)
    near(objective((0.6,0.4)),0.0336)
    near(gradient((0.6,0.4))[0],0.056)
    near(gradient((0.6,0.4))[1],0.084)
    f=a["financial_report"]
    near(f["expected_return"],0.068)
    near(f["gross_turnover"],0.2)
    near(f["gross_traded_notional"],200000)
    near(f["modeled_transaction_cost"],200)
    assert not f["taxes_included"]
    assert not f["market_impact_included"]
    # Inactive first cap: unconstrained-on-budget benchmark.
    unconstrained=optimize(1,1)
    assert unconstrained["certificate"]["passes"]
    near(unconstrained["weights"][0],8/11)
    near(unconstrained["variance"],7/220)
    # Binding second cap: the optimizer must certify the opposite regime.
    second_cap=optimize(1,0.2)
    assert second_cap["certificate"]["passes"]
    near(second_cap["weights"][0],0.8)
    near(second_cap["weights"][1],0.2)
    assert second_cap["multipliers"][3]>0
    # Both caps exactly sum to one: feasible but multiplier nonuniqueness.
    endpoint=optimize(0.6,0.4)
    assert endpoint["certificate"]["passes"]
    # Negative cases: feasibility, stationarity, and multiplier signs.
    bad=verify_candidate((0.7,0.3),-0.084,(0,0,0.028,0))
    assert not bad["passes"] and bad["primal_violation"]>0
    nonstationary=verify_candidate((0.5,0.5),0,(0,0,0,0))
    assert not nonstationary["passes"]
    wrong_sign=verify_candidate((0.6,0.4),-0.084,(0,0,-0.028,0))
    assert not wrong_sign["passes"]
    rejects(ValueError,validate_caps,0.4,0.4)
    rejects(ValueError,optimize,-0.1,1)
    rejects(TypeError,finite,True,"value")
    rejects(ValueError,financial_report,(0.6,0.4),(0.5,0.5),-1)
    assert a["runtime_certified"] is False
    assert a["independent_review_completed"] is False
    print("PASS: Section 17.9 independent analytic reference checks")

if __name__=="__main__":
    run()
