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
