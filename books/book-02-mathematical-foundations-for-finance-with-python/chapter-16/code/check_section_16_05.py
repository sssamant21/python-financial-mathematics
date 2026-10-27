"""Independent analytic reference checks for Book 02 Section 16.5."""
import math
from section_16_05 import (assessment,finite,normalized_loss,normalized_gradient,
                           quadratic_loss,quadratic_gradient,gradient_descent,
                           armijo_step)

def close(a,b,rel=1e-9,abs_=1e-9):
    assert math.isclose(a,b,rel_tol=rel,abs_tol=abs_),(a,b)

def rejects(exc,fn,*args,**kwargs):
    try:
        fn(*args,**kwargs)
    except exc:
        return
    raise AssertionError("expected "+exc.__name__)

def run():
    a=assessment()
    for x,expected in zip(a["first_five_rates"],
                          (0,0.025,0.0375,0.04375,0.046875)):
        close(x,expected)
    close(a["optimal_rate"],0.05)
    close(a["final_rate"],0.05,abs_=1e-8)
    assert a["status"]=="gradient_tolerance"
    close(a["final_loss"],0,abs_=1e-14)
    close(normalized_gradient(0),-0.1)
    close(normalized_loss(0),0.0025)
    close(quadratic_loss(0),0.0025)
    close(quadratic_gradient(0),-0.1)
    one=gradient_descent(0,normalized_loss,normalized_gradient,step=0.5)
    close(one["x"],0.05)
    assert one["iterations"]==1
    oscillating=gradient_descent(0,normalized_loss,normalized_gradient,
                                 step=1.0,tolerance=0,max_iterations=4)
    close(oscillating["x"],0)
    assert oscillating["status"]=="max_iterations"
    diverging=gradient_descent(0,normalized_loss,normalized_gradient,
                               step=1.25,tolerance=0,max_iterations=3)
    assert abs(diverging["x"]-0.05)>0.05
    assert a["armijo"]["status"]=="accepted"
    assert a["armijo"]["new_objective"]<normalized_loss(0)
    stagnant=armijo_step(1.0,lambda x:x,lambda x:1,initial_step=1e-20)
    assert stagnant["status"]=="stagnation" and stagnant["new_x"]==1.0
    flat=armijo_step(1.0,lambda x:1.0,lambda x:1,initial_step=0.1,max_backtracks=2)
    assert flat["status"]=="line_search_failed"
    rejects(TypeError,finite,True,"value")
    rejects(ValueError,gradient_descent,0,normalized_loss,normalized_gradient,step=0)
    rejects(ValueError,gradient_descent,0,normalized_loss,normalized_gradient,max_iterations=0)
    rejects(ValueError,armijo_step,0,normalized_loss,normalized_gradient,shrink=1)
    assert a["runtime_certified"] is False
    assert a["independent_review_completed"] is False
    print("PASS: Section 16.5 independent reference checks")

if __name__=="__main__":
    run()
