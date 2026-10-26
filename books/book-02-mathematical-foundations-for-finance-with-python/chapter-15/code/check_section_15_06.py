"""Independent reference checks for Book 02 Section 15.6."""
import math
from section_15_06 import (assessment,polynomial,polynomial_hessian,value,
                           rate_time_hessian,second_order_change,portfolio_hessian)

def close(a,b):
    assert math.isclose(a,b,rel_tol=1e-10,abs_tol=1e-9),(a,b)

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
    v=1000*math.exp(0.1)
    close(a["polynomial_value"],15)
    vector(a["polynomial_gradient"],(8,11))
    assert a["polynomial_hessian"]==((2.0,3.0),(3.0,4.0))
    close(a["polynomial_hessian_determinant"],-1)
    close(a["polynomial_exact_change"],-1.37)
    close(a["future_value"],v)
    vector(a["rate_time_gradient"],(2*v,0.05*v))
    h=a["rate_time_hessian"]
    vector(h[0],(4*v,1.1*v))
    vector(h[1],(1.1*v,0.0025*v))
    close(h[0][1],h[1][0])
    close(a["first_order_change"],0.045*v)
    close(a["quadratic_correction"],0.0060125*v)
    close(a["second_order_change"],0.0510125*v)
    close(a["exact_change"],1000*(math.exp(0.15)-math.exp(0.1)))
    vector(a["portfolio_hessian"][0],(0.08,0.02))
    vector(a["portfolio_hessian"][1],(0.02,0.18))
    rejects(ValueError,value,1000,0.05,-1)
    rejects(TypeError,value,True,0.05,2)
    rejects(ValueError,value,1000,float("nan"),2)
    rejects(ValueError,portfolio_hessian,((1,2),(3,1)))
    rejects(ValueError,portfolio_hessian,((1,2),(2,1)))
    assert a["runtime_certified"] is False
    assert a["independent_review_completed"] is False
    print("PASS: Section 15.6 independent reference checks")

if __name__=="__main__":
    run()
