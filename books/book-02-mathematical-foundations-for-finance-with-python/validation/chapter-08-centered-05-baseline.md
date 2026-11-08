# Next checkpoint: Section 8.5 centered-difference copy

Executable revision `67cfc7f76615c8144d200c0b9478547b894fe506`. [Five actual probes, reference values and callback traces](chapter-08-centered-05-baseline.json).

The identity function at x=0 with either sign of maximum-float step returns NaN rather than the exact sampled quotient 1, despite finite perturbations and callback results. A minimum-subnormal step at x=1 collapses both perturbations yet still calls the callback twice and returns zero. A nonfinite upper perturbation calls the callback with infinity before rejecting. The latter two observations retain explicit desired preflight requirements, not two additional numerical defect claims.

The default-step control independently derives the exact quotient from the actual rounded perturbations and represented default step; it is about 0.9999999999998899, not exactly the analytic derivative 1. All traces are actual helper calls. Probes replay identically beside the pinned hash-verified source/dependency; runnable code is in JSON.

Next reconcile the Section 8.5 copy with the guarded Section 8.1 sampled-difference helper while retaining callable-before-controls validation priority, default step 1e-4, callback order/count, finite-result checks and exception propagation. Use independent rational sampled quotients and actual call traces. Resource limits and broader independent review remain open. Do not repeat completed stable exponential quotient or other Section 8.5 analytic examples.
