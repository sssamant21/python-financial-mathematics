# V10 — Section15.10 exogeneity, influence and upstream boundaries

Executed source pin: `5da9c8d7875acd64ab532feed63537cbe63749c6`. [Runnable review](review.py), [first](first.json), [replay](replay.json).

```bash
python books/book-01-python-foundations-for-financial-mathematics/qa/v10-regression-boundaries/review.py first
python books/book-01-python-foundations-for-financial-mathematics/qa/v10-regression-boundaries/review.py replay
```

**501 predicates pass twice with identical rows.** There are457 exact-source fit-field/ratio/SE comparisons across27 selected fits (six scalar fields, two canonical ratios, every fitted/residual field and one slope SE per fit),32 omitted-term projection/residual-orthogonality checks,two exact-law mean/bias checks,three caller leverage/deletion checks,four benchmark/pairing checks and three project-lineage checks. An additional fit replays the identical training slice after caller holdout mutation. Exact coefficient ratios use an independent uncentered2×2 determinant solver; displayed float fixtures follow the manuscript's decimal interpretation. Numeric reports/root/orthogonality tolerance:rtol5e-14,atol1e-15. Supplemental roots use100-digit Decimal. No random simulation or causal-estimation algorithm is introduced.

For fixed x=[−3,−1,1,3], enumerate all16 IID ±1 u paths with exact equal weights. Define **the hypothetical structural equation** y=1+2x+3z, z=x+u. Source simple OLS of y on x has expected slope5 rather than the specified direct coefficient2: beta−2=Σx(3z)/20 has exact expected bias3. Every fitted residual is orthogonal to x, while the omitted structural disturbance has E[3z|x]=3x. The OLS residual identity therefore does not establish exogeneity. The structural coefficient is supplied by the hypothetical model, not discovered or causally identified by the lab. No actual market confounder, intervention or independent causal validation is claimed.

Starting with the line x=y=[−1,0,1], append(10,100). Source full/leave-one-out fits match rational oracles. The appended observation has caller-computed hat diagonal151/154, versus9/22,51/154,43/154 for the original points; deleting it restores the original line. Hat diagonals sum to2. Deletion and leverage calculations are supplemental, not native influence/robust-regression APIs. This arithmetic sensitivity does not justify automatic outlier deletion or a probability claim about future observations.

|Input/boundary|Executed behavior|Meaning and limit|
|---|---|---|
|Raw x=[1,2,3,4],y=[3,5,7,9]|Slope2/intercept1|Hypothetical common-period percentage-point units; no market data|
|Subtract constant benchmark1 from both|Slope2/intercept2|Exact identity alpha_excess=alpha+(beta−1)×benchmark|
|Subtract benchmark[0,1,0,2] from both|Slope21/11/intercept21/11|Time-varying benchmark changes the model and can change slope; no CAPM calibration|
|Reverse response order only|Accepted positional input, slope−2|Equal lengths do not establish correct timestamp alignment|
|Prescribed project labels1–10, train1–8|Training model unchanged after holdout outcomes become[−999,999]|Caller slices exclude holdout; source has no date/availability/leakage detector|

The prescribed raw-daily-simple-return fixture hash matches prior project evidence (`a5cda21173172c91656e226cef9b51d53df6a400f7388a958489b4e0ad2cfff0`). Labels, training/holdout split, no risk-free adjustment and unspecified real dates are retained. This is provenance of a supplied synthetic fixture, not authenticity, calendar, settlement, mixed-frequency, revised-price or as-of availability acceptance. Those upstream contracts remain caller responsibilities and broader F32 integration remains open. Prerequisite/answer contracts for alpha/beta, residuals, raw versus excess, leakage and extrapolation align with these limits; the earlier24 answer/ten project-task records are not recreated or recounted.

Each run executes the full verbatim demo/twelve existing methods and compilation:four command records/24 invocations of twelve existing methods total. Whole-source and fence hashes match F136 corrected evidence. Its twelve initial failures/61 arithmetic predicates and prior703 V10 error-law/selection checks retain scope. No source change/defect or new workflow/answer/step/historical-method totals. This records the selected15.10 assumption crosswalk; next V10 Section15.11 financial-return statistics (annualization/moments/dependence/selection boundaries), preserving prior exact-source arithmetic evidence. V10/Book1 and F28/F32/F209/F165/F185 plus broad numerical/resource/data/model/platform/release/independent/canonical gates remain open. No causal, supported-platform or independent acceptance is claimed.
