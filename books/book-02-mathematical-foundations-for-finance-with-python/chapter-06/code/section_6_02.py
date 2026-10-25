"""Section 6.2: finite geometric sums and recurring cash flows."""
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

def geometric_sum(ratio, n):
    """Sum of n terms 1 + ratio + ... + ratio**(n-1)."""
    q = finite(ratio, "ratio")
    n = periods(n)
    if n == 0:
        return 0.0
    if q == 1:
        return float(n)
    if q > 0:
        # Preserve small q-1 as passed; log(q) remains stable for positive q.
        delta = q - 1.0
        value = math.expm1(n * math.log1p(delta)) / delta
    else:
        value = (1 - q**n) / (1 - q)
    if not math.isfinite(value):
        raise OverflowError("nonfinite geometric sum")
    return value

def rate_geometric_sum(rate, n):
    """Stable form when periodic rate i is supplied directly."""
    i = finite(rate, "rate")
    n = periods(n)
    if i <= -1:
        raise ValueError("rate must exceed -1")
    if n == 0:
        return 0.0
    if i == 0:
        return float(n)
    value = math.expm1(n * math.log1p(i)) / i
    if not math.isfinite(value):
        raise OverflowError("nonfinite geometric sum")
    return value

def balance_closed(initial, rate, cash_flow, n, timing="end"):
    b = finite(initial, "initial")
    i = finite(rate, "rate")
    c = finite(cash_flow, "cash_flow")
    n = periods(n)
    if i <= -1:
        raise ValueError("rate must exceed -1")
    if timing not in ("end", "begin"):
        raise ValueError("timing must be end or begin")
    q = 1 + i
    factor = math.exp(n * math.log1p(i)) if n else 1.0
    contribution = c * rate_geometric_sum(i, n)
    if timing == "begin":
        contribution *= q
    result = b * factor + contribution
    if not math.isfinite(result):
        raise OverflowError("nonfinite balance")
    return result

def balance_iterative(initial, rate, cash_flow, n, timing="end"):
    b = finite(initial, "initial")
    i = finite(rate, "rate")
    c = finite(cash_flow, "cash_flow")
    n = periods(n)
    if i <= -1:
        raise ValueError("rate must exceed -1")
    if timing not in ("end", "begin"):
        raise ValueError("timing must be end or begin")
    for _ in range(n):
        b = b * (1 + i) + c if timing == "end" else (b + c) * (1 + i)
        if not math.isfinite(b):
            raise OverflowError("nonfinite balance")
    return b

if __name__ == "__main__":
    print("G3 at 1.02:", rate_geometric_sum(0.02, 3))
    print("End contributions:", balance_closed(1000, 0.02, 100, 3))
    print("Begin contributions:", balance_closed(1000, 0.02, 100, 3, "begin"))
