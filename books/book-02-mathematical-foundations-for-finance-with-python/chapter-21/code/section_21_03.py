"""Educational cash-flow and rate functions; not production valuation."""
import math
from numbers import Real

def _finite(x, name):
    if isinstance(x, bool) or not isinstance(x, Real):
        raise TypeError(f"{name} must be a real number, excluding bool")
    try: x = float(x)
    except OverflowError as exc: raise ValueError(f"{name} exceeds float range") from exc
    if not math.isfinite(x): raise ValueError(f"{name} must be finite")
    return x

def _exp_checked(x):
    try: result = math.exp(x)
    except OverflowError as exc: raise OverflowError("discount factor exceeds float range") from exc
    if not math.isfinite(result): raise OverflowError("discount factor exceeds float range")
    return result

def discount_factor(rate, years, convention):
    rate, years = _finite(rate, "rate"), _finite(years, "years")
    if years < 0: raise ValueError("years must be nonnegative")
    if convention == "continuous":
        exponent = -rate * years
    elif convention == "effective_annual":
        if rate <= -1: raise ValueError("effective annual rate must exceed -1")
        exponent = -math.log1p(rate) * years
    else: raise ValueError("unsupported rate convention")
    return _exp_checked(exponent)

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
    discount_factor(rate, 0, convention)
    terms = []
    for amount, years in flows:
        amount = _finite(amount, "amount")
        factor = discount_factor(rate, years, convention)
        term = amount * factor
        if not math.isfinite(term): raise OverflowError("cash-flow value exceeds float range")
        terms.append(term)
    try: result = math.fsum(terms)
    except OverflowError as exc: raise OverflowError("portfolio exceeds float range") from exc
    if not math.isfinite(result): raise OverflowError("portfolio exceeds float range")
    return result

if __name__ == "__main__":
    print("Zero-rate value:", present_value([(100, 1), (200, 2)], 0, "continuous"))
    print("Equivalent continuous rate:", to_continuous(.25))
