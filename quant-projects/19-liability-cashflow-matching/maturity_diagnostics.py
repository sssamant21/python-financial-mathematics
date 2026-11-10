"""Synthetic fixed-holdings maturity and discount sensitivity diagnostics."""
from math import isfinite
from cashflow_matching import present_value, coverage_by_year


def duration(flows, rate):
    """Macaulay duration in years for annual nonnegative end-of-year flows."""
    pv = present_value(flows, rate)
    if pv <= 0 or not isfinite(pv):
        raise ValueError("cash flows must have positive finite present value")
    weighted = sum(year * amount / (1 + rate) ** year for year, amount in flows.items())
    return weighted / pv


def diagnostics(assets, liabilities, rates=(0.02, 0.04, 0.06)):
    """Fixed promised flows; no reinvestment, re-optimization or trading."""
    if not rates:
        raise ValueError("rates must not be empty")
    balances = coverage_by_year(assets, liabilities)
    rows = []
    for rate in rates:
        asset_pv = present_value(assets, rate)
        liability_pv = present_value(liabilities, rate)
        asset_duration = duration(assets, rate)
        liability_duration = duration(liabilities, rate)
        rows.append({
            "rate": rate,
            "asset_pv": asset_pv,
            "liability_pv": liability_pv,
            "pv_gap": asset_pv - liability_pv,
            "asset_duration": asset_duration,
            "liability_duration": liability_duration,
            "duration_gap_years": asset_duration - liability_duration,
            "gap_rate_derivative": (-asset_pv * asset_duration + liability_pv * liability_duration) / (1 + rate),
        })
    return {"coverage": balances, "minimum_cumulative_balance": min(b for _, b in balances), "rates": rows}


if __name__ == "__main__":
    assets = {1: 80., 2: 120.}
    liabilities = {1: 100., 2: 100.}
    for row in diagnostics(assets, liabilities)["rates"]:
        print(row)
