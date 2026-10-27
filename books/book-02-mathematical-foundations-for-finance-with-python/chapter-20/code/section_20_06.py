"""Metamorphic checks with bounded, synthetic cash flows; educational draft."""
import math
import random

def pv(amount, rate, years):
    """Continuous discounting for finite inputs and nonnegative time."""
    if not all(math.isfinite(x) for x in (amount, rate, years)):
        raise ValueError("inputs must be finite")
    if years < 0:
        raise ValueError("years must be nonnegative")
    return amount * math.exp(-rate * years)

def portfolio(flows, rate):
    """flows is a sequence of (amount, years) pairs."""
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
