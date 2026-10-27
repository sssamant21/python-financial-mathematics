"""Independent analytic reference checks for Book 02 Section 17.7."""
import math
from section_17_07 import (assessment,finite,covariance_valid,variance,
                           allocation,trade_report)

def near(a,b):
    assert math.isclose(a,b,rel_tol=1e-10,abs_tol=1e-9),(a,b)

def rejects(exc,fn,*args,**kwargs):
    try:
        fn(*args,**kwargs)
    except exc:
        return
    raise AssertionError("expected "+exc.__name__)

def run():
    a=assessment()
    assert covariance_valid()
    assert not covariance_valid(((0.04,0.01),(0.02,0.09)))
    assert not covariance_valid(((0.04,0.1),(0.1,0.09)))
    p=a["allocation"]
    assert p["feasible"]
    near(p["weights"][0],0.6)
    near(p["weights"][1],0.4)
    near(p["variance"],0.0336)
    near(variance((0.6,0.4)),0.0336)
    near(p["expected_return"],0.068)
    t=a["trades"]
    near(t["signed_trades"][0],100000)
    near(t["signed_trades"][1],-100000)
    near(t["gross_turnover"],0.2)
    near(t["gross_traded_notional"],200000)
    near(t["modeled_cost"],200)
    benchmark=allocation(1,1)
    near(benchmark["weights"][0],8/11)
    near(benchmark["weights"][1],3/11)
    rejects(ValueError,allocation,0.4,0.4)
    rejects(ValueError,allocation,-0.1,1)
    rejects(ValueError,trade_report,(0.6,0.4),(0.5,0.5),-1)
    rejects(TypeError,finite,True,"value")
    assert not a["assumptions"]["taxes_included"]
    assert not a["runtime_certified"]
    assert not a["independent_review_completed"]
    print("PASS: Section 17.7 independent analytic reference checks")

if __name__=="__main__":
    run()
