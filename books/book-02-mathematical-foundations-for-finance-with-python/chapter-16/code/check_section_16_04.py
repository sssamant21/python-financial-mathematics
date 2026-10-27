"""Independent analytic reference checks for Book 02 Section 16.4."""
import math
from section_16_04 import (assessment,convex_combination,quadratic,quartic,
                           nonconvex,convexity_gap,portfolio_variance,
                           portfolio_gradient,portfolio_hessian,
                           covariance_determinant,weighted_linear_loss,
                           weighted_linear_hessian,centered_second_difference)

def close(a,b):
    assert math.isclose(a,b,rel_tol=1e-8,abs_tol=1e-7),(a,b)

def rejects(exc,fn,*args):
    try:
        fn(*args)
    except exc:
        return
    raise AssertionError("expected "+exc.__name__)

def run():
    a=assessment()
    close(a["convex_combination"],1.5)
    close(a["quadratic_gap"],4)
    close(convexity_gap(quadratic,0,2,0.5),1)
    close(convexity_gap(quartic,-1,1,0.5),1)
    close(a["quartic_second_derivative_at_zero"],0)
    close(a["nonconvex_second_derivative_at_one"],-10)
    close(nonconvex(1),0)
    close(a["portfolio_variance"],0.0336)
    close(a["portfolio_gradient"][0],0.056)
    close(a["portfolio_gradient"][1],0.084)
    assert a["portfolio_hessian"]==((0.08,0.02),(0.02,0.18))
    close(a["covariance_determinant"],0.0035)
    close(weighted_linear_loss(2,-1),0)
    close(weighted_linear_loss(3,0),1.5)
    assert weighted_linear_hessian()==((1.0,0.0),(0.0,2.0))
    close(a["quadratic_second_derivative_numeric"],2)
    close(centered_second_difference(quartic,0),2e-8)
    rejects(ValueError,convex_combination,0,1,1.1)
    rejects(TypeError,quadratic,True)
    rejects(ValueError,portfolio_variance,float("nan"),0.5)
    rejects(ValueError,centered_second_difference,quadratic,1,0)
    assert a["runtime_certified"] is False
    assert a["independent_review_completed"] is False
    print("PASS: Section 16.4 independent reference checks")

if __name__=="__main__":
    run()
