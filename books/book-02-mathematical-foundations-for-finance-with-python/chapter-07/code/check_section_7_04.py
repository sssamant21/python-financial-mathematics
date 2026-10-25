"""Reference checks for Section 7.4."""
import math
from section_7_04 import (
    finite, rational, reciprocal, steady_state, balance,
    iterative_balance, perpetuity, tail)

def close(a, b, rel_tol=1e-10, abs_tol=1e-9):
    assert math.isclose(a, b, rel_tol=rel_tol, abs_tol=abs_tol), (a, b)

def rejects(error, fn, *args):
    try:
        fn(*args)
    except error:
        return
    raise AssertionError("expected " + error.__name__)

def run():
    for x in (-1000, -10, -1, -0.5, 0, 0.5, 1, 10, 1000):
        close(rational(x), (4*x*x+3*x+1)/(2*x*x+7))
    close(rational(1e100), 2)
    close(rational(-1e100), 2)
    close(reciprocal(1), -1)
    close(reciprocal(3), 1)
    rejects(ValueError, reciprocal, 2)
    close(steady_state(100, 50, 0.9), 500)
    for initial, contribution, multiplier in (
        (100, 50, 0.9), (100, 50, 0), (-20, -5, 0.5),
        (10, 2, 1), (10, 2, 1.05), (-1000, 50, 1.05)
    ):
        for n in (0, 1, 2, 5, 10, 30):
            close(balance(initial, contribution, multiplier, n),
                  iterative_balance(initial, contribution, multiplier, n))
    close(balance(100, 50, 0.9, 1000), 500)
    close(balance(-1000, 50, 1.05, 100), -1000)
    close(perpetuity(100, 0.02, 0.06), 2500)
    close(perpetuity(100, 0, 0.05), 2000)
    close(tail(100, 0.02, 0.06, 0), 2500)
    close(tail(100, 0.02, 0.06, 10), 2500*(1.02/1.06)**10)
    rejects(ValueError, perpetuity, 100, 0.06, 0.06)
    rejects(ValueError, perpetuity, 100, 0.08, 0.06)
    rejects(ValueError, steady_state, 100, 50, 1)
    rejects(ValueError, balance, 100, 50, -0.5, 5)
    rejects(TypeError, balance, 100, 50, 0.9, True)
    rejects(ValueError, balance, 100, 50, 0.9, -1)
    rejects(TypeError, finite, True, "value")
    rejects(ValueError, finite, float("nan"), "value")
    print("PASS: Section 7.4 reference checks")

if __name__ == "__main__":
    run()
