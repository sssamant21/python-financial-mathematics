"""Section 6.1: summation, products, and financial cash flows."""
import math

def finite(value, name):
    if type(value) not in (int, float):
        raise TypeError(f"{name} must be numeric, excluding bool")
    try:
        x = float(value)
    except OverflowError as exc:
        raise ValueError(f"{name} outside finite range") from exc
    if not math.isfinite(x):
        raise ValueError(f"{name} must be finite")
    return x

def net_cash_flow(flows):
    return math.fsum(finite(x, "cash_flow") for x in flows)

def accumulation_factor(rates):
    values = tuple(finite(r, "rate") for r in rates)
    if any(r <= -1 for r in values):
        raise ValueError("rates must be greater than -1")
    result = math.prod(1 + r for r in values)
    if not math.isfinite(result):
        raise OverflowError("nonfinite growth factor")
    return result

def future_value(initial, rates, flows):
    """End-of-period cash flows, product/sum expression."""
    initial = finite(initial, "initial")
    rates = tuple(finite(r, "rate") for r in rates)
    flows = tuple(finite(c, "cash_flow") for c in flows)
    if len(rates) != len(flows):
        raise ValueError("rates and flows must have equal lengths")
    if any(r <= -1 for r in rates):
        raise ValueError("rates must be greater than -1")
    factors = tuple(1 + r for r in rates)
    initial_value = initial * math.prod(factors)
    cash_value = math.fsum(
        flow * math.prod(factors[k+1:]) for k, flow in enumerate(flows))
    result = initial_value + cash_value
    if not math.isfinite(result):
        raise OverflowError("nonfinite future value")
    return result

def iterative_value(initial, rates, flows):
    """Independent recurrence for cross-checking future_value."""
    balance = finite(initial, "initial")
    rates = tuple(finite(r, "rate") for r in rates)
    flows = tuple(finite(c, "cash_flow") for c in flows)
    if len(rates) != len(flows):
        raise ValueError("rates and flows must have equal lengths")
    if any(r <= -1 for r in rates):
        raise ValueError("rates must be greater than -1")
    for rate, flow in zip(rates, flows):
        balance = balance * (1 + rate) + flow
        if not math.isfinite(balance):
            raise OverflowError("nonfinite balance")
    return balance

if __name__ == "__main__":
    rates = (0.02, -0.01, 0.03)
    print("Net cash flow:", net_cash_flow((100, -40, 60)))
    print("Growth factor:", accumulation_factor(rates))
    print("No-flow final balance:", future_value(1000, rates, (0, 0, 0)))
    print("Variable-rate future value:",
          future_value(1000, rates, (100, -50, 0)))
