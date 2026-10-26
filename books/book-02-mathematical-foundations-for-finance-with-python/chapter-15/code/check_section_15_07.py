"""Independent analytic reference checks for Book 02 Section 15.7."""
import math
from section_15_07 import assessment,taylor_changes,valuation,polynomial

def close(a,b):
    assert math.isclose(a,b,rel_tol=1e-10,abs_tol=1e-9),(a,b)

def rejects(exc,fn,*args):
    try:
        fn(*args)
    except exc:
        return
    raise AssertionError("expected "+exc.__name__)

def run():
    a=assessment()
    close(a["polynomial_base"],15)
    close(a["polynomial_first_order_change"],-1.4)
    close(a["polynomial_second_order_change"],-1.37)
    close(a["polynomial_exact_change"],-1.37)
    v=1000*math.exp(0.1)
    f=a["future_value"]
    close(f["base"],v)
    close(f["shocked"],1000*math.exp(0.15))
    close(f["first_order_change"],0.045*v)
    close(f["quadratic_correction"],0.0060125*v)
    close(f["second_order_change"],0.0510125*v)
    close(f["exact_change"],1000*(math.exp(0.15)-math.exp(0.1)))
    close(f["first_order_error"],f["first_order_change"]-f["exact_change"])
    close(f["second_order_error"],f["second_order_change"]-f["exact_change"])
    p=1000*math.exp(-0.1)
    d=a["present_value"]
    close(d["base"],p)
    close(d["shocked"],1000*math.exp(-0.15))
    close(d["first_order_change"],-0.045*p)
    close(d["quadratic_correction"],-0.0039875*p)
    close(d["second_order_change"],-0.0489875*p)
    close(d["exact_change"],1000*(math.exp(-0.15)-math.exp(-0.1)))
    close(d["first_order_error"],d["first_order_change"]-d["exact_change"])
    close(d["second_order_error"],d["second_order_change"]-d["exact_change"])
    zero=taylor_changes(1000,0.05,2,0,0)
    close(zero["exact_change"],0)
    close(zero["second_order_change"],0)
    rejects(ValueError,taylor_changes,1000,0.05,2,0,-3)
    rejects(ValueError,valuation,-1,0.05,2)
    rejects(ValueError,valuation,1000,float("nan"),2)
    rejects(TypeError,valuation,True,0.05,2)
    assert a["runtime_certified"] is False
    assert a["independent_review_completed"] is False
    print("PASS: Section 15.7 independent reference checks")

if __name__=="__main__":
    run()
