# V10 — Section 18.12: VaR/ES aggregation assumptions

Source pin: `4e4dba9e89d0448ab378b6c6a1d8735bec198942`. Reviewed November 21, 2026. [Runnable review](review.py), [first run](first.json), [replay](replay.json), [prior source identity](identity.json).

Run from the repository root:

```bash
python books/book-01-python-foundations-for-financial-mathematics/qa/v10-risk-aggregation/review.py first
python books/book-01-python-foundations-for-financial-mathematics/qa/v10-risk-aggregation/review.py replay
```

Both runs pass **62 checks** with identical rows: three loss-conversion lists, 27 native numeric fields, 24 permutation results and eight caller aggregation decisions. Each run also executes the complete verbatim reference demo, its twelve existing unittest methods, and compilation. Across both runs: four command records and 24 invocations of the same twelve methods. No new historical unique methods, answers, workflows or lab-step totals are claimed.

The listing matches the earlier F184 review. Its 58 predicates, fourteen initial failures and explicit policy decisions remain at their original scope. No financial source change or new implementation defect was found.

## Exact common joint-law fixture

Two one-period positions each lose 100 with probability 1/25 and otherwise lose zero. Independence defines a 25×25 product model, expanded to **625 equally weighted joint states**. These are enumerated states, not 625 simulated IID observations. Initial values are 100 for each component and 200 combined, so all terminal values are nonnegative. No negative path is clipped or dropped.

Native `losses_from_values` produces the aligned losses A, B and A+B exactly. The combined loss distribution has masses 576/625 at zero, 48/625 at 100 and 1/625 at 200. An independent atom-CDF calculation gives VaR. ES combines upper-atom mass with precisely enough VaR-boundary mass to fill 1−alpha. This differs from the source's equal-weight sorting and fractional-tail algorithm. It does not add an unequal-weight API.

| Alpha | VaR(A)+VaR(B) | VaR(A+B) | ES(A)+ES(B) | ES(A+B) |
|---:|---:|---:|---:|---:|
| .90 | 0 | 0 | 80 | 80 |
| .95 | 0 | 100 | 160 | 103.2 |
| .96 | 0 | 100 | 200 | 104 |
| .99 | 200 | 100 | 200 | 116 |

At .95 and .96, VaR of the sum exceeds the sum of the component VaRs. This finite example disproves a universal VaR subadditivity claim. The ES values satisfy the subadditive inequality in these selected cases; the numerical check is not a general proof of ES axioms. ES of 103.2 at .95 is below the maximum possible loss of 200. Averaging only strictly positive losses would not implement the specified integrated-quantile ES.

The .96 level lies exactly at the component zero-loss CDF boundary under the source's displayed-decimal convention. Reversing input order preserves all checked VaR/ES results. Risk levels are quantile levels, not confidence-interval coverage probabilities.

## Contracts and remaining scope

- One fictional common period and currency; no actual horizon length, market date or calibrated probabilities are supplied.
- Positive loss is initial minus terminal value. Loss frequency uses strict L>0. VaR uses the lower nearest rank; ES includes fractional boundary mass.
- Positions share aligned joint states. Component risk measures alone cannot reconstruct the sum's distribution or dependence.
- No quantile/ES interval, bootstrap, backtest or sampling-independence acceptance is claimed.
- F185 remains open: the selected terminals are nonnegative and do not reconcile the upstream normal-portfolio model's negative terminals. F32 shared-model, metadata and valuation integration also remains open.
- No liquidity, funding, cost, multi-period, market sampler or unequal-weight implementation is supplied.

Numeric comparisons use rtol 5e-14 and atol 1e-12; these are arithmetic tolerances, not statistical bands. Next: **18.13 computational-performance assumptions**. V10 and Book 1 remain in progress. F28/F32/F209/F165/F185 and broader resource, model, platform, release, independent and canonical acceptance remain open.
