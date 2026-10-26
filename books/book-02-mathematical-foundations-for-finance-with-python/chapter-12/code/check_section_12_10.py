"""Independent reference checks for Section 12.10 cumulative assessment."""
import math
from section_12_10 import finite,checked_labels,align,gaussian_solve,condition_inf,assess,assessment

def close(actual,expected,rel=1e-8,abs_tol=1e-8):
    assert math.isclose(actual,expected,rel_tol=rel,abs_tol=abs_tol),(actual,expected)

def rejects(exc,fn,*args):
    try:
        fn(*args)
    except exc:
        return
    raise AssertionError("expected "+exc.__name__)

def run():
    a=((2,1),(1,-1))
    report=assessment()
    ref=report["reference"]
    assert ref["decision"]=="ACCEPT"
    close(ref["positions"]["BOND_A"],2)
    close(ref["positions"]["BOND_B"],1)
    close(ref["condition_number_inf"],3)
    assert all(abs(v)<1e-10 for v in ref["residual"].values())
    fragile=report["fragile"]
    assert fragile["decision"]=="REJECT"
    assert fragile["reason"]=="condition_guardrail_exceeded"
    close(fragile["condition_number_inf"],40004.0001)
    assert not ref["runtime_certified"]
    assert align(("CREDIT","RATE"),(1,5),("RATE","CREDIT"))==(5.0,1.0)
    assert gaussian_solve(((0,1),(2,3)),(1,5))==(1.0,1.0)
    close(condition_inf(a),3)
    reordered=assess(a,("RATE","CREDIT"),("BOND_A","BOND_B"),
                     ("RATE","CREDIT"),(5,1),("RATE","CREDIT"),(0.15,0.10))
    assert reordered==ref
    rejects(ValueError,gaussian_solve,((1,2),(2,4)),(3,6))
    rejects(ValueError,assess,a,("RATE","CREDIT"),("BOND_A","BOND_B"),
            ("RATE","WRONG"),(5,1),("RATE","CREDIT"),(0.15,0.10))
    rejects(ValueError,assess,a,("RATE","CREDIT"),("BOND_A","BOND_B"),
            ("RATE","CREDIT"),(5,1),("RATE","CREDIT"),(-0.15,0.10))
    rejects(ValueError,checked_labels,("RATE","RATE"),"factors")
    rejects(ValueError,gaussian_solve,((1,2),(3,)),(1,2))
    rejects(TypeError,finite,True,"value")
    rejects(ValueError,finite,float("nan"),"value")
    print("PASS: Section 12.10 independent reference checks")

if __name__=="__main__":
    run()
