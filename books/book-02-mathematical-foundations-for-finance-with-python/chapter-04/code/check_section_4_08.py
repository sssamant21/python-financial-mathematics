"""Reference checks for Section 4.8."""
import math
from section_4_08 import (
    finite, continuous_future_value, relative_fv_sensitivity_to_rate,
    periodic_relative_fv_sensitivity, implied_continuous_rate,
    implied_rate_sensitivity_to_final, implied_time,
    time_sensitivity_to_rate, central_difference)

def close(a, b, rel=1e-7, absolute=1e-9):
    assert math.isclose(a, b, rel_tol=rel, abs_tol=absolute), (a, b)

def rejects(error, fn, *args):
    try:
        fn(*args)
    except error:
        return
    raise AssertionError("expected " + error.__name__)

def run():
    close(continuous_future_value(1000, 0.05, 30), 1000*math.exp(1.5))
    close(relative_fv_sensitivity_to_rate(30), 30)
    close(periodic_relative_fv_sensitivity(0.05, 10), 10/1.05)
    close(implied_continuous_rate(100, 150, 5), math.log(1.5)/5)
    close(implied_rate_sensitivity_to_final(150, 5), 1/750)
    close(implied_time(100, 150, math.log(1.5)/5), 5)
    close(time_sensitivity_to_rate(100, 150, 0.08),
          -math.log(1.5)/0.08**2)
    r, t = 0.05, 30
    # Derivative of log future value with respect to the rate equals time.
    numerical = central_difference(
        lambda rate: math.log(continuous_future_value(1000, rate, t)),
        r, 1e-5)
    close(numerical, t)
    # Derivative of implied rate with respect to final value.
    numerical = central_difference(
        lambda final: implied_continuous_rate(100, final, 5),
        150, 1e-3)
    close(numerical, implied_rate_sensitivity_to_final(150, 5))
    # A 10-basis-point rate change across 30 years has about 3% effect.
    base = continuous_future_value(1000, 0.05, 30)
    changed = continuous_future_value(1000, 0.051, 30)
    close(changed/base - 1, math.expm1(0.03))
    rejects(ValueError, implied_time, 100, 150, 0)
    rejects(ValueError, implied_time, 100, 50, 0.05)
    rejects(ValueError, implied_continuous_rate, 100, 150, 0)
    rejects(ValueError, periodic_relative_fv_sensitivity, -1, 5)
    rejects(ValueError, periodic_relative_fv_sensitivity, 0.1, -1)
    rejects(ValueError, central_difference, lambda x: x*x, 1.0, 0)
    rejects(ValueError, central_difference, lambda x: x*x, 1.0, 1e-20)
    rejects(TypeError, finite, True, "x")
    rejects(ValueError, finite, float("inf"), "x")
    print("PASS: Section 4.8 reference checks")

if __name__ == "__main__":
    run()
