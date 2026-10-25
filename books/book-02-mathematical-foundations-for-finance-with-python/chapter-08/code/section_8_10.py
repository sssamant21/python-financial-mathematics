"""Section 8.10: Chapter 08 exercises and financial acceptance lab."""
import math

def finite(value, name):
    if type(value) not in (int, float):
        raise TypeError(f"{name} must be numeric, excluding bool")
    try:
        result = float(value)
    except OverflowError as exc:
        raise ValueError(f"{name} outside finite float range") from exc
    if not math.isfinite(result):
        raise ValueError(f"{name} must be finite")
    return result

def profit(quantity):
    q = finite(quantity, "quantity")
    if not 0 <= q <= 200:
        raise ValueError("quantity must be in [0, 200]")
    return -600+50*q-0.2*q*q

def marginal_profit(quantity):
    q = finite(quantity, "quantity")
    if not 0 <= q <= 200:
        raise ValueError("quantity must be in [0, 200]")
    return 50-0.4*q

def present_value(amount, rate, years):
    c, r, t = finite(amount, "amount"), finite(rate, "rate"), finite(years, "years")
    if c < 0 or t < 0:
        raise ValueError("amount and years must be nonnegative")
    return c*math.exp(-r*t)

def pv_rate_derivatives(amount, rate, years):
    t = finite(years, "years")
    pv = present_value(amount, rate, t)
    return pv, -t*pv, t*t*pv

def pv_rate_shock(amount, rate, years, shock):
    h, t = finite(shock, "shock"), finite(years, "years")
    pv, first, second = pv_rate_derivatives(amount, rate, t)
    return {"first_order":first*h,
            "second_order":first*h+0.5*second*h*h,
            "exact":pv*math.expm1(-t*h)}

def log_return(start, end):
    s, e = finite(start, "start"), finite(end, "end")
    if s <= 0 or e <= 0:
        raise ValueError("prices must be positive")
    return math.log1p((e-s)/s)

def break_even_quantity(price, variable_cost, fixed_cost):
    p, c, k = finite(price, "price"), finite(variable_cost, "variable_cost"), finite(fixed_cost, "fixed_cost")
    if k <= 0 or p <= c:
        raise ValueError("require fixed_cost > 0 and price > variable_cost")
    return k/(p-c)

def break_even_derivative(price, variable_cost, fixed_cost):
    p, c = finite(price, "price"), finite(variable_cost, "variable_cost")
    q = break_even_quantity(p, c, fixed_cost)
    return -q/(p-c)

def bond_yield_from_price(payment, price):
    c, p = finite(payment, "payment"), finite(price, "price")
    if c <= 0 or p <= 0:
        raise ValueError("payment and price must be positive")
    return c/p-1

def bond_yield_price_derivative(payment, price):
    c, p = finite(payment, "payment"), finite(price, "price")
    if c <= 0 or p <= 0:
        raise ValueError("payment and price must be positive")
    return -c/(p*p)

def centered_first(function, x, step):
    if not callable(function):
        raise TypeError("function must be callable")
    x, h = finite(x, "x"), finite(step, "step")
    if h <= 0 or x+h == x or x-h == x:
        raise ValueError("step must be positive and representable")
    return (finite(function(x+h), "f(x+h)")-finite(function(x-h), "f(x-h)"))/(2*h)

def centered_second(function, x, step):
    if not callable(function):
        raise TypeError("function must be callable")
    x, h = finite(x, "x"), finite(step, "step")
    if h <= 0 or x+h == x or x-h == x:
        raise ValueError("step must be positive and representable")
    return (finite(function(x+h), "f(x+h)")-2*finite(function(x), "f(x)")
            +finite(function(x-h), "f(x-h)"))/(h*h)

def chapter_report():
    pv, first, second = pv_rate_derivatives(10000, 0.04, 5)
    return {
        "profit_maximizer":125.0,
        "marginal_profit_at_maximizer":marginal_profit(125),
        "pv":pv, "pv_rate_first":first, "pv_rate_second":second,
        "pv_shock_10bp":pv_rate_shock(10000, 0.04, 5, 0.001),
        "log_return_80_to_84":log_return(80, 84),
        "break_even_quantity":break_even_quantity(45, 15, 900),
        "break_even_derivative":break_even_derivative(45, 15, 900),
        "bond_yield":bond_yield_from_price(110, 100),
        "bond_yield_price_derivative":bond_yield_price_derivative(110, 100),
        "cubic_centered_first":centered_first(lambda x:x**3, 2, 0.1),
        "quadratic_centered_second":centered_second(lambda x:x*x, 2, 0.1),
    }

if __name__ == "__main__":
    import json
    print(json.dumps(chapter_report(), indent=2, allow_nan=False))
