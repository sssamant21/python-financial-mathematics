"""Independent analytic reference checks for Book 02 Section 17.10."""
import math
from section_17_09 import verify_candidate
from section_17_10 import (assessment,finite,portfolio,two_sided,
                           linear_program_reference,financial_reference)

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
    regimes=a["portfolio_regimes"]
    assert len(regimes)==4
    expected=((0.4,0.6,0.0436,0.072),
              (0.6,0.4,0.0336,0.028),
              (8/11,3/11,7/220,0),
              (8/11,3/11,7/220,0))
    for case,(x,y,v,mu) in zip(regimes,expected):
        assert case["feasible"]
        near(case["weights"][0],x)
        near(case["weights"][1],y)
        near(case["variance"],v)
        near(case["multipliers"][2],mu)
        for z in case["stationarity"]+case["complementarity"]:
            near(z,0)
    t=a["two_sided"]
    near(t["interval"][0],0.8)
    near(t["interval"][1],0.9)
    near(t["weights"][0],0.8)
    near(t["weights"][1],0.2)
    near(t["variance"],0.0324)
    near(t["lambda"],-0.068)
    near(t["multipliers"][3],0.016)
    assert t["multipliers"][:3]==(0,0,0)
    cert=verify_candidate(t["weights"],t["lambda"],t["multipliers"],(0.9,0.2))
    assert cert["passes"]
    # Omitting the binding second-cap multiplier must fail stationarity.
    missing=verify_candidate(t["weights"],t["lambda"],(0,0,0,0),(0.9,0.2))
    assert not missing["passes"]
    near(missing["stationarity_norm"],0.016)
    # A feasible endpoint with a zero multiplier is not the optimum.
    false_success=verify_candidate((0.9,0.1),-0.074,(0,0,0,0),(0.9,0.2))
    assert not false_success["passes"]
    near(false_success["primal_violation"],0)
    near(false_success["stationarity_norm"],0.038)
    near(false_success["objective"],0.0351)
    assert false_success["objective"]>t["variance"]
    for caps in ((0.6,1),(1,1),(0.6,0.4)):
        case=two_sided(*caps)
        assert verify_candidate(case["weights"],case["lambda"],
                                case["multipliers"],caps)["passes"]
    # Rounded cap addition can equal one while the actual interval is empty.
    rejects(ValueError,two_sided,math.nextafter(0.5,0),0.5)
    assert two_sided(0.5,0.5)["weights"]==(0.5,0.5)
    lp=a["linear_program"]
    assert lp["optimal_point"]==(2,6)
    near(lp["primal_value"],34)
    near(lp["dual_value"],34)
    assert lp["scores"]==(0,25,34,32)
    f=a["financial_report"]
    near(f["expected_return"],0.068)
    near(f["gross_turnover"],0.2)
    near(f["gross_traded_notional"],200000)
    near(f["modeled_cost"],200)
    rejects(ValueError,portfolio,-0.1)
    rejects(ValueError,two_sided,0.4,0.4)
    rejects(TypeError,finite,True,"value")
    assert not a["runtime_certified"]
    assert not a["independent_review_completed"]
    print("PASS: Section 17.10 independent analytic reference checks")

if __name__=="__main__":
    run()
