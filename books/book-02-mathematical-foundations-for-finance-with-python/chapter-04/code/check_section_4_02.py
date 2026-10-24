"""Reference checks for Section 4.2."""
import math
from section_4_02 import (finite, continuous_value, continuous_present_value,
                          continuous_rate, time_to_target, effective_rate,
                          continuous_rate_from_effective)

def close(actual, expected):
    assert math.isclose(actual, expected, rel_tol=1e-12, abs_tol=1e-12), (
        actual, expected)

def rejects(error, fn, *args):
    try:
        fn(*args)
    except error:
        return
    raise AssertionError("expected " + error.__name__)

def run():
    close(continuous_value(100, 0, 5), 100)
    close(continuous_value(100, math.log(1.1), 2), 121)
    close(continuous_value(500, -math.log(2), 1), 250)
    close(continuous_present_value(1000, 0.05, 3), 1000*math.exp(-0.15))
    close(continuous_present_value(0, 0.05, 3), 0)
    close(continuous_rate(100, 121, 2), math.log(1.21)/2)
    close(time_to_target(100, 200, 0.06), math.log(2)/0.06)
    close(time_to_target(200, 100, -0.06), math.log(0.5)/(-0.06))
    close(time_to_target(100, 100, 0.06), 0)
    close(effective_rate(math.log1p(0.05)), 0.05)
    close(continuous_rate_from_effective(0.1), math.log1p(0.1))
    for rate in (-0.5, -0.01, 0, 1e-12, 0.1, 0.5):
        close(continuous_rate_from_effective(effective_rate(rate)), rate)
    for rate in (-0.2, 0.03, 0.15):
        for time in (0, 1, 2, 10):
            result = continuous_value(100, rate, time)
            close(continuous_present_value(result, rate, time), 100)
    rejects(ValueError, continuous_rate, 0, 100, 2)
    rejects(ValueError, continuous_rate, 100, 100, 0)
    rejects(ValueError, time_to_target, 100, 200, 0)
    rejects(ValueError, time_to_target, 100, 50, 0.1)
    rejects(ValueError, continuous_value, 100, 0.1, -1)
    rejects(ValueError, continuous_present_value, -1, 0.1, 1)
    rejects(ValueError, continuous_rate_from_effective, -1)
    rejects(ValueError, finite, float("nan"), "value")
    rejects(ValueError, finite, float("inf"), "value")
    rejects(TypeError, finite, True, "value")
    print("PASS: Section 4.2 reference checks")

if __name__ == "__main__":
    run()
