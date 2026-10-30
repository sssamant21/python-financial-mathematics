# Chapter 14 — Final assessment computed integration follow-up

**Date:** 2026-10-30  
**Inspected revision:** `92f746af05de331c50676a2bf07f988be7187b4c`  
**Implementation commit:** `c0654f9646812da727bea484cd2e16bc77a5f7d4`  
**Implementation blob:** `176dd7db2b15bd9218f7b195a1ce48da3517c9b2`  
**Disposition:** Selected COV-67 final-report integration gap addressed; category partially open.

## Before and after

Section 14.10 previously returned several literal eigenvalues/factors/singular summaries and reference positions. Those correct fixed reference numbers did not establish integration with chapter solvers. The new integration checker fails against that original source because the eigen helper is never called; this is an evidence gap, not a claim that the original numeric answers were wrong.

The assessment now calls the actual eigenpair, covariance Cholesky, restricted diagonal SVD and low-rank helpers. It recomputes reconstruction/approximation errors from returned factors/matrices and residuals from returned positions and exposures. Eigenvalues, matrix determinant, singular summaries, rank, condition and retained energy propagate helper results. Quadratic and portfolio arithmetic remain explicit fixed-input calculations. The Hessian is calculated from twice the input matrix. Existing result fields remain and calculation_source identifies computed_teaching_helpers.

## Verification

The existing final-assessment checker still verifies known values: eigenvalues (3,1), quadratic 14, covariance variance 0.0336, Cholesky entries, singular values (4,2), positions (2,2), residual (0,0,5), objective 12.5 and rank-one error/energy 2/0.8.

[New integration checker](../chapter-14/code/check_final_spectral_integration.py) observes four actual helper calls and detects five scoped corruptions: wrong eigenvalues, wrong Cholesky factor, zero positions, wrong singular values and zero rank-one approximation. Each mutation is restored after its test.

All 30 Chapter 14 Python files compiled and all 20 scripts passed on Python 3.12.14/Linux, assertions enabled and 15-second timeout per script. [Raw evidence](chapter-14-final-integration-followup.json) retains the original integration failure and corrected outputs. This follows [V-36](runtime-refresh-2026-10-29-r5.md); no new full-book runtime is claimed.

## Remaining scope and next checkpoint

This completes the selected Section 14.8/14.10 computed-helper wiring obligation, not all COV-67 coverage, general solver behavior, full exercise proofs, range analysis or independent review. Twenty-five selected categories remain partially addressed. Section 14.6 remains a restricted diagonal-column SVD, not a general factorization.

Next executable item: Chapter 15 COV-71 selected Hessian finite-difference accuracy/convergence benchmarks and representability guards, guided by its coverage map before extending scope. Refresh full-book runtime after further related implementation changes accumulate; reviewer, environment and release gates remain open.
