# Section 15.10 — scoped regression lab and worked-answer review

Baseline source revision: `ab22ac3e67e392ab51e78cafd276eca561e0ea76`. Scope: one core workflow, 24 local answer records and one ten-task mini-project. Workflow, exercise, predicate and historical unique method counts remain separate.

Run from the repository root:

```bash
python books/book-01-python-foundations-for-financial-mathematics/qa/chapter-15-regression-review/review.py
```

The observer extracts the single exact Python fence, runs the printed demonstration and twelve existing unittest methods, verifies silent import and runs the printed compilation command in isolation. Three commands and 61 supplemental predicates pass in `results.json`; no historical unique methods added. Python/platform, source/listing hashes, raw command output, numerical expectations/tolerances and project outputs are retained. `baseline.json` retains twelve failed predicates against the unchanged source revision above, reproducible with the same observer. All twelve existing methods already passed on baseline.

F136 corrects integer predictor spread lost by coercion, a tiny spurious intercept in the declared synthetic fixture, decimal constant predictors not rejected, intermediate fit/RMSE overflow or underflow, prediction cancellation overflow, and unreportable aggregates or predictions silently returning nonfinite values/raising raw OverflowError. Rational intermediate arithmetic follows the documented displayed-decimal interpretation of floats. Roots use 80-digit Decimal. All reported numeric fields must be finite floats without erasing nonzero values by underflow; a model with an unreportable required aggregate is rejected even if some coefficients are reportable.

Exact rational coefficient strings accompany rounded display coefficients in `coefficient_ratios`. Prediction uses these canonical ratios, preserving small intercept contributions when large display coefficients cancel. For predictor 10^18+[0,1,2,3], response [3,5,7,9], the intercept is −1999999999999999997; rounded display alone would lose the offset. The retained ratios give prediction 11 at 10^18+4. Changing display coefficients without matching ratios is rejected; manually supplied numeric-only models use their declared values. Fitted values, residuals and fit diagnostics use unrounded coefficients before reporting. This is an educational representation policy, not a performance or binary-float compatibility guarantee.

For constant responses, the usual 1−SSE/SST fraction is undefined. The existing implementation convention R²=1 for exact constant fit is now explicitly documented; it is not explained response variation or predictive evidence. A perfect fitted line's zero slope SE does not validate conventional inference.

## Independent derivation and local answers

The observer solves the 2×2 normal equations using uncentered exact rational sums: determinant nΣx²−(Σx)²; slope [nΣxy−ΣxΣy]/determinant. This is independent of source centered-product arithmetic. Coefficients then determine rational fitted values, residuals, SSE, SST and slope SE; roots use Decimal.

| Prompts | Reviewed alignment and evidence |
|---|---|
| 1–5 | Model y=alpha+beta*x+error; worked means 2.5/6, Sxx=5, Sxy=10 verified by independent arithmetic. Means and centered sums are derivations, not additional source report fields. |
| 6–12 | Exact source slope 2, intercept 1, prediction 11, zero residual/SSE, SST=20 and R²=1 checked. |
| 13–15 | Residual df n−2=2; hypothetical SSE=2 gives residual variance 1 and slope SE √(1/5). These hypothetical inputs differ from the perfect example's SSE=0; independently derived, not falsely claimed as its source output. Noisy project source variance/SE checked separately. |
| 16 | Source RMSE of residuals [1,−1,1,−1] against zero is 1. |
| 17 | Integer and decimal constant predictors rejected. |
| 18–19 | Source response shift increases intercept by 10; doubling predictor halves slope. |
| 20–21 | Beta is sample sensitivity, daily raw-return intercept is conditional and unit-dependent; neither guarantees skill. CAPM excess-return interpretation requires a different declared specification. Conceptual review. |
| 22–23 | Serial dependence invalidates classical SE assumptions; future information in predictors is leakage. No HAC or point-in-time market feed audited here. |
| 24 | x=100 lies outside [1,4]; extrapolation arithmetic does not establish reliability. Conceptual review; the lab holdout is also a disclosed extrapolation in the synthetic market range. |

## Fully specified project and step contracts

The manuscript previously supplied no concrete financial return fixture, windows, holdout or baseline. It now fixes ten synthetic paired daily simple returns and period labels 1–10, with real dates unspecified. Numeric pairing validates lengths, not calendars. No risk-free adjustment is made, so this is a raw-return market model, not a CAPM excess-return specification.

| Task | Executed result and limit |
|---|---|
| 1–2 | Market [.01,.02,.03,.04,.01,.02,.03,.04,.05,.06], asset [.02,.04,.05,.09,.03,.03,.07,.08,.11,.10], raw decimal simple returns paired by synthetic label. Actual calendar alignment remains upstream. |
| 3 | Training only periods 1–8: means .025/.05125, Sxx=.001, Sxy=.00205; source slope 2.05, intercept 0. Independent normal-equation reference checked. |
| 4 | Every one of eight source fitted values and residuals checked. SSE=.000485, SST=.0046875, R²≈.8965333333. |
| 5 | Source RMSE≈.0077862058, residual variance=.000485/6, slope SE≈.2843120352. Coefficient inferential assumptions not validated by these arithmetic checks. |
| 6 | Period/fitted/residual table retained in `results.json`; satisfies the tabulation option. No plot or statistical residual-diagnostic test is claimed. |
| 7 | Non-overlapping windows 1–4 and 5–8 fitted separately; both slope/intercept pairs checked against rational oracles. Synthetic differences do not establish structural breaks. |
| 8 | Autocorrelation/heteroskedasticity invalidate classical SE calibration; conceptual review only, no robust/HAC implementation. |
| 9 | Fixed training model predicts periods 9–10 as [.1025,.123], holdout RMSE≈.0171062854. Training-only asset-mean baseline .05125 gives RMSE≈.0539820572. No holdout fitting; two synthetic holdout points cannot certify forecasting value. |
| 10 | Input hash, source/listing hashes, period split, runtime, full reports, residual table and baseline failures retained. Corrected revision is the containing commit. |

Source functions execute all fits, predictions and RMSE calls. The observer's dataset assembly, rational normal-equation solver, residual table and chronological split are supplemental, not a second previously published complete lab script. Statistical suitability, causality, economic alpha, robust inference and real data provenance remain conceptual/unexecuted. Prerequisites: Python functions/sequences, paired return units, mean/variance/covariance, and upstream alignment. Standard-library runtime only.

## Limits and resume checkpoint

Scoped local Linux CPython only. F28 notebook/platform and F32 broader shared-input integration remain open, as do other unresolved findings. No Windows/macOS/notebook run, exhaustive branch proof, independent acceptance, real-market forecasting or certification. Chapter 15 now records ten reviewed workflows and 240 local answer records. Next: Section 15.11 — Financial Return Statistics.
