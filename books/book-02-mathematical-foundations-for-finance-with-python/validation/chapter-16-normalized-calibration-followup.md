# Sections 16.9–16.10 — Normalized calibration range follow-up

**Date:** 2026-10-30  
**Category:** COV-74, partially addressed; independent review pending.  
**Original main:** `13aac60b2163429ae750eaa2d29355f0baadd0e5`  
**Corrected executable snapshot:** `b5b04e9fbee6367d5d81136d47d9475c96a2dea5`

## Retained original results

[Machine evidence](chapter-16-normalized-calibration-followup.json) retains eight probes, the original exit-1 regression, original source blobs, final scoped hashes and all twenty script outputs. It also records an initial probe-harness import-path error corrected before numerical probes; this is not a manuscript defect.

Both copies rejected finite single-observation fitted rates at times `2^-540` and `2^540`; Section 16.10 raised ZeroDivisionError for the small-time case. Both reported zero curvature for a mathematically positive but unrepresentable result. Section 16.10 failed a finite cancelling gradient; Section 16.9's corresponding `0.002` result was a passing control and is retained as such.

## Correction and objective scale

The analytical quotient, curvature and gradient aggregates now retain exact Fraction expressions through final output rounding, using Section 16.8's shared rounding/range guard. True zero is accepted; final overflow and nonzero-to-zero underflow raise ValueError. Fitting does not convert the denominator separately, allowing a finite quotient even when a direct curvature request is out of range.

Correction commits: Section 16.9 `e7dc8e8a859457cf2af0e0dcaa65bddae418dd94`; Section 16.10 `26a34966fbaad1d0a6fea9580e171fbc46295c88`.

The normalized curvature remains `sum(t*t)`, not `sum((1000*t)^2)`. For time `2^510`, normalized curvature `2^1020` is finite even though raw-price curvature is not. No already-rounded raw-price result is used.

Each existing residual convention remains: Section 16.9 aggregates its rounded normalized residuals; Section 16.10 aggregates rounded raw residuals with division by1000 in the exact expression. For `t=3, observed price997, rate0`, the two last-bit gradient results can differ. These are explicitly checked policies, not a claim of identical arbitrary-input gradients.

## Independent expectations and actual checks

[Runnable checker](../chapter-16/code/check_normalized_calibration_range.py) passes:
- Sixteen analytical-rate pairs against the independent 2500-digit Decimal normal equation retained in the preceding calibration checker. Single-observation price2000 gives the independently known rate `1/t`; opposing equal-time prices give zero fitted price.
- Ten normalized dyadic curvature references, including subnormal and large finite cases.
- Six gradient references computed from each API's represented residual contract, including cancellation and a finite normalized product after an overflowing raw intermediate.
- Eighteen range/input rejections and three default-scale/residual-policy assertions.

All **30 Chapter 16 sources compiled; 20/20 check scripts exited zero**, Python 3.12.14/Linux, assertions enabled, 15-second timeout, cwd each script's parent. All unchanged sources matched pinned original hashes; all corrected scoped hashes matched the published executable tree.

[V-43 full refresh](runtime-refresh-2026-10-30-r7.md) at the same executable snapshot then compiled **474 files**, passed **263 scripts**, and verified **475 required hashes before/after**, covering this and the preceding Section 16.8 correction/checker.

From a checkout of `b5b04e9fbee6367d5d81136d47d9475c96a2dea5`:
```bash
cd books/book-02-mathematical-foundations-for-finance-with-python/chapter-16/code
python check_normalized_calibration_range.py
```
For the original failure, copy only the new checker into a separate checkout of the original revision above, beside its existing `check_calibration_range.py`. Run before changing helpers; the first small-time analytical fit fails. The raw evidence records the original outputs and corrected rerun.

## Limits and next checkpoint

These helpers remain scalar synthetic-model APIs. Existing price/residual rounding, objective/loss intermediate range and iterative update/stopping behavior are separate obligations; exact aggregation does not repair derivative input errors or certify conditioning. Manuscripts now distinguish actual candidate execution from independent review, supported environments and reviewed release validation.

Twenty-eight selected categories remain partially addressed; none is closed by the register. Independent mathematical/editorial review, release acceptance and canonical approval remain pending.

Next executable item: COV-74 Section 16.10 per-candidate training/holdout metrics and acceptance at each returned optimizer rate. Its current final report retains benchmark metrics rather than independently validating every candidate's residuals.
