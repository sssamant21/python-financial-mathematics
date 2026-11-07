# Section 16.2 — scoped portfolio-weight lab and answer review

Baseline source: `9f0f28f8ab3ff8b72233aac6f1b300431622d45f`. One core workflow, 24 local answers and ten lab-step records reviewed. Predicates, workflow/answer counts and historical unique methods remain distinct.

Run from repository root:

```bash
python books/book-01-python-foundations-for-financial-mathematics/qa/chapter-16-weights-review/review.py
```

The observer extracts the single exact Python fence, executes the printed demonstration and twelve existing unittest methods, checks silent import and runs the printed compilation command in isolation. Three commands and 51 supplemental predicates pass in `results.json`; no historical unique methods added. Runtime/platform, raw outputs, hashes, independent rational references/tolerances and project results are retained. `baseline.json` preserves twelve failed predicates on unchanged baseline manuscript above, reproducible with the same runner and that revision. All twelve existing methods already passed.

F143 corrects normalization/signed-sum overflow, lost integer net exposure, oversized intermediate NAV/growth values preventing reportable trades/weights, invalid tolerance/policy controls and silently nonfinite/zero reported components. Integer/displayed-decimal floats use rational intermediates. Each market-value/exposure field must be reportable as a finite float; nonzero underflow raises ValueError. Normalized output weights must preserve the budget within the declared tolerance. Large signed vectors whose reported weights lose the net budget are explicitly rejected. A trade helper may use an unreportable intermediate NAV if each final trade is reportable, since it does not return that NAV field. No partial report or financing model is implied.

A weight residual acceptable under the default tolerance can become a material cash discrepancy at large NAV. Baseline target [.5,.50000000005] on NAV 10^16 created a nonzero trade sum; the corrected helper explicitly normalizes only targets already accepted within tolerance before calculating pre-cost trades. Invalid budgets such as [.6,.3] remain rejected; general weight validation does not normalize. Budget conservation is exact internally; rounded float outputs may have residuals and are not executable lot-rounded orders. This policy is documented rather than silently concealing missing exposure. Educational numerical conventions only, not binary-float compatibility or performance acceptance.

## Independent expectations and all local answers

References use exact rational market values, ratios, sums of signed/absolute weights, squared weights and budget equations. Drift is independently derived from end market values [660,380], rather than source's weight-growth path. Trade plans are independently derived from target dollar values minus current positions. Cost/cash scenarios are supplemental designs and only their underlying source valuations/weight checks are executed.

| Answers | Scoped review |
|---|---|
| 1–5 | Source [.6,.4], market values [200,150] with weights [4/7,3/7], explicit cash [.6,.3,.1], rejected missing budget and long-only [.7,.3] checked. |
| 6–8 | Source signed net=1, gross=1.4, long=1.2, signed short=−.2 checked against rational sums. No collateral/margin acceptance. |
| 9–11 | Source HHI .5/1 and four-equal effective holdings 4 checked. Effective count is concentration-equivalent, not covariance-aware risk diversification. |
| 12–13 | Source equal-weight drift [11/21,10/21] checked. Beginning-weight return .6(.1)+.4(−.05)=.04 is supplemental arithmetic; this listing has no portfolio-return function. |
| 14–16 | Source initial trades [−100,+100], one-way turnover .1 and hypothetical cost .20 checked. These refer to the initial stage, not after modeled returns. |
| 17–18 | Near-one budget accepted under declared tolerance; invalid nonpositive NAV rejected. Input normalization policy and output-range limits explicit. |
| 19–20 | Common valuation times and FX conversion €100×1.10=$110 reviewed; no real quote/calendar or FX feed audit. |
| 21–24 | Gross leverage, issuer cap, costs/constraints and whole-share infeasibility reviewed. No issuer/lot/cash optimizer or actual order execution claimed. |

HHI is applied only to long-only weights. Net exposure is calculated from original rational inputs before reporting; recombining very large rounded long/short display components can lose a small net. Retain source positions and use the separately calculated net. The drift helper still deliberately excludes individual returns at or below −100%; it does not implement extinguished holdings or signed leveraged drift.

## Ten lab steps and timing reconciliation

| Step | Executed evidence and limit |
|---|---|
| 1–3 | Initial values [600,400], source weights [.6,.4], source HHI=.52. Synthetic valuation labels; fictional USD and raw one-period returns. |
| 4 | Supplemental beginning-weight return .04 for [.10,−.05], ending values [660,380], NAV=1040. Not a source-return helper invocation. |
| 5 | Source end weights [33/52,19/52] checked from independent position values. |
| 6 | Two distinct stages now explicit. Initial independent example: target [500,500], source trades [−100,+100]. Main after-return example: target [520,520], source trades [−140,+140]. Original wording could mix initial acceptance values with a post-return task. |
| 7 | Initial gross traded=200/turnover=.1; post-return gross=280/turnover=7/52≈.1346153846. Turnover uses half absolute traded value divided by current NAV. |
| 8 | Hypothetical post-return cost .001×280=.28, funded wealth 1039.72 and targets 519.86 each. Supplemental funded trades [−140.14,+139.86] sum to −.28, absolute sum remains 280. Exact budget identity checked; source market-value calls on fractional target shares reconcile. This cost design is separate from source pre-cost target_trades. |
| 9 | At prices [110,47.5], exact target holdings require fractions, so whole-share feasibility is not promised. Separate no-cost explicit cash target [.475,.475,.05] validates and source trades current [660,380,0] to [494,494,52] via [−166,+114,+52]. It does not implement a constrained/fee-inclusive cash optimizer. |
| 10 | Inputs, fixture hash, valuation-stage labels, units, source/listing hashes, runtime, outputs and baseline failures retained. Actual dates, fills, taxes, liquidity, funding and source provenance unavailable. Corrected revision is the containing commit. |

Prerequisites: Python sequences/functions, value/return units, common valuation currency/time, positive NAV and explicit exposure/weight policy. Source functions/commands are execution evidence. Turnover, weighted return, funded-cost equations, fractional-share and cash-reserve designs are supplemental. Calendar quality, actual financing, lot constraints, economic suitability and operations acceptance are conceptual/unexecuted. Standard library only.

## Limits and resume checkpoint

Scoped local Linux CPython only. F28 notebook/platform, F32 broader shared-input integration and other unresolved findings remain open. No external-platform run, independent reviewer acceptance, exhaustive branch proof, real orders, constrained optimization or certification. Chapter 16 now records two workflows and 48 local answers reviewed. Next: Section 16.3 — Portfolio Return.
