"""Reference checks for Section 7.3."""
import math
from section_7_03 import (
    finite, removable, jump, reciprocal, oscillating,
    threshold_fee, continuous_kink, annuity_factor, approach)

def close(a, b):
    assert math.isclose(a, b, rel_tol=1e-11, abs_tol=1e-10), (a, b)

def rejects(error, function, *args):
    try:
        function(*args)
    except error:
        return
    raise AssertionError("expected " + error.__name__)

def run():
    close(removable(2.9), 5.9)
    close(removable(3.1), 6.1)
    rejects(ValueError, removable, 3)
    close(removable(3, True), 6)
    close(jump(4.999), 2)
    close(jump(5), 7)
    close(jump(5.001), 7)
    close(reciprocal(1.5), -2)
    close(reciprocal(2.5), 2)
    rejects(ValueError, reciprocal, 2)
    close(oscillating(1), math.sin(1))
    rejects(ValueError, oscillating, 0)
    close(threshold_fee(999), 5)
    close(threshold_fee(1000), 10)
    close(continuous_kink(999), 0)
    close(continuous_kink(1000), 0)
    close(continuous_kink(1100), 1)
    for left, fl, right, fr in approach(jump, 5):
        assert left < 5 < right
        close(fl, 2)
        close(fr, 7)
    for left, fl, right, fr in approach(removable, 3):
        close(fl, left+3)
        close(fr, right+3)
    for n in (0, 1, 5, 12):
        for r in (-0.5, -0.01, 0, 1e-12, 0.01, 0.05):
            expected = math.fsum((1+r)**k for k in range(n))
            close(annuity_factor(r, n), expected)
    rejects(ValueError, annuity_factor, -1, 5)
    rejects(ValueError, annuity_factor, 0, -1)
    rejects(TypeError, annuity_factor, 0, True)
    rejects(ValueError, threshold_fee, -1)
    rejects(ValueError, continuous_kink, -1)
    rejects(TypeError, finite, True, "x")
    rejects(ValueError, finite, float("nan"), "x")
    rejects(ValueError, approach, jump, 5, (0,))
    print("PASS: Section 7.3 reference checks")

if __name__ == "__main__":
    run()
