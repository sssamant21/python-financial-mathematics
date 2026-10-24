"""Section 4.1: exact rational exponential growth and decay."""
from fractions import Fraction
from math import isqrt

def rational(value):
    if type(value) not in (int, str, Fraction):
        raise TypeError("expected int, rational string, or Fraction")
    return Fraction(value)

def nonnegative_integer(value, name):
    value = rational(value)
    if value < 0 or value.denominator != 1:
        raise ValueError(f"{name} must be a nonnegative integer")
    return int(value)

def future_value(initial, rate, periods):
    initial, rate = rational(initial), rational(rate)
    n = nonnegative_integer(periods, "periods")
    if initial < 0 or rate <= -1:
        raise ValueError("require initial >= 0 and rate > -1")
    return initial * (1 + rate) ** n

def cumulative_change(rate, periods):
    rate = rational(rate)
    n = nonnegative_integer(periods, "periods")
    if rate <= -1:
        raise ValueError("require rate > -1")
    return (1 + rate) ** n - 1

def linear_value(initial, increment, periods):
    initial, increment = rational(initial), rational(increment)
    n = nonnegative_integer(periods, "periods")
    if initial < 0:
        raise ValueError("initial must be nonnegative")
    return initial + increment * n

def _integer_nth_root(value, n):
    """Exact integer root or None, using binary search."""
    if value < 0 or n < 1:
        raise ValueError("require value >= 0 and n >= 1")
    if value in (0, 1):
        return value
    lo, hi = 0, value + 1
    while hi - lo > 1:
        mid = (lo + hi) // 2
        if mid ** n <= value:
            lo = mid
        else:
            hi = mid
    return lo if lo ** n == value else None

def implied_rate(initial, final, periods):
    """Exact positive growth-factor inverse; classify irrational roots."""
    initial, final = rational(initial), rational(final)
    n = nonnegative_integer(periods, "periods")
    if initial <= 0 or final <= 0 or n == 0:
        raise ValueError("require positive values and periods >= 1")
    ratio = final / initial
    numerator = _integer_nth_root(ratio.numerator, n)
    denominator = _integer_nth_root(ratio.denominator, n)
    if numerator is None or denominator is None:
        return {"kind": "not_rational", "ratio": ratio, "periods": n}
    rate = Fraction(numerator, denominator) - 1
    assert future_value(initial, rate, n) == final
    return {"kind": "exact", "rate": rate}

if __name__ == "__main__":
    print("Growth:", future_value(1000, "1/20", 3))
    print("Decay:", future_value(500, "-1/5", 3))
    print("Implied rate:", implied_rate(100, 121, 2))
