"""Independent analytic reference checks for Book 02 Section 18.5."""
import math
from section_18_05 import (assessment,finite,npv,scan_brackets,
                           bisect_npv,discover_roots)

def near(a,b,tol=1e-9):
    assert math.isclose(a,b,rel_tol=1e-10,abs_tol=tol),(a,b)

def rejects(exc,fn,*args):
    try:
        fn(*args)
    except exc:
        return
    raise AssertionError("expected "+exc.__name__)

def run():
    a=assessment()
    roots=a["discovered"]["roots"]
    assert len(roots)==2,roots
    near(roots[0],0.1)
    near(roots[1],0.2)
    near(npv(0),-2)
    near(npv(0.1),0,1e-10)
    near(npv(0.2),0,1e-10)
    expected=-100+230/1.15-132/(1.15**2)
    near(a["npv_at_15_percent"],expected)
    assert expected>0
    assert npv(0.05)<0 and npv(0.25)<0
    scan=scan_brackets((-100,230,-132),0.0,0.3,7)
    assert scan["exhaustive"] is False
    assert len(scan["brackets"])==2
    near(bisect_npv((-100,230,-132),0.05,0.15),0.1)
    near(bisect_npv((-100,230,-132),0.15,0.25),0.2)
    # A repeated root need not produce a sign change:
    # -(1-z)^2 = -1+2z-z^2 has a double root at r=0.
    repeated=scan_brackets((-1,2,-1),-0.5,0.5,3)
    assert repeated["brackets"]==[]
    assert repeated["exhaustive"] is False
    rejects(ValueError,npv,-1)
    rejects(ValueError,npv,0,(0,0,0))
    rejects(ValueError,scan_brackets,(-100,230,-132),0.3,0)
    rejects(ValueError,bisect_npv,(-100,230,-132),0,0.3)
    rejects(TypeError,finite,True,"value")
    assert a["discovered"]["completeness_certified"] is False
    assert a["runtime_certified"] is False
    assert a["independent_review_completed"] is False
    print("PASS: Section 18.5 independent analytic reference checks")

if __name__=="__main__":
    run()
