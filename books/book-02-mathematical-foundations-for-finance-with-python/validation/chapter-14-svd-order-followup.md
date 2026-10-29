# Chapter 14 — Restricted SVD factor-order follow-up

**Date:** 2026-10-29  
**Implementation blob tested:** `44f150d74f9a2ac16012a2c23dd181b2e1d81b06`  
**Disposition:** COV-67 partially addressed; independent review pending.

The [new checker](../chapter-14/code/check_svd_factor_order.py) tests diagonal-column magnitudes (3,2), (2,3), (2,2), (3,0), (0,3) and (0,0), each at rank tolerance 0 and 2. These twelve cases assert left/right direction orthonormality, full matrix reconstruction, sorted singular-value summary, positions, achieved exposures, signed residuals, objective, threshold rank and exact full-column-rank condition convention.

The helper's existing directions remain in factor order. Reconstruction therefore pairs the first direction with the first input magnitude and the second with the second input magnitude. The separately sorted singular-values field is a summary, not a matched list of direction/value triples. In particular, blindly zipping sorted values with factor-order directions gives the wrong matrix for (2,3). Implementation and output convention are unchanged.

Thresholding uses magnitude > tolerance, including exact boundary magnitude 2. Full-matrix reconstruction uses both original magnitudes even when a direction is omitted from the thresholded solve. A positive dropped singular value may coexist with a finite full-column-rank condition number; threshold rank and exact condition are separate diagnostics.

All 24 Chapter 14 Python files compiled and all 14 check scripts exited zero on Python 3.12.14/Linux, assertions enabled and a 15-second timeout per script. The local implementation blob matched GitHub. This scoped run includes the recent spectral/Cholesky checkers and follows the [third full-book refresh](runtime-refresh-2026-10-29-r3.md).

## Limits

This verifies only the stated nonnegative diagonal-column 3x2 helper, not a general SVD. Copied-reference reports in 14.8/14.10, general solver integration, broader numerical ranges and independent review remain open under COV-67 and related categories. Twenty-five selected COV categories are now partially addressed; none is closed here.
