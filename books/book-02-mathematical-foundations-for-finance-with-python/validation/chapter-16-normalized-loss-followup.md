# Sections 16.9–16.10 — Normalized objective/loss range correction

**Date:** 2026-10-30  
**Category:** COV-74, partially addressed; independent review pending.  
**Original main:** `a040bbf7a49fcc9d5cf924b7db3c053bc9560bbd`  
**Corrected executable snapshot:** `4c122d5aea349f6e4802ce9201814008d2252b70`

## Retained initial results

[Machine evidence](chapter-16-normalized-loss-followup.json) retains eight original probes, the checker's original exit-1 result, original source hashes and all twenty-three final script outputs.

For normalized residual `2^512`, the original half-square helpers rejected a finite result `2^1023`: Section16.9 raised ValueError; Section16.10 raised OverflowError. For sixteen normalized residuals `2^-538`, both returned zero, although the complete half-sum is exactly `2^-1073`, a representable positive subnormal. They also returned zero for a positive loss below float range. Two true-zero controls are retained as passing controls, not defects.

## Correction and independent oracle

Source correction commits:
- Section16.9 `e07821b87dc0fa9949aae99bc1178cca55267868`, blob `8ddf08136c64f1b476e44bf241acc5fa0c705662`.
- Section16.10 `768cd189aabc31978089aabfdb9ea14e0469a5bf`, blob `98a7acd7fd75ae492955d48d1cf0c5e1057c141d`.

Both paths now aggregate exact Fraction expressions and use the shared final-rounding/range guard. Section16.9 preserves rounding of each normalized residual before summing its half-squares, and now rejects a nonzero residual normalization that rounds to zero. Section16.10 computes the complete normalized loss as the exact sum of represented raw residual squares divided by2,000,000, converting only the final result. This removes its earlier extra normalization rounding, so ordinary last-bit results need not exactly match the old expression or Section16.9. Price/raw-residual evaluation remains unchanged.

The [runnable checker](../chapter-16/code/check_normalized_loss_range.py) uses a separately implemented **2500-digit Decimal** half-square sum, observing each API's declared normalization policy. Fourteen exact float-reference comparisons cover true zero, ordinary residuals, a finite half-square after an overflowing unhalved square, four-term overflow before halving, collective subnormal accumulation, small finite values and nondyadic normalized residuals.

The collective-underflow expectation follows directly:
`16*(2^-538)^2/2 = 2^-1073`.
The finite-overflow expectation is
`(2^512)^2/2 = 2^1023`.
Neither expectation relies on a production floating-point square.

Fourteen range/input rejection cases cover genuinely unrepresentable positive losses, nonzero normalization underflow, Inf/NaN/Boolean observations and empty data. A direct Section16.9 normalization-underflow rejection is also checked. Nonzero final results that overflow or round to zero raise ValueError; exact zero remains accepted. Synthetic negative prices construct zero-model-price residual cases and are numerical probes, not economic acceptance.

## Actual scoped rerun and reproduction

**33/33 Chapter16 sources compiled; 23/23 check scripts exited zero**, Python3.12.14/Linux, assertions enabled, cwd each script's parent, 15-second timeout. All original source blobs were verified against the pinned tree before copying; all final scoped hashes match the published executable snapshot.

From a checkout of `4c122d5aea349f6e4802ce9201814008d2252b70`:
```bash
cd books/book-02-mathematical-foundations-for-finance-with-python/chapter-16/code
python check_normalized_loss_range.py
```
For the baseline, copy only this checker into a separate checkout of the original revision and run before changing the helpers. The first finite half-square comparison fails; the other original results are retained in JSON.

Fresh tree inventory is **477 Python files /266 check-test scripts**, not new full-book execution counts. [V-44](runtime-refresh-2026-10-30-r8.md) remains the latest full pass at its earlier pin: 476 compiled, 265 scripts passed, 477 required hashes verified. This subsequent two-source/one-checker batch has the scoped pass above; refresh the full book when related changes accumulate.

## Limits and next checkpoint

Exact aggregation does not recover information lost in price/raw-residual calculation, validate conditioning or establish economic model correctness. Solver-update range, broader acceptance/configuration and independent mathematical/editorial review remain open. Twenty-eight selected categories remain partially addressed; none closed by the register. Supported platforms, reviewed-release validation and canonical approval remain pending.

Next executable item: COV-75 Section16.8 lab step10, the currently absent rank-deficient two-parameter `m(a,b)=a+b` example. Add distinct rank/null-direction/unchanged-prediction evidence without claiming general identifiability or independent sign-off.
