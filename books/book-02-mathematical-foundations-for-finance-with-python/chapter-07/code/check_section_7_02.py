"""Reference checks for Section 7.2."""
import math
from section_7_02 import (
    finite, step, matching_piecewise, threshold_fee, removable, approach)

def close(a, b):
    assert math.isclose(a, b, rel_tol=1e-11, abs_tol=1e-10), (a, b)

def rejects(exc, fn, *args):
    try:
        fn(*args)
    except exc:
        return
    raise AssertionError("expected " + exc.__name__)

def run():
    close(step(5), 7)
    close(step(4.999), 2)
    close(step(5.001), 7)
    close(matching_piecewise(2), 3)
    close(threshold_fee(999.99), 5)
    close(threshold_fee(1000), 10)
    close(threshold_fee(1000.01), 10)
    close(removable(2.9), 5.9)
    close(removable(3.1), 6.1)
    rejects(ValueError, removable, 3)
    for left, fl, right, fr in approach(step, 5):
        assert left < 5 < right
        close(fl, 2)
        close(fr, 7)
    for left, fl, right, fr in approach(matching_piecewise, 2):
        assert left < 2 < right
        close(fl, left + 1)
        close(fr, 3*right - 3)
    for left, fl, right, fr in approach(threshold_fee, 1000):
        assert left < 1000 < right
        close(fl, 5)
        close(fr, 10)
    rejects(ValueError, threshold_fee, -1)
    rejects(ValueError, approach, step, 5, (0,))
    rejects(TypeError, finite, True, "x")
    rejects(ValueError, finite, float("nan"), "x")
    print("PASS: Section 7.2 reference checks")

if __name__ == "__main__":
    run()
