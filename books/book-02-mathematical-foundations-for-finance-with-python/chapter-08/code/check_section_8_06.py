"""Reference checks for Section 8.6."""
import math
from section_8_06 import (
    finite, polynomial, derivative_coefficients, profit, marginal_profit,
    profit_curvature, present_value, pv_rate_first, pv_rate_second,
    pv_shock, pv_shock_exact, cash_flow_rate_derivatives,
    centered_second_difference)

def close(a, b, rel_tol=1e-7, abs_tol=1e-7):
    assert math.isclose(a, b, rel_tol=rel_tol, abs_tol=abs_tol), (a, b)

def rejects(exc, function, *args):
    try:
        function(*args)
    except exc:
        return
    raise AssertionError("expected " + exc.__name__)

def check_second_difference_orders():
    steps=[2.0**(-k) for k in range(1,6)]
    for x in (0.0,0.5,1.0,-1.0):
        errors=[]
        for h in steps:
            # Exact expansion: D2(x^4)=12*x^2+2*h^2.
            approximation=centered_second_difference(lambda z:z**4,x,h)
            assert approximation==12*x*x+2*h*h
            assert centered_second_difference(lambda z:z**4,x,-h)==approximation
            errors.append(abs(approximation-12*x*x))
            assert centered_second_difference(lambda z:z*z,x,h)==2
        assert all(coarse/fine==4 for coarse,fine in zip(errors,errors[1:]))
    # Vanishing lower error coefficient gives a special fourth-order example.
    errors=[centered_second_difference(lambda z:z**6,0,h) for h in steps]
    assert errors==[2*h**4 for h in steps]
    assert all(coarse/fine==16 for coarse,fine in zip(errors,errors[1:]))
    # Distinct representable perturbations do not guarantee an accurate stencil.
    h=2.0**-40
    assert 1+h!=1 and 1-h!=1 and h*h>0
    cancelled=centered_second_difference(lambda z:z*z,1,h)
    assert cancelled==0  # true second derivative is two
    assert abs(cancelled-2)>abs(centered_second_difference(lambda z:z*z,1,0.25)-2)

def run():
    check_second_difference_orders()
    assert derivative_coefficients((0, 1, 0, -3, 2), 1) == (1.0, 0.0, -9.0, 8.0)
    assert derivative_coefficients((0, 1, 0, -3, 2), 2) == (0.0, -18.0, 24.0)
    assert derivative_coefficients((0, 1, 0, -3, 2), 3) == (-18.0, 48.0)
    assert derivative_coefficients((7,), 3) == (0.0,)
    close(marginal_profit(160), 0)
    close(profit_curvature(160), -0.5)
    assert profit(160) > profit(100) and profit(160) > profit(200)
    for r in (-0.02, 0, 0.04, 0.1):
        for t in (0, 1, 5, 10):
            pv = present_value(10000, r, t)
            close(pv_rate_first(10000, r, t), -t*pv)
            close(pv_rate_second(10000, r, t), t*t*pv)
            close(centered_second_difference(lambda x:present_value(10000, x, t), r, 1e-3),
                  pv_rate_second(10000, r, t), rel_tol=2e-5)
            h = 1e-3
            close(pv_shock_exact(10000, r, t, h),
                  present_value(10000, r+h, t)-pv, rel_tol=1e-6)
    first = pv_shock(10000, 0.04, 5, 0.01, 1)
    second = pv_shock(10000, 0.04, 5, 0.01, 2)
    exact = pv_shock_exact(10000, 0.04, 5, 0.01)
    assert abs(second-exact) < abs(first-exact)
    v, d1, d2 = cash_flow_rate_derivatives([(100, 1), (200, 3)], 0.04)
    close(v, 100*math.exp(-0.04)+200*math.exp(-0.12))
    close(d1, -100*math.exp(-0.04)-600*math.exp(-0.12))
    close(d2, 100*math.exp(-0.04)+1800*math.exp(-0.12))
    assert d2 > 0
    assert cash_flow_rate_derivatives([(-100, 1)], 0.04)[2] < 0
    rejects(ValueError, profit, -1)
    rejects(ValueError, present_value, -1, 0.04, 5)
    rejects(ValueError, pv_shock, 100, 0.04, 5, 0.01, 3)
    rejects(ValueError, cash_flow_rate_derivatives, [(100, -1)], 0.04)
    rejects(ValueError, centered_second_difference, lambda x:x*x, 1, 0)
    rejects(TypeError, finite, True, "value")
    rejects(ValueError, finite, float("nan"), "value")
    print("PASS: Section 8.6 reference checks")

if __name__ == "__main__":
    run()
