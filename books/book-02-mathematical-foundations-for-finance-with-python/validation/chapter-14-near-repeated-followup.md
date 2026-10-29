# Chapter 14 — Repeated and near-repeated eigenpair follow-up

**Date:** 2026-10-29  
**Implementation blob tested:** `4a67b5563998a4b6b933852ec796af3eb905bdea`  
**Disposition:** COV-68 partially addressed; independent review pending.

The [new checker](../chapter-14/code/check_near_repeated_eigenpairs.py) uses matrices ((s,s*epsilon),(s*epsilon,s)). Twelve cases combine scales 1, 1e100 and 1e-100 with epsilon 0, 2^-40, 2^-44 and 2^-50. Independent closed-form eigenvalues are s +/- s*epsilon; above the implementation's gap cutoff, the high-eigenvalue projector has all entries 1/2.

Checks cover those values, sign-invariant projector entries, orthonormality, directly recomputed residual norms and reconstruction error normalized by s. The normalized residual and reconstruction bounds are 1e-14; value comparisons use relative tolerance 5e-16. These tolerances are explicit test bounds for these examples.

At repeated or numerically unresolved gaps the helper intentionally returns coordinate directions. For nonzero epsilon below the cutoff these are approximate eigenvectors, not exact eigenvectors: small normalized residuals/reconstruction error are checked rather than asserting exact directions or identity. This convention should remain visible during independent review.

All 22 Chapter 14 Python files compiled and all 12 check scripts exited zero on Python 3.12.14/Linux, assertions enabled and a 15-second per-script timeout. The local implementation blob matched GitHub; implementation unchanged. This scoped run follows the [third full-book refresh](runtime-refresh-2026-10-29-r3.md).

## Remaining scope

No highly unequal spectra, eigenvalue cancellation fix, exact gap-cutoff transition, adjacent symmetry-policy boundary, near-SPD Cholesky pivot, general determinant/trace range or full numerical stability proof is claimed. These remain COV-68 obligations alongside independent review. Twenty-four selected COV categories are now partially addressed; none is closed by this follow-up.
