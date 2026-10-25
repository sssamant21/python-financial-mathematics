"""Section 6.4: ordinary annuities and annuities due."""
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

def annuity_factor(rate, n, kind="pv"):
    i = finite(rate, "rate")
    n = periods(n)
    if i <= -1:
        raise ValueError("rate must exceed -1")
    if kind not in ("pv", "fv"):
        raise ValueError("kind must be pv or fv")
    if n == 0:
        return 0.0
    if i == 0:
        return float(n)
    x = n * math.log1p(i)
    value = (-math.expm1(-x) if kind == "pv" else math.expm1(x)) / i
    if not math.isfinite(value):
        raise OverflowError("nonfinite annuity factor")
    return value

def annuity_value(payment, rate, n, kind="pv", timing="end"):
    c = finite(payment, "payment")
    i = finite(rate, "rate")
    n = periods(n)
    if timing not in ("end", "begin"):
        raise ValueError("timing must be end or begin")
    factor = annuity_factor(i, n, kind)
    result = c * factor * (1 + i if timing == "begin" else 1)
    if not math.isfinite(result):
        raise OverflowError("nonfinite annuity value")
    return result

def payment_for_present_value(present_value, rate, n, timing="end"):
    pv = finite(present_value, "present_value")
    i = finite(rate, "rate")
    n = periods(n)
    if n == 0:
        raise ValueError("cannot solve payment for zero periods")
    if timing not in ("end", "begin"):
        raise ValueError("timing must be end or begin")
    factor = annuity_factor(i, n, "pv")
    if timing == "begin":
        factor *= 1 + i
    result = pv / factor
    if not math.isfinite(result):
        raise OverflowError("nonfinite payment")
    return result

def direct_value(payment, rate, n, kind="pv", timing="end"):
    """Independent finite-sum calculation for verification."""
    c = finite(payment, "payment")
    i = finite(rate, "rate")
    n = periods(n)
    if i <= -1:
        raise ValueError("rate must exceed -1")
    if kind not in ("pv", "fv") or timing not in ("end", "begin"):
        raise ValueError("invalid valuation convention")
    q = 1 + i
    payment_times = range(1, n + 1) if timing == "end" else range(n)
    exponents = ((-k if kind == "pv" else n - k) for k in payment_times)
    value = math.fsum(c * q ** power for power in exponents)
    if not math.isfinite(value):
        raise OverflowError("nonfinite direct value")
    return value

if __name__ == "__main__":
    for timing in ("end", "begin"):
        print(timing, "PV:", annuity_value(100, 0.02, 3, "pv", timing))
        print(timing, "FV:", annuity_value(100, 0.02, 3, "fv", timing))
