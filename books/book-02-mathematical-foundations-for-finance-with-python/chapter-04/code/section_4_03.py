"""Section 4.3: logarithm rules and positive-price log returns."""
import math

def finite_positive(value, name):
    if type(value) not in (int, float):
        raise TypeError(f"{name} must be a real int or float (not bool)")
    try:
        x = float(value)
    except OverflowError as exc:
        raise ValueError(f"{name} is outside finite float range") from exc
    if not math.isfinite(x) or x <= 0:
        raise ValueError(f"{name} must be finite and positive")
    return x

def log_product(a, b):
    a, b = finite_positive(a, "a"), finite_positive(b, "b")
    return math.log(a) + math.log(b)

def log_quotient(a, b):
    a, b = finite_positive(a, "a"), finite_positive(b, "b")
    return math.log(a) - math.log(b)

def log_power(base, exponent):
    base = finite_positive(base, "base")
    if type(exponent) not in (int, float):
        raise TypeError("exponent must be real int or float")
    exponent = float(exponent)
    if not math.isfinite(exponent):
        raise ValueError("exponent must be finite")
    return exponent * math.log(base)

def log_return(initial, final):
    """Stable log(final / initial), for strictly positive finite prices."""
    initial = finite_positive(initial, "initial")
    final = finite_positive(final, "final")
    change = (final - initial) / initial
    if math.isfinite(change) and change > -1:
        return math.log1p(change)
    return math.log(final) - math.log(initial)

def cumulative_log_return(prices):
    """Sum log returns for a sequence of at least two positive prices."""
    values = tuple(finite_positive(x, f"prices[{i}]") for i, x in enumerate(prices))
    if len(values) < 2:
        raise ValueError("at least two prices are required")
    return sum(log_return(a, b) for a, b in zip(values, values[1:]))

def simple_return_from_log(log_change):
    if type(log_change) not in (int, float):
        raise TypeError("log_change must be real int or float")
    log_change = float(log_change)
    if not math.isfinite(log_change):
        raise ValueError("log_change must be finite")
    return math.expm1(log_change)

if __name__ == "__main__":
    prices = [100, 110, 105]
    value = cumulative_log_return(prices)
    print("Cumulative log return:", value)
    print("Cumulative simple return:", simple_return_from_log(value))
