"""Independent reference checks for Book 02 Section 15.1."""
import math
from section_15_01 import account_value,present_value,rate_for_target,assessment

def close(a,b):
    assert math.isclose(a,b,rel_tol=1e-11,abs_tol=1e-10),(a,b)

def rejects(exc,fn,*args):
    try:
        fn(*args)
    except exc:
        return
    raise AssertionError("expected "+exc.__name__)

def run():
    p=assessment()
    close(p["reference_value"],1000*math.exp(0.1))
    close(p["higher_rate_value"],1000*math.exp(0.12))
    close(p["scenario_difference"],1000*(math.exp(0.12)-math.exp(0.1)))
    close(p["reference_present_value"],1000*math.exp(-0.1))
    expected=((1000,1000),
              (1000*math.exp(0.05),1000*math.exp(0.1)),
              (1000*math.exp(0.1),1000*math.exp(0.2)))
    for row,reference in zip(p["scenario_grid"],expected):
        for actual,answer in zip(row,reference):
            close(actual,answer)
    close(p["recovered_rate"],0.05)
    close(account_value(0,0.05,2),0)
    close(account_value(1000,0,2),1000)
    close(present_value(-100,0,0),-100)
    rejects(ValueError,account_value,-1,0.05,2)
    rejects(ValueError,account_value,1000,0.05,-2)
    rejects(ValueError,account_value,1000,float("nan"),2)
    rejects(TypeError,account_value,True,0.05,2)
    rejects(ValueError,rate_for_target,1000,1100,0)
    rejects(ValueError,present_value,1000,0.05,-1)
    assert p["runtime_certified"] is False
    assert p["independent_review_completed"] is False
    print("PASS: Section 15.1 independent reference checks")

if __name__=="__main__":
    run()
