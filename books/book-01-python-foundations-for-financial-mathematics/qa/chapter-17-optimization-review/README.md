# Section 17.5 — scoped optimization review

Affected baseline: `18b6240459c2480a3bb54793c080177985d0dc9b`. Finding F162, severity medium (educational numerical correctness), owner Book 1 manuscript maintainers. Decision: repair numeric defects, disclose budget normalization and extend generic covariance screening. Reviewer: automated execution plus mathematical/prompt/step review, not external independent acceptance. Corrected revision is the containing publication commit.

One workflow, 40 local answer records and twelve lab steps are separate from four exact-source commands, 52 supplemental predicates and twelve existing unittest methods. Zero historical unique methods added. [results.json](results.json) retains raw stdout/stderr, actual values, tolerances, model inputs, Python/platform/SciPy versions and source/listing SHA256.

From repository root:

```bash
python books/book-01-python-foundations-for-financial-mathematics/qa/chapter-17-optimization-review/review.py
```

Reproduce unchanged-source baseline (expected nonzero exit, requires history):

```bash
python books/book-01-python-foundations-for-financial-mathematics/qa/chapter-17-optimization-review/review.py 18b6240459c2480a3bb54793c080177985d0dc9b
```

[baseline.json](baseline.json) retains seventeen failed predicates; all twelve original methods and the SciPy snippet already passed. Failures include false nonuniqueness at small covariance scale, invalid two-asset PSD accepted at huge/tiny scales, tolerated budget residual amplified into risk, overflowed grid/golden coordinates, tiny asymmetry accepted, positive risk underflow silently reported as zero, repeated grid coordinates and false golden convergence after float-coordinate collapse, and invalid-input exception contracts.

Some baseline predicates exercise explicit additions rather than violations of an existing guarantee: full-matrix PSD screening extends the generic function's disclosed original limitation; `budget_tolerance=0` is a new strict policy control and originally raised unsupported-keyword TypeError. Seventeen failed predicates are not seventeen distinct defects. Initial failure records are retained under the final observer and no observer failures were encountered. Supplemental tests cover singular PSD, zero pivots with/without coupling and a three-asset diagonal benchmark in addition to two-asset scale cases.

## Source execution versus independent expectations

Verbatim reference demonstration/twelve tests, silent import and compilation execute in an isolated temporary directory. A fourth command runs the verbatim SciPy bounded scalar/SLSQP example. A separate execution of that unchanged snippet in a namespace inspects its result objects; five supplemental predicates check analytic optima and feasibility beyond the snippet's original assertions. SciPy 1.17.0 is the installed version, not a cross-version acceptance claim.

For the scalar model f(x)=(x−.3)^2, derivative2(x−.3) and curvature2 establish continuous optimum.3, or boundary.5 on [.5,1]. Grids10/100/1000 and golden search call source exports. The distinct .34 target has coarse winner.3 and refined winner.34. Finite-grid winners are not continuous-optimum certificates. The SciPy vector model x²+2y² with x+y=1 reduces to3x²−4x+2: optimum x=2/3,y=1/3 and objective2/3; independent rational repricing and explicit bounds/budget checks supplement source success flags.

Portfolio fixture Σ=diag(.04,.09), same hypothetical period, long-only fully invested weights. Differentiating .04w²+.09(1−w)² gives w=9/13, variance9/325≈.02769230769. Mean return at means.08/.04 is22/325≈.06769230769. Equal-weight variance13/400=.0325; cap w≤.4 yields boundary w=.4 and variance97/2500=.0388. The1000-subinterval source grid winner is173/250=.692, with variance evaluated independently as (.04)(173/250)²+(.09)(77/250)². No actual market estimates or dates exist; returns, means and covariance use compatible period units.

Covariance validity uses nonnegative diagonal, symmetry and PSD. Full exact rational Schur complements now check arbitrary supplied dimensions, including a zero pivot's necessary zero coupling. The two-asset determinant and nonuniqueness decisions have no absolute variance threshold. Accepted long-only budget residuals within explicit absolute1e−10 are normalized exactly before variance evaluation; strict displayed equality is selectable with tolerance0. Source results still report finite floats, with required nonzero outputs rejecting if unreportable. Float callback values retain their original type for comparisons, preserving integer objective ordering.

Golden search records actual interval reductions, objective evaluations, stopping reason and final interval. The width bound is conditional on unimodality and reliable objective comparisons, not a guarantee for arbitrary multimodal or rounded-flat callbacks. Endpoints remain candidates for boundary minima. Exhausted float coordinates raise rather than claiming convergence at an artificially collapsed interval. Rational coordinate construction prevents intermediate span overflow but cannot create additional representable coordinates.

## Forty local answers

