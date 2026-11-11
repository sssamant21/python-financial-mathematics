# Project 20 — Retirement Sequence-of-Returns Risk

**Question:** Why can two portfolios earn exactly the same set of annual returns but finish with different balances when money is withdrawn along the way?

This synthetic, beginner-friendly lab studies **sequence risk** in retirement-style liability funding. It is not financial advice, a withdrawal recommendation, or a calibrated retirement model.

## Business and mathematical context

Let starting capital be `W_0`, the start-of-year withdrawal be `C_t = C_1 (1+i)^(t-1)`, and the annual portfolio return be `r_t`. The deliberately simplified wealth recurrence is

`W_t = max(0, W_(t-1) - C_t) * (1 + r_t)`.

A **ruin event** is recorded at the first year when the *scheduled* withdrawal exceeds the capital available before that withdrawal. Exact exhaustion after a fully funded withdrawal is **not** counted as ruin in that year; this convention is explicit and should not be confused with other ruin definitions.

Without withdrawals, the product of all `(1+r_t)` terms is independent of return order. With withdrawals, losses early in the horizon reduce the capital base from which subsequent spending is funded. Thus return order matters even when arithmetic average and geometric total return are held fixed.

## Reproducible lab (Python 3.11+, standard library only)

```bash
cd quant-projects/20-retirement-sequence-risk
python -m unittest -v test_sequence_risk.py
python -m compileall -q sequence_risk.py test_sequence_risk.py
python sequence_risk.py --draws 500 --seed 2026
```

The CLI uses **ten invented annual returns** (not historical prices, not 2020/2022 observations), initial capital 100 units, and a fixed first-year withdrawal of 7 units. It compares early versus late losses, then permutes the same return multiset with a seeded local RNG. `ruin_fraction` is only the fraction of shuffled scenarios with an unfunded scheduled withdrawal; it is **not** a calibrated probability of retirement failure. No provider access or third-party dataset is required.

### Interpretation and safeguards

- Fixed synthetic returns are held constant across permutations, isolating order rather than expected-return differences.
- Withdrawals happen **before** each annual return; returns below -100%, nonfinite inputs, nonpositive starting capital, invalid inflation, more than 120 years, and more than 10,000 draws are rejected.
- The model has no taxes, fees, social benefits, mortality, cash flows beyond withdrawals, asset allocation, serial dependence, or uncertainty about the future return distribution.
- Permutation destroys autocorrelation and volatility clustering; it should be used as a controlled sensitivity experiment, not as a realistic forward simulation.
- No trading, broker integration, licensed market data, or live account actions are involved.

## Validation evidence

On 2026-11-10 a local standalone copy passed **10/10 unittest cases**, Python compilation, and a 20-draw CLI smoke test. This does not establish that the exact published GitHub revision passed CI. The hosted GitHub Actions result and independent quantitative model review must be checked separately.

## Next exercise

Add fixed, predeclared withdrawal-rate and inflation grids, and distinguish funded-withdrawal shortfalls from terminal wealth depletion. Then test a block-bootstrap variant with a separate point-in-time market-data provenance workflow.

## Extension — funded withdrawal and inflation sensitivity (2026-11-10)

A *scheduled* withdrawal can exceed the wealth available at the start of the year. The baseline model floors wealth at zero. This extension makes the accounting explicit:

`funded_t = min(wealth_(t-1), due_t)`, `shortfall_t = due_t - funded_t`,
`wealth_t = (wealth_(t-1) - funded_t) * (1 + r_t)`.

The nominal funding ratio is `sum(funded_t) / sum(due_t)` (defined as 1 when no withdrawals are scheduled). It is not an inflation-adjusted welfare metric. **Ruin** means the first *partially unfunded* withdrawal, not merely terminal wealth equal to zero. Predeclared withdrawal rates are 3%, 5%, 7%, 9% of initial wealth, and inflation rates are 0%, 2%, 4%. The grid is a synthetic stress comparison, **not** a recommended withdrawal rate or an estimated probability of success.

```bash
cd quant-projects/20-retirement-sequence-risk
python -m unittest -v test_sequence_risk.py test_withdrawal_sensitivity.py
python -m compileall -q sequence_risk.py withdrawal_sensitivity.py test_sequence_risk.py test_withdrawal_sensitivity.py
python withdrawal_sensitivity.py --initial 100
```

The extension uses only Python 3.11+ standard library and the fixed invented returns from the baseline lab. Its 11 new regression tests check the accounting identity, partial funding, exact exhaustion, baseline equivalence, invalid inputs, and repeatability. An isolated source-equivalent local test run passed 11/11, compilation and CLI smoke; full GitHub revision integration and hosted CI are **unverified**. Inflation is deterministic and the annual return path is hypothetical; no historical-data validation or independent review is claimed.
