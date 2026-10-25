"""Section 6.3: infinite geometric series and discounted cash flows."""
import math

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

def nonnegative_int(value, name):
    if type(value) is not int:
        raise TypeError(f"{name} must be an integer")
    if value < 0:
        raise ValueError(f"{name} must be nonnegative")
    return value

def geometric_partial(ratio, terms):
    """Sum of terms k=0,...,terms-1, including an empty sum."""
    q = finite(ratio, "ratio")
    n = nonnegative_int(terms, "terms")
    if n == 0:
        return 0.0
    if q == 1:
        return float(n)
    if q > 0:
        delta = q - 1
        value = math.expm1(n * math.log1p(delta)) / delta
    else:
        value = (1 - q ** n) / (1 - q)
    if not math.isfinite(value):
        raise OverflowError("nonfinite partial sum")
    return value

def geometric_infinite(ratio, first=1):
    """Sum first * q**k, k>=0; requires |q|<1 for nonzero first."""
    q = finite(ratio, "ratio")
    a = finite(first, "first")
    if a == 0:
        return 0.0
    if abs(q) >= 1:
        raise ValueError("nonzero geometric series requires |ratio| < 1")
    return a / (1 - q)

def geometric_remainder(ratio, terms, first=1):
    """Exact infinite-series tail after terms initial terms."""
    q = finite(ratio, "ratio")
    n = nonnegative_int(terms, "terms")
    a = finite(first, "first")
    if a == 0:
        return 0.0
    if abs(q) >= 1:
        raise ValueError("nonzero geometric series requires |ratio| < 1")
    value = a * q ** n / (1 - q)
    if not math.isfinite(value):
        raise OverflowError("nonfinite remainder")
    return value

def perpetuity(payment, rate, timing="end"):
    """PV of level payments, first at t=1 (end) or t=0 (begin)."""
    c = finite(payment, "payment")
    r = finite(rate, "rate")
    if timing not in ("end", "begin"):
        raise ValueError("timing must be end or begin")
    if r <= 0:
        raise ValueError("positive discount rate required")
    result = c / r
    if timing == "begin":
        result *= 1 + r
    if not math.isfinite(result):
        raise OverflowError("nonfinite present value")
    return result

def perpetuity_tail(payment, rate, completed_periods):
    """PV at t=0 of end-of-period payments after period N."""
    c = finite(payment, "payment")
    r = finite(rate, "rate")
    n = nonnegative_int(completed_periods, "completed_periods")
    if r <= 0:
        raise ValueError("positive discount rate required")
    value = (c / r) * math.exp(-n * math.log1p(r))
    if not math.isfinite(value):
        raise OverflowError("nonfinite tail")
    return value

if __name__ == "__main__":
    print("Infinite sum at q=0.8:", geometric_infinite(0.8))
    print("First four terms:", geometric_partial(0.8, 4))
    print("Remainder:", geometric_remainder(0.8, 4))
    print("Ordinary perpetuity:", perpetuity(100, 0.05))
    print("Due perpetuity:", perpetuity(100, 0.05, "begin"))
