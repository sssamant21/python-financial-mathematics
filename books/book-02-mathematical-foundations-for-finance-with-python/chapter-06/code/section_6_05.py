"""Section 6.5: finite growing payment streams and growing perpetuities."""
import math

def finite(value, name):
    if type(value) not in (int, float):
        raise TypeError(f"{name} must be numeric, excluding bool")
    x = float(value)
    if not math.isfinite(x):
        raise ValueError(f"{name} must be finite")
    return x

def periods(value):
    if type(value) is not int:
        raise TypeError("periods must be an integer")
    if value < 0:
        raise ValueError("periods must be nonnegative")
    return value

def geometric_factor(log_ratio, n):
    if n == 0:
        return 0.0
    if log_ratio == 0:
        return float(n)
    value = math.expm1(n * log_ratio) / math.expm1(log_ratio)
    if not math.isfinite(value):
        raise OverflowError("nonfinite geometric factor")
    return value

def growing_value(first_payment, growth, rate, n, kind="pv", timing="end"):
    c = finite(first_payment, "first_payment")
    g = finite(growth, "growth")
    r = finite(rate, "rate")
    n = periods(n)
    if g <= -1 or r <= -1:
        raise ValueError("rates must exceed -1")
    if kind not in ("pv", "fv") or timing not in ("end", "begin"):
        raise ValueError("invalid valuation convention")
    if n == 0 or c == 0:
        return 0.0
    x = math.log1p(g) - math.log1p(r)
    pv = c / (1 + r) * geometric_factor(x, n)
    result = pv if kind == "pv" else pv * math.exp(n * math.log1p(r))
    if timing == "begin":
        result *= 1 + r
    if not math.isfinite(result):
        raise OverflowError("nonfinite value")
    return result

def direct_value(first_payment, growth, rate, n, kind="pv", timing="end"):
    c = finite(first_payment, "first_payment")
    g = finite(growth, "growth")
    r = finite(rate, "rate")
    n = periods(n)
    if g <= -1 or r <= -1:
        raise ValueError("rates must exceed -1")
    if kind not in ("pv", "fv") or timing not in ("end", "begin"):
        raise ValueError("invalid valuation convention")
    q, h = 1 + r, 1 + g
    return math.fsum(
        c * h**k * q**(
            -(k + 1) if timing == "end" else -k
        ) if kind == "pv" else
        c * h**k * q**(
            n - k - 1 if timing == "end" else n - k
        )
        for k in range(n)
    )

def growing_perpetuity(first_payment, growth, rate, timing="end"):
    c = finite(first_payment, "first_payment")
    g = finite(growth, "growth")
    r = finite(rate, "rate")
    if g <= -1 or r <= -1:
        raise ValueError("rates must exceed -1")
    if timing not in ("end", "begin"):
        raise ValueError("timing must be end or begin")
    if c == 0:
        return 0.0
    if r <= g:
        raise ValueError("nonzero perpetuity requires rate > growth")
    result = c / (r - g)
    if timing == "begin":
        result *= 1 + r
    return result

if __name__ == "__main__":
    for timing in ("end", "begin"):
        print(timing, "PV:", growing_value(100, 0.03, 0.05, 3, "pv", timing))
        print(timing, "FV:", growing_value(100, 0.03, 0.05, 3, "fv", timing))
