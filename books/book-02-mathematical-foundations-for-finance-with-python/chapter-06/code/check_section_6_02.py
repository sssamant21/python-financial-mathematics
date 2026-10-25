"""Reference checks for Section 6.2."""
import math
from section_6_02 import (
    finite, periods, geometric_sum, rate_geometric_sum,
    balance_closed, balance_iterative)

def close(a, b, rel_tol=1e-11, abs_tol=1e-10):
    assert math.isclose(a, b, rel_tol=rel_tol, abs_tol=abs_tol), (a, b)

def rejects(error, fn, *args):
    try:
        fn(*args)
    except error:
        return
    raise AssertionError("expected " + error.__name__)

def run():
    close(geometric_sum(2, 5), 31)
    close(geometric_sum(1, 4), 4)
    close(geometric_sum(0.5, 3), 1.75)
    close(geometric_sum(1.02, 3), 3.0604)
    close(geometric_sum(-0.5, 4), 0.625)
    close(geometric_sum(100, 0), 0)
    close(rate_geometric_sum(0, 4), 4)
    close(rate_geometric_sum(0.02, 3), 3.0604)
    close(balance_closed(1000, 0.02, 100, 3), 1367.248)
    close(balance_closed(1000, 0.02, 100, 3, "begin"), 1373.3688)
    close(balance_closed(1000, 0, 100, 3), 1300)
    close(balance_closed(1000, 0.02, 100, 0), 1000)
    for rate in (-0.5, -0.01, 0, 1e-12, 0.02, 0.1):
        for n in (0, 1, 2, 5, 12):
            for timing in ("end", "begin"):
                close(balance_closed(500, rate, 25, n, timing),
                      balance_iterative(500, rate, 25, n, timing))
    close(rate_geometric_sum(1e-12, 100), 100, rel_tol=1e-10)
    rejects(ValueError, rate_geometric_sum, -1, 2)
    rejects(ValueError, periods, -1)
    rejects(TypeError, periods, True)
    rejects(TypeError, finite, True, "x")
    rejects(ValueError, finite, float("nan"), "x")
    rejects(ValueError, balance_closed, 100, 0.01, 10, 2, "bad")
    print("PASS: Section 6.2 reference checks")

if __name__ == "__main__":
    run()
