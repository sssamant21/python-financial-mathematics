# Section 16.8 — Calibration arithmetic range correction

**Date:** 2026-10-30  
**Category:** COV-74, partially addressed; independent review pending.  
**Original main:** `a751ac0a9e3dfbe620e4da7ab9db4cadd8a70b33`  
**Corrected executable snapshot:** `7968be83604ba6d801b05e6d61ba9fec8726e7b6`

## Retained failures and correction

[Machine evidence](chapter-16-calibration-range-followup.json) retains seven original probes, the new checker's original exit-1 result, original source hashes, all corrected scoped hashes and all nineteen script outputs.

The original helpers:
- Raised OverflowError for a fitted rate with time `2^600`, and rejected time `2^-600`, although the single-observation fitted rates are exactly their reciprocal times.
- Rejected the finite fitted rate `-1` from equal-time observations `+1e308,-1e308`, and failed a cancelling gradient whose exact represented-residual sum gives `1000`.
- Returned false zero curvature for time `2^-600`.
- Rejected a finite weighted half-square `2^1023` because the square overflowed before halving, and returned zero for a positive weighted loss below the output range.

Correction commit `1803e96432617bc3816ee89296186d3827437453`, blob `a7573a34e36c2d41e2110ae03ac0115f4eb68844`, uses exact Fraction intermediates for the complete expressions. Fitting computes the linear least-squares normal-equation quotient with exact represented times/prices and sensitivities `1000*t`. Curvature forms their exact square sum. Gradient and weighted loss aggregate the existing **rounded price residuals**, preserving that API's residual semantics. Final overflow and nonzero-to-zero underflow raise ValueError; exact zero remains valid.

A finite fitted rate can be returned even when the raw curvature cannot be represented: fitting divides the exact numerator/denominator before converting, while a direct curvature request must represent that curvature itself. This distinction is intentional.

## Independently derived expectations and actual rerun

[Runnable checker](../chapter-16/code/check_calibration_range.py) passes:
- Nine fit references from an independently implemented 2500-digit Decimal normal equation, including six single-time powers, opposing prices, disparate times and a true-zero fit at the smallest positive time.
- Eight exact gradient references: opposite residual cancellation, six row permutations preserving the residual sum one, and an individually overflowing sensitivity multiplied by a small residual.
- Five dyadic curvature references and four exact weighted-loss references.
- Eight explicit unrepresentable-result rejections across fitting, curvature, gradient and weighted loss.

For a single observation with price2000, solving `1000*(1+t*r)=2000` gives `r=1/t`. Equal-time prices of opposite signs have mean zero, so the fitted model price is zero and `r=-1`. These expectations do not depend on the production normal-equation implementation. The weighted cases include a finite half-square and a finite half-sum whose unhalved intermediates exceed float range.

**29/29 Chapter 16 files compiled; 19/19 scripts passed**, Python 3.12.14/Linux, assertions enabled, 15-second timeout per script, cwd each script's parent. Unchanged source bytes matched original pinned blobs, and the complete corrected scoped manifest matched the published executable tree.

From a checkout of `7968be83604ba6d801b05e6d61ba9fec8726e7b6`:
```bash
cd books/book-02-mathematical-foundations-for-finance-with-python/chapter-16/code
python check_calibration_range.py
```
For the original failure, use a separate checkout of the original revision above and copy only the new checker into its code directory before changing helpers. The first small-time fit raises ValueError; the other original probes are retained in the raw evidence.

Fresh pinned inventory is **473 Python files / 262 check-test scripts**. These are inventory counts, not a new full-book runtime pass. [V-42](runtime-refresh-2026-10-30-r6.md) remains the last full pass at its earlier pin (472 compiled /261 scripts /473 required hashes). This one subsequent source correction/checker has the scoped evidence above; refresh again after related executable changes accumulate.

## Limits and next checkpoint

Price and residual calculation retain their existing floating-point order/range. Exact aggregation cannot restore residual information lost there; gradient zero is not an independently certified optimum. Synthetic negative prices and extreme times test numeric APIs, not economic acceptance. General conditioning/noise analysis, financial interpretation and other normalized objective copies remain open.

Twenty-eight selected COV categories remain partially addressed; none closed by the register. Independent review, supported environments, release acceptance and canonical approval remain pending.

Next executable item: COV-74 Section 16.9/16.10 normalized analytic-rate, curvature and gradient range copies. Preserve their normalized objective scale (curvature `sum(t*t)`, one millionth of Section 16.8's raw-price curvature); do not substitute an already-rounded unscaled result.
