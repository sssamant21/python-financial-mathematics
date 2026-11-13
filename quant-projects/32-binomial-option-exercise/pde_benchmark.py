"""Independent explicit finite-difference American-put benchmark (synthetic only).

Solves Black--Scholes PDE on a uniform spot grid, projecting onto intrinsic
value at every backward time step. Not a market-calibrated pricing engine.
"""
import argparse
import math


def finite_difference_put(spot=100.0, strike=100.0, rate=0.05, dividend=0.0,
                          volatility=0.2, years=1.0, american=True,
                          spot_steps=400, time_steps=20000, spot_max=None):
    params = (spot, strike, rate, dividend, volatility, years)
    if any(type(x) not in (int, float) or not math.isfinite(x) for x in params):
        raise ValueError('financial parameters must be finite numbers')
    if min(spot, strike, volatility, years) <= 0:
        raise ValueError('spot, strike, volatility and years must be positive')
    if not (-0.2 <= rate <= 0.5 and -0.2 <= dividend <= 0.5):
        raise ValueError('rate/dividend outside educational bounds')
    if type(american) is not bool:
        raise ValueError('american must be bool')
    if type(spot_steps) is not int or not 20 <= spot_steps <= 1000:
        raise ValueError('spot_steps must be in [20, 1000]')
    if type(time_steps) is not int or not 1 <= time_steps <= 200000:
        raise ValueError('time_steps must be in [1, 200000]')
    if spot_max is None:
        spot_max = max(4 * strike, 2 * spot)
    if type(spot_max) not in (int, float) or not math.isfinite(spot_max) or spot_max <= max(spot, strike):
        raise ValueError('spot_max must exceed spot and strike')
    ds = spot_max / spot_steps
    dt = years / time_steps
    # Upwind first derivative and explicit second derivative; reject nonmonotone grids.
    coeffs = []
    for j in range(1, spot_steps):
        diffusion = 0.5 * volatility**2 * j**2
        drift = (rate - dividend) * j
        left = diffusion + max(-drift, 0.0)
        right = diffusion + max(drift, 0.0)
        a = dt * left
        b = 1 - dt * (left + right + rate)
        c = dt * right
        if min(a, b, c) < -1e-14:
            raise ValueError('unstable explicit grid; increase time_steps or reduce spot_steps')
        coeffs.append((a, b, c))
    values = [max(strike - j * ds, 0.0) for j in range(spot_steps + 1)]
    for k in range(time_steps):
        remaining = (k + 1) * dt
        lower = strike if american else strike * math.exp(-rate * remaining)
        updated = [lower] + [0.0] * (spot_steps - 1) + [0.0]
        for j, (a, b, c) in enumerate(coeffs, 1):
            continuation = a * values[j-1] + b * values[j] + c * values[j+1]
            updated[j] = max(continuation, strike - j * ds) if american else continuation
        values = updated
    location = spot / ds
    low = int(location)
    fraction = location - low
    return values[low] * (1 - fraction) + values[low+1] * fraction


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Synthetic explicit PDE put benchmark')
    parser.add_argument('--spot-steps', type=int, default=100)
    parser.add_argument('--time-steps', type=int, default=10000)
    args = parser.parse_args()
    for american in (False, True):
        result = finite_difference_put(american=american, **vars(args))
        print(('American' if american else 'European') + f' put: {result:.6f}')
