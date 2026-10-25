"""Reference checks for Section 6.5."""
import math
from section_6_05 import (
    finite, periods, growing_value, direct_value, growing_perpetuity)

def close(a, b):
    assert math.isclose(a, b, rel_tol=1e-11, abs_tol=1e-10), (a, b)

def rejects(error, fn, *args):
    try:
        fn(*args)
    except error:
        return
    raise AssertionError("expected " + error.__name__)

def run():
    pv = 100/1.05 + 103/1.05**2 + 106.09/1.05**3
    close(growing_value(100, 0.03, 0.05, 3), pv)
    close(growing_value(100, 0.03, 0.05, 3, "fv"), pv * 1.05**3)
    close(growing_value(100, 0.04, 0.04, 3), 300/1.04)
    close(growing_value(100, 0.04, 0.04, 3, "fv"), 300 * 1.04**2)
    close(growing_value(100, 0.03, 0.05, 3, "pv", "begin"), pv*1.05)
    close(growing_value(100, 0.03, 0.05, 0), 0)
    close(growing_perpetuity(100, 0.02, 0.05), 100/0.03)
    close(growing_perpetuity(100, 0.02, 0.05, "begin"), 105/0.03)
    for g, r in ((0, 0), (0.03, 0.05), (0.05, 0.03),
                 (-0.02, 0.01), (0.04, 0.04), (0.050000000001, 0.05)):
        for n in (0, 1, 3, 8):
            for kind in ("pv", "fv"):
                for timing in ("end", "begin"):
                    close(growing_value(100, g, r, n, kind, timing),
                          direct_value(100, g, r, n, kind, timing))
    rejects(ValueError, growing_value, 100, -1, 0.05, 3)
    rejects(ValueError, growing_value, 100, 0.02, -1, 3)
    rejects(ValueError, growing_value, 100, 0.02, 0.05, 3, "bad")
    rejects(ValueError, growing_perpetuity, 100, 0.05, 0.05)
    rejects(ValueError, growing_perpetuity, 100, 0.06, 0.05)
    rejects(TypeError, periods, True)
    rejects(TypeError, finite, True, "x")
    rejects(ValueError, finite, float("nan"), "x")
    print("PASS: Section 6.5 reference checks")

if __name__ == "__main__":
    run()
