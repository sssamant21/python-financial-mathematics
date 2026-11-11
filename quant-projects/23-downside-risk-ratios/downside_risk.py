"""Project 23: descriptive downside-risk ratios, synthetic observations only."""
from __future__ import annotations

import math
from statistics import mean


def _validate(returns, target):
    if isinstance(returns, (str, bytes)):
        raise ValueError("returns must be a sequence of numeric simple returns")
    try:
        values = list(returns)
    except TypeError as exc:
        raise ValueError("returns must be iterable") from exc
    if len(values) < 3:
        raise ValueError("at least three aligned observations are required")
    for value in values:
        if isinstance(value, bool) or not isinstance(value, (int, float)):
            raise ValueError("returns must be numeric, not boolean")
        if not math.isfinite(value) or value < -1:
            raise ValueError("returns must be finite simple returns >= -1")
    if isinstance(target, bool) or not isinstance(target, (int, float)):
        raise ValueError("target must be numeric, not boolean")
    if not math.isfinite(target) or target <= -1:
        raise ValueError("target must be finite and greater than -1")
    return [float(v) for v in values]


def downside_metrics(returns, target=0.0, periods_per_year=12):
    """Population downside deviation and arithmetic Sortino/Omega at a period target.

    None denotes undefined ratios when downside shortfall is zero.
    No forward prediction, compounded annualization, or statistical significance.
    """
    values = _validate(returns, target)
    if isinstance(periods_per_year, bool) or not isinstance(periods_per_year, int):
        raise ValueError("periods_per_year must be an integer")
    if not 1 <= periods_per_year <= 366:
        raise ValueError("periods_per_year must be between 1 and 366")
    differences = [r - target for r in values]
    losses = [max(-d, 0.0) for d in differences]
    gains = [max(d, 0.0) for d in differences]
    downside = math.sqrt(math.fsum(x * x for x in losses) / len(values))
    loss_sum = math.fsum(losses)
    gain_sum = math.fsum(gains)
    excess = mean(differences)
    return {
        "observations": len(values),
        "target_per_period": float(target),
        "mean_excess_per_period": excess,
        "downside_deviation_per_period": downside,
        "annualized_downside_deviation": downside * math.sqrt(periods_per_year),
        "annualized_arithmetic_excess": excess * periods_per_year,
        "sortino": (excess * math.sqrt(periods_per_year) / downside) if downside > 0 else None,
        "omega": gain_sum / loss_sum if loss_sum > 0 else None,
        "shortfall_fraction": sum(x > 0 for x in losses) / len(values),
    }


def trailing_metrics(returns, window, target=0.0, periods_per_year=12):
    """End-of-window descriptive metrics; no observations after each window end."""
    values = _validate(returns, target)
    if isinstance(window, bool) or not isinstance(window, int) or not 3 <= window <= len(values):
        raise ValueError("window must be an integer between 3 and sample length")
    return [
        {"end_index": end - 1, **downside_metrics(values[end - window:end], target, periods_per_year)}
        for end in range(window, len(values) + 1)
    ]


if __name__ == "__main__":
    invented_monthly_returns = [0.02, -0.03, 0.01, 0.04, -0.02, 0.00, 0.03, -0.01]
    print("Synthetic monthly downside metrics:", downside_metrics(invented_monthly_returns))
    print("Trailing four-month windows:", len(trailing_metrics(invented_monthly_returns, 4)))
