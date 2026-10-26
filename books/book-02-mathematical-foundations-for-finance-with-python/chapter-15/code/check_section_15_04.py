"""Independent reference checks for Book 02 Section 15.4."""
import math
from section_15_04 import (assessment,portfolio_variance,portfolio_gradient,
                           directional_derivative,unit_direction,valuation_gradient)

def close(a,b):
    assert math.isclose(a,b,rel_tol=1e-9,abs_tol=1e-10),(a,b)

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
    c=((0.04,0.01),(0.01,0.09))
    w=(0.6,0.4)
    u=(1/math.sqrt(2),-1/math.sqrt(2))
    close(a["portfolio_variance"],0.0336)
    vector(a["portfolio_gradient"],(0.056,0.084))
    vector(a["unit_weight_preserving_direction"],u)
    close(a["directional_derivative"],-0.028/math.sqrt(2))
    close(a["quadratic_curvature_coefficient"],0.055)
    close(a["exact_variance_change"],
          -0.028/math.sqrt(2)*0.01+0.055*0.01**2)
    close(a["linear_variance_change"],-0.028/math.sqrt(2)*0.01)
    e=math.exp(0.1)
    vector(a["valuation_gradient"],(e,2000*e,50*e))
    close(a["valuation_path_derivative"],145*e)
    h=1e-5
    plus=portfolio_variance(c,(w[0]+h*u[0],w[1]+h*u[1]))
    minus=portfolio_variance(c,(w[0]-h*u[0],w[1]-h*u[1]))
    close((plus-minus)/(2*h),a["directional_derivative"])
    rejects(ValueError,unit_direction,(0,0))
    rejects(ValueError,portfolio_variance,((1,2),(3,1)),w)
    rejects(ValueError,portfolio_variance,((1,2),(2,1)),w)
    rejects(TypeError,portfolio_gradient,c,(True,0.4))
    rejects(ValueError,valuation_gradient,1000,float("nan"),2)
    rejects(ValueError,valuation_gradient,1000,0.05,-1)
    assert a["runtime_certified"] is False
    assert a["independent_review_completed"] is False
    print("PASS: Section 15.4 independent reference checks")

if __name__=="__main__":
    run()
