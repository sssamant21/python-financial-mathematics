"""Independent analytic reference checks for Book 02 Section 16.10."""
import math
from section_16_10 import (TRAIN,HOLDOUT,assessment,finite,model_price,residuals,
                           loss,gradient,hessian,analytical_rate,solve,metrics,
                           portfolio_variance)

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
    near(a["gradient_at_reference"],0)
    near(a["hessian"],14)
    near(loss(0.05),0)
    near(gradient(0),-0.7)
    near(model_price(0.05,4),1200)
    assert residuals(0.05,TRAIN)==(0.0,0.0,0.0)
    assert residuals(0.05,HOLDOUT)==(-1.0,)
    near(a["training_metrics"]["rmse"],0)
    near(a["holdout_metrics"]["rmse"],1)
    near(a["holdout_metrics"]["bias"],-1)
    near(a["portfolio_variance"],0.0336)
    near(portfolio_variance(1,0),0.04)
    near(metrics((-2,0,2))["mae"],4/3)
    near(metrics((-2,0,2))["rmse"],math.sqrt(8/3))
    near(metrics((-2,0,2))["bias"],0)
    assert len(a["runs"])==6
    for item in a["runs"]:
        assert item["status"]=="gradient_tolerance"
        near(item["rate"],0.05)
    assert all(item["iterations"]==1 for item in a["runs"] if item["method"]=="newton")
    rejects(TypeError,finite,True,"value")
    rejects(ValueError,model_price,0.05,0)
    rejects(ValueError,solve,0,method="unsupported")
    rejects(ValueError,solve,0,step=0)
    rejects(ValueError,solve,0,max_iterations=0)
    assert a["runtime_certified"] is False
    assert a["independent_review_completed"] is False
    print("PASS: Section 16.10 independent analytic reference checks")

if __name__=="__main__":
    run()
