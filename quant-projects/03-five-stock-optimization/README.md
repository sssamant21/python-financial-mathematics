# Quant Finance Lab 03 — Five-stock portfolio optimization and Monte Carlo

An educational, reproducible Python lab for quantitative finance beginners.
This uses **hypothetical assets and assumptions**, not market data or financial advice.

## Learning objectives

1. Understand why cross-asset **correlations** matter for diversification.
2. Build an annualized **covariance matrix** using volatilities and correlations.
3. Optimize long-only allocations for minimum volatility, maximum Sharpe, and maximum return subject to a volatility ceiling.
4. Simulate 10,000 correlated one-year **GBM endpoints** and compare portfolio-level Value at Risk (VaR) and Conditional VaR (CVaR).
5. Understand why modeled annualized volatility and 95% one-year VaR are different risk metrics.

## Run

```powershell
python -m pip install -r requirements.txt
python five_stock_quant_lab.py
```

The main script places all generated reports and images alongside itself.

## Scenario

- Initial wealth: **$100,000**, one-year buy-and-hold.
- Five illustrative industry assets: Technology, Healthcare, Banking, Consumer, Utilities.
- One-year expected simple returns: 12.0%, 9.0%, 8.5%, 7.5%, 6.0%.
- Annual log-return shock volatilities: 30%, 20%, 25%, 16%, 13%.
- Illustrative simple risk-free return: 3%.
- Portfolio weights sum to 100%; no short sales; no asset exceeds 40% at inception.
- The risk-capped optimizer limits **initial annualized portfolio volatility** to 16% (it does not cap VaR at 16%).
- Reproducible random seed: 42; 10,000 Monte Carlo outcomes. All strategies share the same market scenarios.

## Techniques

### Covariance

`covariance[i,j] = volatility[i] * volatility[j] * correlation[i,j]`.

Portfolio volatility is `sqrt(weights.T @ covariance @ weights)`.

### Optimization

- Minimum variance: minimize `weights.T @ covariance @ weights`.
- Maximum Sharpe: maximize `(expected_return - risk_free_rate) / annualized_volatility`.
- Highest return under the risk cap: maximize expected return subject to volatility <=16%.
- Every optimizer enforces `sum(weights) = 1`, `0 <= weights[i] <= 0.40`.
- The efficient frontier uses constrained minimum-variance solutions at 42 expected-return targets.

### Monte Carlo

Generate jointly normal shocks with the Cholesky factor of the correlation matrix, then simulate GBM gross returns over one year:

`gross_return[i] = exp(log(1 + expected_simple_return[i]) - 0.5 * sigma[i]**2 + sigma[i] * correlated_normal[i])`.

The drift mapping ensures the **model's mathematical expected one-year simple return** for each asset equals the stated assumption. One-year endpoint sampling is equivalent to accumulating daily GBM increments for constant parameters.

Portfolio terminal value = `100000 * (gross_asset_returns @ initial_weights)` because the initial holdings remain unchanged. All portfolios use identical market shocks for comparability.

- VaR 95%: 95th percentile of modeled dollar loss (`starting_wealth - terminal_wealth`).
- CVaR 95%: average modeled dollar loss in worst 5% of scenarios.
- Loss probability: fraction of terminal values below initial wealth.

## Files

| File | Purpose |
|---|---|
| `five_stock_quant_lab.py` | Complete reproducible source |
| `portfolio_risk_report.csv` | Model risk and Monte Carlo results by strategy |
| `portfolio_weights.csv` | Optimized initial percentage allocations |
| `correlation_matrix.csv` | Assumed asset-shock correlations |
| `covariance_matrix.csv` | Derived annual covariance matrix |
| `correlation_matrix.png` | Correlation heatmap |
| `portfolio_allocations.png` | Stacked strategy allocations |
| `efficient_frontier.png` | Risk-return curve, optimizers, 16% volatility limit |
| `ending_value_distributions.png` | Distribution of simulated terminal wealth |

## Observed reference outputs (seed 42)

| Strategy | Expected return | Initial annual vol | Sharpe | Monte Carlo VaR 95% | Probability of loss |
|---|---:|---:|---:|---:|---:|
| Equal weight | 8.60% | 14.62% | 0.383 | $15,606 | 31.5% |
| Minimum volatility | 7.47% | 12.19% | 0.366 | $12,730 | 30.5% |
| Maximum Sharpe | 8.53% | 13.80% | 0.401 | $14,460 | 31.2% |
| Max return at 16% risk | 9.29% | 16.00% | 0.393 | $17,174 | 32.8% |

## Suggested exercises

1. Lower the concentration cap from 40% to 30%; run again and compare outputs.
2. Increase pairwise correlations by a modest amount, while maintaining a positive-definite matrix. Does the minimum-variance portfolio change?
3. Change the risk cap from 16% to 14%; measure how the constrained expected return changes.
4. Increase the scenario count from 10,000 to 100,000 to reduce Monte Carlo sampling noise.
5. Add transaction costs, dividends, periodic rebalancing, or estimation uncertainty as separate enhancements.

## Model limitations

The covariance-based risk model measures *initial instantaneous annualized volatility*. Monte Carlo VaR/CVaR are measured on the **one-year distribution of terminal wealth**, so they need not map linearly to annualized volatility. A GBM model assumes constant volatility, fixed correlations and lognormal stock price changes. It omits fat tails, volatility clustering, correlation spikes, liquidity risk, taxes, fees, and dividends. Historical parameter estimation errors can dominate the optimization benefits. Portfolio weights drift over time in the buy-and-hold Monte Carlo model.

This lab is educational and is not an investment forecast or recommendation.