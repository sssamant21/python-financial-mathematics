"""Educational deterministic cash-flow matching; no trading or market data."""
from math import isfinite


def _amount(value, name):
    if isinstance(value, bool) or not isinstance(value, (int, float)) or not isfinite(value) or value < 0:
        raise ValueError(f"{name} must be finite and nonnegative")
    return float(value)


def present_value(flows, annual_rate):
    """flows: mapping of positive integer year -> nonnegative cash amount."""
    rate = _amount(annual_rate, "annual_rate")
    if not flows:
        raise ValueError("cash flows must not be empty")
    result = 0.0
    for year, amount in flows.items():
        if isinstance(year, bool) or not isinstance(year, int) or year < 1 or year > 100:
            raise ValueError("years must be integers from 1 to 100")
        result += _amount(amount, "cash flow") / (1 + rate) ** year
    return result


def funding_gap(assets, liabilities, annual_rate):
    """Positive means discounted assets exceed discounted liabilities."""
    return present_value(assets, annual_rate) - present_value(liabilities, annual_rate)


def coverage_by_year(assets, liabilities):
    """Cumulative undiscounted cash-flow coverage; no borrowing or reinvestment."""
    if not assets or not liabilities:
        raise ValueError("assets and liabilities must not be empty")
    # Reuse input validation before aggregating.
    present_value(assets, 0)
    present_value(liabilities, 0)
    balance = 0.0
    rows = []
    for year in sorted(set(assets) | set(liabilities)):
        balance += assets.get(year, 0) - liabilities.get(year, 0)
        rows.append((year, balance))
    return rows


def stress(assets, liabilities, rates=(0.02, 0.04, 0.06)):
    if not rates:
        raise ValueError("rates must not be empty")
    return [(rate, funding_gap(assets, liabilities, rate)) for rate in rates]


if __name__ == "__main__":
    assets = {1: 600.0, 2: 600.0, 3: 600.0}
    liabilities = {1: 500.0, 2: 650.0, 3: 550.0}
    print("Year-end cumulative cash balances:", coverage_by_year(assets, liabilities))
    print("Discount-rate sensitivity:", stress(assets, liabilities))
