"""Boundary input examples: educational draft."""
import math
import sys
from decimal import Context, Decimal, localcontext
from fractions import Fraction
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

def _rounded_value(value, name):
    try:
        result = float(value)
    except OverflowError as exc:
        raise OverflowError(f"{name} exceeds numerical range") from exc
    if not math.isfinite(result):
        raise OverflowError(f"{name} exceeds numerical range")
    return result


def _discount_exponent(rate, periods):
    # Even the smallest nonzero binary64 rate reaches the limiting branch
    # at these counts. Avoid converting an arbitrarily large int to Decimal.
    if periods.bit_length() > 1100:
        return Decimal("-Infinity" if rate > 0 else "Infinity")
    return -Decimal(periods) * (1 + Decimal(rate)).ln()


def _annuity_limit(payment, rate):
    # The finite sum approaches its positive magnitude limit from below.
    # At exponent < -4000, the tail is smaller than the minimum nonzero
    # distance from a ratio of two binary64 values to a rounding midpoint:
    # the ratio denominator is < 2**2098, the midpoint denominator <= 2**1075.
    magnitude = Fraction(abs(payment)) / Fraction(rate)
    maximum = sys.float_info.max
    overflow_midpoint = Fraction(maximum) + Fraction(math.ulp(maximum)) / 2
    if magnitude == overflow_midpoint:
        return math.copysign(maximum, payment)
    value = _rounded_value(magnitude, "annuity")
    lower = math.nextafter(value, 0.)
    if value and 2 * magnitude == Fraction(lower) + Fraction(value):
        value = lower
    return math.copysign(value, payment)


def present_value(amount, rate, years):
    amount, rate = finite_real(amount, "amount"), finite_real(rate, "rate")
    if isinstance(years, bool) or not isinstance(years, int):
        raise TypeError("years must be an integer, excluding bool")
    if years < 0 or rate <= -1:
        raise ValueError("years must be nonnegative and rate must exceed -1")
    if amount == 0 or rate == 0 or years == 0:
        return amount
    if years <= 128:
        gross = 1 + Fraction(rate)
        return _rounded_value(Fraction(amount) / gross**years, "present value")
    with localcontext(Context(prec=1800)):
        exponent = _discount_exponent(rate, years)
        if exponent > 4000:
            raise OverflowError("present value exceeds numerical range")
        if exponent < -4000:
            return math.copysign(0., amount)
        return _rounded_value(Decimal(amount) * exponent.exp(), "present value")

def annuity_pv(payment, rate, periods):
    payment, rate = finite_real(payment, "payment"), finite_real(rate, "rate")
    if isinstance(periods, bool) or not isinstance(periods, int):
        raise TypeError("periods must be an integer, excluding bool")
    if periods < 0 or rate <= -1:
        raise ValueError("periods must be nonnegative and rate must exceed -1")
    if periods == 0:
        return 0.0
    if payment == 0:
        return payment
    if rate == 0:
        return _rounded_value(Fraction(payment) * periods, "annuity")
    if periods <= 128:
        r = Fraction(rate)
        return _rounded_value(Fraction(payment) * (1 - (1 + r)**(-periods)) / r, "annuity")
    with localcontext(Context(prec=1800)):
        exponent = _discount_exponent(rate, periods)
        if exponent > 4000:
            raise OverflowError("annuity exceeds numerical range")
        if exponent < -4000:
            return _annuity_limit(payment, rate)
        amount = Decimal(payment) * (1 - exponent.exp()) / Decimal(rate)
        return _rounded_value(amount, "annuity")

if __name__ == "__main__":
    print("Zero rate:", annuity_pv(100, 0, 3))
    print("Negative rate:", present_value(100, -.1, 2))
    try: present_value(100, -1, 2)
    except ValueError as exc: print("Rejected:", exc)
