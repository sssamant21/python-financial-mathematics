# Project 09 — Path-Dependent Drawdown and Recovery Risk

**Business question:** Two portfolios can have the same average return but very different losses along the way. How deep could the worst peak-to-trough loss be, and how long might the portfolio remain below a previous high?

## Math and interpretation

For simple period returns `r[t]`, wealth evolves as `W[t] = W[t-1] * (1+r[t])`, starting at 1. The running peak is `P[t] = max(W[0], ..., W[t])`; drawdown is `D[t] = 1-W[t]/P[t]`. Maximum drawdown is `max(D[t])`. Recovery is the first later period when wealth regains the previous peak, or null when censored by the sample end. Underwater duration counts consecutive periods below the high-water mark.

A circular moving-block bootstrap samples contiguous return groups with replacement, retaining some short-term dependence. For each simulated path, calculate maximum drawdown. Report its 95th percentile and the proportion of paths exceeding a 20% loss. These are *conditional scenario diagnostics*, not future guarantees or market forecasts.

## Reproduce

Python 3.11+, with dependencies from `quant-projects/requirements.txt`. From this directory:

```bash
python drawdown.py --seed 2026 --observations 260 --simulations 1000
python -m pytest -q test_drawdown.py
```

The output is JSON. Index zero is the initial wealth before the first return. `recovery_index: null` means no observed recovery. Data are seeded synthetic weekly returns; no licensed prices are included.

## Guardrails and model validation

- Inputs must be finite, one-dimensional simple returns greater than -100%, with at least two observations. Block length must fit the sample; simulation count is capped at 100,000.
- This first milestone is **in-sample**: the bootstrap uses the entire input series. It does not claim walk-forward performance. A later exercise must estimate at each forecast origin from training data only.
- Circular resampling cannot create unseen regimes; outcomes depend strongly on sample length, block length, and the assumed return process. Liquidity, taxes, costs, leverage, selection/survivorship bias, and future regime changes are excluded.
- No broker connectivity, financial advice, real-market claims, or production certification.

## Evidence and next step

Local prototype on 2026-11-09: **8 tests passed** and a seeded 20-simulation CLI smoke test completed. Published-revision CI and independent review are not established by those local checks. Next: out-of-sample walk-forward drawdown scenario scoring and block-length sensitivity.

## Walk-forward extension — training-only scenario scoring (2026-11-09)

Run `python walkforward.py --observations 260 --simulations 200` and `python -m pytest -q test_walkforward.py`. The new `walkforward.py` trains on the preceding 104 synthetic weekly returns, predicts maximum drawdown over the next 26 weeks, and advances by 26 weeks so **held-out outcomes do not overlap**. It compares circular-block lengths 2, 4 and 8, reporting the forecast 95th-percentile maximum drawdown, realized drawdown, exceedance flags, and mean absolute scenario error. All forecast inputs end strictly before each held-out horizon. Block length is a prespecified sensitivity scenario, **not** optimized using future outcomes.

A 95th-percentile maximum-drawdown exceedance is not a calibrated 5% breach guarantee: the bootstrap model, finite sample and regime shifts may invalidate coverage. With only 260 observations and 104-week training, the number of independent 26-week evaluations is small. Avoid conclusions from the exceedance rate alone. Use authorized point-in-time historical prices and document download time, adjustments, missing observations and investable universe before real-market studies. No historical prices are committed.

Local prototype: 9/9 new tests passed on 2026-11-09 with a lightweight local stand-in for the already-published `drawdown.py` API; CLI smoke test and Python compilation passed. **Exact published-revision CI remains unverified** until GitHub Actions completes. Independent review and real-market calibration are pending.
