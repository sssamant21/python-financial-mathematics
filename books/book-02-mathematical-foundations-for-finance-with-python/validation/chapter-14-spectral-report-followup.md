# Chapter 14 — Spectral report integration and diagnostic correction

**Date:** 2026-10-29  
**Inspected revision:** `ac223164d72403638340a7ef60cd099ab30e5f8e`  
**Corrected source commit:** `bef5acefa1aaaddec27ae4082532129b04792cd0`  
**Corrected blob:** `d3966571868a9bfdc55578f5c5d58bbbc389bbcc`  
**Disposition:** Two selected report defects corrected; COV-68 remains partially open.

## Investigation and failures

Section 14.2 imports Section 14.1's eigenpair helper; the earlier checkpoint's “duplicate spectral path” wording meant the downstream path, not a separate eigensolver. Six exact diagonal integration cases now confirm that Section 14.2 retains the small roots fixed in the preceding follow-up, including the smallest positive subnormal and negative counterparts.

Two additional failures were reproduced. A one-shot matrix iterator was consumed by the eigenpair helper, then read again for reconstruction diagnostics, raising IndexError. For ((1e-200,1e-215),(1e-215,1e-200)), the reported reconstruction error was zero while direct hypot of its represented reconstruction differences was 2.166275824600653e-215. Squaring those differences had underflowed.

The implementation now materializes matrix/row iterables once, validates the resulting snapshot through the shared helper and reuses it for diagnostics. Reconstruction and orthogonality norms use math.hypot instead of sqrt(sum of raw squares). Eigenvalue, symmetry and unresolved-gap policies are unchanged.

## Evidence

[New checker](../chapter-14/code/check_spectral_report_range.py) covers six small-root integration cases; two valid one-shot forms matching the sequence result; two malformed iterator shapes rejected with ValueError; and three scale cases whose nonzero reconstruction norms are compared with independently computed 100-digit Decimal sums of squares. Relative norm tolerance is 3e-15 without absolute slack. The checker fails on the original source at the iterator case.

All 26 Chapter 14 Python files compiled and all 16 scripts passed on Python 3.12.14/Linux, assertions enabled and a 15-second timeout per script. [Raw evidence](chapter-14-spectral-report-followup.json) retains the initial traceback, tiny-error probe, corrected outputs and source commits. This is a scoped pass after [V-35](runtime-refresh-2026-10-29-r4.md), not a new full-book pass.

## Remaining scope and checkpoint

The eigen helper still limits trace/determinant report range, averaging and symmetry behavior; downstream subtraction and other raw norms remain separate obligations. General stability, all iterator/input classes, platform support and independent review are not established. Twenty-five selected categories remain partially addressed; none is closed.

Next executable item: Section 14.1 off-diagonal averaging and exact-versus-tolerant symmetry boundary, using adjacent represented inputs and explicit report-range expectations before any fix. Then reconcile other shared consumers.
