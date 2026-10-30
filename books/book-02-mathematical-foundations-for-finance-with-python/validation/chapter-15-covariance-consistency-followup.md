# Chapter 15 — Covariance derivative consistency correction

**Date:** 2026-10-30  
**Inspected revision:** `ddb839244c0831b8595dcebe709b4d88316290c4`  
**Correction commits:** `4896c6d9a3e42d3d2046fc451cae4df953c55bf7`, `f5dbc1f92153201ca7fd017db490a6cad4be02af`  
**Disposition:** Selected COV-72 inconsistency corrected; category partially open.

## Confirmed inconsistency

For accepted input ((1e-12,0),(1e-14,1e-12)) and weights (1,1), Section 15.4 returned gradient (2e-12,2.02e-12). The quadratic's gradient should use the symmetric part and equal (2.01e-12,2.01e-12). Section 15.6 returned a nonsymmetric Hessian. Its PD screen also used a different off-diagonal expression than Section 15.4. The absolute symmetry allowance makes this visible at small scales.

The shared validator now replaces both accepted off-diagonal entries with the float-rounded exact midpoint of their represented values. Variance and gradient use that matrix, and Section 15.6 delegates validation to it before computing twice the covariance. A nonfinite determinant rejects explicitly instead of passing an infinity/NaN comparison. Existing symmetry tolerances and positive-definite-only scope remain; singular PSD support is not added.

## Evidence

[Checker](../chapter-15/code/check_covariance_consistency.py): three covariance inputs cover small accepted asymmetry, adjacent off-diagonal floats and exact symmetry. Nine weight/input cases use Fraction quadratic/gradient references on the stated normalized matrix. Hessian symmetry and twice-normalized-covariance entries are exact checks. Shared rejection cases cover singular PSD, indefinite, excessive asymmetry and determinant overflow. The initial checker fails on the original unnormalized covariance.

All 26 Chapter 15 files compiled and all 16 scripts passed on Python 3.12.14/Linux, assertions enabled, 15-second script timeout. [Raw evidence](chapter-15-covariance-consistency-followup.json) retains initial probe/failure, correction commits and all script outputs. This follows [V-37](runtime-refresh-2026-10-30.md); no new full-book pass is claimed.

## Remaining scope and checkpoint

The determinant is still a floating-point screen: near-singular cancellation and underflow, extreme derivatives, covariance units, broader PSD/model assumptions and independent review remain open. Normalization may change rounded outputs for accepted asymmetric inputs; exact symmetric reference cases retain their existing expected behavior. Twenty-six categories remain partially addressed, none closed.

Next executable item: selected covariance determinant underflow/cancellation benchmarks for this shared screen, distinguishing valid mathematical PD inputs from the explicitly limited numerical contract before any further change. Reconcile the maturity and covariance source changes in a full-book refresh after that investigation.
