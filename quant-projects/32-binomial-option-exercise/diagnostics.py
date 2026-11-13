"""Predeclared CRR convergence and American-put exercise-boundary diagnostics.

Synthetic inputs only. Boundary is the highest spot where immediate exercise is
strictly positive and at least as valuable as continuation (within tolerance).
"""
import argparse
import math
from binomial import price_put

STEPS = (25, 50, 100, 200, 400)
BENCHMARK = 5.573526022256971  # independent closed-form BS European put


def convergence(steps=STEPS):
    if not steps or any(type(n) is not int or n < 1 or n > 2000 for n in steps):
        raise ValueError("steps must contain integers from 1 to 2000")
    rows = []
    for n in steps:
        european = price_put(steps=n)
        american = price_put(steps=n, american=True)
        rows.append((n, european, american, abs(european - BENCHMARK)))
    return rows


def exercise_boundary(steps=100, spot=100.0, strike=100.0,
                      rate=0.05, dividend=0.0, volatility=0.2, years=1.0):
    """Return (time, boundary spot or None, exercised node count) for each pre-expiry layer.

    A discrete lattice boundary is not a continuous-time optimal-exercise boundary.
    Only strictly positive intrinsic-value nodes qualify; ties at zero do not.
    """
    # Reuse the pricing engine's complete parameter/probability guards.
    price_put(spot, strike, rate, dividend, volatility, years, steps, True)
    dt = years / steps
    u = math.exp(volatility * math.sqrt(dt))
    d = 1 / u
    p = (math.exp((rate - dividend) * dt) - d) / (u - d)
    disc = math.exp(-rate * dt)
    values = [max(strike - spot * u ** j * d ** (steps - j), 0.0)
              for j in range(steps + 1)]
    rows = []
    for i in range(steps - 1, -1, -1):
        eligible = []
        for j in range(i + 1):
            s = spot * u ** j * d ** (i - j)
            continuation = disc * (p * values[j + 1] + (1 - p) * values[j])
            intrinsic = max(strike - s, 0.0)
            if intrinsic > 0 and intrinsic >= continuation - 1e-12:
                eligible.append(s)
            values[j] = max(intrinsic, continuation)
        rows.append((i * dt, max(eligible) if eligible else None, len(eligible)))
    rows.reverse()
    return rows


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Synthetic CRR convergence and exercise boundary")
    parser.add_argument("--steps", type=int, default=100)
    args = parser.parse_args()
    print("steps european american absolute_BS_error")
    for n, european, american, error in convergence():
        print(f"{n:4d} {european:.8f} {american:.8f} {error:.8f}")
    boundary = exercise_boundary(steps=args.steps)
    print(f"exercise layers: {sum(count > 0 for _, _, count in boundary)}/{len(boundary)}")
    print(f"first positive-exercise layer: {next((round(t, 6) for t, _, count in boundary if count), None)}")
