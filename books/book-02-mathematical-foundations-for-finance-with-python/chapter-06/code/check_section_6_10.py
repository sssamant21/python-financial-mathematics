"""Reference and boundary checks for Chapter 6 final assessment."""
import math
from section_6_10 import (
    analytic_pv, enumerated_pv, future_value, perpetuity, tail, relative_horizon)

def close(a, b):
    assert math.isclose(a, b, rel_tol=1e-11, abs_tol=1e-9), (a, b)

def rejects(exc, fn, *args):
    try:
        fn(*args)
    except exc:
        return
    raise AssertionError(f"expected {exc.__name__}")

def run():
    cases = 0
    for c in (-100, 0, 100, 1000):
        for g, r in ((0, 0), (0, 0.05), (0.03, 0.05),
                     (0.08, 0.03), (0.04, 0.04), (-0.02, -0.01)):
            for n in (0, 1, 3, 10):
                for due in (False, True):
                    pv = analytic_pv(c, g, r, n, due)
                    close(pv, enumerated_pv(c, g, r, n, due))
                    close(future_value(c, g, r, n, due), pv*(1+r)**n)
                    cases += 1
    close(analytic_pv(100, 0, 0.05, 3), 100/1.05+100/1.05**2+100/1.05**3)
    close(future_value(100, 0, 0.05, 3), 315.25)
    close(future_value(100, 0, 0.05, 3, True), 331.0125)
    close(analytic_pv(250, 0, 0, 8), 2000)
    close(analytic_pv(100, 0.04, 0.04, 5), 500/1.04)
    close(perpetuity(150, 0, 0.06), 2500)
    close(perpetuity(150, 0.02, 0.06), 3750)
    for n in (0, 1, 5, 10, 30):
        close(analytic_pv(1000, 0.03, 0.05, n) +
              tail(1000, 0.03, 0.05, n), perpetuity(1000, 0.03, 0.05))
    assert relative_horizon(0.8, 0.01) == 21
    rejects(ValueError, perpetuity, 100, 0.05, 0.05)
    rejects(ValueError, perpetuity, 100, 0.08, 0.03)
    rejects(ValueError, analytic_pv, 100, 0, -1, 3)
    rejects(ValueError, analytic_pv, 100, -1, 0, 3)
    rejects(ValueError, analytic_pv, 100, 0, 0, -1)
    rejects(TypeError, analytic_pv, 100, 0, 0, True)
    rejects(TypeError, analytic_pv, True, 0, 0, 3)
    rejects(ValueError, analytic_pv, float("nan"), 0, 0, 3)
    rejects(ValueError, relative_horizon, 1, 0.01)
    print(f"PASS: {cases} Chapter 6 valuation scenarios plus boundary checks")

if __name__ == "__main__":
    run()
