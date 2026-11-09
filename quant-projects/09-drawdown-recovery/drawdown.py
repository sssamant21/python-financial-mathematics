"""Synthetic-first path-dependent drawdown and recovery diagnostics."""
import argparse
import json
import numpy as np


def analyze(returns):
    r = np.asarray(returns, dtype=float)
    if r.ndim != 1 or r.size < 2 or not np.all(np.isfinite(r)) or np.any(r <= -1):
        raise ValueError("returns must be finite 1-D, length >=2, and > -1")
    wealth = np.r_[1.0, np.cumprod(1.0 + r)]
    peaks = np.maximum.accumulate(wealth)
    dd = 1.0 - wealth / peaks
    trough = int(np.argmax(dd))
    peak = int(np.argmax(wealth[:trough + 1]))
    recovered = np.flatnonzero(wealth[trough + 1:] >= wealth[peak] * (1 - 1e-12))
    recovery = int(trough + 1 + recovered[0]) if recovered.size else None
    longest = current = 0
    for flag in dd > 1e-12:
        current = current + 1 if flag else 0
        longest = max(longest, current)
    return {"max_drawdown": float(dd[trough]), "peak_index": peak,
            "trough_index": trough, "recovery_index": recovery,
            "longest_underwater_periods": longest, "terminal_wealth": float(wealth[-1])}


def bootstrap_risk(returns, *, horizon=52, block=4, simulations=1000, seed=2026):
    r = np.asarray(returns, dtype=float)
    analyze(r)
    if not isinstance(horizon, int) or horizon < 2 or not isinstance(block, int) or block < 1 or block > r.size or not isinstance(simulations, int) or simulations < 10 or simulations > 100000:
        raise ValueError("invalid horizon, block, or simulations")
    rng = np.random.default_rng(seed)
    nblocks = (horizon + block - 1) // block
    starts = rng.integers(0, r.size, size=(simulations, nblocks))
    draws = r[(starts[:, :, None] + np.arange(block)) % r.size].reshape(simulations, -1)[:, :horizon]
    wealth = np.concatenate([np.ones((simulations, 1)), np.cumprod(1 + draws, axis=1)], axis=1)
    dd = 1 - wealth / np.maximum.accumulate(wealth, axis=1)
    max_dd = np.max(dd, axis=1)
    return {"horizon": horizon, "block": block, "simulations": simulations,
            "mean_max_drawdown": float(max_dd.mean()),
            "p95_max_drawdown": float(np.quantile(max_dd, .95)),
            "probability_drawdown_over_20pct": float(np.mean(max_dd > .20))}


def main():
    p = argparse.ArgumentParser(description="Educational synthetic drawdown lab; no market predictions")
    p.add_argument("--seed", type=int, default=2026)
    p.add_argument("--observations", type=int, default=260)
    p.add_argument("--simulations", type=int, default=1000)
    args = p.parse_args()
    if not 52 <= args.observations <= 100000:
        p.error("observations must be between 52 and 100000")
    rng = np.random.default_rng(args.seed)
    returns = np.clip(rng.normal(.001, .025, args.observations), -.95, 2)
    print(json.dumps({"data": "seeded synthetic weekly returns", "observed": analyze(returns),
                      "bootstrap": bootstrap_risk(returns, simulations=args.simulations, seed=args.seed)}, indent=2))


if __name__ == "__main__":
    main()
