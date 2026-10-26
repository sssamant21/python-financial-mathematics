"""Independent analytic reference checks for Book 02 Section 15.8."""
import math
from section_15_08 import (assessment,future_value,iso_value_slope,
                           exact_unchanged_value_time,portfolio_variance,
                           portfolio_gradient,iso_variance_slope,
                           fully_invested_derivative)

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
    close(a["base_future_value"],1000*math.exp(0.1))
    close(a["iso_value_slope"],-40)
    close(a["linear_time_adjustment"],-0.04)
    close(a["exact_adjusted_maturity"],0.1/0.051)
    close(a["exact_time_adjustment"],0.1/0.051-2)
    close(a["revalued_future_value"],1000*math.exp(0.1))
    close(a["portfolio_variance"],0.0336)
    close(a["portfolio_gradient"][0],0.056)
    close(a["portfolio_gradient"][1],0.084)
    close(a["unconstrained_iso_variance_slope"],-2/3)
    close(a["fully_invested_derivative"],-0.028)
    h=1e-6
    fd=(portfolio_variance(0.6+h,0.4-h)-
        portfolio_variance(0.6-h,0.4+h))/(2*h)
    close(fd,a["fully_invested_derivative"])
    rejects(ValueError,iso_value_slope,0,2)
    rejects(ValueError,exact_unchanged_value_time,0.05,2,-0.05)
    rejects(ValueError,fully_invested_derivative,0.6,0.3)
    rejects(ValueError,future_value,0,0.05,2)
    rejects(TypeError,portfolio_variance,True,0.4)
    rejects(ValueError,portfolio_gradient,float("nan"),0.4)
    assert a["runtime_certified"] is False
    assert a["independent_review_completed"] is False
    print("PASS: Section 15.8 independent reference checks")

if __name__=="__main__":
    run()
