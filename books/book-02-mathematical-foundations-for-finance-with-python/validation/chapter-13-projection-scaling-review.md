# Book 02 — Chapter 13 Projection Scaling Review

**Date:** 2026-10-27  
**Scope:** Selected line-projection numerical boundaries; not comprehensive least-squares coverage or independent mathematical review.

The local Chapter 13 code matched tree `b2bad41b584a483077fcd6a34b0644c7fb6e14eb` except for the modified Section 13.4 module and new regression script. Those changes were published through `e483f6c8294f4f86af5cbc7cd0475c20c9e8556e`.

## Finding and correction

The original line projection calculated the direction's squared norm directly. Directions proportional to `(1e200,2e200)` were rejected because squaring overflowed, while `(1e-200,2e-200)` were misclassified as zero because squaring underflowed.

The implementation now scales the direction by its largest absolute component before forming the norm and dot product, computes the projection in those coordinates, and converts the reported coefficient back to the original direction's scale.

For target `(3,7)` and line direction `(1,2)`, the independently derived projection is `(3.4,6.8)`, the coefficient is 3.4, and residual distance is `sqrt(0.2)`. New regression cases verify those values under positive large, positive small and negative direction rescaling; zero directions remain rejected.

## Runtime evidence

All ten Section 13.1–13.10 check scripts and the new projection-scaling script exited zero on Python 3.12.14/Linux. Each was run from its code directory with a 15-second timeout. This scoped run does not certify the chapter, measure complete coverage, or establish a final book-wide revision.

## Remaining work

- Assess large targets, dot-product cancellation, and coefficient range; a projected vector can be representable even when its coefficient is not.
- Review the scale-dependent direction-dot-residual diagnostic and define a normalized residual criterion where appropriate.
- Independently review QR rank screening, weighted scaling, rank-deficient cases, objectives, examples and exercises.
- Rerun the final agreed suite on the exact revision and supported environments.
