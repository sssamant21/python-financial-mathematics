"""Beginner-friendly, reproducible Monte Carlo simulation of a two-stock portfolio.

Run:
    python -m pip install numpy matplotlib
    python quant_two_stock_monte_carlo.py

All stocks and assumptions are hypothetical. All portfolio values are in USD.
"""

from pathlib import Path
import csv

import matplotlib
matplotlib.use("Agg")  # Saves plots without requiring a GUI display.
import matplotlib.pyplot as plt
import numpy as np

# 1. Portfolio: buy 60 tech shares and 40 bank shares at $100 each.
INITIAL_TECH_PRICE = 100.0
INITIAL_BANK_PRICE = 100.0
TECH_SHARES = 60
BANK_SHARES = 40
INITIAL_PORTFOLIO = (TECH_SHARES * INITIAL_TECH_PRICE
                     + BANK_SHARES * INITIAL_BANK_PRICE)

# 2. GBM annual drifts, annual volatilities, and simulation settings.
TECH_DRIFT = 0.10
BANK_DRIFT = 0.06
TECH_VOL = 0.30
BANK_VOL = 0.18
TRADING_DAYS = 252
YEARS = 1.0
SIMULATIONS = 10_000
DT = YEARS / TRADING_DAYS
CORRELATIONS = (-0.20, 0.25, 0.90)
SEED = 42

# 3. Draw independent standard-normal shocks once. Use the SAME shocks
#    for each scenario so comparisons isolate changes in correlation.
rng = np.random.default_rng(SEED)
z_tech = rng.standard_normal((TRADING_DAYS, SIMULATIONS))
z_independent = rng.standard_normal((TRADING_DAYS, SIMULATIONS))


def gbm_paths(initial_price, drift, volatility, shocks):
    """Return (TRADING_DAYS+1, SIMULATIONS) simulated price paths."""
    daily_multipliers = np.exp(
        (drift - 0.5 * volatility**2) * DT
        + volatility * np.sqrt(DT) * shocks
    )
    return np.vstack((
        np.full(SIMULATIONS, initial_price),
        initial_price * np.cumprod(daily_multipliers, axis=0),
    ))


tech_prices = gbm_paths(INITIAL_TECH_PRICE, TECH_DRIFT, TECH_VOL, z_tech)

results = []
ending_distributions = {}
baseline_portfolio_paths = None

for rho in CORRELATIONS:
    # 4. Two shocks with desired correlation rho (exact in population).
    z_bank = rho * z_tech + np.sqrt(1.0 - rho**2) * z_independent
    bank_prices = gbm_paths(INITIAL_BANK_PRICE, BANK_DRIFT, BANK_VOL, z_bank)

    # Buy and hold: number of shares remains constant throughout the year.
    portfolio_paths = TECH_SHARES * tech_prices + BANK_SHARES * bank_prices
    ending_values = portfolio_paths[-1]
    percentile_5 = float(np.percentile(ending_values, 5))

    # Initial instantaneous annualized portfolio volatility. Because this
    # strategy is buy-and-hold, actual weights change during the simulation.
    initial_weight_tech = TECH_SHARES * INITIAL_TECH_PRICE / INITIAL_PORTFOLIO
    initial_weight_bank = BANK_SHARES * INITIAL_BANK_PRICE / INITIAL_PORTFOLIO
    initial_vol = np.sqrt(
        (initial_weight_tech * TECH_VOL)**2
        + (initial_weight_bank * BANK_VOL)**2
        + 2 * rho * initial_weight_tech * initial_weight_bank
        * TECH_VOL * BANK_VOL
    )

    results.append({
        "correlation": rho,
        "mean_ending_value": float(np.mean(ending_values)),
        "median_ending_value": float(np.median(ending_values)),
        "percentile_5": percentile_5,
        "percentile_95": float(np.percentile(ending_values, 95)),
        "probability_of_loss": float(np.mean(ending_values < INITIAL_PORTFOLIO)),
        "var_95": max(0.0, INITIAL_PORTFOLIO - percentile_5),
        "initial_annual_volatility": float(initial_vol),
    })
    ending_distributions[rho] = ending_values
    if rho == 0.25:
        baseline_portfolio_paths = portfolio_paths

# 5. Print clear results.
print("TWO-STOCK MONTE CARLO SIMULATION — 10,000 ONE-YEAR PATHS")
print(f"Initial portfolio: ${INITIAL_PORTFOLIO:,.2f}  "
      f"(Tech: ${TECH_SHARES * INITIAL_TECH_PRICE:,.0f}; "
      f"Bank: ${BANK_SHARES * INITIAL_BANK_PRICE:,.0f})")
print("Correlation | Mean end | Median end | 5th pct | 95th pct | "
      "P(loss) | 95% VaR | Initial vol")
for r in results:
    print(f"{r['correlation']:+.2f}        "
          f"${r['mean_ending_value']:>9,.2f}   "
          f"${r['median_ending_value']:>9,.2f}   "
          f"${r['percentile_5']:>8,.2f}   "
          f"${r['percentile_95']:>9,.2f}   "
          f"{r['probability_of_loss']:>6.2%}   "
          f"${r['var_95']:>8,.2f}   "
          f"{r['initial_annual_volatility']:>6.2%}")

# 6. Save summary and charts to the same directory as this script.
output_dir = Path(__file__).resolve().parent
with (output_dir / "two_stock_monte_carlo_results.csv").open(
    "w", newline="", encoding="utf-8"
) as f:
    writer = csv.DictWriter(f, fieldnames=list(results[0].keys()))
    writer.writeheader()
    writer.writerows(results)

fig, ax = plt.subplots(figsize=(11, 6))
for i in range(30):
    ax.plot(baseline_portfolio_paths[:, i], alpha=0.35, linewidth=0.8)
ax.plot(baseline_portfolio_paths.mean(axis=1),
        linewidth=3, label="Mean portfolio value (10,000 paths)")
ax.axhline(INITIAL_PORTFOLIO, linestyle="--", label="Starting value ($10,000)")
ax.set(title="Two-stock buy-and-hold portfolio: 30 sample paths (rho=0.25)",
       xlabel="Trading day", ylabel="Portfolio value ($)")
ax.legend()
ax.grid(alpha=0.2)
fig.tight_layout()
fig.savefig(output_dir / "two_stock_portfolio_paths.png", dpi=150)
plt.close(fig)

fig, ax = plt.subplots(figsize=(11, 6))
for rho in CORRELATIONS:
    ax.hist(ending_distributions[rho], bins=65, density=True,
            alpha=0.3, label=f"Correlation {rho:+.2f}")
ax.axvline(INITIAL_PORTFOLIO, linestyle="--", label="Starting value ($10,000)")
ax.set(title="One-year ending portfolio values: correlation scenarios",
       xlabel="Ending portfolio value ($)", ylabel="Probability density")
ax.legend()
ax.grid(alpha=0.2)
fig.tight_layout()
fig.savefig(output_dir / "two_stock_correlation_distributions.png", dpi=150)
plt.close(fig)

print("\nFiles written:")
for filename in ("two_stock_monte_carlo_results.csv",
                 "two_stock_portfolio_paths.png",
                 "two_stock_correlation_distributions.png"):
    print(f"  {output_dir / filename}")