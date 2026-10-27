"""Independent analytic reference checks for Book 02 Section 18.1."""
import math
from decimal import Decimal
from section_18_01 import (assessment,finite,present_value,errors,
                           exponential_approximation,cancellation_demo,money_cents)

def near(a,b):
    assert math.isclose(a,b,rel_tol=1e-11,abs_tol=1e-12),(a,b)

def rejects(exc,fn,*args):
    try:
        fn(*args)
    except exc:
        return
    raise AssertionError("expected "+exc.__name__)

def run():
    a=assessment()
    reference=1000/1.1025
    near(a["present_value_reference"],reference)
    near(present_value(1000,0.05,2),reference)
    near(a["period_specification_error"]["estimate"],1000/(1.05**3))
    near(a["rate_unit_error"]["estimate"],1000/36)
    assert a["period_specification_error"]["errors"]["absolute"]>0
    assert a["rate_unit_error"]["errors"]["absolute"]>0
    e=errors(100,101)
    near(e["absolute"],1)
    near(e["relative"],0.01)
    assert errors(0,1)["relative"] is None
    exp=a["approximation"]
    near(exp["exact"],math.exp(0.1))
    near(exp["first_order"],1.1)
    near(exp["error"]["absolute"],math.exp(0.1)-1.1)
    cancellation=cancellation_demo(1e-12)
    near(cancellation["stable"],math.expm1(1e-12))
    assert abs(cancellation["direct"]-cancellation["stable"])>0
    assert a["binary_float_example"]!=0.3
    assert Decimal(a["rounded_cents"])==Decimal("907.03")
    rejects(TypeError,finite,True,"value")
    rejects(ValueError,present_value,1000,-1,2)
    rejects(ValueError,present_value,1000,0.05,-1)
    assert not a["runtime_certified"]
    assert not a["independent_review_completed"]
    print("PASS: Section 18.1 independent analytic reference checks")

if __name__=="__main__":
    run()
