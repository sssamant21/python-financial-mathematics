# Section 17.12 — scoped convergence/error review

Affected baseline: `4c6a7c1eb7dc519eb46379fa1e59c93b2e6f8f02`. F169, severity medium (educational numerical correctness), owner Book 1 manuscript maintainers; decision repair scale/coordinate/finite-report contracts without turning diagnostics into unconditional bounds. Reviewer: automated execution and mathematical/prompt/step review, not external independent acceptance. Corrected revision is the containing publication commit.

One workflow,40 local answer records and twelve lab steps are separate from five exact-source commands,48 supplemental predicates and **eight** existing unittest methods. Zero historical unique methods added. [results.json](results.json) retains runtime/platform/SciPy, raw stdout/stderr, input model, values/tolerances, lab bracket/refinement/sensitivity records and source/listing SHA256.

From repository root:

```bash
python books/book-01-python-foundations-for-financial-mathematics/qa/chapter-17-convergence-review/review.py
```

Reproduce unchanged source (expected nonzero exit; requires history):

```bash
python books/book-01-python-foundations-for-financial-mathematics/qa/chapter-17-convergence-review/review.py 4c6a7c1eb7dc519eb46379fa1e59c93b2e6f8f02
```

[baseline.json](baseline.json) retains16 failed predicates; original eight methods and both SciPy examples already passed. Defects include midpoint/span/weighted-sum overflow, error-estimate difference overflow, tiny-order denominator cancellation, high-order conversion overflow despite finite estimate, derivative numerator overflow, collapsed derivative coordinates, nonfinite/boolean callbacks and invalid-input exception contracts. Strict typed callback/coordinate/order checks are explicit contract tightening. Sixteen predicates are not16 distinct defects. No observer failures occurred.

## Exact execution and independent expectations

Five isolated commands execute the verbatim eight-method reference, silent import, compilation, printed SciPy root_scalar snippet and printed quad snippet. A separate execution of those unchanged snippets in a namespace supports three independent root/repricing/integration checks; its stdout is retained. SciPy's error estimate is not a guaranteed actual error bound. No supplemental root/quadrature/derivative solver substitutes for source execution.

Fictional one-period price100 and future cashflow110 imply exact annual effective yield1/10. Residual f(y)=110/(1+y)−100 has f(0)=10, f(.2)=−25/3. Source bisection at width tolerances1e−6,1e−9,1e−12 retains estimate/bracket/halving counter/residual, actual float midpoint radius and conversion to basis points. Known-root error is compared in rate units, not currency. Earlier callback-zero termination may collapse a numerical bracket without proving that the ideal financial model has exactly that root. Continuity/accurate signs remain caller assumptions.

A width1 interval after ten ideal halvings has width1/1024 and midpoint bound1/2048, or625/128=4.8828125 basis points. In actual float reporting use max(x−a,b−x) for radius, which includes midpoint rounding rather than blindly half-width. `bisect` tuple counter is earlier interval halvings; midpoint evaluations are normally counter+1, endpoints0. Width convergence, callback zero, iteration exhaustion and stagnation have distinct meanings; failures raise rather than returning unconditional success.

For ∫x² on[0,1], source trapezoids n2/4/8 are matched against T_n=1/3+1/(6n²). Independent exact errors1/24,1/96,1/384 show factor4. The source estimate |T4−T2|/(2²−1)=1/96 matches fine error for this polynomial; it is not a general error certificate. Numeric stresses use exact rational expected |1e308−(−1e308)|/3, a tiny order p1e−308 with finite ratio1e−308/(2^p−1), and p2000 with finite estimate1e308/(2^2000−1), independently evaluated using Decimal1000.

Price sensitivity at y=.1 has true derivative−110/(1.1²). At an ideal central step h the finite secant slope is−110/(1.1²−h²), a different value. Source h=.01,.001,.0001 results are compared to that finite-step formula, with recorded1e−8 relative budget for callback/node rounding. Reported node separation, not unrounded2h, is used in the source denominator; a collapsed step rejects. Derivative units are currency per decimal yield; multiply by.0001 for a first-order one-basis-point price change under that convention. No production DV01 or market schedule implementation is claimed.

Supplemental rational materiality/error-budget calculations preserve units: .01 per unit×1e6=10000; price error.01/sensitivity100 gives yield error.0001=1bp; two valid additive absolute bounds.01+.02 sum conservatively to.03. Those arithmetic examples do not validate the assumptions behind any actual error budget.

## Numeric and interpretation contracts

Inputs/callbacks are finite Python int/float, booleans excluded. Float coordinates must retain integer identity. Rational binary endpoint construction and distinct grid checks prevent tested span/repetition failures; callback integer/displayed-decimal values are weighted/subtracted rationally before finite float reports. Required nonzero computed reports may not silently underflow. Fine-error denominator2^p−1 uses scale-aware Decimal guards; no proof of asymptotic order or arbitrary correctly rounded transcendental behavior follows.

A small residual can coexist with large root error: (1.01−1)^3=1e−6 while root error.01. A fixed-grid method may converge to the wrong model. Richardson agreement, small solver step, finite-difference result, positive success status and seeded simulation are evidence only within their assumptions. No Monte Carlo generator/error estimator, optimizer, independent holdings validator or market instrument scheduler is exported here.

## Forty worked-answer records

