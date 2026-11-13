"""Independent top-down memoized CRR reference for small synthetic trees.

Uses recursive node valuation rather than the production pricer's in-place
backward vector. This is an implementation cross-check, not an independent
pricing model or an external market benchmark.
"""
import functools
import math

MAX_STEPS = 24


def reference_put(spot=100.0, strike=100.0, rate=0.05, dividend=0.0,
                  volatility=0.2, years=1.0, steps=10, american=True):
    if type(steps) is not int or not 1 <= steps <= MAX_STEPS:
        raise ValueError("reference steps must be an integer in [1, 24]")
    parameters = (spot, strike, rate, dividend, volatility, years)
    if any(not isinstance(x, (int, float)) or not math.isfinite(x) for x in parameters):
        raise ValueError("all parameters must be finite numbers")
    if min(spot, strike, volatility, years) <= 0:
        raise ValueError("spot, strike, volatility, years must be positive")
    if not (-0.2 <= rate <= 0.5 and -0.2 <= dividend <= 0.5):
        raise ValueError("rate/dividend outside educational limits")
    if type(american) is not bool:
        raise ValueError("american must be bool")

    dt = years / steps
    up = math.exp(volatility * math.sqrt(dt))
    down = 1.0 / up
    probability = (math.exp((rate - dividend) * dt) - down) / (up - down)
    if not 0 <= probability <= 1:
        raise ValueError("invalid risk-neutral probability")
    discount = math.exp(-rate * dt)

    @functools.lru_cache(maxsize=None)
    def node(time_index, up_count):
        stock = spot * (up ** up_count) * (down ** (time_index - up_count))
        intrinsic = max(strike - stock, 0.0)
        if time_index == steps:
            return intrinsic
        hold = discount * (probability * node(time_index + 1, up_count + 1)
                           + (1 - probability) * node(time_index + 1, up_count))
        return max(intrinsic, hold) if american else hold

    return node(0, 0)


def compare_grid():
    """Precommitted cases; no data fitting or parameter optimization."""
    from binomial import price_put
    cases = (
        (100.0, 100.0, 0.05, 0.0, 0.2, 1.0),
        (70.0, 100.0, 0.05, 0.0, 0.2, 1.0),
        (120.0, 100.0, 0.03, 0.01, 0.3, 0.5),
    )
    rows = []
    for params in cases:
        for steps in (1, 2, 5, 10, 20):
            for american in (False, True):
                ref = reference_put(*params, steps=steps, american=american)
                actual = price_put(*params, steps=steps, american=american)
                rows.append((params, steps, american, ref, actual, abs(ref - actual)))
    return rows


if __name__ == "__main__":
    rows = compare_grid()
    print("cases", len(rows), "max_absolute_difference",
          f"{max(row[-1] for row in rows):.12g}")
