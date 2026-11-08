"""Section 8.7: implicit differentiation and financial sensitivity."""
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

def circle_upper(x, radius=5):
    x, radius = finite(x, "x"), finite(radius, "radius")
    if radius <= 0 or abs(x) > radius:
        raise ValueError("radius must be positive and |x| <= radius")
    if abs(x) == radius:
        return 0.0
    if x == 0:
        return radius
    radicand = (Fraction(radius)-Fraction(x))*(Fraction(radius)+Fraction(x))
    with localcontext(Context(prec=100)):
        exact_scale = Decimal(radicand.numerator)/Decimal(radicand.denominator)
        return finite(float(exact_scale.sqrt()), "circle height")

def circle_slope(x, y):
    x, y = finite(x, "x"), finite(y, "y")
    if y == 0:
        raise ValueError("implicit slope undefined where y=0")
    if x == 0:
        return -x/y
    return _implicit_report(-Fraction(x)/Fraction(y))

def _break_even_inputs(price, variable_cost, fixed_cost):
    p, c, k = finite(price, "price"), finite(variable_cost, "variable_cost"), finite(fixed_cost, "fixed_cost")
    if k <= 0 or p <= c:
        raise ValueError("require fixed_cost > 0 and price > variable_cost")
    return Fraction(p)-Fraction(c), Fraction(k)

def _break_even_report(value):
    try:
        return finite(float(value), "break-even result")
    except OverflowError as exc:
        raise ValueError("break-even result outside finite float range") from exc

def break_even_quantity(price, variable_cost, fixed_cost):
    gap, k = _break_even_inputs(price, variable_cost, fixed_cost)
    return _break_even_report(k/gap)

def break_even_sensitivity(price, variable_cost, fixed_cost):
    gap, k = _break_even_inputs(price, variable_cost, fixed_cost)
    return _break_even_report(-k/gap**2)

def _bond_inputs(cash_flows, yield_per_period):
    y = finite(yield_per_period, "yield_per_period")
    if y <= -1:
        raise ValueError("yield_per_period must exceed -1")
    flows = tuple(finite(c, "cash_flow") for c in cash_flows)
    if not flows or any(c <= 0 for c in flows):
        raise ValueError("cash flows must be a nonempty positive sequence")
    # Retain the existing represented binary64 1+y base convention.
    return tuple(map(Fraction, flows)), 1/Fraction(1+y)

def _bond_exact(flows, discount, derivative=False):
    total = Fraction(0)
    for i in range(len(flows), 0, -1):
        total = total*discount+(i*flows[i-1] if derivative else flows[i-1])
    return -discount**2*total if derivative else discount*total

def _bond_report(exact):
    try:
        return finite(float(exact), "bond result")
    except OverflowError as exc:
        raise ValueError("bond result outside finite float range") from exc

def bond_price(cash_flows, yield_per_period):
    flows, discount = _bond_inputs(cash_flows, yield_per_period)
    return _bond_report(_bond_exact(flows, discount))

def bond_price_derivative(cash_flows, yield_per_period):
    flows, discount = _bond_inputs(cash_flows, yield_per_period)
    return _bond_report(_bond_exact(flows, discount, derivative=True))

def yield_price_sensitivity(cash_flows, yield_per_period):
    flows, discount = _bond_inputs(cash_flows, yield_per_period)
    # Positive flows imply a strictly negative exact derivative, even when
    # its float report would be zero or nonfinite.
    return _bond_report(1/_bond_exact(flows, discount, derivative=True))

def _implicit_report(exact):
    try:
        return finite(float(exact), "implicit result")
    except OverflowError as exc:
        raise ValueError("implicit result outside finite float range") from exc

def exposure_slope(x, y, a, b):
    x, y, a, b = (finite(v, n) for v, n in ((x,"x"),(y,"y"),(a,"a"),(b,"b")))
    if a <= 0 or b <= 0 or y == 0:
        raise ValueError("a and b must be positive and y nonzero")
    if x == 0:
        return -x/y
    return _implicit_report(-Fraction(a)*Fraction(x)/(Fraction(b)*Fraction(y)))

def centered_difference(function, x, step=1e-4):
    if not callable(function):
        raise TypeError("function must be callable")
    x, h = finite(x, "x"), finite(step, "step")
    if h == 0:
        raise ValueError("step must be nonzero")
    if not math.isfinite(x+h) or not math.isfinite(x-h) or x+h == x or x-h == x:
        raise ValueError("step must produce finite distinct perturbations")
    first = finite(function(x+h), "f(x+h)")
    last = finite(function(x-h), "f(x-h)")
    exact = (Fraction(first)-Fraction(last))/(2*Fraction(h))
    if exact == 0:
        # Preserve represented numerator-zero/denominator signs without 2*h.
        return (first-last)/math.copysign(1.0,h)
    return _implicit_report(exact)

if __name__ == "__main__":
    print("Circle slope at (3,4):", circle_slope(3, 4))
    print("Break-even quantity:", break_even_quantity(50, 20, 1200))
    print("Break-even sensitivity:", break_even_sensitivity(50, 20, 1200))
    print("One-period bond price:", bond_price((105,), 0.05))
    print("Bond yield sensitivity:", yield_price_sensitivity((105,), 0.05))
    print("Exposure slope:", exposure_slope(3, 4, 1, 1))
