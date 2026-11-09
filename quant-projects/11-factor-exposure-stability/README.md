# Project 11 — Rolling Factor Exposures and Regime Stability

**Business question:** Is a portfolio's exposure to market, size, or value-style return drivers stable, or does its sensitivity change across market regimes?

## Mathematical idea

Model a portfolio's period return as `r[t] = alpha + beta[1]*f[1,t] + ... + beta[k]*f[k,t] + error[t]`. Ordinary least squares estimates intercept and factor loadings using **only completed training observations**. A ridge option minimizes squared training residuals plus `lambda * sum(beta[j]^2)`; the intercept is not penalized. The factor return columns here are **fictional** and are not claimed to be Fama–French or investable indices.

At origin `t`, fit on `[t-window,t)`, predict using held-out factors `[t,t+horizon)`, and score held-out mean squared error. Origins advance by the horizon so evaluation periods do not overlap. Using realized factor values to score the decomposition is **ex-post explanatory attribution**, not a tradable return forecast known at origin `t`. The fitted coefficients themselves never use the held-out portfolio returns or factors.

## Reproduce

Python 3.11+; use the repository's shared requirements (NumPy and pytest). From the repository root:

```bash
python -m pip install -r quant-projects/requirements.txt
cd quant-projects/11-factor-exposure-stability
python factor_lab.py --seed 20261109 --window 80 --horizon 20
python -m pytest -q test_factor_lab.py
```

The deterministic synthetic example has three hypothetical factor series, an exposure shift halfway through the sample, and independent noise. Outputs are JSON with training-estimated betas, held-out errors, and origin indices.

## Safety, interpretation, and evidence

- Validate finite aligned observations, at least five training observations beyond the factor count, and full held-out windows; reject singular ordinary-least-squares training designs (positive ridge can regularize them).
- A factor regression does not establish causality, identify a hedge, or provide a reliable alpha estimate. Factor collinearity, omitted exposures, structural breaks, errors-in-variables, and unstable coefficients can invalidate conclusions.
- This introductory exercise **does not yet estimate coefficient confidence intervals**, select a ridge parameter, or demonstrate a live market regime. Those are follow-up validation milestones.
- If studying actual factor returns, obtain authorized point-in-time observations, record provider, retrieval date, universe, publication lags, revisions and adjustment policy; do not commit licensed third-party data.
- No live trading, broker integration, investment advice, historical performance claims, independent certification, or production readiness.

**Validation checkpoint (2026-11-09):** local Python compilation, seeded CLI smoke test, and **9/9 pytest cases passed** against the authored source. Published-revision GitHub Actions and independent review remain unverified until confirmed.

**Next:** exact-revision CI, rolling beta drift diagnostics, coefficient uncertainty, ridge sensitivity, and explicit factor-release lag assumptions.

## Extension — release-lagged beta uncertainty and drift

`beta_diagnostics.py` fits each factor regression on the `window` observations ending **before** origin minus an explicit `release_lag` (default: two periods). No observations at or after the training cutoff enter the coefficient estimates or residual-bootstrap draws. Origins advance by a non-overlapping `horizon`. The script reports factor betas, 2.5%/97.5% conditional residual-bootstrap percentile bounds (200 seeded draws by default), and L2 distance from the previous fitted beta vector. This illustrates sampling uncertainty and exposure drift, not a calibrated predictive interval for future returns.

```bash
python beta_diagnostics.py --seed 20261109 --release-lag 2 --ridge 0
python -m pytest -q test_beta_diagnostics.py
```

**Interpretation:** The release lag is an *assumed* data-availability delay in synthetic periods, not a real factor provider's publication schedule. Real datasets require timestamped point-in-time releases and revision tracking. Residual resampling assumes exchangeable errors conditional on fixed historical factors; it does not preserve serial dependence, correct omitted factors, or protect against regime changes. Ridge introduces bias; these intervals are descriptive and are not coverage guarantees. No live trading or investment advice. Extension tests and exact-revision CI remain unverified until executed.
