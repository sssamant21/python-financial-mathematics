"""Independent reference checks for Section 9.3."""
import math
from section_9_03 import (
    finite, linear_taylor, compare_change, discount_value,
    discount_shock, discount_step_ladder, revenue, revenue_derivative)

def close(a,b,rel_tol=1e-9,abs_tol=1e-8):
    assert math.isclose(a,b,rel_tol=rel_tol,abs_tol=abs_tol),(a,b)

def rejects(exc,fn,*args):
    try:
        fn(*args)
    except exc:
        return
    raise AssertionError("expected "+exc.__name__)

def run():
    close(linear_taylor(9,6,0.2),10.2)
    for h in (-0.2,-0.1,0,0.1,0.2):
        result=compare_change(lambda x:x*x,lambda x:2*x,3,h)
        close(result["linear_value"],9+6*h)
        close(result["signed_error"],h*h)
    for h in (0.01,0.005,0.001,0.0001,-0.001):
        result=discount_shock(10000,5,0.04,h)
        v=10000*math.exp(-0.2)
        close(result["baseline_value"],v)
        close(result["exact_change"],v*math.expm1(-5*h))
        close(result["linear_change"],-5*v*h)
        assert result["signed_error"]>=0
        close(result["absolute_error"],result["signed_error"])
    ladder=discount_step_ladder(10000,5,0.04,(0.01,0.005,0.001))
    assert len(ladder)==3
    ratio=ladder[0]["absolute_error"]/ladder[1]["absolute_error"]
    assert 3.9<ratio<4.1
    close(discount_value(10000,5,0.04),10000*math.exp(-0.2))
    revenue_result=compare_change(revenue,revenue_derivative,100,5)
    close(revenue_result["linear_value"],3100)
    close(revenue_result["exact_change"],97.5)
    close(revenue_result["signed_error"],-2.5)
    assert compare_change(lambda x:x,lambda x:1,2,0)["relative_change_error"] is None
    rejects(ValueError,discount_value,0,5,0.04)
    rejects(ValueError,discount_value,1000,-1,0.04)
    rejects(ValueError,revenue,-1)
    rejects(TypeError,compare_change,3,lambda x:x,1,0.1)
    rejects(TypeError,finite,True,"value")
    rejects(ValueError,finite,float("nan"),"value")
    print("PASS: Section 9.3 reference checks")

if __name__=="__main__":
    run()
