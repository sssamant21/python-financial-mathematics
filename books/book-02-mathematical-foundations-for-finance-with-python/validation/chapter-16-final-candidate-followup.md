# Section 16.10 — Per-candidate calibration validation

**Date:** 2026-10-30  
**Category:** COV-74, partially addressed; independent review pending.  
**Original main:** `0796d390e6a22c541143a3fb230c41614aff03a9`  
**Corrected executable snapshot:** `2d61bd212ca245578b0f6d192dbe824a71132d6c`

## Original gap and retained failure

[Machine evidence](chapter-16-final-candidate-followup.json) retains the baseline run keys, a stale-rate probe, the original exit-1 assertion failure, an intermediate oracle-harness failure/correction, original source hashes and the complete passing scoped rerun.

The original report evaluated training/holdout metrics only at the analytical benchmark. Replacing all six returned optimizer rates with zero still produced top-level training MAE/RMS zero, with no candidate-specific metric fields. Those benchmark metrics were numerically correct for the benchmark; their presence did not validate the returned candidates. The new checker failed on the missing per-candidate evidence.

## Correction and explicit numerical policy

Source correction `4fa2aa23130bff07d82e85deeee2403a4d649b6f`, blob `e3bbac8741f623e76ab905fc65a20518345d8c12`, recomputes each run's training/holdout residuals, metrics, normalized loss and gradient at its actual returned rate. Each run retains named acceptance checks and provisional acceptance. Overall provisional acceptance requires every candidate to pass.

The report retains these synthetic numerical limits:
- Absolute rate error from the analytical benchmark: `1e-8`.
- Both reported and recomputed absolute gradient: `1e-8`.
- Absolute difference between reported and recomputed normalized loss: `1e-12`.
- Training MAE and RMS: `1e-5` price units.
- Holdout maximum absolute residual: `1.01` price units, permitting the known one-dollar synthetic holdout error.
- Solver status must be `gradient_tolerance`.

These are teaching-case choices, not universal financial thresholds or approval. The top-level legacy metric fields remain benchmark metrics and now have an explicit `benchmark_metric_rate` label. The numerical scope and limits are retained in the report; runtime/reviewer certification flags remain false.

## Independent expectations and actual checks

[Runnable checker](../chapter-16/code/check_final_candidate_acceptance.py) checks six returned candidates against independent exact-Fraction price residual formulas and a 100-digit Decimal RMS reference. Forty-eight metric fields agree within an absolute `2e-12` price-unit tolerance, allowing the production price-evaluation rounding. Independent normalized quadratic references use `L=7*(r-1/20)^2` and `g=14*(r-1/20)`, with loss absolute tolerance `1e-24` and gradient `2e-12` for these selected near-optimal candidates.

Six deliberately failed scenarios reject a changed solver status, stale returned rate, incorrect reported gradient, incorrect reported loss, a two-dollar holdout residual and a real one-iteration budget for the three gradient-descent starts. A nonfinite candidate is separately rejected. At the injected rate zero, independent exact checks require training residuals `(-50,-100,-150)`, normalized loss `0.0175` and gradient `-0.7`. The ordinary complete report serializes with strict JSON.

An intermediate oracle accidentally mixed Fraction residual calculations with float observation prices, causing AttributeError during Decimal RMS calculation. Both the failed scoped rerun and conversion correction are retained. This was a checker defect, not another manuscript/solver finding.

**31/31 Chapter 16 sources compiled; 21/21 scripts passed**, Python 3.12.14/Linux, assertions enabled, cwd each script's parent, 15-second timeout. Unchanged source blobs matched the original pinned tree; all corrected scoped hashes match the published executable snapshot.

From a checkout of `2d61bd212ca245578b0f6d192dbe824a71132d6c`:
```bash
cd books/book-02-mathematical-foundations-for-finance-with-python/chapter-16/code
python check_final_candidate_acceptance.py
```
For the baseline, copy only the new checker into a separate checkout of the original revision and run before changing the assessment. Its first per-candidate metric assertion fails.

## Runtime scope and remaining work

Fresh pinned inventory: **475 Python files /264 check-test scripts**. These are not new full-book execution counts. [V-43](runtime-refresh-2026-10-30-r7.md) remains the last full runtime at its earlier pin (474 compiled /263 scripts /475 required hashes); this subsequent one-source/one-checker change has the scoped rerun above. Refresh after related executable changes accumulate.

Broader acceptance-limit sensitivity, complete solver configuration/provenance, arbitrary data/conditioning, objective/loss range and financial model validation remain open. Twenty-eight selected categories remain partially addressed; none closed by the register. Independent review, supported environments, release acceptance and canonical approval remain pending.

Next executable item: COV-75 Section 16.10 exact exercise objectives: Exercises1–5 use curvature4, Exercises11–13 curvature1, while the three-observation calibration uses curvature14. Add distinct expected values/histories without claiming general proof or completion of all worked solutions.
