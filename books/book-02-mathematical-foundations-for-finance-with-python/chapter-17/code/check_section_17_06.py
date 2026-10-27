"""Independent analytic reference checks for Book 02 Section 17.6."""
import math
from section_17_06 import (assessment,finite,variance,gradient,
                           positive_definite,solve,kkt_report)

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
    assert positive_definite()
    s=a["solution"]
    near(s["weights"][0],0.6)
    near(s["weights"][1],0.4)
    near(s["variance"],0.0336)
    near(s["gradient"][0],0.056)
    near(s["gradient"][1],0.084)
    near(s["lambda"],-0.084)
    near(s["multipliers"][2],0.028)
    assert a["kkt"]["passes"]
    near(a["kkt"]["equality_residual"],0)
    for v in a["kkt"]["stationarity"]+a["kkt"]["complementarity"]:
        near(v,0)
    near(variance(0.6,0.4),0.0336)
    assert gradient(0.6,0.4)==s["gradient"]
    benchmark=a["benchmark"]
    near(benchmark["weights"][0],8/11)
    near(benchmark["weights"][1],3/11)
    near(benchmark["variance"],7/220)
    near(benchmark["multipliers"][2],0)
    assert kkt_report(benchmark)["passes"]
    eps=1e-5
    derivative=(solve(0.6+eps)["variance"]-solve(0.6-eps)["variance"])/(2*eps)
    near(derivative,-0.028)
    rejects(TypeError,finite,True,"value")
    rejects(ValueError,solve,-0.1)
    rejects(ValueError,solve,1.1)
    rejects(ValueError,kkt_report,s,-1)
    assert a["runtime_certified"] is False
    assert a["independent_review_completed"] is False
    print("PASS: Section 17.6 independent analytic reference checks")

if __name__=="__main__":
    run()
