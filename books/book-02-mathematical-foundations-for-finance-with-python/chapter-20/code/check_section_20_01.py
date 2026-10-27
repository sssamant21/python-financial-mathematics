"""Independent reference-check source for Book 02 Section 20.1."""
import math
from section_20_01 import present_value,assess

def near(actual,expected,rel=1e-12,abs_=1e-10):
    assert math.isclose(actual,expected,rel_tol=rel,abs_tol=abs_),(actual,expected)

def rejects(exc,fn,*args):
    try:
        fn(*args)
    except exc:
        return
    raise AssertionError("expected "+exc.__name__)

def run():
    near(present_value(1000,0,5),1000)
    near(present_value(1000,0.05,0),1000)
    near(present_value(1000,0.05,2),1000*math.exp(-0.1))
    near(present_value(1000,-0.02,2),1000*math.exp(0.04))
    near(present_value(0,0.05,2),0)
    near(present_value(-1000,0.05,2),-1000*math.exp(-0.1))
    near(present_value(400+600,0.05,2),
         present_value(400,0.05,2)+present_value(600,0.05,2))
    assert present_value(1000,0.04,2)<present_value(1000,0.03,2)
    assert present_value(-1000,0.04,2)>present_value(-1000,0.03,2)
    rejects(ValueError,present_value,1000,0.05,-1)
    rejects(ValueError,present_value,float("nan"),0.05,2)
    rejects(ValueError,present_value,1000,float("inf"),2)
    rejects(ValueError,present_value,1000,-1000,2)
    rejects(TypeError,present_value,True,0.05,2)
    a=assess()
    assert a["runtime_certified"] is False
    assert a["independent_review_completed"] is False
    print("PASS: Section 20.1 independent reference checks")

if __name__=="__main__":
    run()
