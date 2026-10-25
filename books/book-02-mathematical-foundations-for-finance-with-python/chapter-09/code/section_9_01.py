"""Book 02 Section 9.1: absolute and relative financial sensitivity."""
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

def discounted_value(cash_flow, rate, years):
    c, r, t = finite(cash_flow, "cash_flow"), finite(rate, "rate"), finite(years, "years")
    if c <= 0 or t < 0:
        raise ValueError("cash_flow must be positive and years nonnegative")
    return c*math.exp(-r*t)

def discounted_sensitivity(cash_flow, rate, years):
    r, t = finite(rate, "rate"), finite(years, "years")
    v = discounted_value(cash_flow, r, t)
    derivative = -t*v
    return {"value":v, "absolute":derivative,
            "normalized_rate":-derivative/v, "elasticity":r*derivative/v}

def discounted_shock(cash_flow, rate, years, shock):
    r, t, h = finite(rate, "rate"), finite(years, "years"), finite(shock, "shock")
    v = discounted_value(cash_flow, r, t)
    return {"first_order":-t*v*h, "exact":v*math.expm1(-t*h)}

def demand_quantity(price, scale=400.0, exponent=-1.5):
    p, a, e = finite(price, "price"), finite(scale, "scale"), finite(exponent, "exponent")
    if p <= 0 or a <= 0:
        raise ValueError("price and scale must be positive")
    return a*p**e

def demand_sensitivity(price, scale=400.0, exponent=-1.5):
    p, e = finite(price, "price"), finite(exponent, "exponent")
    q = demand_quantity(p, scale, e)
    derivative = e*q/p
    return {"quantity":q, "absolute":derivative, "elasticity":p*derivative/q}

def portfolio_sensitivity(shares, price, cash):
    n, p, b = finite(shares, "shares"), finite(price, "price"), finite(cash, "cash")
    if n < 0 or p <= 0 or b < 0:
        raise ValueError("require shares and cash nonnegative, price positive")
    v = n*p+b
    if v <= 0:
        raise ValueError("portfolio value must be positive for elasticity")
    return {"value":v, "absolute":n, "elasticity":p*n/v}

if __name__ == "__main__":
    print("Discounted sensitivity:", discounted_sensitivity(10000, 0.04, 5))
    print("1bp shock:", discounted_shock(10000, 0.04, 5, 0.0001))
    print("Demand:", demand_sensitivity(20))
    print("Portfolio:", portfolio_sensitivity(20, 50, 1000))