| Exercise | Alignment and execution boundary |
|---|---|
| 01 | Supplemental exact price absolute error100.02−100=.02. |
| 02 | Supplemental relative error.0002=.02%; not2%. |
| 03 | Zero-reference relative division undefined; conceptual absolute-scale requirement. |
| 04 | Exact ideal ten-halving width1/1024. |
| 05 | Exact ideal midpoint bound1/2048; actual reported midpoint radius separately retained. |
| 06 | .0001 decimal yield=1bp; bound conversion executed. |
| 07 | Supplemental rational flat-function residual1e−6. |
| 08 | Supplemental root error.01, distinct units from residual. |
| 09 | Source one-period yield versus1/10. |
| 10 | Price100.10−100=.10 currency residual; actual f(0)/f(.2) source checks separate. |
| 11 | Source n2 trapezoid3/8=.375. |
| 12 | Source n4 trapezoid11/32=.34375. |
| 13 | Actual rational error ratio4 checked. |
| 14 | Source Richardson/fine estimate1/96, polynomial-specific independent expectation. |
| 15 | O(h²) leading error quarters only in assumed smooth asymptotic regime; conceptual. |
| 16 | Smooth forward difference ordinarily O(h); no forward-difference export here. |
| 17 | Smooth central difference ordinarily O(h²); finite-step source price examples checked. |
| 18 | Source tiny-step collapsed-coordinate rejection; callback cancellation remains possible. |
| 19 | IID finite-variance standard error scales1/sqrtN, so4N halves it; conceptual, no Monte Carlo run. |
| 20 | More paths do not remove model bias; conceptual. |
| 21 | Source float-coordinate stagnation raises; unchanged step alone not success. |
| 22 | Optimization feasibility required independently; conceptual, no optimizer export. |
| 23 | Sign change implies conditional existence, not uniqueness; conceptual. |
| 24 | Wrong coupon date can yield wrong model despite small residual; no schedule acceptance. |
| 25 | Supplemental aggregate materiality10000. |
| 26 | Price residual currency versus decimal-yield tolerance explicit in source lab. |
| 27 | Continuity needed for root existence; code cannot certify arbitrary callbacks. |
| 28 | Newton quadratic convergence local under assumptions; no Newton export here. |
| 29 | Independent yield, polynomial integral, sensitivity and Decimal benchmarks executed. |
| 30 | Similar refinements can share bias; no generic correctness certificate. |
| 31 | Nominal statistical interval omits model/implementation errors and depends on assumptions; no interval simulation here. |
| 32 | Finite precision can dominate refinement; coordinate collapse exercised, arbitrary roundoff-floor study absent. |
| 33 | Source max-iteration failure preserved distinctly from convergence. |
| 34 | .05 decimal yield=5%; units reviewed. |
| 35 | Supplemental local yield error.01/100=.0001=1bp. |
| 36 | Supplemental additive valid bound sum.03; assumptions not automatically validated. |
| 37 | Budget residual1.001−1=.001; conceptual, no holdings-check API. |
| 38 | Seed supports reproducibility, not validity; no seeded simulation claim. |
| 39 | Solver convergence on each grid does not eliminate discretization bias; finite-grid/limiting values distinguished. |
| 40 | Units, methods, limits, runtime/hashes, residuals and benchmarks retained; external approval absent. |

## Twelve lab-step records

Prerequisites: Python, callable finite typed residual/integrand, representable ordered bounds and a valid continuous sign-changing bracket for mathematical interpretation; positive grid panels, positive assumed order, representable two-sided derivative nodes. Fictional periodic yield model; SciPy installed for separate root/continuous-cashflow examples.

| Step | Actual evidence and limit |
|---|---|
| 1 | Verbatim reference saved isolated; runtime/source/listing hashes retained. |
| 2 | Exact rational price absolute/relative errors.02/.0002. |
| 3 | Source residuals at0/.2 plus known root.1 and source yield/residual records. |
| 4 | Source bisection tuples retained, residual separate from interval width. |
| 5 | Actual float midpoint radius in decimal rate and basis points; ideal1/2048 example separate. |
| 6 | Width tolerances1e−6/1e−9/1e−12 and nondecreasing earlier-halving counts retained; not a universal strict iteration increase claim. |
| 7 | Source invalid bracket, max_iter0 and stagnation paths reject/raise. |
| 8 | Source x² trapezoids n2/4/8 versus finite-grid formula. |
| 9 | Rational actual error factor4, conditional order interpretation. |
| 10 | Source fine estimate1/96 versus actual polynomial fine error. |
| 11 | Source price sensitivities at three h, finite-step formula distinct from derivative limit. |
| 12 | Five exact commands,48 supplemental predicates and eight existing methods pass;16 baseline failed predicates retained. |

## Limits and resume checkpoint

Local Linux CPython/SciPy only. No rigorous general error bound, Monte Carlo/optimizer/market schedule implementation, economic data/model acceptance, arbitrary-conditioning proof, full derivative/roundoff analysis, production performance, broad shared-input integration, notebook/platform or external independent certification. Source execution, supplemental rational/Decimal derivations and conceptual scope remain separate above. F28/F32, F165 integrated-CDF tail limits and all unresolved tracker findings remain open.

Chapter17 has twelve core workflows and475 local answers scoped. Next: Section17.13 — Validation of Numerical Results; resume from fresh main without duplication.
