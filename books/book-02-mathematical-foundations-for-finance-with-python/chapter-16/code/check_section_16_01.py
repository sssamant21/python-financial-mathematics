"""Independent analytic reference checks for Book 02 Section 16.1."""
import math
from section_16_01 import (assessment,model_price,residual,loss,gradient,hessian,
                           analytic_minimizer,weighted_loss,two_variable_objective)

def close(a,b):
    assert math.isclose(a,b,rel_tol=1e-10,abs_tol=1e-8),(a,b)

def rejects(exc,fn,*args):
    try:
        fn(*args)
    except exc:
        return
    raise AssertionError("expected "+exc.__name__)

def run():
    a=assessment()
    close(model_price(0.05),1100)
    close(residual(0.04),-20)
    close(residual(0.06),20)
    close(a["optimal_rate"],0.05)
    close(a["optimal_loss"],0)
    close(a["loss_at_004"],400)
    close(a["loss_at_006"],400)
    close(a["gradient_at_optimum"],0)
    close(a["hessian"],8_000_000)
    close(analytic_minimizer(1200),0.1)
    close(loss(0.1,1200),0)
    close(two_variable_objective(2,3,2,3),0)
    close(two_variable_objective(3,4,2,3),5)
    close(a["weighted_reference_loss"],1200)
    h=1e-6
    close((loss(0.04+h)-loss(0.04-h))/(2*h),gradient(0.04))
    rejects(TypeError,loss,True)
    rejects(ValueError,loss,float("nan"))
    rejects(ValueError,weighted_loss,(0.05,),(1100,),(0,))
    rejects(ValueError,weighted_loss,(0.05,),(1100,1100),(1,))
    assert a["runtime_certified"] is False
    assert a["independent_review_completed"] is False
    print("PASS: Section 16.1 independent reference checks")

if __name__=="__main__":
    run()
