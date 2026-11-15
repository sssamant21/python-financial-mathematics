"""Book 02 Section 9.1: absolute and relative financial sensitivity."""
import math
from fractions import Fraction
from decimal import Decimal, Context, localcontext

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

def _report(exact):
    try:
        result = float(exact)
    except OverflowError as exc:
        raise ValueError("result outside finite float range") from exc
    if not math.isfinite(result):
        raise ValueError("result outside finite float range")
    return result

def _scaled_discount(coefficient, exponent, gap=None, zero=0.0):
    if coefficient == 0 or gap == 0:
        return zero
    # Finite binary64 input products cannot rescue an exponent this large.
    if exponent > 10000:
        raise ValueError("discounted result outside finite float range")
    if exponent < -10000:
        return -0.0 if coefficient < 0 else 0.0
    if exponent == 0 and gap is None:
        return _report(coefficient)
    with localcontext(Context(prec=1300)):
        def dec(x):return Decimal(x.numerator)/Decimal(x.denominator)
        factor = Decimal(1) if gap is None or gap > 10000 else 1-(-dec(gap)).exp()
        return _report(dec(coefficient)*dec(exponent).exp()*factor)

def _discount_inputs(cash_flow, rate, years):
    c, r, t = finite(cash_flow, "cash_flow"), finite(rate, "rate"), finite(years, "years")
    if c <= 0 or t < 0:
        raise ValueError("cash_flow must be positive and years nonnegative")
    return c, r, t

def discounted_value(cash_flow, rate, years):
    c, r, t = _discount_inputs(cash_flow, rate, years)
    return _scaled_discount(Fraction(c), -Fraction(r)*Fraction(t))

def discounted_sensitivity(cash_flow, rate, years):
    r, t = finite(rate, "rate"), finite(years, "years")
    c, r, t = _discount_inputs(cash_flow, r, t)
    C, R, T = map(Fraction, (c, r, t))
    v = _scaled_discount(C, -R*T)
    derivative = _scaled_discount(-T*C, -R*T, zero=-t*0.0)
    elasticity = -r*t if r == 0 or t == 0 else _report(-R*T)
    # Exact C*exp(-r*t)>0 even when its final float report underflows.
    return {"value":v, "absolute":derivative,
            "normalized_rate":t, "elasticity":elasticity}

def discounted_shock(cash_flow, rate, years, shock):
    r, t, h = finite(rate, "rate"), finite(years, "years"), finite(shock, "shock")
    c, r, t = _discount_inputs(cash_flow, r, t)
    if t == 0 or h == 0:
        zero = -0.0*c*t*h
        return {"first_order":zero, "exact":zero}
    C, R, T, H = map(Fraction, (c, r, t, h))
    first = _scaled_discount(-C*T*H, -R*T)
    exact = (_scaled_discount(-C, -R*T, T*H) if h > 0 else
             _scaled_discount(C, -(R+H)*T, -T*H))
    return {"first_order":first, "exact":exact}

def _demand_inputs(price, scale, exponent):
    p, a, e = finite(price, "price"), finite(scale, "scale"), finite(exponent, "exponent")
    if p <= 0 or a <= 0:
        raise ValueError("price and scale must be positive")
    return p, a, e

def _scaled_power(coefficient, price, exponent, zero=0.0):
    if coefficient == 0:
        return zero
    if price == 1 or exponent == 0:
        return _report(coefficient)
    with localcontext(Context(prec=1300)):
        def dec(x):return Decimal(x.numerator)/Decimal(x.denominator)
        amplitude = abs(dec(coefficient)).ln()+dec(exponent)*Decimal(price).ln()
        if amplitude > 10000:
            raise ValueError("power result outside finite float range")
        if amplitude < -10000:
            return -0.0 if coefficient < 0 else 0.0
        return _report(amplitude.exp().copy_sign(Decimal(-1 if coefficient < 0 else 1)))

def demand_quantity(price, scale=400.0, exponent=-1.5):
    p, a, e = _demand_inputs(price, scale, exponent)
    return _scaled_power(Fraction(a), p, Fraction(e))

def demand_sensitivity(price, scale=400.0, exponent=-1.5):
    p, e = finite(price, "price"), finite(exponent, "exponent")
    p, a, e = _demand_inputs(p, scale, e)
    A, E = Fraction(a), Fraction(e)
    q = _scaled_power(A, p, E)
    derivative = _scaled_power(E*A, p, E-1, zero=e*0.0)
    # Analytic Q>0 for valid finite inputs,even if its float report underflows.
    return {"quantity":q, "absolute":derivative, "elasticity":e}

def portfolio_sensitivity(shares, price, cash):
    n, p, b = finite(shares, "shares"), finite(price, "price"), finite(cash, "cash")
    if n < 0 or p <= 0 or b < 0:
        raise ValueError("require shares and cash nonnegative, price positive")
    position = Fraction(n)*Fraction(p)
    exact_value = position+Fraction(b)
    if exact_value <= 0:
        raise ValueError("portfolio value must be positive for elasticity")
    value = _report(exact_value)
    elasticity = _report(position/exact_value) if n != 0 else n*0.0
    return {"value":value, "absolute":n, "elasticity":elasticity}

if __name__ == "__main__":
    print("Discounted sensitivity:", discounted_sensitivity(10000, 0.04, 5))
    print("1bp shock:", discounted_shock(10000, 0.04, 5, 0.0001))
    print("Demand:", demand_sensitivity(20))
    print("Portfolio:", portfolio_sensitivity(20, 50, 1000))
