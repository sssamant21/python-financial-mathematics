# Book 02 — Chapter 16 Optimization Stopping Review

**Date:** 2026-10-27  
**Scope:** Selected scalar line-search and convergence behavior; not a complete chapter or independent optimization review.

The local Chapter 16 code matched tree `169bd5ea85c96c6417c14fb8a6c354502363b31a` except for two modified Section 16.5 files. Those changes were published through `8b2de08b9ae3520ea9d75f7ef66fc246ee92df4f`; the manuscript was subsequently clarified.

## Finding and fix

At `x=1.0` with gradient 1 and initial step `1e-20`, floating-point rounding makes the trial equal the current point. Previously the Armijo example reported **accepted** even though no move occurred. It now reports **stagnation**. An accepted step must also show a strict decrease in the computed objective, so rounding a sufficient-decrease threshold back to the original objective cannot silently accept a flat computed value.

Added regression cases for an unchanged trial and a flat computed objective. This conservative policy does not prove that the exact objective cannot decrease; it describes the observed floating-point result.

## Evidence

All ten Section 16.1–16.10 check scripts exited zero on Python 3.12.14/Linux from their own directory with a 15-second timeout. This is a script-level run on a scoped local snapshot, not independent review, comprehensive coverage or a full book-wide final-revision run.

## Remaining work

- Review gradient descent and Newton routines for explicit stagnation diagnostics; some currently run until their iteration limit when an update rounds to the same point.
- Independently assess Armijo arithmetic, overflow, cancellation, inconsistent user-supplied gradients and near-stationary stopping.
- Review the earlier Section 16.7 polynomial-difference change and all chapter exercises, tolerances and assumptions.
- Rerun the final exact revision on supported environments.
