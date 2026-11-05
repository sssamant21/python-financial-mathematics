"""Educational continuous-discount sensitivity calculations."""
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

def inputs(amount, rate, years):
    amount, rate, years = finite(amount, "amount"), finite(rate, "rate"), finite(years, "years")
    if years < 0: raise ValueError("years must be nonnegative")
    return amount, rate, years

def checked(x):
    if not math.isfinite(x): raise OverflowError("result exceeds float range")
    return x

def _scaled_terms(coefficients, exponent):
    if not exponent or not any(coefficients):
        return tuple(checked(float(c)) for c in coefficients)
    # The finite binary64 inputs give dyadic coefficients with magnitude
    # below 2**5120 and nonzero magnitude at least 2**-5371, even for
    # amount * (1 - years*change + (years*change)**2/2).
    if exponent > 5000:
        raise OverflowError("result exceeds float range")
    if exponent < -5000:
        return tuple(-0. if c < 0 else 0. for c in coefficients)
    with localcontext(Context(prec=1800)):
        factor = (Decimal(exponent.numerator) / Decimal(exponent.denominator)).exp()
        return tuple(checked(float(Decimal(c.numerator) * factor / Decimal(c.denominator)))
                     for c in coefficients)

def pv(amount, rate, years):
    amount, rate, years = inputs(amount, rate, years)
    if not amount or not rate or not years:
        return amount
    return _scaled_terms((Fraction(amount),), -Fraction(rate) * Fraction(years))[0]

def derivatives(amount, rate, years):
    amount, rate, years = inputs(amount, rate, years)
    a, r, t = map(Fraction, (amount, rate, years))
    return _scaled_terms((-a*t, a*t*t), -r*t)

def central_difference(amount, rate, years, step):
    amount, rate, years = inputs(amount, rate, years)
    step = finite(step, "step")
    if step <= 0: raise ValueError("step must be positive")
    up, down = rate + step, rate - step
    if not math.isfinite(up) or not math.isfinite(down) or up == rate or down == rate:
        raise ValueError("step does not produce finite distinct perturbations")
    if not math.isfinite(2 * step):
        raise OverflowError("central-difference denominator exceeds float range")
    return checked((pv(amount, up, years) - pv(amount, down, years)) / (2 * step))

def approximations(amount, rate, years, change):
    change = finite(change, "change")
    a, r, t = map(Fraction, inputs(amount, rate, years))
    z = t * Fraction(change)
    return _scaled_terms((a*(1-z), a*(1-z+z*z/2)), -r*t)

if __name__ == "__main__":
    print("First and second derivatives:", derivatives(100, 0, 2))
    print("Approximations:", approximations(100, 0, 2, .01))
    print("Central difference:", central_difference(100, 0, 2, 1e-5))
