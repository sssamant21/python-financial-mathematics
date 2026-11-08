"""Walk-forward circular-block bootstrap risk, using training observations only.

Run alongside multi_horizon.py; educational research, not a risk certification.
"""
import argparse
from pathlib import Path

import numpy as np
import pandas as pd

from dependent_bootstrap import bootstrap_horizon_losses, bootstrap_var_cvar
from multi_horizon import horizon_risk, portfolio_returns, synthetic_prices


def score_bootstrap(weekly, horizon=4, lookback=104, block_length=4,
                    draws=2000, seed=2026, alpha=0.05):
    """Return horizon-aligned bootstrap forecasts and non-overlapping outcomes.

    The t-th forecast trains on weekly returns [t-lookback, t), and scores
    [t, t+horizon). Seeds are deterministic but vary by forecast origin.
    """
    baseline = horizon_risk(weekly, horizon=horizon, lookback=lookback, alpha=alpha)
    if type(block_length) is not int or block_length < 1 or block_length > lookback:
        raise ValueError("block_length must be between 1 and lookback")
    if type(draws) is not int or not 100 <= draws <= 100000:
        raise ValueError("draws must be between 100 and 100000")
    if type(seed) is not int or not 0 <= seed < 2**64:
        raise ValueError("seed must be a nonnegative integer below 2**64")
    if not np.isfinite(alpha) or not 0 < alpha < 0.5:
        raise ValueError("alpha must be in (0, 0.5)")
    returns = pd.to_numeric(weekly["Return"], errors="raise").to_numpy(dtype=float)
    rows = []
    for i, t in enumerate(range(lookback, len(returns)-horizon+1, horizon)):
        # SeedSequence avoids arithmetic overflow when seeds approach 2**64.
        origin_seed = int(np.random.SeedSequence([seed & 0xffffffff,
            seed >> 32, i]).generate_state(1, dtype=np.uint64)[0])
        simulated = bootstrap_horizon_losses(
            returns[t-lookback:t], horizon=horizon,
            block_length=block_length, draws=draws, seed=origin_seed)
        var, cvar = bootstrap_var_cvar(simulated, alpha=alpha)
        rows.append((var, cvar))
    if len(rows) != len(baseline):
        raise AssertionError("Forecast origins and baseline scoring do not align")
    result = baseline.copy()
    result["BootstrapVaR95"] = [x[0] for x in rows]
    result["BootstrapCVaR95"] = [x[1] for x in rows]
    result["BootstrapBreach"] = (
        result["RealizedLoss"] > result["BootstrapVaR95"]).astype(int)
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--prices", type=Path, help="Licensed weekly price CSV")
    parser.add_argument("--output", type=Path, default=Path(__file__).parent / "reports-bootstrap")
    parser.add_argument("--lookback", type=int, default=104)
    parser.add_argument("--horizons", type=int, nargs="+", default=[1, 4, 13])
    parser.add_argument("--block-length", type=int, default=4)
    parser.add_argument("--draws", type=int, default=2000)
    parser.add_argument("--seed", type=int, default=2026)
    args = parser.parse_args()
    if len(set(args.horizons)) != len(args.horizons):
        parser.error("Horizons must be distinct")
    prices = pd.read_csv(args.prices) if args.prices else synthetic_prices()
    weekly = portfolio_returns(prices)
    # Compute all results before writing anything; avoid partial reports on failure.
    results = {h: score_bootstrap(
        weekly, horizon=h, lookback=args.lookback,
        block_length=args.block_length, draws=args.draws, seed=args.seed)
        for h in args.horizons}
    args.output.mkdir(parents=True, exist_ok=True)
    summaries = []
    for h, scored in results.items():
        scored.to_csv(args.output / f"horizon_{h}_bootstrap.csv", index=False)
        summaries.append({"horizon_weeks": h, "scored_periods": len(scored),
            "bootstrap_breaches": int(scored.BootstrapBreach.sum()),
            "bootstrap_breach_rate": float(scored.BootstrapBreach.mean()),
            "mean_bootstrap_var": float(scored.BootstrapVaR95.mean()),
            "mean_bootstrap_cvar": float(scored.BootstrapCVaR95.mean())})
    pd.DataFrame(summaries).to_csv(args.output / "summary.csv", index=False)
    print(pd.DataFrame(summaries).to_string(index=False))
    print("Synthetic by default. Bootstrap draws are not independent market observations.")


if __name__ == "__main__":
    main()
