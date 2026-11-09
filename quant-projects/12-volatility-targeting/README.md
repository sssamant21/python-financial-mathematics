# Project 12 — Lagged Volatility Targeting and Turnover Costs

**Business question:** Can an investor maintain a more stable *estimated* risk budget when market volatility changes, and what do frequent rebalances cost?

## Mathematics

At observation `t`, compute sample volatility from the **previous** `window` simple returns: `sigma_t = std(r[t-window:t], ddof=1) * sqrt(252)`. Set `weight_t = min(max_leverage, target_vol / sigma_t)` for positive volatility; otherwise stay in cash. The weight is held for period `t` only, never estimated using that period's realized return.

Turnover is `abs(weight_t - weight_(t-1))`; the first rebalance is measured from zero exposure. Transaction cost is `turnover * cost_bps / 10000`; net simple return is `weight_t * r_t - cost`. This is a deliberately simplified linear-cost, cash-financed exposure model, not a margin or execution simulator. A leverage cap limits the exposure but does **not** prevent losses or model financing costs.

## Reproduce

Python 3.11+, NumPy and pytest from `quant-projects/requirements.txt`. From the repository root:

```bash
python -m pip install -r quant-projects/requirements.txt
cd quant-projects/12-volatility-targeting
python volatility_targeting.py --seed 20261109 --window 20 --target-vol 0.12 --cost-bps 10
python -m pytest -q test_volatility_targeting.py
```

Synthetic daily returns switch from a low-volatility to a high-volatility regime halfway through. Use `--cost-bps 0` and `--cost-bps 25` to compare cost sensitivity. The reported turnover is absolute exposure change, not round-trip traded notional. No third-party data are stored.

## Guardrails and limitations

- Historical-only rolling estimates, no look-ahead; fixed parameters are chosen for demonstration, not tuned on the evaluation sample.
- Zero historical volatility gives zero weight rather than infinite leverage. Reject nonfinite inputs, impossible simple returns, invalid settings and insufficient observations.
- This example assumes frictionless cash, no borrow/financing cost, no short sales, immediate execution, and constant linear transaction costs; actual slippage and market impact may differ.
- Annualization assumes 252 observations per year and approximately equally spaced daily returns. The strategy can miss volatility jumps and lose more than its intended risk target.
- For licensed market validation, record point-in-time universe, retrieval timestamp, adjustment policy, and exact observation dates; never commit unlicensed price histories.
- Synthetic test passes establish software behavior, **not** statistical validity, independent review, market performance, or production certification.

**Next:** walk-forward risk-target calibration, leverage-cap and cost sensitivity, realized-volatility tracking error under structural breaks.
