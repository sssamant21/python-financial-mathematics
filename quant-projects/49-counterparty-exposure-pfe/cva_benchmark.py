"""Closed-form expected CVA under independent default and Brownian exposure.

Synthetic educational model, not a pricing or regulatory engine.
"""
import math
from diagnostics import brownian_epe
from exposure import simulate, validate


def analytical_cva(*, notional=1_000_000., volatility=.2, years=5,
                   threshold=0., lgd=.6, hazard=.02, rate=.03):
    """Year-end default-mass approximation, matching exposure.simulate."""
    validate(notional, volatility, years, 100, threshold, lgd, hazard, rate)
    rows = []
    previous_survival = 1.
    for year in range(1, years + 1):
        survival = math.exp(-hazard * year)
        mass = previous_survival - survival
        epe = brownian_epe(notional=notional, volatility=volatility,
                           year=year, threshold=threshold)
        increment = lgd * mass * math.exp(-rate * year) * epe
        rows.append({"year": year, "epe": epe, "default_mass": mass,
                     "incremental_cva": increment})
        previous_survival = survival
    return rows


def compare_cva(*, paths=2000, seed=49, **economics):
    """Matched-convention Monte Carlo versus analytical CVA; no CI coverage claim."""
    simulated = simulate(paths=paths, seed=seed, **economics)
    benchmark = analytical_cva(**economics)
    mc = math.fsum(row["incremental_cva"] for row in simulated)
    exact = math.fsum(row["incremental_cva"] for row in benchmark)
    return {"simulated_cva": mc, "analytical_cva": exact,
            "absolute_error": abs(mc-exact)}


if __name__ == "__main__":
    print(compare_cva())
