"""Independent analytic reference checks for Book 02 Section 17.3."""
import math
from section_17_03 import (assessment,finite,variance,portfolio,kkt_report,
                           scalar_example)

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
    s=a["solution"]
    near(s["weights"][0],0.6)
    near(s["weights"][1],0.4)
    near(s["variance"],0.0336)
    near(s["lambda"],-0.084)
    near(s["multipliers"][2],0.028)
    near(variance(*s["weights"]),0.0336)
    assert a["kkt"]["passes"]
    near(a["kkt"]["equality_residual"],0)
    for v in a["kkt"]["stationarity"]:
        near(v,0)
    for v in a["kkt"]["complementarity"]:
        near(v,0)
    near(a["scalar"]["x"],0.6)
    near(a["scalar"]["multipliers"][1],0.4)
    near(a["scalar"]["stationarity"],0)
    relaxed=portfolio(0.8)
    near(relaxed["weights"][0],8/11)
    near(relaxed["multipliers"][2],0)
    assert kkt_report(relaxed["weights"],relaxed["lambda"],
                      relaxed["multipliers"],relaxed["cap"])["passes"]
    assert not kkt_report((0.8,0.2),-0.084,(0,0,0.028),0.6)["passes"]
    rejects(TypeError,finite,True,"value")
    rejects(ValueError,portfolio,-0.1)
    rejects(ValueError,portfolio,1.1)
    rejects(ValueError,kkt_report,(0.6,0.4),-0.084,(0,0))
    assert a["runtime_certified"] is False
    assert a["independent_review_completed"] is False
    print("PASS: Section 17.3 independent analytic reference checks")

if __name__=="__main__":
    run()
