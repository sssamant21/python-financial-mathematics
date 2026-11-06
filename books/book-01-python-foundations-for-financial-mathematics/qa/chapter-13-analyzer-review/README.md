# Section 13.14 — scoped Investment Performance Analyzer review

Reviewed [the chapter project](../../chapter-13/13.14-chapter-project-investment-performance-analyzer.md) at parent `8a3d34131068229cf92bbd61e1f31d931980c741`. Run `python -B review.py` here. [Baseline](baseline.json) retains 14 failures; [results](results.json) record the corrected rerun and both Python fence hashes. The whole standard-library listing was copied byte for byte to the named file, run with all twelve existing methods, compiled and imported in isolation. The geometric log expression was separately evaluated as written with its declared contextual inputs. All three command checks and 52 additional predicates passed; no historical unique methods were added.

| Acceptance steps | Evidence |
|---|---|
| 1–4 | The program prints Dataset A; exact products from rational input factors give a final index of 107.0664442848 from 100. The six returns average 7/600. A separately evaluated root of the terminal factor gives 1.144490% geometric monthly, and compounding it reconstructs the final index. |
| 5–6 | Pairwise differences give the independent sample variance; annualizing the standard deviation by √12 gives 8.024961%. Pairwise ordered wealth ratios reproduce each drawdown and locate the −2% minimum. |
| 7–8 | The portfolio's pre-flow valuations give 110/100 × 144/160 − 1 = −1%; the investor's signed ledger gives a periodic IRR of −2.423493% by the positive gross quadratic root. Repricing at the unrounded result is within 1e−7 currency units. |
| 9–12 | Executed true total loss, invalid inputs, zero volatility, and the existing methods. A true zero wealth path stays depleted. The QA output records source snapshots, conventions and runtime; no independent sign-off was performed. |

| Worked answers | Prompt alignment and calculation |
|---|---|
| 1–7 | Six returns sum to 7%; first two gross factors give 1.0094. For +20% and −10%, gross is 1.08, geometric is √1.08−1 and arithmetic is 5%. The opposing 10% returns give sample variance .02; annualizing .02 standard deviation gives .02√12. |
| 8–11 | Wealth 90 leaves a 30/120 drawdown and requires 30/90 recovery gain. A .008 monthly excess divided by .02 yields .4, then multiply by √12 for 1.3856. |
| 12–18 | Subperiod gains are +10% and −10%; linked factor .99 contrasts with unadjusted balance factor 1.44. One receipt of 110 on an outlay of 100 gives 10% periodic IRR and zero discounted residual at that rate. Identical returns have zero volatility and an undefined Sharpe. |

**F108.** The original listing erased small nonzero values, overflowed before cancellation, could report false depletion, and allowed empty or impossible input in some methods. The IRR residual stop depended on currency scale. The printed Dataset C rate was incorrect, and the program omitted annualized volatility and could abort the full report when Sharpe alone was undefined. The fixes use exact intermediate fractions, a decimal geometric root, range checks, scale-independent bracket signs, and a report that retains the other fields. The evidence uses synthetic inputs with unspecified currency and fee basis. The five extensions, data lineage beyond the fixture, operational runbook, and independent review are design or acceptance scope, not claimed runtime execution. F28 and F32 remain open.
