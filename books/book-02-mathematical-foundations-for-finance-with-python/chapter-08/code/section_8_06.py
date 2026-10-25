"""Section 8.6: higher derivatives, curvature, and PV convexity."""
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

def polynomial(values, x):
    values = tuple(finite(c, "coefficient") for c in values)
    if not values:
        raise ValueError("coefficients must not be empty")
    x = finite(x, "x")
    result = 0.0
    for coefficient in reversed(values):
        result = result*x+coefficient
    return result

def derivative_coefficients(values, order=1):
    values = tuple(finite(c, "coefficient") for c in values)
    if not values:
        raise ValueError("coefficients must not be empty")
    if type(order) is not int or order < 0:
        raise ValueError("order must be a nonnegative integer")
    for _ in range(order):
        values = tuple(i*values[i] for i in range(1, len(values))) or (0.0,)
    return values

def profit(q):
    q = finite(q, "quantity")
    if not 0 <= q <= 500:
        raise ValueError("quantity must lie in [0,500]")
    return -1000+80*q-0.25*q*q

def marginal_profit(q):
    q = finite(q, "quantity")
    if not 0 <= q <= 500:
        raise ValueError("quantity must lie in [0,500]")
    return 80-0.5*q

def profit_curvature(q):
    q = finite(q, "quantity")
    if not 0 <= q <= 500:
        raise ValueError("quantity must lie in [0,500]")
    return -0.5

def present_value(payment, rate, years):
    c, r, t = finite(payment, "payment"), finite(rate, "rate"), finite(years, "years")
    if c < 0 or t < 0:
        raise ValueError("payment and years must be nonnegative")
    return c*math.exp(-r*t)

def pv_rate_first(payment, rate, years):
    t = finite(years, "years")
    return -t*present_value(payment, rate, years)

def pv_rate_second(payment, rate, years):
    t = finite(years, "years")
    return t*t*present_value(payment, rate, years)

def pv_shock(payment, rate, years, shock, order=2):
    h, t = finite(shock, "shock"), finite(years, "years")
    if order not in (1, 2) or type(order) is not int:
        raise ValueError("order must be 1 or 2")
    first = pv_rate_first(payment, rate, years)*h
    return first if order == 1 else first+0.5*pv_rate_second(payment, rate, years)*h*h

def pv_shock_exact(payment, rate, years, shock):
    h, t = finite(shock, "shock"), finite(years, "years")
    return present_value(payment, rate, years)*math.expm1(-t*h)

def cash_flow_rate_derivatives(cash_flows, rate):
    r = finite(rate, "rate")
    value = first = second = 0.0
    for payment, years in cash_flows:
        c, t = finite(payment, "payment"), finite(years, "years")
        if t < 0:
            raise ValueError("cash-flow horizons must be nonnegative")
        pv = c*math.exp(-r*t)
        value += pv
        first -= t*pv
        second += t*t*pv
    return value, first, second

def centered_second_difference(function, x, step=1e-3):
    if not callable(function):
        raise TypeError("function must be callable")
    x, h = finite(x, "x"), finite(step, "step")
    if h == 0:
        raise ValueError("step must be nonzero")
    return (finite(function(x+h), "f(x+h)")-2*finite(function(x), "f(x)")
            +finite(function(x-h), "f(x-h)"))/(h*h)

if __name__ == "__main__":
    print("Polynomial third derivative:", derivative_coefficients((0, 1, 0, -3, 2), 3))
    print("Profit maximum at q=160:", profit(160))
    print("PV first derivative:", pv_rate_first(10000, 0.04, 5))
    print("PV second derivative:", pv_rate_second(10000, 0.04, 5))
    print("First-order rate shock:", pv_shock(10000, 0.04, 5, 0.01, 1))
    print("Second-order rate shock:", pv_shock(10000, 0.04, 5, 0.01, 2))
    print("Exact rate shock:", pv_shock_exact(10000, 0.04, 5, 0.01))
