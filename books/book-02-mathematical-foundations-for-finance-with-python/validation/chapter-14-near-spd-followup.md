# Chapter 14 — Selected near-SPD Cholesky follow-up

**Date:** 2026-10-29  
**Implementation blob tested:** `9152f1cb2b957e08c6d5700c5ca996c9ba06438a`  
**Disposition:** COV-68 remains partially open.

The [new checker](../chapter-14/code/check_near_spd_cholesky.py) uses A=s*((1,1),(1,1+delta)), at s=1,2^40,2^-40 and delta=2^-20,2^-40,2^-52. These nine matrices have exact represented determinant s^2*delta and Schur complement s*delta, verified using Fraction arithmetic.

Checks compare Cholesky entries with (sqrt(s),0;sqrt(s),sqrt(s*delta)), determinant and reconstructed entries. A known solution (1,-1), with exactly represented right-hand side (0,-s*delta), checks backward and forward solution fields and the normalized solve residual. Relative comparison bounds are 2e-15. This selected right-hand side avoids asserting that arbitrary nearly singular solves retain the same forward accuracy.

At each scale, matrices with lower-right multiplier 1 and nextafter(1,0) have nonpositive exact determinants. Both factorization and solve entry points reject all six matrices at the second pivot. The smallest accepted positive delta, 2^-52, is nextafter(1,+infinity)-1.

All 23 Chapter 14 Python files compiled and all 13 check scripts exited zero on Python 3.12.14/Linux, assertions enabled and a 15-second timeout per script. Local/GitHub implementation blob hashes matched; implementation unchanged. This scoped run includes the preceding near-repeated spectral checker and follows the [third full-book refresh](runtime-refresh-2026-10-29-r3.md).

## Limits

Dyadic scales make the first square root and off-diagonal division exact, deliberately isolating the second-pivot boundary. Nondyadic rounding, arbitrary right-hand-side forward error, extreme ranges, unequal eigenvalue cancellation, symmetry-policy boundaries, raw diagnostic norms and independent review remain open. These checks do not establish general stability or close COV-68. Twenty-four selected categories remain partially addressed.
