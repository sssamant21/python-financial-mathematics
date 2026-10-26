"""Independent reference checks for Section 13.1."""
import math
from section_13_01 import finite,labels,classify,assessment

def rejects(exc,fn,*args):
    try:
        fn(*args)
    except exc:
        return
    raise AssertionError("expected "+exc.__name__)

def run():
    report=assessment()
    a=report["independent"]
    assert a["in_span"] and a["unique"] and a["long_only_feasible"]
    assert math.isclose(a["positions"]["BOND_A"],2)
    assert math.isclose(a["positions"]["BOND_B"],1)
    short=report["requires_short"]
    assert short["in_span"] and short["unique"] and not short["long_only_feasible"]
    assert math.isclose(short["positions"]["BOND_A"],1)
    assert math.isclose(short["positions"]["BOND_B"],-2)
    assert report["redundant_attainable"]["in_span"]
    assert not report["redundant_attainable"]["unique"]
    assert report["redundant_attainable"]["long_only_feasible"]
    assert not report["redundant_unattainable"]["in_span"]
    assert not report["redundant_unattainable"]["long_only_feasible"]
    assert classify(("RATE","CREDIT"),("BOND_A","BOND_B"),((2,1),(1,-1)),
                    ("RATE","CREDIT"),(5,1),True)==a
    rejects(ValueError,labels,("RATE","RATE"),"factors")
    rejects(ValueError,classify,("RATE","CREDIT"),("A","B"),((1,2),(3,)),
            ("RATE","CREDIT"),(1,2))
    rejects(ValueError,classify,("RATE","CREDIT"),("A","B"),((1,2),(3,4)),
            ("RATE","WRONG"),(1,2))
    rejects(TypeError,finite,True,"entry")
    rejects(ValueError,finite,float("inf"),"entry")
    assert not a["runtime_certified"]
    print("PASS: Section 13.1 independent reference checks")

if __name__=="__main__":
    run()
