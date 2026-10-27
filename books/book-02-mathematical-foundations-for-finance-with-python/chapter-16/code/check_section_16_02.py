"""Independent analytic reference checks for Book 02 Section 16.2."""
import math
from section_16_02 import (assessment,scalar_quadratic,scalar_gradient,cubic,
                           saddle,separable,separable_gradient,coupled_loss,
                           coupled_gradient,financial_loss,financial_gradient,
                           financial_optimum,centered_difference)

def close(a,b):
    assert math.isclose(a,b,rel_tol=1e-9,abs_tol=1e-7),(a,b)

def rejects(exc,fn,*args):
    try:
        fn(*args)
    except exc:
        return
    raise AssertionError("expected "+exc.__name__)

def run():
    a=assessment()
    close(a["scalar_stationary_point"],3)
    close(a["scalar_minimum_value"],5)
    close(a["scalar_gradient_at_optimum"],0)
    close(scalar_quadratic(2),6)
    close(scalar_gradient(2),-2)
    close(cubic(-0.1),-0.001)
    close(cubic(0.1),0.001)
    close(saddle(1,0),1)
    close(saddle(0,1),-1)
    close(separable(1,-2),0)
    close(separable_gradient(1,-2)[0],0)
    close(separable_gradient(1,-2)[1],0)
    close(coupled_loss(2,1),0)
    close(coupled_gradient(2,1)[0],0)
    close(coupled_gradient(2,1)[1],0)
    close(coupled_loss(0,0),10)
    close(financial_optimum(),0.05)
    close(financial_loss(0.05),0)
    close(financial_gradient(0.05),0)
    close(financial_loss(0.04),400)
    close(financial_gradient(0.04),-80000)
    close(a["financial_gradient_finite_difference"],-80000)
    close(centered_difference(scalar_quadratic,2),-2)
    rejects(TypeError,scalar_quadratic,True)
    rejects(ValueError,financial_loss,float("nan"))
    rejects(ValueError,centered_difference,scalar_quadratic,2,0)
    assert a["runtime_certified"] is False
    assert a["independent_review_completed"] is False
    print("PASS: Section 16.2 independent reference checks")

if __name__=="__main__":
    run()
