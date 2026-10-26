"""Independent reference checks for Book 02 Section 15.5."""
import math
from section_15_05 import (assessment,algebra_outputs,financial_outputs,
                           financial_jacobian,apply_jacobian,
                           centered_financial_column)

def close(a,b):
    assert math.isclose(a,b,rel_tol=1e-8,abs_tol=1e-8),(a,b)

def vector(a,b):
    assert len(a)==len(b)
    for x,y in zip(a,b):
        close(x,y)

def rejects(exc,fn,*args):
    try:
        fn(*args)
    except exc:
        return
    raise AssertionError("expected "+exc.__name__)

def run():
    a=assessment()
    vector(a["algebra_outputs"],(7,18))
    assert a["algebra_jacobian"]==((4,1.0),(9,12))
    vector(a["algebra_first_order_change"],(0.2,-1.5))
    vector(a["algebra_exact_change"],(0.21,-1.536))
    e1=math.exp(0.1)
    e2=math.exp(0.2)
    vector(a["financial_outputs"],(1000*e1,500*e2))
    j=a["financial_jacobian"]
    vector(j[0],(2000*e1,50*e1))
    vector(j[1],(2000*e2,50*e2))
    vector(a["financial_first_order_change"],(45*e1,45*e2))
    vector(a["financial_exact_change"],
           (1000*(math.exp(0.15)-e1),
            500*(math.exp(0.3)-e2)))
    vector(a["centered_rate_column"],(j[0][0],j[1][0]))
    vector(a["centered_time_column"],(j[0][1],j[1][1]))
    close(a["jacobian_determinant"],0)
    rejects(ValueError,financial_outputs,0.05,-1)
    rejects(TypeError,financial_outputs,True,2)
    rejects(ValueError,financial_outputs,float("nan"),2)
    rejects(ValueError,centered_financial_column,0.05,0,1,1e-5)
    rejects(ValueError,centered_financial_column,0.05,2,0,0)
    rejects(ValueError,apply_jacobian,((1,2),),(0,1))
    assert a["runtime_certified"] is False
    assert a["independent_review_completed"] is False
    print("PASS: Section 15.5 independent reference checks")

if __name__=="__main__":
    run()
