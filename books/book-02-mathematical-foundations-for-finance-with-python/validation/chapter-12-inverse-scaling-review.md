# Book 02 — Chapter 12 Inverse Scaling Review

**Date:** 2026-10-27  
**Scope:** Selected two-by-two inverse and conditioning boundaries; not comprehensive linear-system or independent mathematical review.

The local Chapter 12 code matched tree `4a5a63c02e5d1b06c1226964f63e4b33c4db16d8` except for two modified modules and a new regression script. Changes were published through `c8d14ec86362c57201f5a123632feb5ba5f0bc70`.

## Finding and correction

Sections 12.6 and 12.7 screened a normalized determinant, then recomputed an unscaled determinant to form the inverse. A scalar identity matrix at scale `1e200` was rejected for determinant overflow, while scale `1e-200` was incorrectly reported singular after determinant underflow. Both matrices have representable inverses and infinity-norm condition number 1.

The examples now form the inverse of the normalized matrix and divide its entries by the matrix scale. The standalone determinant function retains its finite-output contract; this change does not imply every determinant is representable.

New regression cases cover identity matrices at ordinary, large and small scales, a nondiagonal analytic inverse across scales, and rejection of a genuinely singular matrix.

## Runtime evidence

All ten Section 12.1–12.10 check scripts and the new inverse-scaling script exited zero on Python 3.12.14/Linux, each from its code directory with a 15-second timeout. This is not a full book-wide, final-revision or cross-platform validation, and script success does not establish complete mathematical coverage.

## Remaining work

- Independently assess normalized determinant screening, conditioning and inverse-entry overflow/underflow for more general matrices.
- Review Gaussian elimination, pivot thresholds and residual normalizers at extreme scales, including cases where the solution is representable but a diagnostic is not.
- Review all chapter examples and exercises and rerun the final agreed suite on supported environments.
