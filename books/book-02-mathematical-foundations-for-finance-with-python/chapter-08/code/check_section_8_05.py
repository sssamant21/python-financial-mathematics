"""Reference checks for Section 8.5."""
import math
from section_8_05 import (
    finite, exponential_derivative, logarithm_derivative,
    accumulation, accumulation_time_derivative, accumulation_rate_derivative,
    present_value, present_value_rate_derivative, present_value_rate_shock,
    log_return, power_elasticity, stable_exponential_difference_quotient,
    centered_difference)

def close(a, b, rel_tol=1e-8, abs_tol=1e-8):
    assert math.isclose(a, b, rel_tol=rel_tol, abs_tol=abs_tol), (a, b)

def rejects(exc, fn, *args):
    try:
        fn(*args)
    except exc:
        return
    raise AssertionError("expected " + exc.__name__)

def run():
    for x in (-2, -1, 0, 1, 3):
        close(exponential_derivative(x, 7, 3), 21*math.exp(3*x))
        close(centered_difference(lambda z:7*math.exp(3*z), x, 1e-5),
              exponential_derivative(x, 7, 3), rel_tol=1e-6)
    for x in (0, 0.5, 1, 5):
        close(logarithm_derivative(x), 2/(1+2*x))
        close(centered_difference(lambda z:math.log1p(2*z), x, 1e-5),
              logarithm_derivative(x), rel_tol=1e-6)
    for r in (-0.02, 0, 0.03, 0.08):
        for t in (0, 1, 4, 10):
            a = accumulation(1000, r, t)
            close(accumulation_time_derivative(1000, r, t), r*a)
            close(accumulation_rate_derivative(1000, r, t), t*a)
            pv = present_value(5000, r, t)
            close(present_value_rate_derivative(5000, r, t), -t*pv)
            h = 1e-4
            close(present_value_rate_shock(5000, r, t, h),
                  present_value(5000, r+h, t)-pv, rel_tol=1e-6, abs_tol=1e-8)
    close(accumulation(1000, 0.04, 5), 1000*math.exp(0.2))
    close(log_return(100, 103), math.log(1.03))
    close(power_elasticity(1.5), 1.5)
    for h in (1e-2, 1e-6, 1e-10):
        close(stable_exponential_difference_quotient(0.3, h),
              math.exp(0.3)*math.expm1(h)/h)
    rejects(ValueError, logarithm_derivative, -0.5)
    rejects(ValueError, accumulation, -1, 0.05, 3)
    rejects(ValueError, present_value, 100, 0.05, -1)
    rejects(ValueError, log_return, 0, 100)
    rejects(ValueError, stable_exponential_difference_quotient, 1, 0)
    rejects(ValueError, centered_difference, lambda x:x*x, 1, 0)
    rejects(TypeError, finite, True, "value")
    rejects(ValueError, finite, float("nan"), "value")
    print("PASS: Section 8.5 reference checks")

if __name__ == "__main__":
    run()
