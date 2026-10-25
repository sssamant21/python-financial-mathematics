"""Reference checks for Section 7.1."""
import math
from section_7_01 import (
    finite, removable, modified, approach_table, annuity_factor, direct_factor)

def close(a, b, rel_tol=1e-11, abs_tol=1e-10):
    assert math.isclose(a, b, rel_tol=rel_tol, abs_tol=abs_tol), (a, b)

def rejects(exc, fn, *args):
    try:
        fn(*args)
    except exc:
        return
    raise AssertionError(f"expected {exc.__name__}")

def run():
    for x in (1, 1.9, 1.99, 2.01, 2.1, 3):
        close(removable(x), x+2)
        close(modified(x), x+2)
    close(modified(2), 100)
    rejects(ValueError, removable, 2)
    for left, fl, right, fr in approach_table(2):
        assert left < 2 < right
        close(fl, left+2)
        close(fr, right+2)
    for n in (0, 1, 3, 5, 12):
        for r in (-0.5, -0.01, 0, 1e-12, 1e-8, 0.01, 0.05):
            close(annuity_factor(r, n), direct_factor(r, n))
    close(annuity_factor(0, 5), 5)
    close(annuity_factor(1e-10, 5), 5, rel_tol=1e-9)
    rejects(ValueError, annuity_factor, -1, 5)
    rejects(ValueError, annuity_factor, 0, -1)
    rejects(TypeError, annuity_factor, 0, True)
    rejects(TypeError, finite, True, "x")
    rejects(ValueError, finite, float("nan"), "x")
    rejects(ValueError, approach_table, 2, (0,))
    print("PASS: Section 7.1 reference checks")

if __name__ == "__main__":
    run()
