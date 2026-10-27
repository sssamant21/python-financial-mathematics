"""Independent analytic reference checks for Book 02 Section 16.3."""
import math
from section_16_03 import (assessment,quadratic_minimum,quadratic_maximum,
                           saddle,quartic_minimum,quartic_saddle,
                           classify_hessian_2x2,financial_loss,
                           financial_gradient,financial_hessian,
                           centered_second_difference)

def close(a,b,rel=1e-7,abs_=1e-5):
    assert math.isclose(a,b,rel_tol=rel,abs_tol=abs_),(a,b)

def rejects(exc,fn,*args):
    try:
        fn(*args)
    except exc:
        return
    raise AssertionError("expected "+exc.__name__)

def run():
    a=assessment()
    assert a["minimum"]["category"]=="positive definite"
    assert a["maximum"]["category"]=="negative definite"
    assert a["saddle"]["category"]=="indefinite"
    assert "inconclusive" in a["zero_hessian"]["category"]
    close(a["minimum"]["determinant"],24)
    close(a["maximum"]["determinant"],24)
    close(a["saddle"]["determinant"],-4)
    close(a["minimum"]["eigenvalues"][0],6)
    close(a["minimum"]["eigenvalues"][1],4)
    close(quadratic_minimum(1,-2),0)
    close(quadratic_maximum(1,-2),0)
    close(saddle(1,0),1)
    close(saddle(0,1),-1)
    close(quartic_minimum(1,0),1)
    close(quartic_minimum(0,1),1)
    close(quartic_saddle(1,0),1)
    close(quartic_saddle(0,1),-1)
    close(a["financial_optimum"],0.05)
    close(a["financial_loss_at_optimum"],0)
    close(a["financial_gradient_at_optimum"],0)
    close(a["financial_hessian"],8_000_000)
    close(a["financial_hessian_finite_difference"],8_000_000)
    close(centered_second_difference(lambda x:x*x,0),2)
    rejects(TypeError,quadratic_minimum,True,0)
    rejects(ValueError,classify_hessian_2x2,1,float("nan"),1)
    rejects(ValueError,classify_hessian_2x2,1,0,1,-1)
    rejects(ValueError,centered_second_difference,financial_loss,0.05,0)
    assert a["runtime_certified"] is False
    assert a["independent_review_completed"] is False
    print("PASS: Section 16.3 independent reference checks")

if __name__=="__main__":
    run()
