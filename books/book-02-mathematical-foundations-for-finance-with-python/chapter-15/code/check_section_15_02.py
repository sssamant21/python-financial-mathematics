"""Independent mathematical checks for Book 02 Section 15.2."""
import math
from section_15_02 import (assessment,future_value,present_value,
                           future_partials,present_partials,centered_rate_difference)

def close(a,b,rel=1e-8):
    assert math.isclose(a,b,rel_tol=rel,abs_tol=1e-8),(a,b)

def rejects(exc,fn,*args):
    try:
        fn(*args)
    except exc:
        return
    raise AssertionError("expected "+exc.__name__)

def run():
    a=assessment()
    exp=math.exp(0.1)
    disc=math.exp(-0.1)
    close(a["future_value"],1000*exp)
    close(a["future_partials"]["principal"],exp)
    close(a["future_partials"]["rate"],2000*exp)
    close(a["future_partials"]["time"],50*exp)
    close(a["present_value"],1000*disc)
    close(a["present_partials"]["cash_flow"],disc)
    close(a["present_partials"]["rate"],-2000*disc)
    close(a["present_partials"]["time"],-50*disc)
    close(a["first_order_rate_change"],20*exp)
    close(a["exact_rate_change"],1000*(math.exp(0.12)-exp))
    close(a["centered_future_rate_derivative"],2000*exp)
    close(a["centered_present_rate_derivative"],-2000*disc)
    close(future_partials(1000,0.05,0)["rate"],0)
    close(present_partials(1000,0.05,0)["rate"],0)
    rejects(ValueError,future_value,-1,0.05,2)
    rejects(ValueError,present_value,1000,0.05,-1)
    rejects(TypeError,future_value,True,0.05,2)
    rejects(ValueError,future_value,1000,float("nan"),2)
    rejects(ValueError,centered_rate_difference,future_value,1000,0.05,2,0)
    rejects(ValueError,centered_rate_difference,future_value,1000,0.05,2,-1)
    assert a["runtime_certified"] is False
    assert a["independent_review_completed"] is False
    print("PASS: Section 15.2 independent reference checks")

if __name__=="__main__":
    run()
