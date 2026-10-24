"""Reference checks for Section 4.7."""
import math
from section_4_07 import (
    finite, log_change, simple_change, cumulative_log_change,
    cumulative_simple_change, log_periodic_factor, periodic_factor,
    effective_annual_rate, continuous_ear, continuous_from_ear)

def close(a, b, rel=1e-12, absolute=1e-12):
    assert math.isclose(a, b, rel_tol=rel, abs_tol=absolute), (a, b)

def rejects(error, fn, *args):
    try:
        fn(*args)
    except error:
        return
    raise AssertionError(f"expected {error.__name__}")

def run():
    assert math.log(1 + 1e-16) == 0.0
    assert log_change(1e-16) > 0
    close(log_change(1e-16), 1e-16, absolute=1e-30)
    close(simple_change(1e-16), 1e-16, absolute=1e-30)
    close(cumulative_log_change((1.0, -0.5)), 0)
    close(cumulative_simple_change((1.0, -0.5)), 0)
    close(cumulative_simple_change((0.1, -0.05, 0.08)), 0.1286)
    close(log_periodic_factor(0.12, 12, 12), 12 * math.log1p(0.01))
    close(periodic_factor(0.12, 12, 12), 1.01**12)
    close(effective_annual_rate(0.12, 12), 1.01**12 - 1)
    close(log_periodic_factor(0, 12, 0), 0)
    close(cumulative_log_change((0.0,)*10000), 0)
    close(cumulative_simple_change((1e-12,)*1000),
          math.expm1(1000*math.log1p(1e-12)), absolute=1e-18)
    for r in (-0.9, -0.1, 0, 1e-12, 0.05, 0.5):
        close(continuous_ear(continuous_from_ear(r)), r)
        close(simple_change(log_change(r)), r)
    rejects(ValueError, log_change, -1)
    rejects(ValueError, log_change, -1.2)
    rejects(ValueError, log_periodic_factor, -1, 1, 2)
    rejects(ValueError, log_periodic_factor, 0.1, 0, 2)
    rejects(ValueError, log_periodic_factor, 0.1, 12, -1)
    rejects(ValueError, log_periodic_factor, 0.1, 12, 1.5)
    rejects(TypeError, finite, True, "x")
    rejects(ValueError, finite, float("nan"), "x")
    rejects(ValueError, finite, float("inf"), "x")
    rejects(OverflowError, simple_change, 1000)
    print("PASS: Section 4.7 reference checks")

if __name__ == "__main__":
    run()
