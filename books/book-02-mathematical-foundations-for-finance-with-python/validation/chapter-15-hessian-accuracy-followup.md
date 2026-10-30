# Chapter 15 — Selected Hessian accuracy follow-up

**Date:** 2026-10-30  
**Inspected revision:** `54c45c471f9135db4147ebc2e504ca1ea62e9dc6`  
**Disposition:** Selected COV-71 accuracy evidence added; implementation unchanged.

## Scope correction and independent oracle

Sections 15.6/15.9 return analytic Hessians; neither exposes a numerical Hessian API. The queued “Hessian finite-difference helper” wording is therefore interpreted as an independent reference benchmark, not validation of an API that does not exist. Existing centered helpers calculate first derivatives/Jacobian columns.

The [new checker](../chapter-15/code/check_hessian_accuracy.py) uses direct Decimal valuation p*exp(r*t) and p*exp(-r*t)/2 at 90-digit precision. It forms diagonal central second differences and four-corner mixed stencils independently of the implementation's Jacobian/Hessian/contraction helpers.

At (p,r,t)=(2,0.125,2), all 18 Hessian entries are checked. Steps 1/16, 1/32 and 1/64 provide a three-point ladder for every entry. Principal-principal curvature is zero and its Decimal stencils must remain below 1e-80. For the sixteen nonzero ordered entries, successive absolute-error ratios relative to the analytic float must lie between 3.9 and 4.1. Richardson extrapolation from the two finer references must agree within relative tolerance 2e-6 and absolute tolerance 1e-12. Off-diagonal symmetric entries are counted separately; they are not eighteen independent mathematical identities.

The Section 15.6 two-by-two rate-time block must equal the future-value subblock returned by 15.9. That cross-module equality is integration evidence, not an additional independent oracle.

## Runtime evidence

All 22 Chapter 15 Python files compiled and all 12 scripts exited zero on Python 3.12.14/Linux with assertions enabled and a 15-second script timeout. All 21 existing source blobs matched the inspected Git tree exactly. [Machine evidence](chapter-15-hessian-accuracy-followup.json) retains hashes, interpreter/platform, paths and raw script outputs.

No defect was confirmed in these selected cases; implementation was preserved. This checker addition follows [V-36](runtime-refresh-2026-10-29-r5.md) and the later Chapter 14 integrations; no refreshed full-book run is claimed.

## Limits and next checkpoint

This is one interior input, two fixed valuation outputs and selected high-precision stencil steps. It does not establish float-stencil cancellation/noise behavior, all step/domain guards, arbitrary input scales, universal convergence or general Hessian accuracy. COV-71 retains those and independent-review obligations. Twenty-five selected categories remain partially addressed; none is closed.

Next executable item: Section 15.9 centered Jacobian-column convergence across principal/rate/time steps, including a selected cancellation/perturbation-asymmetry case. Keep production float evaluations distinct from these supplemental Decimal references.
