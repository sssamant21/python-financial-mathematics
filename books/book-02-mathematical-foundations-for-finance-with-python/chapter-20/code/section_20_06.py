"""Metamorphic checks with bounded, synthetic cash flows; educational draft."""
import math
import random
from numbers import Real

def finite(value, name):
    if isinstance(value, bool) or not isinstance(value, Real):
        raise TypeError(f"{name} must be real, excluding bool")
    try:
        result = float(value)
    except OverflowError as exc:
        raise ValueError(f"{name} outside float range") from exc
    if not math.isfinite(result):
        raise ValueError(f"{name} must be finite")
    return result

def pv(amount, rate, years):
    """Continuous discounting for finite inputs and nonnegative time."""
    amount, rate, years = (finite(x, name) for x, name in
                           ((amount, "amount"), (rate, "rate"), (years, "years")))
    if years < 0:
        raise ValueError("years must be nonnegative")
    exponent = -rate * years
    if not math.isfinite(exponent):
        raise OverflowError("discount exponent exceeds float range")
    result = amount * math.exp(exponent)
    if not math.isfinite(result):
        raise OverflowError("present value exceeds float range")
    return result

def portfolio(flows, rate):
    """flows is a sequence of (amount, years) pairs."""
    rate = finite(rate, "rate")
    return math.fsum(pv(amount, rate, years) for amount, years in flows)

def close(a, b):
    return math.isclose(a, b, rel_tol=1e-12, abs_tol=1e-9)

def cases(seed=2006, count=20):
    rng = random.Random(seed)
    for _ in range(count):
        yield (rng.uniform(-1000, 1000), rng.uniform(-.05, .15),
               rng.uniform(0, 10), rng.uniform(-3, 3))

if __name__ == "__main__":
    for amount, rate, years, factor in cases():
        source = pv(amount, rate, years)
        assert close(pv(factor * amount, rate, years), factor * source)
    flows = [(100, 1), (200, 2)]
    assert close(portfolio(flows, .05), portfolio(list(reversed(flows)), .05))
    print("Metamorphic demonstration completed; retain output and environment for evidence.")
