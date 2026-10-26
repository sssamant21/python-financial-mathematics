"""Independent reference checks for Book 02 Section 15.3."""
import math
from section_15_03 import (assessment,future_value,total_differential,
                           scenario_change,polynomial_value,polynomial_differential)

def close(actual,expected):
    assert math.isclose(actual,expected,rel_tol=1e-10,abs_tol=1e-9),(actual,expected)

def rejects(exc,fn,*args):
    try:
        fn(*args)
    except exc:
        return
    raise AssertionError("expected "+exc.__name__)

def run():
    a=assessment()
    exp=math.exp(0.1)
    approximate=exp*(100+2000*0.01+50*0.5)
    exact=1100*math.exp(0.15)-1000*exp
    close(a["base_value"],1000*exp)
    close(a["shocked_value"],1100*math.exp(0.15))
    close(a["total_differential"],approximate)
    close(a["exact_scenario_change"],exact)
    close(a["path_derivative_at_zero"],approximate)
    close(a["linearization_error_exact_minus_approximate"],exact-approximate)
    close(a["polynomial_differential"],-0.1)
    close(a["polynomial_exact_change"],-0.103)
    close(total_differential(1000,0.05,2,0,0,0),0)
    close(scenario_change(1000,0.05,2,0,0,0),0)
    rejects(ValueError,future_value,-1,0.05,2)
    rejects(ValueError,scenario_change,1000,0.05,2,-1100,0,0)
    rejects(ValueError,scenario_change,1000,0.05,2,0,0,-3)
    rejects(TypeError,total_differential,True,0.05,2,100,0.01,0.5)
    rejects(ValueError,total_differential,1000,float("nan"),2,100,0.01,0.5)
    assert a["runtime_certified"] is False
    assert a["independent_review_completed"] is False
    print("PASS: Section 15.3 independent reference checks")

if __name__=="__main__":
    run()
