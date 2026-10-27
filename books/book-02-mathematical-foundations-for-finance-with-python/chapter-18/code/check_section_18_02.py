"""Independent analytic reference checks for Book 02 Section 18.2."""
import math
import sys
from decimal import Decimal
from section_18_02 import (assessment,finite,growth_factor,growth_increment,
                           discount_change,annuity_present_value,decimal_cents)

def near(a,b,rel=1e-11,abs_=1e-13):
    assert math.isclose(a,b,rel_tol=rel,abs_tol=abs_),(a,b)

def rejects(exc,fn,*args):
    try:
        fn(*args)
    except exc:
        return
    raise AssertionError("expected "+exc.__name__)

def run():
    a=assessment()
    assert a["machine_epsilon"]==sys.float_info.epsilon==2**-52
    assert a["unit_roundoff"]==2**-53
    assert a["decimal_float_example"]!=0.3
    x=1e-12
    near(a["expm1_comparison"]["stable"],math.expm1(x))
    assert a["expm1_comparison"]["direct"]!=a["expm1_comparison"]["stable"]
    near(a["log1p_comparison"]["stable"],math.log1p(x))
    near(growth_factor(0.05,2),1.1025)
    near(growth_increment(0.05,2),0.1025)
    near(discount_change(0.05,2),(1.05)**-2-1)
    near(growth_increment(1e-12,12),12e-12,rel=1e-9)
    near(annuity_present_value(100,0.05,12),
         sum(100/(1.05)**k for k in range(1,13)))
    near(annuity_present_value(100,0,12),1200)
    assert a["naive_sum"]==0
    assert a["accurate_sum"]==1
    assert Decimal(a["decimal_cents"])==Decimal("907.02")
    assert decimal_cents("1.005")=="1.00"
    rejects(TypeError,finite,True,"value")
    rejects(ValueError,growth_factor,-1,2)
    rejects(ValueError,growth_increment,0.05,-1)
    rejects(ValueError,annuity_present_value,-1,0.05,12)
    rejects(TypeError,decimal_cents,0.1)
    rejects(ValueError,decimal_cents,"NaN")
    assert a["runtime_certified"] is False
    assert a["independent_review_completed"] is False
    print("PASS: Section 18.2 independent analytic reference checks")

if __name__=="__main__":
    run()
