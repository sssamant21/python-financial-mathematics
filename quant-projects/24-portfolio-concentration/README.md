# Project 24 — Portfolio Concentration and Diversification Diagnostics

**Business question:** A portfolio may contain many assets but still be dominated by one position. How can we quantify concentration, measure post-return weight drift, and estimate the turnover required to restore target weights?

This Python 3.11+ **synthetic-only educational lab** uses the standard library; it does not download prices, connect to brokers, or recommend allocations.

## Mathematics

For long-only, fully invested weights `w_i >= 0` with `sum(w_i) = 1` and `N >= 2`:

- **Herfindahl–Hirschman index (HHI):** `sum(w_i ** 2)`; minimum `1/N` at equal weights, maximum 1 at a single position.
- **Effective number of holdings:** `1 / HHI`. It measures weight concentration, **not** the number of statistically independent risks.
- **Shannon entropy:** `-sum(w_i * log(w_i))` over strictly positive weights, treating `0 log 0 = 0`.
- **Normalized entropy:** entropy divided by `log(N)`, between 0 and 1.
- **Post-return drift:** `w'_i = w_i (1+r_i) / sum_j w_j(1+r_j)`, using contemporaneous realized simple returns.
- **One-way rebalance turnover:** `0.5 * sum(abs(w'_i - w_i))` for equal-valued fully invested portfolios; excludes fees, slippage, cash flows, and execution constraints.

HHI and entropy describe **capital-weight concentration**, not covariance diversification, tail-risk independence, or expected investment performance. The drift and turnover exercise is an **ex-post accounting illustration**, not a predictive backtest.

## Reproduce

From the repository root:

```bash
cd quant-projects/24-portfolio-concentration
python -m unittest -v test_concentration.py
python -m compileall -q concentration.py test_concentration.py
python concentration.py
```

No third-party packages or market data are needed.

## Worked synthetic scenario

Start with four equal 25% positions and apply hypothetical returns of +20%, -10%, +5%, and 0%. Observe the change in HHI and effective count, then calculate the turnover to restore equal weights. Try a 70/10/10/10 allocation and compare its concentration to equal weighting.

## Guardrails and limitations

Reject fewer than two assets, negative/nonfinite/boolean weights, sums outside absolute tolerance 1e-9, mismatched vector lengths, nonfinite or below -100% simple returns, and fully depleted portfolio wealth. Asset order must match between weight and return vectors. There is no shorting, leverage, external cash flow, fee model, point-in-time constituent history, or data-vendor provenance. Future returns must never be used to select historical target weights.

## Validation evidence

Eleven deterministic `unittest` cases, Python compilation and the CLI demonstration **passed in a local standalone source-equivalent run on 2026-11-11**. Exact published-revision GitHub Actions CI and independent model review remain **unverified**. No historical market validation or production certification is claimed.
