"""Section 8.2: polynomial differentiation and financial marginal analysis."""
import math

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

def coefficients(values):
    try:
        data = tuple(values)
    except TypeError as exc:
        raise TypeError("coefficients must be iterable") from exc
    if not data:
        raise ValueError("coefficients must not be empty")
    return tuple(finite(value, "coefficient") for value in data)

def polynomial(values, x):
    coeffs = coefficients(values)
    x = finite(x, "x")
    result = 0.0
    for coefficient in reversed(coeffs):
        result = result*x+coefficient
    if not math.isfinite(result):
        raise OverflowError("polynomial overflow")
    return result

def derivative_coefficients(values):
    coeffs = coefficients(values)
    return tuple(i*coeffs[i] for i in range(1, len(coeffs))) or (0.0,)

def polynomial_derivative(values, x):
    return polynomial(derivative_coefficients(values), x)

def centered_difference(function, x, step):
    if not callable(function):
        raise TypeError("function must be callable")
    x, h = finite(x, "x"), finite(step, "step")
    if h == 0:
        raise ValueError("step must be nonzero")
    return (finite(function(x+h), "f(x+h)")-finite(function(x-h), "f(x-h)"))/(2*h)

def revenue(quantity):
    q = finite(quantity, "quantity")
    if q < 0 or q > 500:
        raise ValueError("quantity must lie in [0,500]")
    return 100*q-0.2*q*q

def marginal_revenue(quantity):
    q = finite(quantity, "quantity")
    if q < 0 or q > 500:
        raise ValueError("quantity must lie in [0,500]")
    return 100-0.4*q

def cost(quantity):
    q = finite(quantity, "quantity")
    if q < 0:
        raise ValueError("quantity must be nonnegative")
    return 1000+20*q+0.05*q*q

def marginal_cost(quantity):
    q = finite(quantity, "quantity")
    if q < 0:
        raise ValueError("quantity must be nonnegative")
    return 20+0.1*q

def profit(quantity):
    q = finite(quantity, "quantity")
    if q < 0 or q > 500:
        raise ValueError("quantity must lie in [0,500]")
    return revenue(q)-cost(q)

def marginal_profit(quantity):
    q = finite(quantity, "quantity")
    if q < 0 or q > 500:
        raise ValueError("quantity must lie in [0,500]")
    return marginal_revenue(q)-marginal_cost(q)

if __name__ == "__main__":
    p = (12, -9, 5, -3, 7)
    print("Polynomial derivative coefficients:", derivative_coefficients(p))
    print("Derivative at x=2:", polynomial_derivative(p, 2))
    for q in (50, 100, 150):
        print("q=", q, "MR=", marginal_revenue(q), "MC=", marginal_cost(q),
              "marginal profit=", marginal_profit(q))
    print("Finite profit change from 100 to 101:", profit(101)-profit(100))
