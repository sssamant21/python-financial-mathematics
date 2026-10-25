"""Reference checks for Section 7.5."""
import math
from section_7_05 import (
    finite, periodic_factor, continuous_factor,
    effective_from_continuous, continuous_from_effective,
    continuous_discount, present_value, relative_error)

def close(a, b, rel_tol=1e-11, abs_tol=1e-10):
    assert math.isclose(a, b, rel_tol=rel_tol, abs_tol=abs_tol), (a, b)

def rejects(exc, fn, *args):
    try:
        fn(*args)
    except exc:
        return
    raise AssertionError("expected " + exc.__name__)

def run():
    close(periodic_factor(0.06, 1, 2), 1.06**2)
    close(continuous_factor(0.06, 2), math.exp(0.12))
    close(effective_from_continuous(0.06), math.exp(0.06)-1)
    close(continuous_from_effective(0.05), math.log(1.05))
    close(present_value(500, 0.03, 2), 500*math.exp(-0.06))
    for delta in (-0.3, -0.01, 0, 1e-12, 0.03, 0.2):
        close(continuous_from_effective(effective_from_continuous(delta)), delta)
        for t in (0, 0.5, 1, 2, 10):
            close(continuous_factor(delta, t)*continuous_discount(delta, t), 1)
    for j in (-0.2, 0, 0.06, 0.2):
        for t in (0, 0.5, 2, 5):
            errors = [relative_error(j, m, t) for m in (1, 10, 100, 10000)]
            assert errors[-1] <= errors[0] + 1e-12
            close(periodic_factor(j, 10000, t), continuous_factor(j, t), rel_tol=1e-4)
    close(periodic_factor(0, 12, 3), 1)
    close(continuous_factor(0, 3), 1)
    rejects(ValueError, periodic_factor, -2, 1, 1)
    rejects(ValueError, periodic_factor, 0.05, 0, 1)
    rejects(TypeError, periodic_factor, 0.05, True, 1)
    rejects(ValueError, periodic_factor, 0.05, 12, -1)
    rejects(ValueError, continuous_factor, 0.05, -1)
    rejects(ValueError, continuous_discount, 0.05, -1)
    rejects(ValueError, continuous_from_effective, -1)
    rejects(TypeError, finite, True, "value")
    rejects(ValueError, finite, float("nan"), "value")
    print("PASS: Section 7.5 reference checks")

if __name__ == "__main__":
    run()
