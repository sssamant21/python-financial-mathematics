# Chapter 16 — Residual metric range and report integration

**Date:** 2026-10-30  
**Category:** COV-74, partially addressed; independent review pending.  
**Initial source:** `dac1146409e3a8f4cefcb1bd63de93d9d0dabcf9`  
**Corrected executable snapshot:** `c42fb1965a8febe91dc9ed310b2db9b0d0cb9ca2`

## Retained initial failures

[Machine evidence](chapter-16-residual-metric-followup.json) preserves two original exit-1 checker runs, eight original probes, original source blob hashes, the first scoped rerun and the final complete scoped rerun.

Section 16.8 rejected `(1e308,1e308)` while computing MAE, even though MAE, RMS, bias and maximum absolute error are each finite. It returned zero RMSE for `(1e-200,-2e-200)` and for opposite smallest subnormals, despite a representable nonzero RMS. Naive squaring caused the underflow.

Continuing into the downstream paths at `1dcae51ee5b21525ece7bb0185b6dbe4a7c9d6bf` reproduced infinities in Section 16.9's price-metric report and Section 16.10's metric helper, plus false zero RMSE in both copies. Original infinities are retained as explicit repr strings in valid JSON. These are arithmetic/report findings, not extra COV categories.

## Correction and independent expectations

Section 16.8 now forms MAE and bias with exact Fraction sums of validated represented residuals, dividing before final float conversion. RMSE normalizes by the maximum absolute residual, sums squared normalized residuals with fsum, averages, takes the square root and restores scale. The zero vector returns zero. Sections 16.9/16.10 call that shared checked helper instead of repeating naive arithmetic.

Correction commits:
- Section 16.8: `cabf4837657802d64fc823a8990cd2eec1681750`, blob `5a67719acbc9d1b501cb59f19f9685a9162253ab`.
- Section 16.9: `11c1bbe914913eb24489d77d3f2050bde9c1c009`.
- Section 16.10: `87f38a5f825c089f3946700a526c2b30b651c315`.

[Metric/input checker](../chapter-16/code/check_residual_metric_boundaries.py) compares eight datasets and four fields: **32 pairs**. Mean expectations follow exact rational mean definitions; RMS uses an independent exact rational mean-square followed by a **100-digit Decimal square root**, avoiding the production normalization algorithm. MAE/bias/max-abs require exact float-reference agreement. Selected RMS comparisons allow two output ulps, including subnormals; this tolerance describes the selected checks, not an arbitrary-input accuracy theorem.

Six permutations of `(1e308,1,-1e308)` preserve bias `1/3` and the RMS reference. Thirty-nine explicit rejection cases cover empty/malformed observation and residual containers, nonpositive/nonfinite times, invalid/nonfinite/Boolean numeric values, weight shape/sign/all-zero constraints and nonfinite rates. Two independently known integer residual/weighted-loss results include a permitted zero weight.

[Integration checker](../chapter-16/code/check_metric_integration.py) checks six independent reference sets through actual Section 16.9/16.10 entry points, observes two shared-helper calls and serializes all eight checked results with `allow_nan=False`. Synthetic boundary rows include negative prices to construct tiny residuals at zero model price; these are numerical API probes, not economically accepted observations.

## Actual reruns and reproduction

First Section 16.8 correction: **27 files compiled; 17 scripts passed**. After completing both downstream integrations: **28 files compiled; 18 scripts passed**. Environment: Python 3.12.14/Linux, assertions enabled, each script run from its parent with a 15-second timeout. All unchanged chapter sources matched pinned original hashes; all final scoped source hashes matched the published executable tree.

[V-42 full refresh](runtime-refresh-2026-10-30-r6.md), at the same final executable snapshot, compiled **472 files**, passed **261 scripts**, and verified **473 required hashes before/after**. Counts were freshly derived from the pinned tree.

From a checkout of `c42fb1965a8febe91dc9ed310b2db9b0d0cb9ca2`:
```bash
cd books/book-02-mathematical-foundations-for-finance-with-python/chapter-16/code
python check_residual_metric_boundaries.py
python check_metric_integration.py
```
For the first baseline, copy only the first new checker into a separate checkout of the initial revision and run before changing the helpers. For the downstream baseline, use the intermediate revision above and copy the new integration checker beside its already-present metric checker. Both original failures and actual outputs are in the evidence JSON.

## Limits and checkpoint

This validates selected arithmetic and input contracts, not economic input plausibility, all possible RMS rounding cases, noisy-data suitability or calibration quality. Final small means may round to zero; exact represented sums do not restore information already lost before residuals were passed in. Fitting, gradient, curvature and weighted-loss intermediate range remains a distinct open obligation. Other chapters' metric copies are not covered by this correction.

Twenty-eight selected categories remain partially addressed; none is closed by the register. Independent review, supported platforms, release acceptance and canonical approval remain open. Next executable item: COV-74 Section 16.8 fit-rate/curvature/gradient/weighted-loss range boundaries, using independent exact represented-observation references before any correction.
