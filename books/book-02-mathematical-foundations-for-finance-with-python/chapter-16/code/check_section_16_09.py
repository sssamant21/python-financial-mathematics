"""Independent analytic reference checks for Book 02 Section 16.9."""
import math
from section_16_09 import (TRAIN,HOLDOUT,STARTS,assessment,finite,price,
                           objective,gradient,curvature,analytical_rate,
                           optimize,price_metrics)

def near(a,b):
    assert math.isclose(a,b,rel_tol=1e-10,abs_tol=1e-8),(a,b)

def rejects(exc,fn,*args,**kwargs):
    try:
        fn(*args,**kwargs)
    except exc:
        return
    raise AssertionError("expected "+exc.__name__)

def run():
    a=assessment()
    near(a["analytical_rate"],0.05)
    near(a["curvature"],14)
    near(objective(0.05),0)
    near(gradient(0.05),0)
    near(gradient(0),-0.7)
    near(price(0.05,4),1200)
    assert len(a["runs"])==6
    assert len(STARTS)==3
    for item in a["runs"]:
        assert item["status"]=="gradient_tolerance"
        near(item["rate"],0.05)
        assert abs(item["gradient"])<=1e-9
    for item in a["runs"]:
        if item["method"]=="newton" and item["start"]!=0.05:
            assert item["iterations"]==1
    near(a["training"]["mae"],0)
    near(a["training"]["rmse"],0)
    assert a["holdout"]["residuals"]==(-1.0,)
    near(a["holdout"]["rmse"],1)
    near(price_metrics(0.05,HOLDOUT)["bias"],-1)
    near(analytical_rate(TRAIN),0.05)
    assert a["provisional_acceptance"] is True
    rejects(TypeError,finite,True,"value")
    rejects(ValueError,optimize,0,method="unknown")
    rejects(ValueError,optimize,0,step=0)
    rejects(ValueError,optimize,0,max_iterations=0)
    assert a["runtime_certified"] is False
    assert a["independent_review_completed"] is False
    print("PASS: Section 16.9 independent analytic reference checks")

if __name__=="__main__":
    run()
