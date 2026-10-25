"""Reference and boundary checks for the Chapter 6 valuation project."""
import math
from section_6_09 import (
    number, inputs, closed_form, direct_sum, verify, perpetuity, tail)

def close(a, b):
    assert math.isclose(a, b, rel_tol=1e-10, abs_tol=1e-9), (a, b)

def rejects(error, function, *args):
    try:
        function(*args)
    except error:
        return
    raise AssertionError(f"expected {error.__name__}")

def run():
    cases = 0
    for first in (-100, 0, 100):
        for growth, rate in ((0, 0), (0, 0.05), (0.02, 0.05),
                             (0.05, 0.02), (0.04, 0.04),
                             (-0.1, -0.02), (0.050000000001, 0.05)):
            for n in (0, 1, 3, 12):
                for timing in ("end", "begin"):
                    result = verify(first, growth, rate, n, timing)
                    close(result["pv"], direct_sum(first, growth, rate, n, "pv", timing))
                    cases += 1
    close(closed_form(250, 0, 0, 8), 2000)
    close(closed_form(100, 0, 0.02, 3, "fv"), 306.04)
    close(closed_form(100, 0, 0.02, 3, "fv", "begin"), 312.1608)
    close(closed_form(100, 0.04, 0.04, 3), 300/1.04)
    close(perpetuity(100, 0, 0.05), 2000)
    close(perpetuity(100, 0.02, 0.05), 100/0.03)
    close(perpetuity(100, -0.1, 0), 100/0.1)
    for n in (0, 1, 3, 10, 50):
        close(closed_form(100, 0.02, 0.05, n) +
              tail(100, 0.02, 0.05, n), perpetuity(100, 0.02, 0.05))
    rejects(ValueError, perpetuity, 100, 0.05, 0.05)
    rejects(ValueError, perpetuity, 100, 0.06, 0.05)
    rejects(ValueError, closed_form, 100, 0, -1, 3)
    rejects(ValueError, closed_form, 100, -1, 0, 3)
    rejects(ValueError, closed_form, 100, 0, 0, -1)
    rejects(TypeError, closed_form, 100, 0, 0, True)
    rejects(TypeError, number, True, "value")
    rejects(ValueError, number, float("nan"), "value")
    rejects(ValueError, closed_form, 100, 0, 0, 3, "invalid")
    rejects(ValueError, closed_form, 100, 0, 0, 3, "pv", "invalid")
    print(f"PASS: {cases} valuation scenarios plus boundary checks")

if __name__ == "__main__":
    run()
