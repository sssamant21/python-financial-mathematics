"""Predeclared synthetic PDE grid sensitivity; descriptive, not certified."""
import argparse
import math
from pde_benchmark import finite_difference_put

GRIDS = ((40, 2000), (60, 5000), (80, 9000))

def black_scholes_european_put(spot=100., strike=100., rate=0.05, volatility=0.2, years=1.):
    """Independent analytic European put for q=0 and positive inputs."""
    values = (spot, strike, rate, volatility, years)
    if any(type(x) not in (float, int) or not math.isfinite(x) for x in values):
        raise ValueError("finite numeric parameters required")
    if min(spot, strike, volatility, years) <= 0:
        raise ValueError("positive spot/strike/volatility/maturity required")
    d1 = (math.log(spot / strike) + (rate + volatility**2 / 2) * years) / (volatility * math.sqrt(years))
    d2 = d1 - volatility * math.sqrt(years)
    cdf = lambda z: 0.5 * math.erfc(-z / math.sqrt(2))
    return strike * math.exp(-rate * years) * cdf(-d2) - spot * cdf(-d1)

def grid_sensitivity(grids=GRIDS):
    """Compare fixed stable grids, never infer monotonicity from a small sample."""
    if not isinstance(grids, (tuple, list)) or not grids:
        raise ValueError("nonempty grid sequence required")
    reference = black_scholes_european_put()
    rows = []
    for grid in grids:
        if not isinstance(grid, (tuple, list)) or len(grid) != 2:
            raise ValueError("each grid must have spot/time steps")
        spatial, temporal = grid
        european = finite_difference_put(american=False, spot_steps=spatial, time_steps=temporal)
        american = finite_difference_put(american=True, spot_steps=spatial, time_steps=temporal)
        rows.append(dict(spot_steps=spatial, time_steps=temporal,
                         european=european, american=american,
                         european_abs_error=abs(european-reference),
                         exercise_premium=american-european))
    return rows

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Synthetic PDE grid refinement")
    parser.parse_args()
    print("Black-Scholes European put reference:", round(black_scholes_european_put(), 8))
    for row in grid_sensitivity():
        print(row)
