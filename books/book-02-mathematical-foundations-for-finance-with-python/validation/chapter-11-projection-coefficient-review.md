# Book 02 — Chapter 11 Projection Coefficient Review

**Date:** 2026-10-27  
**Scope:** Selected vector projection numerical range; not comprehensive exposure-model coverage or independent mathematical review.

The local Chapter 11 code matched tree `37d212d01a3a6da7eb49058629a03a7b3c512b09` except for the modified Section 11.6 module and a new regression script. Those changes were published through `9c5073f5bdb9987553c7af398ba0d1be09665254`.

## Finding and correction

For vector `(1,1)` and direction `(1.5e308,1.5e308)`, the projected vector was approximately `(1,1)`, but the reported coefficient was zero. The calculation formed the direction norm as a product that overflowed to infinity before division. The correct coefficient is approximately `6.66666666666667e-309`, which is representable.

The calculation now divides by the normalized direction length and then the maximum component. New checks verify the analytic coefficient, the projected vector, sign reversal and continued rejection of a zero direction.

## Runtime evidence

All ten Section 11.1–11.10 check scripts and the new projection-coefficient script exited zero on Python 3.12.14/Linux. Each was run from its code directory with a 15-second timeout. This scoped result does not establish whole-book, cross-platform or independent review completion.

## Remaining work

- Assess coefficient underflow/overflow, scalar projection cancellation and relative-distance calculations when unnormalized norms exceed the floating-point range.
- Review the earlier angle-computation change, unit alignment and financial assumptions in the exposure project.
- Complete example/exercise coverage and independent mathematical review; rerun the final agreed revision.
