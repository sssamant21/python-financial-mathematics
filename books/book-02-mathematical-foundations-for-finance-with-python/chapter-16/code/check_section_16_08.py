"""Independent analytic checks for Book 02 Section 16.8; not certification."""
import math
from section_16_08 import TRAINING,assessment,price,metrics,weighted_loss,fit_rate,curvature,gradient

def near(a,b):
    assert math.isclose(a,b,rel_tol=1e-10,abs_tol=1e-8),(a,b)

def run():
    a=assessment()
    near(a["fitted_rate"],0.05)
    assert a["training_residuals"]==(0.0,0.0,0.0)
    assert a["holdout_residuals"]==(-1.0,)
    near(a["training_metrics"]["rmse"],0)
    near(a["holdout_metrics"]["rmse"],1)
    near(a["holdout_metrics"]["bias"],-1)
    near(a["gradient"],0)
    near(a["curvature"],14_000_000)
    near(a["weighted_loss"],0)
    near(price(0.05,4),1200)
    near(metrics((-1,0,1))["mae"],2/3)
    near(metrics((-1,0,1))["rmse"],math.sqrt(2/3))
    near(metrics((-1,0,1))["bias"],0)
    near(metrics((-1,0,1))["max_abs"],1)
    near(weighted_loss(0.04,((1,1050),),(2,)),100)
    near(fit_rate(TRAINING),0.05)
    near(gradient(0.05,TRAINING),0)
    near(curvature(TRAINING),14_000_000)
    assert a["runtime_certified"] is False
    assert a["independent_review_completed"] is False
    print("PASS: Section 16.8 analytic reference checks")

if __name__=="__main__":
    run()
