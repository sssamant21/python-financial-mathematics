"""Section 8.6: higher derivatives, curvature, and PV convexity."""
import math
from fractions import Fraction
from decimal import Context, Decimal, localcontext
from section_8_01 import _scaled_pv

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

def _polynomial_report(exact):
    try:
        result = float(exact)
    except OverflowError as exc:
        raise ValueError("polynomial result outside finite float range") from exc
    if not math.isfinite(result):
        raise ValueError("polynomial result outside finite float range")
    return result

def polynomial(values, x):
    values = tuple(finite(c, "coefficient") for c in values)
    if not values:
        raise ValueError("coefficients must not be empty")
    x = Fraction(finite(x, "x"))
    result = Fraction(0)
    for coefficient in reversed(values):
        result = result*x+Fraction(coefficient)
    return _polynomial_report(result)

def derivative_coefficients(values, order=1):
    values = tuple(finite(c, "coefficient") for c in values)
    if not values:
        raise ValueError("coefficients must not be empty")
    if type(order) is not int or order < 0:
        raise ValueError("order must be a nonnegative integer")
    if order == 0:
        return values
    if order >= len(values):
        return (0.0,)
    # Scale each original coefficient once by its exact falling factorial.
    # No overflowing intermediate derivatives and no loop over excessive order.
    factor = math.factorial(order)
    result = []
    for i in range(order, len(values)):
        if i > order:
            factor = factor*i//(i-order)
        result.append(_polynomial_report(Fraction(values[i])*factor))
    return tuple(result)

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
    if c == 0 or t == 0:
        return c
    return _scaled_pv(Fraction(c), -Fraction(r)*Fraction(t))

def pv_rate_first(payment, rate, years):
    t = finite(years, "years")
    c, r, t = finite(payment, "payment"), finite(rate, "rate"), finite(years, "years")
    if c < 0 or t < 0:
        raise ValueError("payment and years must be nonnegative")
    if c == 0 or t == 0:
        return -t*c
    return _scaled_pv(-Fraction(t)*Fraction(c), -Fraction(r)*Fraction(t))

def pv_rate_second(payment, rate, years):
    t = finite(years, "years")
    c, r, t = finite(payment, "payment"), finite(rate, "rate"), finite(years, "years")
    if c < 0 or t < 0:
        raise ValueError("payment and years must be nonnegative")
    if c == 0 or t == 0:
        # Sign of c*t*t, without squaring a large or tiny horizon first.
        return math.copysign(0.0, c)
    return _scaled_pv(Fraction(c)*Fraction(t)**2, -Fraction(r)*Fraction(t))

def _shock_inputs(payment, rate, years):
    c, r, t = finite(payment, "payment"), finite(rate, "rate"), finite(years, "years")
    if c < 0 or t < 0:
        raise ValueError("payment and years must be nonnegative")
    return c, r, t

def pv_shock(payment, rate, years, shock, order=2):
    h, t = finite(shock, "shock"), finite(years, "years")
    if order not in (1, 2) or type(order) is not int:
        raise ValueError("order must be 1 or 2")
    c, r, t = _shock_inputs(payment, rate, years)
    if c == 0 or t == 0 or h == 0:
        first = -0. * c * t * h
        return first if order == 1 else first + math.copysign(0.0, c)
    c, r, t, h = map(Fraction, (c, r, t, h))
    gap = t*h
    coefficient = -c*gap if order == 1 else c*gap*(gap/2-1)
    if coefficient == 0:
        return 0.0
    return _scaled_pv(coefficient, -r*t)

def pv_shock_exact(payment, rate, years, shock):
    h, t = finite(shock, "shock"), finite(years, "years")
    c, r, t = _shock_inputs(payment, rate, years)
    if c == 0 or t == 0 or h == 0:
        return -0. * c * t * h
    c, r, t, h = map(Fraction, (c, r, t, h))
    gap = abs(t*h)
    if h > 0:
        return _scaled_pv(-c, -r*t, gap)
    return _scaled_pv(c, -(r+h)*t, gap)

def _cash_flow_component(groups):
    groups={exponent:coefficient for exponent,coefficient in groups.items() if coefficient}
    if not groups:return 0.0
    if len(groups)==1 and 0 in groups:
        try:return finite(float(groups[0]), "cash-flow aggregate")
        except OverflowError as exc:raise ValueError("cash-flow aggregate outside finite float range") from exc
    pivot=max(groups)
    with localcontext(Context(prec=1600)):
        def dec(x):return Decimal(x.numerator)/Decimal(x.denominator)
        # Group equal exponents exactly first; sum complete signed contributions
        # relative to a common exponent before converting any term to float.
        total=sum((dec(c)*dec(e-pivot).exp() for e,c in sorted(groups.items())),Decimal(0))
        if not total:return 0.0
        amplitude=dec(pivot)+abs(total).ln()
        if amplitude>10000:raise ValueError("cash-flow aggregate outside finite float range")
        if amplitude< -10000:return -0.0 if total<0 else 0.0
        result=amplitude.exp().copy_sign(total)
        try:return finite(float(result), "cash-flow aggregate")
        except OverflowError as exc:raise ValueError("cash-flow aggregate outside finite float range") from exc

def cash_flow_rate_derivatives(cash_flows, rate):
    r=Fraction(finite(rate, "rate"));groups=[{}, {}, {}]
    for payment,years in cash_flows:
        c,t=finite(payment,"payment"),finite(years,"years")
        if t<0:raise ValueError("cash-flow horizons must be nonnegative")
        c,t=Fraction(c),Fraction(t);exponent=-r*t
        for grouped,coefficient in zip(groups,(c,-t*c,t*t*c)):
            grouped[exponent]=grouped.get(exponent,Fraction(0))+coefficient
    return tuple(_cash_flow_component(grouped) for grouped in groups)

def centered_second_difference(function, x, step=1e-3):
    if not callable(function):
        raise TypeError("function must be callable")
    x, h = finite(x, "x"), finite(step, "step")
    if h == 0:
        raise ValueError("step must be nonzero")
    if not math.isfinite(x+h) or not math.isfinite(x-h) or x+h==x or x-h==x:
        raise ValueError("step must produce finite distinct perturbations")
    samples = [Fraction(finite(function(z), name)) for z, name in
               ((x+h, "f(x+h)"), (x, "f(x)"), (x-h, "f(x-h)"))]
    exact = (samples[0]-2*samples[1]+samples[2])/Fraction(h)**2
    try:
        result = float(exact)
    except OverflowError as exc:
        raise ValueError("sampled second difference outside finite float range") from exc
    if not math.isfinite(result):
        raise ValueError("sampled second difference outside finite float range")
    return result

if __name__ == "__main__":
    print("Polynomial third derivative:", derivative_coefficients((0, 1, 0, -3, 2), 3))
    print("Profit maximum at q=160:", profit(160))
    print("PV first derivative:", pv_rate_first(10000, 0.04, 5))
    print("PV second derivative:", pv_rate_second(10000, 0.04, 5))
    print("First-order rate shock:", pv_shock(10000, 0.04, 5, 0.01, 1))
    print("Second-order rate shock:", pv_shock(10000, 0.04, 5, 0.01, 2))
    print("Exact rate shock:", pv_shock_exact(10000, 0.04, 5, 0.01))
