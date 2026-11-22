# V10 — Section15.11 return-moment and time-scaling assumptions

Executed source pin: `c4e5392d416b692c8737b9e03629397624219802`. [Runnable review](review.py), [first](first.json), [replay](replay.json).

```bash
python books/book-01-python-foundations-for-financial-mathematics/qa/v10-return-scaling/review.py first
python books/book-01-python-foundations-for-financial-mathematics/qa/v10-return-scaling/review.py replay
```

**168 predicates pass twice with identical rows:**120 source path fields over20 four-return paths (mean, exact sample variance, sample SD, four-period annualized SD, compounded return, geometric mean); three exact process-law mass checks;24 marginal mean/variance checks;21 weighted process/estimator/compounding checks. Exact rational coefficient/count/variance checks are separate from reported numeric comparisons (rtol5e-14,atol1e-15). The independent sample-variance oracle uses pairwise differences instead of centered squares. A100-digit nested-square-root of the gross product is independent of the source's log/exp geometric-mean implementation. Native annualized SD squares are weighted after reporting, with arithmetic tolerance, not bit-exact squared-root claims.

Declare **four equal hypothetical periods as one artificial year** (periods_per_year=4). Returns are .02+.1×sign, so all three laws have identical per-period mean.02 and variance.01. Enumerate16 independent-sign paths, two common-sign paths, and two alternating-sign paths with exact uniform weights; no random sampling or financial calendar data.

|Exact process law|True variance of sum of four increments|Expected source annualized SD²=4×sample variance|Expected compounded return|
|---|---:|---:|---:|
|IID signs|1/25=.04|1/25=.04|515201/6250000=.08243216|
|Common sign across all periods|4/25=.16|0|113247/781250=.14495616|
|Alternating sign|0|4/75≈.0533333|24111/390625=.06172416|

The exact sum-variance references follow covariance structure:independent variances add; a common sign gives four times the same shock; alternating shocks cancel. Native annualization correctly reports its declared algebraic formula. It does not estimate time dependence or certify that the formula describes the true horizon distribution. Common-sign paths have zero sample variance despite positive process variance; the alternating process has positive sample dispersion despite deterministic horizon sum. Equality of expected variance estimates in the IID fixture does not prove a calibrated SD estimator or all square-root-of-time assumptions. All processes have the same marginal distributions; marginal moments alone do not identify aggregation risk.

**Additive sums are distinct from compounded wealth.** Every law has exact expected sum.08 and caller linearized annual mean4×one-period mean=.08. Actual native compounded paths match gross-product references: IID expectation(1.02)^4−1; common-sign expectation[(1.12)^4+(.92)^4]/2−1; alternating expectation(1.12×.92)^2−1. None equals.08. The source has no exported annualized-mean function; caller linearization and joint-law weighting are supplemental. The tested sum-volatility references are not the variance of compounded wealth or a forecast of real annual return. Default252 is a user/model frequency convention, not evidence that a supplied sample has daily aligned observations.

The manuscript's existing project/exercise scaling, geometric-growth and dependence warnings align with these selected calculations. Twenty-four earlier answer/ten-task project records are not duplicated or recounted. Each run executes the complete verbatim demo/twelve existing methods and compilation:four command records/24 invocations of twelve existing methods total. Whole-source/fence identities match F137 corrected evidence; its twelve initial failures/46 corrected predicates remain preserved at their own scope. No source defect/change or new workflow/answer/step/historical-method totals.

Section15.11 remains partial in V10. Next: finite-sample historical-tail stability/selection and upstream return-basis/alignment/project-provenance boundaries, before15.12. Real corporate actions, stale quotes, timestamps, reinvestment/cost models, heavy tails and forecasting validity remain unaccepted. V10/Book1,F28/F32/F209/F165/F185 and broad numerical/resource/data/model/platform/release/independent/canonical gates stay open; no independent or supported-platform acceptance claimed.