| Exercise | Alignment, derivation and execution boundary |
|---|---|
| 01 | Source golden on (x−3)^2 versus analytic minimum x3/value0. |
| 02 | Completing square4x−x²=4−(x−2)² establishes maximum4 at2; source minimizes negative objective. Cancellation near minimum warrants explicit2e−8 x budget. |
| 03 | Closed feasible interval[0,1]; conceptual domain definition. |
| 04 | Bounds x≥2,x≤1 inconsistent; empty intersection, conceptual. |
| 05 | 2x−6=0 gives3; analytic. |
| 06 | Positive second derivative2 establishes strict minimum at the preceding exercise's stationary point3; curvature alone does not locate a point. |
| 07 | Source grid and golden constrained intervals give boundary.5 within stated budget. |
| 08 | Ten subintervals mean eleven points and spacing.1; source result checked. |
| 09 | Source .34 target coarse-grid winner.3; discrete, not continuous optimum. |
| 10 | Source100-subinterval grid reaches.34, with evaluation count retained. |
| 11 | (sqrt5−1)/2≈.618034; analytic ratio used by source golden. |
| 12 | Unimodality/continuity support interval interpretation; arbitrary multimodal global acceptance not claimed. |
| 13 | x² has second derivative2≥0 throughout R, so convex. |
| 14 | Broad sine interval has multiple extrema; conceptual nonconvex example. |
| 15 | Local minimum need not be global for nonconvex problems; conceptual. |
| 16 | Partial derivatives of x²+y² give(2x,2y); analytic, no gradient export. |
| 17 | Hessian2I positive definite; analytic, no Hessian export. |
| 18 | PSD covariance makes quadratic variance convex; source full PSD screening now explicit. |
| 19 | Fully invested budget equality, source normalized tolerated residual or strict policy; no hidden relative tolerance. |
| 20 | Long-only inequalities enforced by source portfolio variance. |
| 21 | wA≤.4 is an upper bound; analytic cap projection/supplemental source variance, not a general policy engine. |
| 22 | Source two-asset GMV weight independently matches9/13 at ordinary and huge/tiny scales. |
| 23 | Supplemental exact expected return22/325=.88/13. No source mean-return export exists here. |
| 24 | Source GMV variance versus exact9/325; independent finite-grid value separately checked. |
| 25 | Source rejects covariance.1 because its square exceeds.04*.09. |
| 26 | Determinant0 and nonnegative diagonal prove PSD; source singular-matrix equal-weight variance1/16 checked. |
| 27 | Source exact denominator0 flags nonunique for identical variance/covariance.04; every budget mix risk.04 analytically. |
| 28 | Weight.5 violates cap.4; conceptual policy rejection, not implemented by generic variance function. |
| 29 | Finite penalty may allow constraint violations; conceptual, no penalty solver implemented. |
| 30 | L=f+λh is equality Lagrangian; analytic convention reviewed. |
| 31 | Active bound can offset objective gradient under KKT; conceptual preview. |
| 32 | Dollars/weights need deliberate scaling; scale probes exercise numerical invariance, not a calibrated mixed objective. |
| 33 | Gradient stopping alone does not establish feasibility/optimality; exact SciPy result checked against independent constraints/objective. |
| 34 | Small finite-difference h trades truncation for roundoff; conceptual, no finite-difference routine exported. |
| 35 | Derivative2(x−.3), analytic scalar benchmark. |
| 36 | Estimated covariance uncertainty remains input/model risk; no actual history or statistical confidence claim. |
| 37 | Spread/fees can change net-optimal trades; conceptual, no trading-cost optimizer. |
| 38 | Source/listing hashes, environment, bounds, methods, model and outputs retained; deterministic local execution only. |
| 39 | Source SciPy success supplemented by bounds/budget/objective checks; economic suitability open. |
| 40 | Analytic convex quadratics supply independent test oracles rather than merely solver agreement. |

## Twelve lab steps and prerequisite contracts

Prerequisites: Python; callable finite int/float objectives; representable ordered float coordinates; positive integer grid steps/iteration budget and positive golden tolerance; unimodality for interval guarantees. Portfolio quantities must share a horizon, covariance must be symmetric PSD, weights long-only and budget-valid. SciPy is optional for step11 and installed here. Notebook/environment installation acceptance is not inferred.

| Step | Actual output and limit |
|---|---|
| 1 | Verbatim listing saved in temporary directory; runtime and hashes recorded. |
| 2 | Supplemental derivative and curvature establish analytic.3. |
| 3 | Source10-subinterval grid minimum.3, spacing.1, eleven evaluations. |
| 4 | Source100/1000-subinterval refinements retained, and separate .34 target illustrates resolution differences. |
| 5 | Source golden result compared with.3 within absolute1e−10; interval and iteration/evaluation counts retained. |
| 6 | Source grid/golden [.5,1] versus boundary.5. |
| 7 | Source equal-weight variance.0325 versus13/400. |
| 8 | Source two-asset weights versus rational9/13 and complement4/13. |
| 9 | Source portfolio grid(.692) and independent finite-grid risk are distinct from continuous optimum9/13 and risk9/325. |
| 10 | Source invalid two-asset PSD errors at ordinary/tiny/large scales; generic full-matrix negative-direction and pivot cases separate. |
| 11 | Verbatim SciPy bounded/SLSQP snippet runs; separate result inspection checks analytic scalar/vector optima and feasibility. |
| 12 | Four exact commands,52 supplemental predicates and twelve existing methods pass; seventeen baseline failed predicates retained. |

## Remaining scope and resume checkpoint

Local Linux CPython/SciPy only. No production portfolio optimizer, general mandate/sector/turnover constraints, transaction costs, covariance estimation acceptance, nonconvex global proof, arbitrary conditioning guarantee, performance benchmark, broad shared-input integration, notebook/platform validation, or external independent reviewer/certification. Exact source exports, supplemental analytic calculations and conceptual designs are distinct above. F28/F32 and every unresolved tracker finding remain open.

Chapter17 has five core workflows and195 local answers scoped. Next: Section17.6 — Constrained Optimization. Resume from fresh main without duplicating this batch.
