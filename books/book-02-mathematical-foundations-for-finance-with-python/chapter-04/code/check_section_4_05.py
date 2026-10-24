"""Reference checks for Section 4.5."""
import math
from section_4_05 import (real, log_ratio, periods_to_target,
    periodic_rate_from_values, nominal_rate_from_values,
    continuous_time_to_target, continuous_rate_from_values,
    first_period_at_least)

def close(a, b):
    assert math.isclose(a, b, rel_tol=1e-11, abs_tol=1e-11), (a, b)

def rejects(error, fn, *args):
    try:
        fn(*args)
    except error:
        return
    raise AssertionError("expected " + error.__name__)

def run():
    close(periods_to_target(1000, 2000, 0.05), math.log(2)/math.log1p(0.05))
    assert first_period_at_least(1000, 2000, 0.05) == 15
    assert first_period_at_least(100, 100, 0.1) == 0
    assert first_period_at_least(100, 110, 0.1) == 1
    assert first_period_at_least(100, 115, 0.1) == 2
    close(periodic_rate_from_values(200, 242, 2), 0.1)
    close(nominal_rate_from_values(1000, 1000*1.01**12, 12, 12), 0.12)
    close(continuous_rate_from_values(100, 150, 5), math.log(1.5)/5)
    close(continuous_time_to_target(100, 150, math.log(1.5)/5), 5)
    close(continuous_time_to_target(200, 100, -math.log(2)), 1)
    close(periods_to_target(200, 100, -0.5), 1)
    close(log_ratio(100, 100), 0)
    for rate in (-0.4, -0.1, 0.01, 0.1):
        for n in (1, 2, 5, 10):
            final = 100 * (1 + rate)**n
            close(periodic_rate_from_values(100, final, n), rate)
            close(periods_to_target(100, final, rate), n)
    rejects(ValueError, periods_to_target, 100, 80, 0.05)
    rejects(ValueError, periods_to_target, 100, 100, 0)
    rejects(ValueError, periods_to_target, 100, 100, -1)
    rejects(ValueError, periodic_rate_from_values, 100, 100, 0)
    rejects(ValueError, continuous_time_to_target, 100, 150, 0)
    rejects(ValueError, continuous_time_to_target, 100, 50, 0.1)
    rejects(ValueError, continuous_rate_from_values, 100, 0, 1)
    rejects(ValueError, first_period_at_least, 100, 200, -0.1)
    rejects(ValueError, first_period_at_least, 100, 90, 0.1)
    rejects(TypeError, nominal_rate_from_values, 100, 110, 1, True)
    rejects(TypeError, real, True, "x")
    rejects(ValueError, real, float("nan"), "x")
    print("PASS: Section 4.5 reference checks")

if __name__ == "__main__":
    run()
