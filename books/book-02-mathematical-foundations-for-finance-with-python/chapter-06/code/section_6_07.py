"""Section 6.7: geometric truncation error and horizon selection."""
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

def periods(value):
    if type(value) is not int:
        raise TypeError("period count must be an integer")
    if value < 0:
        raise ValueError("period count must be nonnegative")
    return value

def validate_ratio(ratio):
    q = finite(ratio, "ratio")
    if abs(q) >= 1:
        raise ValueError("convergent geometric series requires |ratio| < 1")
    return q

def infinite_value(first, ratio):
    a, q = finite(first, "first"), validate_ratio(ratio)
    value = a / (1 - q)
    if not math.isfinite(value):
        raise OverflowError("nonfinite sum")
    return value

def partial_value(first, ratio, n):
    a, q, n = finite(first, "first"), validate_ratio(ratio), periods(n)
    value = math.fsum(a * q**k for k in range(n))
    if not math.isfinite(value):
        raise OverflowError("nonfinite partial sum")
    return value

def exact_tail(first, ratio, n):
    a, q, n = finite(first, "first"), validate_ratio(ratio), periods(n)
    value = a * q**n / (1 - q)
    if not math.isfinite(value):
        raise OverflowError("nonfinite tail")
    return value

def relative_error(ratio, n):
    q, n = validate_ratio(ratio), periods(n)
    return abs(q)**n

def minimum_terms_relative(ratio, tolerance):
    q, eps = validate_ratio(ratio), finite(tolerance, "tolerance")
    if not 0 < eps < 1:
        raise ValueError("relative tolerance must lie strictly between 0 and 1")
    if q == 0:
        return 1
    logq = math.log(abs(q))
    n = max(0, math.ceil(math.log(eps) / logq))
    # Correct rounding at the threshold without forming tiny powers.
    while n > 0 and (n - 1) * logq <= math.log(eps):
        n -= 1
    while n * logq > math.log(eps):
        n += 1
    return n

def perpetuity_tail(payment, rate, n):
    c, r, n = finite(payment, "payment"), finite(rate, "rate"), periods(n)
    if r <= 0:
        raise ValueError("discount rate must be positive")
    value = c / r * math.exp(-n * math.log1p(r))
    if not math.isfinite(value):
        raise OverflowError("nonfinite tail")
    return value

def minimum_perpetuity_terms(rate, tolerance):
    r = finite(rate, "rate")
    if r <= 0:
        raise ValueError("discount rate must be positive")
    # q = 1/(1+r); log(q) = -log1p(r).
    eps = finite(tolerance, "tolerance")
    if not 0 < eps < 1:
        raise ValueError("relative tolerance must lie strictly between 0 and 1")
    logq = -math.log1p(r)
    n = max(0, math.ceil(math.log(eps) / logq))
    while n > 0 and (n - 1) * logq <= math.log(eps):
        n -= 1
    while n * logq > math.log(eps):
        n += 1
    return n

if __name__ == "__main__":
    print("Infinite geometric sum:", infinite_value(1, 0.8))
    print("Four-term partial sum:", partial_value(1, 0.8, 4))
    print("Exact remainder:", exact_tail(1, 0.8, 4))
    print("1% horizon at 5%:", minimum_perpetuity_terms(0.05, 0.01))
