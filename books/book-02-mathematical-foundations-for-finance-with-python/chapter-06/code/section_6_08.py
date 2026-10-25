"""Section 6.8: zero rates and independent finite-series verification."""
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
        raise TypeError("periods must be an integer")
    if value < 0:
        raise ValueError("periods must be nonnegative")
    return value

def annuity_value(payment, rate, n, kind="pv", timing="end"):
    c, r, n = finite(payment, "payment"), finite(rate, "rate"), periods(n)
    if r <= -1:
        raise ValueError("rate must exceed -1")
    if kind not in ("pv", "fv") or timing not in ("end", "begin"):
        raise ValueError("invalid valuation convention")
    if n == 0 or c == 0:
        return 0.0
    if r == 0:
        factor = float(n)
    else:
        x = n * math.log1p(r)
        factor = (-math.expm1(-x) if kind == "pv" else math.expm1(x)) / r
    result = c * factor * (1 + r if timing == "begin" else 1)
    if not math.isfinite(result):
        raise OverflowError("nonfinite annuity value")
    return result

def growing_value(first_payment, growth, rate, n, kind="pv", timing="end"):
    c = finite(first_payment, "first_payment")
    g, r, n = finite(growth, "growth"), finite(rate, "rate"), periods(n)
    if g <= -1 or r <= -1:
        raise ValueError("rates must exceed -1")
    if kind not in ("pv", "fv") or timing not in ("end", "begin"):
        raise ValueError("invalid valuation convention")
    if n == 0 or c == 0:
        return 0.0
    x = math.log1p(g) - math.log1p(r)
    factor = float(n) if x == 0 else math.expm1(n*x)/math.expm1(x)
    pv = c / (1 + r) * factor
    result = pv if kind == "pv" else pv * math.exp(n * math.log1p(r))
    if timing == "begin":
        result *= 1 + r
    if not math.isfinite(result):
        raise OverflowError("nonfinite growing value")
    return result

def direct_value(first_payment, growth, rate, n, kind="pv", timing="end"):
    c = finite(first_payment, "first_payment")
    g, r, n = finite(growth, "growth"), finite(rate, "rate"), periods(n)
    if g <= -1 or r <= -1:
        raise ValueError("rates must exceed -1")
    if kind not in ("pv", "fv") or timing not in ("end", "begin"):
        raise ValueError("invalid valuation convention")
    log_growth, log_discount = math.log1p(g), math.log1p(r)
    return math.fsum(
        c * math.exp(k*log_growth +
            ((-k-1 if timing == "end" else -k) if kind == "pv"
             else (n-k-1 if timing == "end" else n-k))*log_discount)
        for k in range(n)
    )

if __name__ == "__main__":
    print("Zero-rate annuity PV:", annuity_value(250, 0, 8))
    print("Zero-rate growing PV:", growing_value(100, 0.02, 0, 3))
    print("Independent growing PV:", direct_value(100, 0.02, 0, 3))
