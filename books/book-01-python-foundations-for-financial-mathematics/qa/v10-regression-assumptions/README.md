# V10 — Section15.10 fixed-design regression assumptions

Executed source pin: `1d5215359aa0b0897cd05778a48ec136a48f50ea`. [Runnable review](review.py), [first](first.json), [replay](replay.json).

```bash
python books/book-01-python-foundations-for-financial-mathematics/qa/v10-regression-assumptions/review.py first
python books/book-01-python-foundations-for-financial-mathematics/qa/v10-regression-assumptions/review.py replay
```

**703 predicates pass twice with identical rows**:646 native fit/projection/normal-equation checks over34 error paths; nine exact-law aggregate checks;42 caller two-model fit/selection fields plus one aggregate comparison;five train/holdout fields. Every path's coefficient ratios are compared exactly with an independent uncentered2×2 determinant solution; reported fields/SE and projection equations use rtol5e-14,atol1e-15. The source uses centered products; the independent oracle uses uncentered sums/determinant. Roots use100-digit Decimal. The expected slope sampling variance is derived independently from the explicit error covariance; the expected classical estimated variance uses the residual-projection trace, not an assumed equality with true variance.

Fixed x=[−3,−1,1,3], y=1+2x+error, Sxx=20. All finite laws have zero conditional mean and uniform exact weights; no random sampling is performed.

|Hypothetical error law|Paths|True slope sampling variance|Expected native classical SE²|
|---|---:|---:|---:|
|Four independent ±1 errors|16|1/20|1/20|
|Independent ±[1,1,1,4] errors|16|31/80|13/80|
|One shared ±1 shock times x|2|1|0|

For independent errors with variances vᵢ, Var(beta)=Σxᵢ²vᵢ/Sxx². E[estimated SE²]=Σ(1−1/4−xᵢ²/Sxx)vᵢ/[(4−2)Sxx]. The correlated slope-shock law has error covariance xxᵀ, fitted slope2±1 and perfect fitted lines, so the native SE is0 despite positive true sampling variance. Source classical arithmetic is correct; its inferential assumptions fail in the latter fixtures. Even the IID ±1 example's unbiased variance estimate does not establish an exact Student-t law (the errors are not normal and can generate zero residual variance). No robust/HAC routine, real-market calibration, causality, or distributional acceptance is claimed.

A separate null-law example conditions four IID ±1 responses on being nonconstant (14 equiprobable paths). For fixed candidate predictors[−3,−1,1,3] and[−1,3,−3,1], average predefined in-sample R²=1/3; choosing the larger R² on the same observations raises it to4/7. The source computes both fits; selection and finite-law aggregation are caller logic. This is not an inferential p-value or out-of-sample score. Constant-response cases are excluded here because the ordinary R² fraction is undefined; the source's separately documented R²=1 reporting convention is not treated as explained variance.

A disclosed chronological regime fixture fits y=1+2x perfectly on four training observations (R²1,SE0), then tests fixed predictions against y=1−2x at holdout x=[−1,1]. Source predictions[−1,3] have RMSE4 versus2 for the training-mean baseline1. The synthetic holdout is fixed before evaluation; no refit or real structural-break detection is claimed. The numeric API has no timestamps and cannot enforce that chronology. Caller data assembly, model selection, exact-law weighting and covariance calculations remain supplemental to exact-source execution.

Each run executes the full verbatim demo/twelve existing unit methods and compilation:four commands/24 invocations of twelve existing methods total. Whole-source/fence hashes match earlier F136 corrected evidence. Its twelve baseline failures,61 corrected arithmetic predicates, one workflow/24 answers/ten-task project retain scope and are not recounted. No new source defect/change, workflow, answer, project-step or historical-method totals.

Section15.10 remains partial in V10. Next: omitted-variable/exogeneity and influence sensitivity, upstream time-alignment/raw-versus-excess-return/project provenance boundaries, before progressing to15.11. Broader model/dependence/selection acceptance remains open. V10/Book1 and F28/F32/F209/F165/F185 plus numerical/resource/data/platform/release/independent/canonical gates remain open; no independent sign-off or certification.
