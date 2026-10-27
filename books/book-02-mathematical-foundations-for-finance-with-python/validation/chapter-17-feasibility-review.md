# Book 02 — Chapter 17 Feasibility Boundary Review

**Date:** 2026-10-27  
**Scope:** Focused review of the two-asset project cap feasibility and selected existing checks; independent mathematical review and complete chapter coverage remain pending.

The local Chapter 17 code matched tree `1dc2b51d4029987983187e856ff77564ad735cf7` except for the two Section 17.9 files modified in this review. Those changes were published through `10375262e491587f4420214893558b0195db5fa2`.

## Finding and fix

The former implementation accepted caps `(0.5, 0.499999999999995)`, although the computed feasible interval had its lower endpoint above its upper endpoint. It returned weights `(0.5,0.5)` and a passing approximate KKT certificate because the cap violation was within the certificate tolerance. An approximate certificate should not turn an explicitly empty computed feasible interval into an exact feasible problem.

The project now rejects a computed interval where `1.0-cap2 > cap1`, without the previous hard-coded slack. A regression check rejects that example and accepts the exact `(0.5,0.5)` boundary. The certificate remains tolerance-based and reports residuals; a passing certificate does not establish exact feasibility.

**Numerical limit:** This comparison uses binary floating-point subtraction and is not an exact rational or decimal feasibility test. Caps near machine precision, input representation and any business tolerance policy require separate specification and review.

## Evidence

All ten Chapter 17 section check scripts exited zero on Python 3.12.14/Linux from their code directory with a 15-second per-script timeout. This is a script-level run, not a complete coverage, independent review, cross-platform run or book-wide final-revision validation.

## Remaining work

- Specify and independently review feasibility and rounding policy near numerical boundaries, including data expressed as decimal percentages.
- Examine KKT residual scaling, multiplier signs, conditioning, overflow and alternative active-set combinations.
- Review all chapter exercises, objectives and assumptions against independent references; rerun the final agreed revision.
