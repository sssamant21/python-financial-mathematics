# Book 02 — Chapter 14 Decomposition Boundary Review

**Date:** 2026-10-27  
**Scope:** Selected Cholesky input handling and Frobenius-error numerical behavior; not comprehensive decomposition validation or independent mathematical review.

The local Chapter 14 code matched tree `7844a56b32490f94a82ff0820a3db1640825be92` except for two modified modules and a new regression script. Those files were published through `0d7074b6ea1866034f89f9839ca60ed56f8b7214`.

## Findings and fixes

1. The Frobenius-error function squared differences before taking a square root, so a one-element difference of `1e200` raised overflow although its norm is representable; `1e-200` could underflow. It now uses the scaled `math.hypot` calculation. Unrepresentable differences or norms still produce a numerical failure.
2. The Cholesky solve accepted a matrix iterator for factorization but tried to iterate it again for residuals, causing an IndexError after consumption. It now materializes rows once and reuses them.
3. The new regression script checks large and small representable norms, a known 3–4–5 norm, unrepresentable output, iterator input and invalid shape.

## Evidence

All ten Section 14.1–14.10 check scripts and the new decomposition-boundary script exited zero on Python 3.12.14/Linux from the code directory with a 15-second timeout. This is not complete numerical coverage, an independent review, a cross-platform run or a full final-revision book-wide validation.

## Remaining work

- Review other direct sum-of-squares calculations, including the Cholesky reconstruction error, for extreme-range overflow and underflow.
- Independently assess positive definiteness, symmetry, eigenvalue classification, reconstruction tolerances and conditioning.
- Audit remaining exercises and examples and rerun the full suite against the final exact revision and supported environments.
