"""Boundary input examples: educational draft."""
import math
from numbers import Real

def finite_real(x, name):
    if isinstance(x, bool) or not isinstance(x, Real):
        raise TypeError(f"{name} must be real and not bool")
    try:
        x = float(x)
    except OverflowError as exc:
        raise ValueError(f"{name} exceeds float range") from exc
    if not math.isfinite(x):
        raise ValueError(f"{name} must be finite")
    return x

def present_value(amount, rate, years):
    amount, rate = finite_real(amount, "amount"), finite_real(rate, "rate")
    if isinstance(years, bool) or not isinstance(years, int):
        raise TypeError("years must be an integer, excluding bool")
    if years < 0 or rate <= -1:
        raise ValueError("years must be nonnegative and rate must exceed -1")
    try:
        result = amount * math.exp(-years * math.log1p(rate))
    except OverflowError as exc:
        raise OverflowError("present value exceeds numerical range") from exc
    if not math.isfinite(result):
        raise OverflowError("present value exceeds numerical range")
    return result

def annuity_pv(payment, rate, periods):
    payment, rate = finite_real(payment, "payment"), finite_real(rate, "rate")
    if isinstance(periods, bool) or not isinstance(periods, int):
        raise TypeError("periods must be an integer, excluding bool")
    if periods < 0 or rate <= -1:
        raise ValueError("periods must be nonnegative and rate must exceed -1")
    if periods == 0: return 0.0
    try:
        # Form the annuity factor before applying the payment to avoid
        # underflow in payment * expm1(...) for tiny nonzero rates.
        result = payment * periods if rate == 0 else payment * ((-math.expm1(-periods * math.log1p(rate))) / rate)
    except OverflowError as exc:
        raise OverflowError("annuity exceeds numerical range") from exc
    if not math.isfinite(result):
        raise OverflowError("annuity exceeds numerical range")
    return result

if __name__ == "__main__":
    print("Zero rate:", annuity_pv(100, 0, 3))
    print("Negative rate:", present_value(100, -.1, 2))
    try: present_value(100, -1, 2)
    except ValueError as exc: print("Rejected:", exc)
