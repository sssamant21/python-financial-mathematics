# Chapter 14 — Unequal-spectrum eigenvalue correction

**Date:** 2026-10-29  
**Inspected revision:** `1c7a1327ae5d731c828e3e2bd8bb35cf1849d840`  
**Corrected source commit:** `86fa9f40c56db668a56053c04ead361af39508c1`  
**Corrected source blob:** `55195509b751532d6e00718a75d2c79748b86a98`  
**Disposition:** Confirmed cancellation defect corrected for the selected cases; COV-68 partially open.

## Initial failure and correction

The previous helper returned (1,0) for diag(1,2^-60), although 2^-60 is representable; negative counterparts also lost the small negative eigenvalue. diag(1,5e-324) lost the smallest positive subnormal. The new regression exits 1 on the original source. [Retained raw evidence](chapter-14-unequal-spectrum-followup.json) includes that failure and corrected outputs.

The helper now computes the root of greater magnitude using the trace-plus-signed-gap expression, then recovers the other root as determinant/root. Fraction arithmetic forms the exact determinant of the represented diagonal and averaged off-diagonal entries, avoiding premature determinant-product overflow, underflow or subtraction cancellation during recovery. Returned eigenvalues remain floats sorted descending. Eigenvectors, symmetry policy and report fields are unchanged.

## Independent reference checks

[New checker](../chapter-14/code/check_unequal_spectra.py): 24 diagonal cases combine three large magnitudes, a relatively tiny or smallest-subnormal diagonal entry, two signs and both axis orders. Results must match the known diagonal eigenvalues exactly. Six nonzero-coupling cases use both trace signs and three scales, with independently evaluated 100-digit Decimal quadratic roots; relative value tolerance is 3e-15 and normalized eigenpair-residual bound 2e-15.

All 25 Chapter 14 Python files compiled and all 15 scripts passed on Python 3.12.14/Linux, assertions enabled, 15-second timeout per script. Raw evidence records source hashes and each output. The corrected local source hash matches the published blob. The chapter suite also includes prior near-repeated, near-SPD and restricted-SVD tests.

## Limits and next checkpoint

This scoped correction follows [V-35](runtime-refresh-2026-10-29-r4.md), whose full-book result does not include it. It does not prove general forward accuracy or change the coordinate-direction approximation at unresolved gaps. Raw trace/determinant/residual report ranges and averaging/symmetry boundaries remain open, as do duplicate spectral helpers. Fraction arithmetic adds small exact-arithmetic overhead to this two-by-two teaching helper.

Next executable item: review Section 14.2's duplicate eigendecomposition path against the same unequal-spectrum references, then address or explicitly reconcile its contract. Twenty-five COV categories remain partially addressed; independent reviewer/platform/release acceptance remains pending.
