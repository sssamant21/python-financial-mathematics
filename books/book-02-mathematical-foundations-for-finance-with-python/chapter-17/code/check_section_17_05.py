"""Independent analytic reference checks for Book 02 Section 17.5."""
import math
from section_17_05 import (assessment,finite,benefit,primal_report,
                           intersections,solve_vertices,dual_report,certificate)

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
    vertices=set(a["solution"]["vertices"])
    assert vertices=={(0.0,0.0),(5.0,0.0),(2.0,6.0),(0.0,8.0)}
    assert a["solution"]["allocation"]==(2.0,6.0)
    near(a["solution"]["benefit"],34)
    assert a["solution"]["primal"]["feasible"]
    assert a["certificate"]["certified_by_residuals"]
    near(a["certificate"]["duality_gap"],0)
    for v in a["certificate"]["complementarity"]:
        near(v,0)
    assert dual_report(3,1)["feasible"]
    near(dual_report(3,1)["dual_objective"],34)
    assert not primal_report(6,4)["feasible"]
    assert not dual_report(0,0)["feasible"]
    near(benefit(5,0),25)
    near(benefit(0,8),32)
    near(benefit(2,6),34)
    # A small budget increase retains both binding constraints.
    shifted=solve_vertices(8.1,10)
    near(shifted["benefit"],34.3)
    near((shifted["benefit"]-34)/0.1,3)
    rejects(TypeError,finite,True,"value")
    rejects(ValueError,primal_report,2,6,8,10,-1)
    rejects(ValueError,solve_vertices,-1,-1)
    assert a["runtime_certified"] is False
    assert a["independent_review_completed"] is False
    print("PASS: Section 17.5 independent analytic reference checks")

if __name__=="__main__":
    run()
