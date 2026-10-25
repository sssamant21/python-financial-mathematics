"""Reference checks for Section 6.8."""
import math
from section_6_08 import (
    finite, periods, annuity_value, growing_value, direct_value)

def close(a, b):
    assert math.isclose(a, b, rel_tol=1e-11, abs_tol=1e-10), (a, b)

def rejects(error, fn, *args):
    try:
        fn(*args)
    except error:
        return
    raise AssertionError("expected " + error.__name__)

def run():
    for timing in ("end", "begin"):
        for kind in ("pv", "fv"):
            close(annuity_value(250, 0, 8, kind, timing), 2000)
            close(growing_value(100, 0, 0, 3, kind, timing), 300)
    close(growing_value(100, 0.02, 0, 3), 306.04)
    close(growing_value(100, -0.1, 0, 3), 271)
    close(annuity_value(100, 0.02, 3, "fv"), 306.04)
    for r in (-0.5, -0.02, 0, 1e-12, 0.02, 0.05):
        for g in (-0.1, 0, 0.02, r):
            for n in (0, 1, 3, 8):
                for kind in ("pv", "fv"):
                    for timing in ("end", "begin"):
                        close(growing_value(100, g, r, n, kind, timing),
                              direct_value(100, g, r, n, kind, timing))
        for n in (0, 1, 3, 8):
            for kind in ("pv", "fv"):
                for timing in ("end", "begin"):
                    close(annuity_value(100, r, n, kind, timing),
                          direct_value(100, 0, r, n, kind, timing))
    rejects(ValueError, annuity_value, 100, -1, 3)
    rejects(ValueError, growing_value, 100, -1, 0, 3)
    rejects(ValueError, annuity_value, 100, 0, 3, "bad")
    rejects(ValueError, growing_value, 100, 0, 0, 3, "pv", "bad")
    rejects(ValueError, periods, -1)
    rejects(TypeError, periods, True)
    rejects(TypeError, finite, True, "x")
    rejects(ValueError, finite, float("nan"), "x")
    print("PASS: Section 6.8 reference checks")

if __name__ == "__main__":
    run()
