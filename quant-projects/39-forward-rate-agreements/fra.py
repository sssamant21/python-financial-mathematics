"""Educational single-period FRA valuation from hypothetical discount factors.

No curve bootstrap, collateral model, credit risk, market quotes or trading.
Rates are simple annualized ACT/365-style fractions supplied by the caller.
"""
from __future__ import annotations
import argparse
import math


def _positive_finite(value: float, label: str) -> float:
    if not math.isfinite(value) or value <= 0:
        raise ValueError(f"{label} must be finite and positive")
    return value


def forward_rate(df_start: float, df_end: float, accrual: float) -> float:
    """Simple forward rate implied by discount factors at t1 and t2."""
    a = _positive_finite(accrual, "accrual")
    start = _positive_finite(df_start, "df_start")
    end = _positive_finite(df_end, "df_end")
    return (start / end - 1.0) / a


def fra_value(
    notional: float,
    strike: float,
    df_start: float,
    df_end: float,
    accrual: float,
    *,
    receive_float: bool = True,
) -> dict[str, float]:
    """Return start-date settlement and present value for a receive-floating FRA.

    Settlement at t1 uses the forward rate as the period's hypothetical fixing.
    The t1 settlement is discounted by df_start to obtain time-zero PV.
    """
    n = _positive_finite(notional, "notional")
    if not math.isfinite(strike):
        raise ValueError("strike must be finite")
    fwd = forward_rate(df_start, df_end, accrual)
    denominator = 1.0 + fwd * accrual
    if denominator <= 0 or not math.isfinite(denominator):
        raise ValueError("invalid FRA settlement discount denominator")
    direction = 1.0 if receive_float else -1.0
    settlement = direction * n * accrual * (fwd - strike) / denominator
    pv = settlement * df_start
    return {"forward": fwd, "settlement_t1": settlement, "pv_t0": pv}


def main() -> None:
    parser = argparse.ArgumentParser(description="Hypothetical FRA forward and PV")
    parser.add_argument("--notional", type=float, default=1_000_000)
    parser.add_argument("--strike", type=float, default=0.04)
    parser.add_argument("--df-start", type=float, default=0.98)
    parser.add_argument("--df-end", type=float, default=0.96)
    parser.add_argument("--accrual", type=float, default=0.5)
    parser.add_argument("--pay-floating", action="store_true")
    args = parser.parse_args()
    result = fra_value(args.notional, args.strike, args.df_start,
                       args.df_end, args.accrual, receive_float=not args.pay_floating)
    for key, value in result.items():
        print(f"{key}: {value:.8f}")


if __name__ == "__main__":
    main()
