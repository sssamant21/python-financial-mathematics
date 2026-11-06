"""Constant-coefficient continuous-account model; educational draft."""
import math
from decimal import Context, Decimal, localcontext
from fractions import Fraction
from numbers import Real

def finite(x, name):
    if isinstance(x, bool) or not isinstance(x, Real):
        raise TypeError(f"{name} must be real, excluding bool")
    try: x = float(x)
    except OverflowError as exc: raise ValueError(f"{name} exceeds float range") from exc
    if not math.isfinite(x): raise ValueError(f"{name} must be finite")
    return x

def _rounded_balance(value):
    try:
        balance = float(value)
    except OverflowError as exc:
        raise OverflowError("transition exceeds float range") from exc
    if not math.isfinite(balance):
        raise OverflowError("transition exceeds float range")
    return balance

def _decimal(value):
    return Decimal(value.numerator) / Decimal(value.denominator)

def _negative_limit(equilibrium, coefficient):
    # At rt < -4000 the exponential correction cannot cross a float
    # rounding boundary, except to decide the side of an exact midpoint.
    if not equilibrium:
        return 0.0 if coefficient > 0 else -0.0
    rounded = _rounded_balance(equilibrium)
    gap = equilibrium - Fraction(rounded)
    if gap * coefficient > 0:
        neighbor = math.nextafter(rounded, math.inf if gap > 0 else -math.inf)
        if math.isfinite(neighbor) and equilibrium == (Fraction(rounded) + Fraction(neighbor))/2:
            return neighbor
    return rounded

def transition(initial, rate, flow, years):
    initial, rate, flow, years = (finite(v, n) for v, n in
        ((initial, "initial"), (rate, "rate"), (flow, "flow"), (years, "years")))
    if years < 0: raise ValueError("years must be nonnegative")
    if years == 0: return initial
    a, r, u, t = map(Fraction, (initial, rate, flow, years))
    if not r:
        return _rounded_balance(a + u*t)
    equilibrium = -u/r
    coefficient = a - equilibrium
    if not coefficient:
        return initial
    exponent = r*t
    # These cutoffs use the bounds of represented binary64 inputs and
    # the nonzero rational coefficient, not the range of float exp().
    if exponent > 4000:
        raise OverflowError("transition exceeds float range")
    if exponent < -4000:
        return _negative_limit(equilibrium, coefficient)
    with localcontext(Context(prec=2400)):
        growth = _decimal(exponent).exp()
        if abs(exponent) <= Fraction(1, 2):
            value = _decimal(a) + _decimal(coefficient)*(growth - 1)
        else:
            value = _decimal(equilibrium) + _decimal(coefficient)*growth
        return _rounded_balance(value)

def scenario_report(initial, rate, flow, years):
    result = transition(initial, rate, flow, years)
    return {"model": "constant-coefficient unconstrained account",
            "inputs": {"initial": initial, "rate": rate, "flow": flow, "years": years},
            "units": {"initial": "currency", "rate": "per year",
                      "flow": "currency per year", "years": "years"},
            "ending_balance": result, "boundary_policy": "unconstrained; negative balances allowed",
            "validation_execution": "not run", "independent_review": "pending",
            "approval": "pending"}

if __name__ == "__main__":
    print(scenario_report(1000, 0, 200, 3))
