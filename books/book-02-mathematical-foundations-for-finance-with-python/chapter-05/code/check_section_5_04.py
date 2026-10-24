"""Reference checks for Section 5.4."""
import math
from section_5_04 import (
    finite, periods_value, annuity_factor, closed_balance,
    iterative_balance, variable_closed_balance)

def close(a, b, rel=1e-11, absolute=1e-10):
    assert math.isclose(a, b, rel_tol=rel, abs_tol=absolute), (a, b)

def rejects(error, fn, *args):
    try:
        fn(*args)
    except error:
        return
    raise AssertionError("expected " + error.__name__)

def run():
    close(closed_balance(1000, 0.02, 100, 3), 1367.248)
    close(closed_balance(1000, 0.02, 100, 3, "begin"), 1373.3688)
    close(annuity_factor(0.02, 3), 3.0604)
    close(annuity_factor(0, 3), 3)
    close(annuity_factor(0.02, 0), 0)
    close(closed_balance(1000, 0, 100, 3), 1300)
    close(closed_balance(1000, 0, 100, 3, "begin"), 1300)
    close(closed_balance(1000, -0.1, -50, 4),
          iterative_balance(1000, (-0.1,)*4, (-50,)*4))
    for n in range(0, 12):
        for rate in (-0.2, 0, 1e-12, 0.03, 0.2):
            for timing in ("end", "begin"):
                close(closed_balance(500, rate, 75, n, timing),
                      iterative_balance(500, (rate,)*n, (75,)*n, timing))
    rates = (0.01, -0.02, 0.03)
    payments = (100, 0, -50)
    close(variable_closed_balance(1000, rates, payments),
          iterative_balance(1000, rates, payments))
    close(variable_closed_balance(1000, (), ()), 1000)
    close(variable_closed_balance(1000, (0.01,), (100,)), 1110)
    rejects(ValueError, closed_balance, 1000, -1, 100, 3)
    rejects(ValueError, closed_balance, 1000, 0.01, 100, -1)
    rejects(ValueError, closed_balance, 1000, 0.01, 100, 2, "invalid")
    rejects(ValueError, iterative_balance, 1000, (0.01,), (100, 100))
    rejects(ValueError, variable_closed_balance, 1000, (0.01,), (100, 100))
    rejects(TypeError, periods_value, True)
    rejects(TypeError, finite, True, "x")
    rejects(ValueError, finite, float("nan"), "x")
    print("PASS: Section 5.4 reference checks")

if __name__ == "__main__":
    run()
