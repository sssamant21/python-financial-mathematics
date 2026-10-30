# Chapter 15 — Restricted covariance determinant-screen benchmarks

**Date:** 2026-10-30  
**Inspected revision:** `63855e2469721fc25d49e5a7edce49eeffb21008`  
**Disposition:** Selected COV-72 range/cancellation evidence recorded; numerical implementation unchanged.

[New checker](../chapter-15/code/check_covariance_screen.py) distinguishes exact mathematical positive definiteness from the documented finite floating determinant screen shared by Sections 15.4/15.6.

Three exact-PD matrices are rejected by that restricted screen:
- Diagonal entries 2^-600: positive determinant underflows to zero.
- Diagonal entries 2^600: positive determinant overflows.
- Diagonals nextafter(1,+infinity) and nextafter(1,0), off-diagonal 1: exact represented determinant is positive but the float product rounds to 1, yielding zero after subtraction.

Fraction arithmetic independently verifies positive exact determinants and positive first pivots. Rejection therefore means the teaching screen cannot establish acceptance under its stated numerical contract; it does not prove these matrices are mathematically non-PD. This limitation is explicitly documented rather than silently broadening the implementation into a general PD classifier.

Three accepted matrices ((1,1),(1,1+delta)), delta=2^-20,2^-40,2^-52, have exact represented determinant delta. Two singular/indefinite boundary matrices reject. Both covariance and Hessian entry points are checked.

All 27 Chapter 15 files compiled and all 17 scripts passed on Python 3.12.14/Linux, assertions enabled and 15-second script timeouts. The subsequent [V-38 full refresh](runtime-refresh-2026-10-30-r2.md) includes these cases and the prior maturity/covariance corrections; its machine evidence retains exact source hashes and raw outputs.

COV-72 remains partially open for broader conditioning/range, model/unit interpretation and independent review. Twenty-six selected categories remain partially addressed; no category is closed. Next executable item: Chapter 16 COV-73/75 optimizer status and scaling obligations, starting from its coverage map; avoid repeating the completed per-candidate acceptance work.
