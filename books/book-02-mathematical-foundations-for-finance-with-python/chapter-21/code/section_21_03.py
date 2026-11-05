"""Educational cash-flow and rate functions; not production valuation."""
import math
from decimal import Context, Decimal, localcontext
from fractions import Fraction
from numbers import Real

def _finite(x, name):
    if isinstance(x, bool) or not isinstance(x, Real):
        raise TypeError(f"{name} must be a real number, excluding bool")
    try: x = float(x)
    except OverflowError as exc: raise ValueError(f"{name} exceeds float range") from exc
    if not math.isfinite(x): raise ValueError(f"{name} must be finite")
    return x

def _rounded(value, name):
    try: result = float(value)
    except OverflowError as exc: raise OverflowError(f"{name} exceeds float range") from exc
    if not math.isfinite(result): raise OverflowError(f"{name} exceeds float range")
    return result

def _validated_rate(rate, convention):
    rate = _finite(rate, "rate")
    if convention == "effective_annual":
        if rate <= -1: raise ValueError("effective annual rate must exceed -1")
    elif convention != "continuous":
        raise ValueError("unsupported rate convention")
    return rate

def _scaled_discount(amount, rate, years, convention, name):
    if not amount or not years or not rate:
        return amount
    with localcontext(Context(prec=850)):
        annual = Decimal(rate)
        if convention == "effective_annual":
            annual = (1 + annual).ln()
        exponent = -annual * Decimal(years)
        # At this scale even the smallest/largest nonzero binary64 amount
        # cannot recover a representable nonzero result on the other side.
        if exponent > 2000:
            raise OverflowError(f"{name} exceeds float range")
        if exponent < -2000:
            return math.copysign(0., amount)
        return _rounded(Decimal(amount) * exponent.exp(), name)

def discount_factor(rate, years, convention):
    rate, years = _finite(rate, "rate"), _finite(years, "years")
    if years < 0: raise ValueError("years must be nonnegative")
    _validated_rate(rate, convention)
    return _scaled_discount(1., rate, years, convention, "discount factor")

def to_continuous(effective_rate):
    rate = _finite(effective_rate, "effective rate")
    if rate <= -1: raise ValueError("effective annual rate must exceed -1")
    return math.log1p(rate)

def to_effective(continuous_rate):
    rate = _finite(continuous_rate, "continuous rate")
    try: result = math.expm1(rate)
    except OverflowError as exc: raise OverflowError("rate exceeds float range") from exc
    if not math.isfinite(result) or result <= -1:
        raise OverflowError("equivalent effective rate cannot be represented")
    return result

def present_value(flows, rate, convention):
    # Validate rate and convention even for an empty stream.
    rate = _validated_rate(rate, convention)
    total = Fraction(0)
    for amount, years in flows:
        amount = _finite(amount, "amount")
        years = _finite(years, "years")
        if years < 0: raise ValueError("years must be nonnegative")
        term = _scaled_discount(amount, rate, years, convention, "cash-flow value")
        total += Fraction(term)
    return _rounded(total, "portfolio")

if __name__ == "__main__":
    print("Zero-rate value:", present_value([(100, 1), (200, 2)], 0, "continuous"))
    print("Equivalent continuous rate:", to_continuous(.25))
