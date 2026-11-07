"""Section 8.3: product and quotient derivatives with financial examples."""
import math
from fractions import Fraction

def finite(value, name):
    if type(value) not in (int, float):
        raise TypeError(f"{name} must be numeric (excluding bool)")
    try:
        result = float(value)
    except OverflowError as exc:
        raise ValueError(f"{name} outside finite float range") from exc
    if not math.isfinite(result):
        raise ValueError(f"{name} must be finite")
    return result

def _derivative_result(value):
    try:
        result = float(value)
    except OverflowError as exc:
        raise ValueError("derivative outside finite float range") from exc
    return finite(result, "derivative")


def product_derivative(u, du, v, dv, x):
    x = finite(x, "x")
    # Preserve the public callback order and evaluate every required value once.
    left_slope = Fraction(finite(du(x), "du"))
    right = Fraction(finite(v(x), "v"))
    left = Fraction(finite(u(x), "u"))
    right_slope = Fraction(finite(dv(x), "dv"))
    return _derivative_result(left_slope*right + left*right_slope)


def quotient_derivative(u, du, v, dv, x):
    x = finite(x, "x")
    denominator = finite(v(x), "v")
    if denominator == 0:
        raise ValueError("denominator must be nonzero")
    denominator = Fraction(denominator)
    left_slope = Fraction(finite(du(x), "du"))
    left = Fraction(finite(u(x), "u"))
    right_slope = Fraction(finite(dv(x), "dv"))
    return _derivative_result(
        (left_slope*denominator-left*right_slope)/(denominator*denominator))

def revenue(q):
    q = finite(q, "quantity")
    if q < 0 or q > 400:
        raise ValueError("quantity must be in [0,400]")
    return q*(120-0.3*q)

def marginal_revenue(q):
    q = finite(q, "quantity")
    if q < 0 or q > 400:
        raise ValueError("quantity must be in [0,400]")
    return 120-0.6*q

def average_cost(q):
    q = finite(q, "quantity")
    if q <= 0:
        raise ValueError("quantity must be positive")
    return (500+10*q+0.1*q*q)/q

def average_cost_derivative(q):
    q = finite(q, "quantity")
    if q <= 0:
        raise ValueError("quantity must be positive")
    return 0.1-500/(q*q)

def coverage_ratio(t):
    t = finite(t, "time")
    if 50+3*t == 0:
        raise ValueError("liabilities denominator is zero")
    return (100+8*t)/(50+3*t)

def coverage_ratio_derivative(t):
    t = finite(t, "time")
    if 50+3*t == 0:
        raise ValueError("liabilities denominator is zero")
    return 100/(50+3*t)**2

def discounted_value(t, rate, payment, payment_derivative):
    t, r = finite(t, "time"), finite(rate, "rate")
    if t < 0:
        raise ValueError("time must be nonnegative")
    return finite(payment(t), "payment")*math.exp(-r*t)

def discounted_value_derivative(t, rate, payment, payment_derivative):
    t, r = finite(t, "time"), finite(rate, "rate")
    if t < 0:
        raise ValueError("time must be nonnegative")
    return math.exp(-r*t)*(finite(payment_derivative(t), "payment derivative")-r*finite(payment(t), "payment"))

def centered_difference(function, x, step=1e-4):
    x, h = finite(x, "x"), finite(step, "step")
    if h == 0:
        raise ValueError("step must be nonzero")
    return (finite(function(x+h), "f(x+h)")-finite(function(x-h), "f(x-h)"))/(2*h)

if __name__ == "__main__":
    print("Product derivative at x=2:", product_derivative(lambda x:x*x, lambda x:2*x, lambda x:3*x+1, lambda x:3, 2))
    print("Quotient derivative at x=2:", quotient_derivative(lambda x:x*x+1, lambda x:2*x, lambda x:x+2, lambda x:1, 2))
    print("Marginal revenue at q=100:", marginal_revenue(100))
    print("Average cost derivative at q=100:", average_cost_derivative(100))
    print("Coverage ratio derivative at t=0:", coverage_ratio_derivative(0))
    print("Discounted payment derivative:", discounted_value_derivative(3, 0.05, lambda t:100+2*t, lambda t:2))
