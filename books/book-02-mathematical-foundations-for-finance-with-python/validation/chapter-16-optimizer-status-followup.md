# Chapter 16 — Selected optimizer status and Armijo follow-up

**Date:** 2026-10-30  
**Inspected revision:** `368236de3380a3b864b8a9b791e40444919a7604`  
**Disposition:** COV-73 partially addressed; implementation unchanged.

[New checker](../chapter-16/code/check_optimizer_status_contract.py) uses f(x)=a*x^2/2, x=1 and c=1/4. The exact Armijo upper step bound is 2*(1-c)/a=1.5/a. For a=1,2,8, the represented boundary and its predecessor are accepted and its successor is rejected with zero backtracking budget: nine adjacent cases. Fraction arithmetic independently verifies accepted trial objectives against the sufficient-decrease RHS and strict-decrease requirement.

A separate initial-step-one case at a=2 backtracks once to step 1/2 and reaches zero. Budget B=2 at initial step 8 evaluates base x=1 and trial points -15,-7,-3 before failure; this explicitly distinguishes backtracking reductions from objective-call counts.

Other real-helper cases cover stationary and representational stagnation Armijo returns; exact fixed-step history (1,1/2,1/4) ending at its two-iteration budget; immediate fixed-step stationarity; double-well no_descent at the unchanged start with zero accepted iterations; and a one-iteration local-descent budget. These do not cover every optimizer copy or failure path.

All 21 Chapter 16 Python files compiled and all 11 scripts passed on Python 3.12.14/Linux with assertions enabled and 15-second timeouts. All 20 existing source blobs matched the inspected tree exactly. [Machine evidence](chapter-16-optimizer-status-followup.json) retains hashes and raw outputs. No implementation defect was found in these selected cases. This checker addition follows [V-38](runtime-refresh-2026-10-30-r2.md), not a new full-book run.

COV-73 remains partially open for other copies, report/count details, boundary families and independent review. Twenty-seven selected categories are now partially addressed; none is closed by this follow-up. Next executable item: Section 16.7's multistart/best-observed results against independent stationary-cubic roots and local classification, retaining the distinction from a global-optimum certificate.
