"""Reference checks for Section 7.6."""
import math
from section_7_06 import (
    finite, log_quotient, exp_quotient, power_quotient, sin_quotient,
    log_return, discount_relative_change, discount_linear_approximation,
    annuity_factor)

def close(a, b, rel_tol=1e-11, abs_tol=1e-10):
    assert math.isclose(a, b, rel_tol=rel_tol, abs_tol=abs_tol), (a, b)

def rejects(exc, fn, *args):
    try:
        fn(*args)
    except exc:
        return
    raise AssertionError("expected " + exc.__name__)

def run():
    close(log_quotient(0), 1)
    close(exp_quotient(0), 1)
    close(power_quotient(0, 7), 7)
    close(sin_quotient(0), 1)
    for h in (-0.1, -0.01, -1e-8, 1e-8, 0.01, 0.1):
        close(log_quotient(h), math.log1p(h)/h)
        close(exp_quotient(h), math.expm1(h)/h)
        close(sin_quotient(h), math.sin(h)/h)
        for a in (-2, 0, 0.5, 1, 7):
            close(power_quotient(h, a), math.expm1(a*math.log1p(h))/h)
    for a in (-2, 0, 0.5, 1, 7):
        close(power_quotient(0, a), a)
    for h in (1e-8, 1e-10, 1e-12):
        close(log_quotient(h), 1, rel_tol=1e-7)
        close(exp_quotient(h), 1, rel_tol=1e-7)
        close(power_quotient(h, 7), 7, rel_tol=1e-7)
    close(log_return(-0.02), math.log(0.98))
    close(discount_relative_change(0.001, 5), math.exp(-0.005)-1)
    close(discount_linear_approximation(0.001, 5), -0.005)
    for t in (0, 1, 5, 10):
        for h in (-0.01, 0, 0.01):
            close(discount_relative_change(h, t), math.expm1(-h*t))
    close(annuity_factor(0, 12), 12)
    for n in (0, 1, 5, 12):
        for r in (-0.1, 0, 1e-10, 0.05):
            close(annuity_factor(r, n), math.fsum((1+r)**k for k in range(n)))
    rejects(ValueError, log_quotient, -1)
    rejects(ValueError, power_quotient, -1, 2)
    rejects(ValueError, log_return, -1)
    rejects(ValueError, annuity_factor, -1, 5)
    rejects(TypeError, annuity_factor, 0, True)
    rejects(ValueError, discount_relative_change, 0.01, -1)
    rejects(TypeError, finite, True, "value")
    rejects(ValueError, finite, float("nan"), "value")
    print("PASS: Section 7.6 reference checks")

if __name__ == "__main__":
    run()
