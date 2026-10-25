"""Reference checks for Section 7.8."""
import math
from section_7_08 import (
    finite, removable_expression, removable_stable,
    oscillation_sequences, exponential_quotient,
    present_value_direct, present_value_log)

def close(a, b, rel_tol=1e-10, abs_tol=1e-9):
    assert math.isclose(a, b, rel_tol=rel_tol, abs_tol=abs_tol), (a, b)

def rejects(exc, fn, *args):
    try:
        fn(*args)
    except exc:
        return
    raise AssertionError("expected " + exc.__name__)

def run():
    for x in (-5, 0, 0.5, 1.5, 2, 10):
        close(removable_expression(x), x+1)
        close(removable_stable(x), x+1)
    rejects(ValueError, removable_expression, 1)
    rejects(ValueError, removable_stable, 1)
    for n in (1, 2, 10, 100):
        x, y = oscillation_sequences(n)
        assert x > 0 and y > 0
        close(math.sin(1/x), 0, abs_tol=1e-11)
        close(math.sin(1/y), 1, abs_tol=1e-11)
    rejects(ValueError, oscillation_sequences, 0)
    rejects(ValueError, oscillation_sequences, True)
    close(exponential_quotient(0), 1)
    for h in (-0.1, -1e-8, 1e-8, 0.1):
        close(exponential_quotient(h), math.expm1(h)/h)
    for c in (-100, 0, 100, 1000):
        for r in (-0.1, 0, 1e-8, 0.05):
            for n in (0, 1, 5, 10):
                close(present_value_direct(c, r, n),
                      present_value_log(c, r, n))
    rejects(ValueError, present_value_direct, 100, -1, 2)
    rejects(ValueError, present_value_log, 100, -1, 2)
    rejects(TypeError, present_value_direct, 100, 0.05, True)
    rejects(ValueError, present_value_log, 100, 0.05, -1)
    rejects(TypeError, finite, True, "value")
    rejects(ValueError, finite, float("nan"), "value")
    print("PASS: Section 7.8 reference checks")

if __name__ == "__main__":
    run()
