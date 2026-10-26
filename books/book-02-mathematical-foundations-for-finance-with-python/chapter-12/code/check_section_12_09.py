"""Independent reference checks for Section 12.9 capstone."""
import math
from section_12_09 import ExposureSystem,Vector,finite,evaluate,assessment

def close(a,b,rel=1e-8,abs_tol=1e-8):
    assert math.isclose(a,b,rel_tol=rel,abs_tol=abs_tol),(a,b)

def rejects(exc,fn,*args):
    try:
        fn(*args)
    except exc:
        return
    raise AssertionError("expected "+exc.__name__)

def run():
    report=assessment()
    ref=report["reference"]
    assert ref["decision"]=="ACCEPT" and ref["reason"]=="accepted"
    close(ref["positions"]["BOND_A"],2)
    close(ref["positions"]["BOND_B"],1)
    close(ref["condition_number_inf"],3)
    close(ref["residual_inf"],0)
    assert all(ref["factor_pass"].values())
    fragile=report["near_duplicate"]
    assert fragile["decision"]=="REJECT"
    assert fragile["reason"]=="condition_guardrail_exceeded"
    close(fragile["condition_number_inf"],40004.0001)
    assert not fragile["runtime_certified"]
    a=ExposureSystem(("RATE","CREDIT"),("BOND_A","BOND_B"),((2,1),(1,-1)),"standardized_sensitivity")
    b=Vector(("RATE","CREDIT"),(5,1),"standardized_exposure")
    t=Vector(("RATE","CREDIT"),(0.15,0.10),"standardized_exposure")
    assert evaluate(a,b,t)==ref
    rejects(ValueError,evaluate,a,Vector(("RATE","WRONG"),(5,1),"standardized_exposure"),t)
    rejects(ValueError,evaluate,a,b,Vector(("RATE","CREDIT"),(-0.1,0.1),"standardized_exposure"))
    rejects(ValueError,evaluate,ExposureSystem(("RATE","CREDIT"),("A","B"),((1,2),(2,4)),"standardized_sensitivity"),b,t)
    rejects(ValueError,ExposureSystem,("RATE","RATE"),("A","B"),((1,2),(3,4)),"standardized_sensitivity")
    rejects(ValueError,ExposureSystem,("RATE","CREDIT"),("A","B"),((1,2),(3,)),"standardized_sensitivity")
    rejects(ValueError,Vector,("RATE",),(float("nan"),),"standardized_exposure")
    rejects(TypeError,finite,True,"value")
    print("PASS: Section 12.9 independent reference checks")

if __name__=="__main__":
    run()
