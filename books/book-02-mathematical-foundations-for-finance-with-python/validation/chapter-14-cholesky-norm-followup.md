# Chapter 14 — Tiny Cholesky reconstruction diagnostic correction

**Date:** 2026-10-29  
**Inspected revision:** `497c651bd1c373a85288d17725b6d94bc9304ddd`  
**Correction commit:** `77d24716bb6eecee028ed507b6ea817110a407ee`  
**Corrected blob:** `b37f9ec77464109992f72a46cf840ee1549e1260`  
**Disposition:** Selected COV-68 diagnostic defect corrected; category partially open.

For matrix 1e-180*((4,2),(2,3)), the old helper reported zero reconstruction error although the represented reconstruction differences have norm 4.280877634782037e-196. Raw squaring underflowed. A second example at scale 1e-250 had the same defect. The original source fails the retained [checker](../chapter-14/code/check_cholesky_tiny_norm.py).

The diagnostic now uses math.hypot; factor construction, pivot acceptance, determinant policy and solves are unchanged. Five cases at scales 1, 1e-100, 1e-180, 1e-200 and 1e-250 compare the norm against a 100-digit Decimal reference formed from exact represented input/reconstruction entries, with relative tolerance 3e-15 and zero absolute slack. Some reconstructions are exactly equal in floating point and legitimately report zero; at least two nonzero cases must remain nonzero. Solve reports must propagate the same factorization diagnostic; their known solution (1,1) is also checked.

All 28 Chapter 14 Python files compiled and all 18 scripts passed on Python 3.12.14/Linux, assertions enabled and 15-second script timeout. [Raw evidence](chapter-14-cholesky-norm-followup.json) retains the failure, probe and corrected outputs. The correction and checker are included in the subsequent [V-36 full refresh](runtime-refresh-2026-10-29-r5.md).

Remaining scope: determinant underflow/overflow, nondyadic near-pivot rounding, arbitrary right-hand-side conditioning, other raw diagnostic copies and independent review. This is a report-norm correction, not general Cholesky stability certification. Twenty-five selected categories remain partially addressed.
