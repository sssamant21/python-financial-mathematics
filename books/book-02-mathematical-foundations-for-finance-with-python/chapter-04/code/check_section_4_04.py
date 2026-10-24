"""Reference checks for Section 4.4."""
import math
from section_4_04 import (finite, positive_frequency, periods_count,
    periodic_factor, periodic_future_value, periodic_present_value,
    effective_annual_rate, nominal_from_effective,
    continuous_future_value, continuous_present_value,
    continuous_from_effective, effective_from_continuous,
    continuous_from_nominal)

def close(actual, expected):
    assert math.isclose(actual, expected, rel_tol=1e-11, abs_tol=1e-11), (
        actual, expected)

def rejects(error, fn, *args):
    try:
        fn(*args)
    except error:
        return
    raise AssertionError("expected " + error.__name__)

def run():
    close(periodic_future_value(1000, 0.12, 1, 1), 1120)
    close(periodic_future_value(1000, 0.12, 2, 2), 1123.6)
    close(periodic_future_value(1000, 0.12, 4, 4), 1125.50881)
    close(periodic_future_value(1000, 0.12, 12, 12),
          1000 * (1.01)**12)
    close(continuous_future_value(1000, 0.12, 1), 1000*math.exp(0.12))
    close(effective_annual_rate(0.12, 12), (1.01)**12 - 1)
    close(periodic_factor(0, 12, 0), 1)
    close(periodic_future_value(100, -0.1, 1, 1), 90)
    close(periodic_present_value(1210, 0.1, 1, 2), 1000)
    close(continuous_present_value(1210, math.log1p(0.1), 2), 1000)
    for m in (1, 2, 4, 12, 365):
        for ear in (-0.3, 0, 1e-12, 0.05, 0.5):
            nominal = nominal_from_effective(ear, m)
            close(effective_annual_rate(nominal, m), ear)
            close(continuous_from_nominal(nominal, m),
                  continuous_from_effective(ear))
    for rate in (-0.3, 0, 1e-12, 0.05, 0.5):
        close(continuous_from_effective(effective_from_continuous(rate)), rate)
    for rate in (-0.05, 0, 0.1):
        for n in (0, 1, 12):
            future = periodic_future_value(1000, rate, 12, n)
            close(periodic_present_value(future, rate, 12, n), 1000)
    rejects(ValueError, periodic_factor, -1, 1, 1)
    rejects(ValueError, periodic_factor, 0.1, 1, -1)
    rejects(TypeError, periodic_factor, 0.1, 1, 1.5)
    rejects(TypeError, positive_frequency, True)
    rejects(ValueError, positive_frequency, 0)
    rejects(TypeError, periods_count, True)
    rejects(ValueError, nominal_from_effective, -1, 12)
    rejects(ValueError, continuous_future_value, 100, 0.1, -1)
    rejects(ValueError, continuous_present_value, -1, 0.1, 1)
    rejects(TypeError, finite, True, "x")
    rejects(ValueError, finite, float("nan"), "x")
    print("PASS: Section 4.4 reference checks")

if __name__ == "__main__":
    run()
