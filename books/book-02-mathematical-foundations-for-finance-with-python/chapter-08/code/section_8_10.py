"""Section 8.10: Chapter 08 exercises and financial acceptance lab."""
import math
from fractions import Fraction
from section_8_08 import (centered_difference as _reviewed_centered_first,
                          second_difference as _reviewed_centered_second)
from section_8_06 import (present_value as _reviewed_pv, pv_rate_first,
                          pv_rate_second, pv_shock, pv_shock_exact)

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
    return _reviewed_pv(amount, rate, years)

def pv_rate_derivatives(amount, rate, years):
    # Keep years-first validation, then evaluate each complete expression.
    t = finite(years, "years")
    return (_reviewed_pv(amount, rate, t), pv_rate_first(amount, rate, t),
            pv_rate_second(amount, rate, t))

def pv_rate_shock(amount, rate, years, shock):
    h, t = finite(shock, "shock"), finite(years, "years")
    # A small shock may rescue a large derivative; do not round derivatives first.
    return {"first_order":pv_shock(amount, rate, t, h, order=1),
            "second_order":pv_shock(amount, rate, t, h, order=2),
            "exact":pv_shock_exact(amount, rate, t, h)}

def log_return(start, end):
    s, e = finite(start, "start"), finite(end, "end")
    if s <= 0 or e <= 0:
        raise ValueError("prices must be positive")
    if 0.5*s <= e <= 2*s:
        return math.log1p((e-s)/s)
    sm, se = math.frexp(s)
    em, ee = math.frexp(e)
    return math.log(em/sm)+(ee-se)*math.log(2.0)

def _rational_report(exact):
    """Round the complete represented-input expression once; allow signed underflow."""
    try:
        result = float(exact)
    except OverflowError as exc:
        raise ValueError("result outside finite float range") from exc
    if not math.isfinite(result):
        raise ValueError("result outside finite float range")
    return result

def _break_inputs(price, variable_cost, fixed_cost):
    p, c, k = finite(price, "price"), finite(variable_cost, "variable_cost"), finite(fixed_cost, "fixed_cost")
    if k <= 0 or p <= c:
        raise ValueError("require fixed_cost > 0 and price > variable_cost")
    return Fraction(p), Fraction(c), Fraction(k)

def break_even_quantity(price, variable_cost, fixed_cost):
    p, c, k = _break_inputs(price, variable_cost, fixed_cost)
    return _rational_report(k/(p-c))

def break_even_derivative(price, variable_cost, fixed_cost):
    p, c, k = _break_inputs(price, variable_cost, fixed_cost)
    return _rational_report(-k/(p-c)**2)

def bond_yield_from_price(payment, price):
    c, p = finite(payment, "payment"), finite(price, "price")
    if c <= 0 or p <= 0:
        raise ValueError("payment and price must be positive")
    return _rational_report((Fraction(c)-Fraction(p))/Fraction(p))

def bond_yield_price_derivative(payment, price):
    c, p = finite(payment, "payment"), finite(price, "price")
    if c <= 0 or p <= 0:
        raise ValueError("payment and price must be positive")
    return _rational_report(-Fraction(c)/Fraction(p)**2)

def centered_first(function, x, step):
    if not callable(function):
        raise TypeError("function must be callable")
    return _reviewed_centered_first(function, x, step)

def centered_second(function, x, step):
    if not callable(function):
        raise TypeError("function must be callable")
    return _reviewed_centered_second(function, x, step)

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
