"""Reference checks for Section 6.4."""
import math
from section_6_04 import (
    finite, periods, annuity_factor, annuity_value,
    payment_for_present_value, direct_value)

def close(a, b):
    assert math.isclose(a, b, rel_tol=1e-11, abs_tol=1e-10), (a, b)

def rejects(error, fn, *args):
    try:
        fn(*args)
    except error:
        return
    raise AssertionError("expected " + error.__name__)

def run():
    close(annuity_factor(0, 3), 3)
    close(annuity_factor(0, 3, "fv"), 3)
    close(annuity_value(100, 0.02, 3, "fv"), 306.04)
    close(annuity_value(100, 0.02, 3, "fv", "begin"), 312.1608)
    close(annuity_value(100, 0, 3, "pv"), 300)
    close(annuity_value(100, 0, 3, "fv", "begin"), 300)
    close(annuity_value(100, 0.02, 0), 0)
    close(annuity_value(100, 0.02, 3, "fv"),
          annuity_value(100, 0.02, 3, "pv") * 1.02**3)
    for rate in (-0.5, -0.01, 0, 1e-12, 0.02, 0.1):
        for n in (0, 1, 2, 5, 12):
            for kind in ("pv", "fv"):
                for timing in ("end", "begin"):
                    close(annuity_value(100, rate, n, kind, timing),
                          direct_value(100, rate, n, kind, timing))
    for timing in ("end", "begin"):
        for rate in (0, 0.02, 1e-12):
            payment = payment_for_present_value(1000, rate, 12, timing)
            close(annuity_value(payment, rate, 12, "pv", timing), 1000)
    rejects(ValueError, annuity_value, 100, -1, 3)
    rejects(ValueError, annuity_value, 100, 0.02, 3, "bad")
    rejects(ValueError, annuity_value, 100, 0.02, 3, "pv", "bad")
    rejects(ValueError, payment_for_present_value, 1000, 0.02, 0)
    rejects(TypeError, periods, True)
    rejects(TypeError, finite, True, "x")
    rejects(ValueError, finite, float("nan"), "x")
    print("PASS: Section 6.4 reference checks")

if __name__ == "__main__":
    run()
