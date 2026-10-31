# Book 02 — Section 18.6 interpolation-bound follow-up

**Date:** 2026-10-30  
**Baseline:** `2699a635954916d388d9a7b6e9191973cb9d0997`  
**Pinned executable source:** `7678af6b436748470a1a1798256d8fd546bcbade`  
**Disposition:** Selected COV-80 oracle evidence; helper unchanged; independent review pending.

For f(x)=ax^2+bx+c and its endpoint linear interpolant L on[A,B], direct expansion gives L(q)-f(q)=a(q-A)(B-q). For q inside the interval, absolute error is at most |a|(B-A)^2/4=M(B-A)^2/8 with M=2|a|. Equality holds at the midpoint; endpoint errors vanish. Halving interval width divides maximum error by four. These exact quadratic identities provide selected test references, not a general smoothness proof for arbitrary callbacks.

The [runnable checker](../chapter-18/code/check_interpolation_bound.py) uses independent Fraction expressions for five signed/zero curvature coefficients, four intervals and five quarter-grid positions:100 exact value/error/bound checks. The dyadic inputs and moderate magnitudes make the selected floating results exact. Sixteen additional half-width midpoint queries verify the factor-four relation. An explicit extrapolated point has signed error-16, exceeding the in-interval bound2; the interpolation guarantee is not extended outside its hypotheses.

Three wrong interpolation functions (left endpoint everywhere, midpoint everywhere and doubled slope) are detected. The first checker run passed against the unchanged Section18.6 helper; there was no numerical defect or correction to conceal. [Machine record](chapter-18-interpolation-bound-followup.json) retains that initial run, exact manifest, environment, commands and scoped outputs.

All24 Chapter18 Python files compiled and14 check/test scripts passed on Python3.12.14/Linux, assertions enabled, separate processes, timeout15 seconds. All24 source hashes match the pinned tree and remained unchanged after execution. Section18.6 helper blob `4aaf3667704d6b8cdd1f952f50962a8a5ed0937b`.

This one-checker addition follows [V-48](runtime-refresh-2026-10-30-r12.md):484 compiled files/273 scripts/485 required hashes at its earlier pin. Current inventory is485 Python files/274 check-test scripts, not a new full execution. The full runtime remains applicable to its recorded source revision; later report/tracker writes are outside executable inputs.

Scope is selected exact dyadic quadratic/affine data. General interpolation conditioning, arbitrary smooth-function error estimates, input/result range, financial curve modeling, derivative-step studies and quadrature orders remain open. COV-80 stays partially addressed. Twenty-nine selected categories remain partially addressed; none closed by the register. Independent mathematics/editorial review, supported environments, final reviewed-release validation and canonical approval remain pending.

Next substantive item: COV-80 Section18.7 measured quadrature-order and derivative-step evidence: selected exact signed trapezoid/Simpson error ladders and three-step first/second sensitivity checks, rather than error decrease alone.
