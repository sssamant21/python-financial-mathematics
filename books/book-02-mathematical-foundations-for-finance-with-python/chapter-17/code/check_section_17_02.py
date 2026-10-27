"""Independent analytic reference checks for Book 02 Section 17.2."""
import math
from section_17_02 import (assessment,finite,variance,optimal_portfolio,
                           residuals,value_function,value_derivative)

def near(a,b):
    assert math.isclose(a,b,rel_tol=1e-10,abs_tol=1e-10),(a,b)

def rejects(exc,fn,*args):
    try:
        fn(*args)
    except exc:
        return
    raise AssertionError("expected "+exc.__name__)

def run():
    a=assessment()
    sol=a["solution"]
    near(sol["weights"][0],8/11)
    near(sol["weights"][1],3/11)
    near(sum(sol["weights"]),1)
    near(sol["variance"],7/220)
    near(sol["multiplier"],-7/110)
    near(variance(*sol["weights"]),7/220)
    near(a["residuals"]["feasibility"],0)
    for g in a["residuals"]["stationarity"]:
        near(g,0)
    near(a["tangent_curvature"],0.22)
    near(a["value_derivative"],7/110)
    near(a["value_derivative"],-sol["multiplier"])
    near(value_function(2),4*7/220)
    scaled=optimal_portfolio(2)
    near(scaled["weights"][0],16/11)
    near(scaled["weights"][1],6/11)
    near(scaled["variance"],4*7/220)
    near(scaled["multiplier"],-14/110)
    r=residuals(*scaled["weights"],scaled["multiplier"],2)
    near(r["feasibility"],0)
    for g in r["stationarity"]:
        near(g,0)
    rejects(TypeError,finite,True,"x")
    rejects(ValueError,optimal_portfolio,float("nan"))
    assert a["runtime_certified"] is False
    assert a["independent_review_completed"] is False
    print("PASS: Section 17.2 independent analytic reference checks")

if __name__=="__main__":
    run()
