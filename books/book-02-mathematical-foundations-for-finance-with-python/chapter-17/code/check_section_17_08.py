"""Independent reference checks for Book 02 Section 17.8."""
import math
from section_17_08 import assessment,finite,verify

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
    good=a["valid"]
    assert good["passes"] and good["convex_hessian_certified"]
    near(good["objective"],0.0336)
    near(good["gradient"][0],0.056)
    near(good["gradient"][1],0.084)
    near(good["equality_residual"],0)
    assert good["inequality_residuals"]==(-0.6,-0.4,0.0)
    for key in ("primal_violation","dual_violation",
                "stationarity_norm","complementarity_norm"):
        near(good[key],0)
    assert not a["cap_violation"]["passes"]
    near(a["cap_violation"]["primal_violation"],0.1)
    assert not a["nonstationary"]["passes"]
    near(a["nonstationary"]["primal_violation"],0)
    assert a["nonstationary"]["stationarity_norm"]>0
    assert not verify((0.6,0.4),-0.084,(0,0,-0.028))["passes"]
    rejects(TypeError,finite,True,"value")
    rejects(ValueError,verify,(0.6,),-0.084,(0,0,0.028))
    rejects(ValueError,verify,(0.6,0.4),-0.084,(0,0,0.028),0.6,-1)
    assert a["runtime_certified"] is False
    assert a["independent_review_completed"] is False
    print("PASS: Section 17.8 independent analytic reference checks")

if __name__=="__main__":
    run()
