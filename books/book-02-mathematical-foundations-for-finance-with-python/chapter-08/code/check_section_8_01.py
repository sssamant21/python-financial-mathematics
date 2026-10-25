"""Reference checks for Section 8.1."""
import math
from section_8_01 import (
    finite, quadratic, quadratic_derivative, forward_difference,
    centered_difference, present_value, present_value_derivative,
    stable_present_value_difference_quotient, profit, marginal_profit)

def close(a, b, rel_tol=1e-9, abs_tol=1e-9):
    assert math.isclose(a, b, rel_tol=rel_tol, abs_tol=abs_tol), (a, b)

def rejects(exc, fn, *args):
    try:
        fn(*args)
    except exc:
        return
    raise AssertionError("expected " + exc.__name__)

def run():
    for x in (-3, 0, 2, 10):
        close(quadratic_derivative(x), 2*x)
        close(centered_difference(quadratic, x, 1e-4), 2*x)
        close(forward_difference(quadratic, x, 1e-4), 2*x+1e-4)
    for c in (0, 100, 1000):
        for r in (-0.01, 0, 0.05):
            for t in (0, 1, 3, 10):
                pv = present_value(c, r, t)
                close(pv, c*math.exp(-r*t))
                close(present_value_derivative(c, r, t), -t*pv)
                for h in (-1e-6, 1e-6):
                    q = stable_present_value_difference_quotient(c, r, t, h)
                    close(q, -t*pv, rel_tol=1e-5)
    close(marginal_profit(100), 8)
    close(profit(101)-profit(100), 7.98)
    rejects(ValueError, forward_difference, quadratic, 1, 0)
    rejects(ValueError, centered_difference, quadratic, 1, 0)
    rejects(ValueError, stable_present_value_difference_quotient, 100, 0.05, 3, 0)
    rejects(ValueError, present_value, -1, 0.05, 3)
    rejects(ValueError, present_value, 100, 0.05, -1)
    rejects(ValueError, marginal_profit, -1)
    rejects(TypeError, finite, True, "value")
    rejects(ValueError, finite, float("nan"), "value")
    print("PASS: Section 8.1 reference checks")

if __name__ == "__main__":
    run()
