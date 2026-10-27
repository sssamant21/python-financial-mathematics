"""Independent analytic reference checks for Book 02 Section 16.6."""
import math
from section_16_06 import (assessment,finite,loss,gradient,hessian,newton_step,
                           newton_solve,scalar_secant_curvature,quasi_newton_step)

def close(a,b):
    assert math.isclose(a,b,rel_tol=1e-10,abs_tol=1e-10),(a,b)

def rejects(exc,fn,*args,**kwargs):
    try:
        fn(*args,**kwargs)
    except exc:
        return
    raise AssertionError("expected "+exc.__name__)

def run():
    a=assessment()
    close(loss(0),0.0025)
    close(gradient(0),-0.1)
    close(hessian(0),2)
    close(newton_step(0,gradient,hessian),0.05)
    close(newton_step(0,gradient,hessian,0.5),0.025)
    assert a["newton_result"]["status"]=="gradient_tolerance"
    assert a["newton_result"]["iterations"]==1
    close(a["newton_result"]["x"],0.05)
    close(a["secant_curvature"],2)
    close(a["quasi_newton_update"],0.05)
    close(scalar_secant_curvature(-0.2,0.2,gradient),2)
    close(quasi_newton_step(0.1,gradient,2),0.05)
    rejects(TypeError,finite,True,"input")
    rejects(ValueError,newton_step,0,gradient,lambda x:-2)
    rejects(ValueError,newton_step,0,gradient,hessian,0)
    rejects(ValueError,scalar_secant_curvature,0,0,gradient)
    rejects(ValueError,scalar_secant_curvature,0,1,lambda x:-x)
    rejects(ValueError,quasi_newton_step,0,gradient,0)
    rejects(ValueError,newton_solve,0,gradient,hessian,max_iterations=0)
    assert a["runtime_certified"] is False
    assert a["independent_review_completed"] is False
    print("PASS: Section 16.6 independent reference checks")

if __name__=="__main__":
    run()
