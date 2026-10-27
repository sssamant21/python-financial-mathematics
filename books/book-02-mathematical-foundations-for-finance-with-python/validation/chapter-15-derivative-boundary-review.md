# Book 02 — Chapter 15 Finite-Difference Boundary Review

**Date:** 2026-10-27  
**Scope:** Selected Jacobian finite-difference inputs; not comprehensive multivariable or independent mathematical review.

The local Chapter 15 code matched tree `4026d828e4befa95d4bb3da1bf832ab373cec1ca` except for two modified modules and a new regression script. Those files were published through `949cb4588a5c48d84591c5ba02c1e95f91113dc6`.

## Finding and changes

At rate 0.05, a step of `1e-30` rounds both perturbed rates back to the original rate. Sections 15.5 and 15.9 previously returned zero derivative columns even though the analytic rate derivatives are nonzero. Both now reject non-finite or indistinguishable perturbations and reject an overflowing `2*h` denominator.

The new `check_finite_difference_boundaries.py` checks those failures, centered time perturbations outside the domain, ordinary rate derivatives against analytic Jacobian entries, and denominator overflow.

## Runtime evidence

All ten Section 15.1–15.10 check scripts and the new regression script exited zero on Python 3.12.14/Linux from their code directory, with a 15-second per-script timeout. This is scoped script execution, not full mathematical coverage, independent review or cross-platform validation.

## Remaining work

- Analyze actual floating-point spacing and asymmetry of positive and negative perturbations; distinct inputs alone do not guarantee an accurate derivative.
- Independently review covariance symmetry tolerance and its effect on portfolio gradients and Hessians, plus positive-definiteness tests at extreme scales.
- Audit all examples, Hessian formulas, approximations, domains and step-selection guidance; run the full suite on the final agreed revision.
