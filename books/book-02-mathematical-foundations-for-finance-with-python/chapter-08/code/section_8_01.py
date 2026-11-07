"""Section 8.1: the derivative as a limit."""
import math
from fractions import Fraction

def finite(value, name):
    if type(value) not in (int, float):
        raise TypeError(f"{name} must be numeric, excluding bool")
    try:
        x = float(value)
    except OverflowError as exc:
        raise ValueError(f"{name} outside finite float range") from exc
    if not math.isfinite(x):
        raise ValueError(f"{name} must be finite")
    return x

def quadratic(x):
    x = finite(x, "x")
    return x*x

def quadratic_derivative(x):
    return 2*finite(x, "x")

def _difference_points(function, x, step, centered):
    x, h = finite(x, "x"), finite(step, "step")
    if not callable(function):
        raise TypeError("function must be callable")
    if h == 0:
        raise ValueError("step must be nonzero")
    up = x+h
    down = x-h if centered else x
    if (not math.isfinite(up) or not math.isfinite(down)
            or up == x or (centered and down == x)):
        raise ValueError("step must produce finite distinct perturbations")
    return up, down, Fraction(h)*(2 if centered else 1)


def _difference_result(first, second, denominator):
    if first == second:
        return (first-second) * (-1. if denominator < 0 else 1.)
    try:
        result = float((Fraction(first)-Fraction(second))/denominator)
    except OverflowError as exc:
        raise ValueError("difference estimate outside finite float range") from exc
    return finite(result, "difference estimate")


def forward_difference(function, x, step):
    up, base, denominator = _difference_points(function, x, step, False)
    first = finite(function(up), "f(x+h)")
    second = finite(function(base), "f(x)")
    return _difference_result(first, second, denominator)


def centered_difference(function, x, step):
    up, down, denominator = _difference_points(function, x, step, True)
    first = finite(function(up), "f(x+h)")
    second = finite(function(down), "f(x-h)")
    return _difference_result(first, second, denominator)

def present_value(amount, rate, years):
    c, r, t = finite(amount, "amount"), finite(rate, "rate"), finite(years, "years")
    if c < 0 or t < 0:
        raise ValueError("amount and years must be nonnegative")
    return c*math.exp(-r*t)

def present_value_derivative(amount, rate, years):
    t = finite(years, "years")
    return -t*present_value(amount, rate, years)

def stable_present_value_difference_quotient(amount, rate, years, step):
    h = finite(step, "step")
    if h == 0:
        raise ValueError("step must be nonzero")
    t = finite(years, "years")
    pv = present_value(amount, rate, years)
    return pv*math.expm1(-t*h)/h

def profit(quantity):
    q = finite(quantity, "quantity")
    if q < 0:
        raise ValueError("quantity must be nonnegative")
    return 12*q-0.02*q*q-500

def marginal_profit(quantity):
    q = finite(quantity, "quantity")
    if q < 0:
        raise ValueError("quantity must be nonnegative")
    return 12-0.04*q

if __name__ == "__main__":
    print("Quadratic derivative at x=3:", quadratic_derivative(3))
    for h in (0.1, 0.01, 0.0001):
        print("step:", h, "forward:", forward_difference(quadratic, 3, h),
              "centered:", centered_difference(quadratic, 3, h))
    print("PV:", present_value(1000, 0.05, 3))
    print("PV derivative:", present_value_derivative(1000, 0.05, 3))
    print("PV stable difference quotient:", stable_present_value_difference_quotient(1000, 0.05, 3, 1e-6))
    print("Marginal profit at 100:", marginal_profit(100))
