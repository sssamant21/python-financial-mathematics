# Project 08 — Portfolio Risk Attribution and Component VaR

**Audience:** Beginner quantitative researchers and portfolio-risk analysts. **Data:** Fully synthetic. **Status:** Educational implementation; not production certified.

## Why this matters

Total portfolio volatility alone does not show which assets drive risk. Euler attribution decomposes a differentiable, positively homogeneous portfolio risk measure into components whose sum equals the portfolio total. A position can have a *negative* component contribution when it hedges other positions.

Let weights be \(w\), annualized covariance \(\Sigma\), and portfolio volatility \(\sigma_p=\sqrt{w^T\Sigma w}\). The marginal volatility contribution is \((\Sigma w)_i/\sigma_p\), and component contribution is \(w_i(\Sigma w)_i/\sigma_p\). Summing components gives \(\sigma_p\). Under a **zero-mean multivariate normal** assumption, the 95% loss VaR attribution is \(z_{0.95}\) times these components. For multiple iid periods, the optional square-root-horizon scaling is an approximation, **not** valid for autocorrelated or regime-switching returns.

## Quick start

From the repository root (Python 3.10+):

```bash
python -m pip install -r quant-projects/requirements.txt
cd quant-projects/08-risk-attribution
python risk_attribution.py
python -m pytest -q test_risk_attribution.py
```

The demonstration uses three hypothetical sectors, annualized volatilities 20%, 15%, and 10%, and a valid synthetic correlation matrix. Expected: printed portfolio volatility, three component contributions, and their sum; the sum must equal portfolio volatility within floating-point precision. No external market data or network access is needed.

## Lab (45–60 minutes)

1. Read `contributions()` and verify the identity \(\sum_i w_i(\Sigma w)_i/\sigma_p=\sigma_p\).
2. Run the demo and explain why component *percentage* risk differs from capital weight.
3. Change the technology weight, renormalize weights to sum to one, and observe how contributions change.
4. Replace correlations with an identity matrix; compare the resulting portfolio risk.
5. Construct a positive-semidefinite negatively correlated covariance matrix and explain negative hedge contribution.
6. Compare `normal_var_contributions(..., horizon=1)` and `horizon=4`; state the iid assumption and why Project 07's dependent bootstrap is more suitable under serial dependence.
7. Run the ten tests and record the exact Python, NumPy, pytest versions and commit SHA.

## Safety and model limitations

This project attributes *covariance-based volatility* and zero-mean **parametric** normal VaR. It does **not** estimate historical VaR/CVaR contributions, account for expected return, non-normal tails, estimation error, liquidity, turnover, short-sale restrictions, dynamic correlations, or point-in-time constituent selection. Annualized covariance must match the horizon of the weights and output; the example's horizon argument is a count of iid covariance periods, not automatically a week. Weight sums are checked but leverage/short positions are not prohibited. The covariance matrix is checked for symmetry and positive semidefiniteness; singular or zero-risk portfolios are rejected when portfolio volatility is zero. Do not apply this code to investment decisions or live trading.

## Validation evidence

A local isolated Python prototype with NumPy and pytest completed **10/10 tests** on 2026-11-08. The published implementation must still be checked against its exact GitHub revision; CI, independent review, and licensed historical-data acceptance remain pending until separately verified.

## Extension — covariance estimation stability and gradient cross-check

Run from this project directory:

```bash
python stability.py
python -m pytest -q test_risk_attribution.py test_stability.py
```

The synthetic example generates 120 monthly three-asset observations with a seeded common factor. It estimates a sample covariance matrix, explicitly multiplies by 12 for **annualized covariance**, and compares fixed diagonal-shrinkage intensities 0, 0.5, and 1.0. The choice of shrinkage is a sensitivity scenario, **not** a statistically optimized estimator. For each case, the program checks the analytical Euler marginal-volatility gradient against a central finite difference. The finite-difference perturbations deliberately do **not** renormalize weights: Euler's derivative is an unconstrained gradient in weight space; a self-financing trade gradient would be a different quantity. Shrinkage to the diagonal may reduce unstable off-diagonal estimates but can erase genuine diversification/hedging effects. Never select a parameter using future realized outcomes. A point-in-time rolling training window and out-of-sample forecast comparison are needed before empirical stability claims.

**Validation boundary:** 13 closely related local prototype tests passed in an isolated Python environment; the two published extension files were adapted for integration with `risk_attribution.py`, so **exact published-revision tests and CI are not yet confirmed**. The prototype used synthetic observations only; no historical market-data acceptance or independent review was performed.

Previous: [Project 07](../07-multi-horizon-risk/README.md). Index: [Quant projects](../README.md).

## Extension — out-of-sample covariance forecasting (2026-11-09)

From this folder run `python oos_covariance.py` and `python -m pytest -q test_oos_covariance.py`. The seeded 260-observation, three-asset example compares fixed diagonal-shrinkage scenarios (0, 0.5, 1) on non-overlapping four-observation test windows. At each forecast origin t, the sample covariance uses only the preceding 52 observations, while realized squared portfolio returns use t through t+3. The squared-error score compares a **per-period conditional variance forecast** with the **forward mean squared return**, a noisy realized proxy that also includes squared drift. It is not a volatility forecast calibrated to a single four-period aggregate return. The reported MSE values are descriptive, not evidence of a statistically superior estimator; never choose the shrinkage intensity using these same out-of-sample scores and then report unbiased performance. Use an additional holdout or nested training-only selection for that purpose.

Run the full suite with `python -m pytest -q test_risk_attribution.py test_stability.py test_oos_covariance.py`. The new 11 tests passed locally on an isolated implementation before publication; exact published-revision CI and independent review must be verified separately. No licensed market data is bundled; fixed synthetic constituents avoid claiming historical survivorship-bias controls.
