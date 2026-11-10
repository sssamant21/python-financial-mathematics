"""Bounded integer-lot cash-flow matching, for education only."""
from itertools import product
from math import isfinite
from cashflow_matching import coverage_by_year, present_value


def _nonnegative(value, label):
    if isinstance(value, bool) or not isinstance(value, (int, float)) or not isfinite(value) or value < 0:
        raise ValueError(f"{label} must be finite and nonnegative")
    return float(value)


def solve(liabilities, candidates, budget, annual_rate=0.04, max_combinations=100000):
    """Enumerate integer lots, minimizing cost subject to cumulative coverage.

    candidates: (name, cost_per_lot, {year: cashflow_per_lot}, max_lots).
    No borrowing, reinvestment income, fractional lots or post-purchase trading.
    """
    present_value(liabilities, annual_rate)
    budget = _nonnegative(budget, "budget")
    if not candidates:
        raise ValueError("at least one candidate required")
    if isinstance(max_combinations, bool) or not isinstance(max_combinations, int) or max_combinations < 1:
        raise ValueError("max_combinations must be a positive integer")
    names, costs, flows, limits = [], [], [], []
    combinations = 1
    for name, cost, schedule, limit in candidates:
        if not isinstance(name, str) or not name.strip() or name in names:
            raise ValueError("candidate names must be unique nonempty strings")
        names.append(name)
        costs.append(_nonnegative(cost, "cost"))
        present_value(schedule, annual_rate)
        flows.append(schedule)
        if isinstance(limit, bool) or not isinstance(limit, int) or not 0 <= limit <= 1000:
            raise ValueError("max_lots must be an integer between 0 and 1000")
        limits.append(limit)
        combinations *= limit + 1
        if combinations > max_combinations:
            raise ValueError("search space exceeds max_combinations")
    best = None
    closest = None
    for lots in product(*(range(n + 1) for n in limits)):
        cost = sum(n * c for n, c in zip(lots, costs))
        if cost > budget + 1e-9:
            continue
        assets = {}
        for count, schedule in zip(lots, flows):
            for year, amount in schedule.items():
                assets[year] = assets.get(year, 0.0) + count * amount
        if not assets:
            assets = {1: 0.0}
        balances = coverage_by_year(assets, liabilities)
        shortfall = max(0.0, -min(balance for _, balance in balances))
        trial = (shortfall, cost, lots)
        if closest is None or trial < closest:
            closest = trial
        if shortfall <= 1e-9 and (best is None or (cost, lots) < (best[0], best[1])):
            best = (cost, lots, assets, balances)
    if best is None:
        return {"feasible": False, "budget": budget, "minimum_max_cumulative_shortfall": None if closest is None else closest[0], "best_effort_lots": None if closest is None else dict(zip(names, closest[2])), "combinations_checked": combinations}
    cost, lots, assets, balances = best
    return {"feasible": True, "cost": cost, "lots": dict(zip(names, lots)), "cashflows": assets, "coverage": balances, "pv_gap": present_value(assets, annual_rate) - present_value(liabilities, annual_rate), "combinations_checked": combinations}


def rate_stress(liabilities, candidates, solution, rates=(0.02, 0.04, 0.06)):
    """Revalue fixed promised flows, without re-optimizing under stress."""
    if not solution["feasible"]:
        raise ValueError("cannot stress an infeasible solution")
    if not rates:
        raise ValueError("rates required")
    return [(rate, present_value(solution["cashflows"], rate) - present_value(liabilities, rate)) for rate in rates]


if __name__ == "__main__":
    obligations = {1: 100.0, 2: 100.0}
    bonds = [("short", 95.0, {1: 100.0}, 2), ("long", 90.0, {2: 100.0}, 2)]
    result = solve(obligations, bonds, 400.0)
    print(result)
    print("Fixed-holdings PV stress:", rate_stress(obligations, bonds, result))
