# Book 02 — Chapter 8 Finite-Difference Denominator Review

**Date:** 2026-10-27  
**Scope:** Selected finite-difference step representation and denominator boundaries; not comprehensive derivative coverage or independent mathematical review.

The local Chapter 8 code matched tree `840bd6d123258a0dfbff4967765f38536d37e17e` except for four modified modules and a new regression script. Changes were published through `371191abd1da165783d0ea5920c966a47b072263`.

## Findings and corrections

A positive, representable step can have a squared step that rounds to zero. At x=0 and h=1e-200, several second-difference examples raised an incidental ZeroDivisionError rather than rejecting an unusable numerical control. A very large step can instead overflow its squared denominator.

Sections 8.6, 8.8, 8.9 and 8.10 now check the relevant squared denominator before calculation. Selected routines also reject non-finite or unchanged perturbations, and Section 8.8's centered first difference rejects a non-finite doubled step. Section 8.9 applies its squared-denominator requirement only when a second derivative is requested.

New checks exercise tiny and huge squared steps, unchanged perturbations, an ordinary analytic quadratic derivative, and doubled-step overflow.

## Runtime evidence

All ten Section 8.1–8.10 check scripts and the new denominator-regression script exited zero on Python 3.12.14/Linux, from the code directory with a 15-second per-script timeout. This includes the earlier corrected Section 8.10 check. It is not a full book-wide or cross-platform run and does not establish independent mathematical review.

## Remaining work

- Review first-derivative denominator and perturbation guards in the other standalone Chapter 8 examples for consistency.
- Assess rounding asymmetry, numerator overflow/cancellation, and accuracy of chosen steps; representable controls alone do not ensure accurate derivatives.
- Review formulas, exercises and floating-point error budgets independently and rerun the final agreed revision.
