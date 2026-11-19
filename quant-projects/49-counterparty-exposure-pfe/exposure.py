"""Synthetic counterparty exposure: PFE, EPE and unilateral CVA (no market data)."""
from __future__ import annotations
import argparse
import math
import random
from statistics import NormalDist

def validate(notional: float, volatility: float, years: int, paths: int,
             threshold: float, lgd: float, hazard: float, rate: float) -> None:
    vals = (notional, volatility, threshold, lgd, hazard, rate)
    if any(isinstance(x, bool) or not isinstance(x, (int, float)) or not math.isfinite(x) for x in vals):
        raise ValueError("parameters must be finite real numbers")
    if notional <= 0 or volatility < 0 or threshold < 0 or not 0 <= lgd <= 1 or hazard < 0 or rate < 0:
        raise ValueError("invalid economic parameters")
    if type(years) is not int or not 1 <= years <= 50 or type(paths) is not int or not 100 <= paths <= 200000:
        raise ValueError("years must be 1..50 and paths 100..200000")

def quantile(values: list[float], q: float) -> float:
    if not 0 < q < 1 or not values:
        raise ValueError("invalid quantile input")
    s = sorted(values)
    idx = (len(s) - 1) * q
    lo = int(idx)
    hi = min(lo + 1, len(s) - 1)
    return s[lo] + (s[hi] - s[lo]) * (idx - lo)

def simulate(*, notional: float = 1_000_000, volatility: float = .20,
             years: int = 5, paths: int = 10000, threshold: float = 0.,
             lgd: float = .6, hazard: float = .02, rate: float = .03,
             seed: int = 49) -> list[dict[str, float]]:
    validate(notional, volatility, years, paths, threshold, lgd, hazard, rate)
    if type(seed) is not int:
        raise ValueError("seed must be integer")
    rng = random.Random(seed)
    # Brownian MTM is a stylized zero-mean exposure proxy, NOT a priced derivative.
    mtm = [0.] * paths
    prev_survival = 1.
    rows = []
    for t in range(1, years + 1):
        for i in range(paths):
            mtm[i] += notional * volatility * rng.gauss(0., 1.)
        exposures = [max(x - threshold, 0.) for x in mtm]
        epe = sum(exposures) / paths
        survival = math.exp(-hazard * t)
        default_mass = prev_survival - survival
        incremental_cva = lgd * epe * default_mass * math.exp(-rate * t)
        rows.append({"year": t, "epe": epe, "pfe95": quantile(exposures, .95),
                     "default_mass": default_mass, "incremental_cva": incremental_cva})
        prev_survival = survival
    return rows

def main() -> None:
    parser = argparse.ArgumentParser(description="Synthetic exposure and CVA, educational only")
    parser.add_argument("--paths", type=int, default=10000)
    parser.add_argument("--seed", type=int, default=49)
    parser.add_argument("--threshold", type=float, default=0.)
    args = parser.parse_args()
    rows = simulate(paths=args.paths, seed=args.seed, threshold=args.threshold)
    print("year,epe,pfe95,default_mass,incremental_cva")
    for row in rows:
        print(f"{row['year']},{row['epe']:.2f},{row['pfe95']:.2f},{row['default_mass']:.8f},{row['incremental_cva']:.2f}")
    print(f"total_cva={sum(row['incremental_cva'] for row in rows):.2f}")

if __name__ == "__main__":
    main()
