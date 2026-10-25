"""Reference checks for Section 8.2."""
import math
from section_8_02 import (
    finite, coefficients, polynomial, derivative_coefficients,
    polynomial_derivative, centered_difference, revenue, marginal_revenue,
    cost, marginal_cost, profit, marginal_profit)

def close(a, b, rel_tol=1e-9, abs_tol=1e-8):
    assert math.isclose(a, b, rel_tol=rel_tol, abs_tol=abs_tol), (a, b)

def rejects(exc, fn, *args):
    try:
        fn(*args)
    except exc:
        return
    raise AssertionError("expected " + exc.__name__)

def run():
    assert derivative_coefficients((12,)) == (0.0,)
    assert derivative_coefficients((12, -9, 5, -3, 7)) == (-9.0, 10.0, -9.0, 28.0)
    close(polynomial_derivative((12, -9, 5, -3, 7), 2), 199)
    for x in (-2, 0, 1, 2, 4):
        close(polynomial_derivative((9, -6, 0, 4), x), 12*x*x-6)
        close(polynomial_derivative((7,), x), 0)
        close(polynomial_derivative((0, 0, 1), x), 2*x)
        close(centered_difference(lambda z: polynomial((9, -6, 0, 4), z), x, 1e-4),
              polynomial_derivative((9, -6, 0, 4), x), rel_tol=1e-6)
    for q in (0, 50, 100, 150, 300):
        close(revenue(q), 100*q-0.2*q*q)
        close(cost(q), 1000+20*q+0.05*q*q)
        close(profit(q), revenue(q)-cost(q))
        close(marginal_profit(q), marginal_revenue(q)-marginal_cost(q))
        close(marginal_profit(q), 80-0.5*q)
    close(marginal_revenue(100), 60)
    close(marginal_cost(100), 30)
    close(marginal_profit(100), 30)
    close(profit(101)-profit(100), 29.75)
    rejects(ValueError, coefficients, ())
    rejects(TypeError, coefficients, None)
    rejects(ValueError, centered_difference, lambda x: x*x, 1, 0)
    rejects(ValueError, revenue, -1)
    rejects(ValueError, revenue, 501)
    rejects(ValueError, cost, -1)
    rejects(TypeError, finite, True, "value")
    rejects(ValueError, finite, float("nan"), "value")
    print("PASS: Section 8.2 reference checks")

if __name__ == "__main__":
    run()
