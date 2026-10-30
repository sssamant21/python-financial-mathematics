# Chapter 16 — Independent multistart reference follow-up

**Date:** 2026-10-30  
**Inspected revision:** `daff965e899612c8330f8e71499bbb356bf281f3`  
**Disposition:** Selected COV-73/75 evidence added; implementation unchanged.

[New checker](../chapter-16/code/check_multistart_references.py) independently brackets three stationary roots of 4*x^3-4*x+tilt, using 80-digit Decimal bisection with 210 iterations and tilt equal to the exactly represented float 0.2. Brackets are [-1.2,-0.8], [0,0.2] and [0.8,1.2]. Second derivative 12*x^2-4 classifies the outer roots as local minima and the middle as a local maximum.

All four default multistart outputs satisfy gradient_tolerance and lie within 2e-10 of an independently computed outer root; both wells are reached. Their objective values are recomputed with Decimal arithmetic within 2e-15 relative/absolute tolerances, and direct gradient magnitudes are below 1.01e-9. Best observed matches the negative-root well, whose independently computed reference objective is lower than the other sampled stationary values.

A real start at 10 produces no_descent under default controls. A pool containing only that start returns best_observed=None; a mixed failed/successful pool chooses a successful result. No mocked solver is used. Starting at the rounded middle root gives gradient_tolerance despite negative curvature, explicitly demonstrating that the status does not certify a minimum.

All 22 Chapter 16 Python files compiled and all 12 scripts passed on Python 3.12.14/Linux, assertions enabled and 15-second timeouts. All 21 existing source blobs matched the pinned tree exactly or after verifying removal of one local trailing newline. [Raw evidence](chapter-16-multistart-reference-followup.json) retains source hashes and script outputs. This checker follows [V-38](runtime-refresh-2026-10-30-r2.md), not a new full-book runtime.

These selected roots/classifications are numerical reference evidence, not a general global optimizer proof, exhaustive basin analysis or independent reviewer sign-off. Implementation and global_optimality_certified=False are preserved. COV-73/75 remain partially open; twenty-eight selected categories are now partially addressed.

Next executable item: Section 16.7 scaling transforms, condition-number claims and stable-step bounds against independently derived diagonal Hessians, keeping parameter and objective units explicit.
