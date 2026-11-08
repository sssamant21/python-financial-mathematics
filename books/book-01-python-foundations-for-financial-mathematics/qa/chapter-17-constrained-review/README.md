# Section 17.6 — scoped constrained-optimization review

Affected baseline: `36a037ec231dcf8fd22c3a9af7b3bb4887defcaf`. F163, severity medium (educational numerical correctness), owner Book 1 manuscript maintainers; decision fix exact feasibility/PSD/scale handling and disclose reporting/diagnostic boundaries. Reviewer: automated source execution and mathematical/prompt/step review, not external independent acceptance. Corrected revision is the containing publication commit.

One workflow, forty local answer records and twelve lab steps are separate from four exact-source commands,52 supplemental predicates and twelve existing unittest methods. Zero historical unique methods added. [results.json](results.json) retains raw stdout/stderr, values/tolerances, lab outputs, model, Python/platform/NumPy/SciPy versions and source/listing SHA256.

From repository root:

```bash
python books/book-01-python-foundations-for-financial-mathematics/qa/chapter-17-constrained-review/review.py
```

Reproduce unchanged source (expected nonzero exit, requires history):

```bash
python books/book-01-python-foundations-for-financial-mathematics/qa/chapter-17-constrained-review/review.py 36a037ec231dcf8fd22c3a9af7b3bb4887defcaf
```

[baseline.json](baseline.json) retains sixteen failed predicates, although the twelve existing tests and SciPy snippet already passed. Defects/contracts addressed include tolerated but real infeasibility, false nonuniqueness at tiny scale and in singleton feasible sets, PSD underflow/overflow, unchecked public variance/slack inputs, risk underflow, wide/repeated grid coordinates and incorrect exception types. Strict variance domain and reporting guards are disclosed contract additions: the original variance helper performed unchecked arithmetic. The final reporting probe rejects an interval whose tiny hard minimum would disappear on float conversion; this is conservative finite-report rejection, not mathematical infeasibility. Sixteen predicates do not mean sixteen distinct defects. Baseline records preserve all tested initial failures; no observer failures occurred.

## Exact execution and independent expectations

The verbatim reference is saved in an isolated temporary directory and run as printed demonstration/twelve tests, silent import and compilation. The fourth command executes the verbatim NumPy/SciPy SLSQP snippet. A separate execution of that unchanged snippet in a namespace enables four additional independent weight/objective/feasibility predicates. No supplemental optimizer replaces exact-source execution; NumPy/SciPy are actually installed and versions recorded.

Bounds reduce exactly to lo=max(minA,1−capB), hi=min(capA,1−minB). A nonempty feasible set requires lo≤hi, without tolerance relaxation. For A=.04,B=.09,C=0, the reduced variance is .13w²−.18w+.09; unconstrained w=9/13 and V=9/325. With capA=.4, projection gives A=.4,B=.6,V=97/2500=.0388. Model cost of the cap is361/32500≈.0111076923 squared-return units. A1000-subinterval grid on[0,.4] has spacing1/2500 and winner.4, exactly a boundary of this finite grid; no inference about arbitrary grids/global nonconvex minima follows.

The supplemental reduced KKT calculation uses g(w)=w−.4≤0. At w=.4, V′=2(.13)(.4)−.18=−19/250. With inactive lower-bound multiplier0, upper multiplier μ=19/250=.076 is nonnegative, stationarity V′+μ=0 and complementarity μg=0 hold. PSD/linear bounds establish convexity for this fixture. This is an analytic certificate for the stated one-variable model, not a source multiplier export, general KKT implementation or external acceptance.

Source arithmetic preserves integer/displayed-decimal quantities rationally through PSD, bound reduction, projection and risk. Exact denominator0 is constant variance; `nonunique` also requires lo<hi. A singleton is unique even for a flat objective. Public variance validates long-only scalar weight and PSD; slacks accept finite possibly violating weights to diagnose negative slacks but require a valid bound policy.

Reported weights/intervals must respect hard bounds or raise ValueError. Exact analytic weights have budget1; displayed float weights may have a disclosed small `reported_budget_residual`, and returned variance concerns the exact analytic weights. `constraint_residuals` derives B=1−A, so its zero budget is an identity, not reconciliation of independent holdings. Required nonzero results may not silently underflow; unreportable outputs reject. This policy can reject a mathematically feasible model whose interval cannot be reported without relaxing a hard bound; it is not a complete floating-point feasibility solver.

## Forty local answers

| Exercise | Alignment and execution boundary |
|---|---|
| 01 | Source default feasible interval[0,1]. |
| 02 | B=1−A used algebraically; source does not accept two independent holdings for slack reconciliation. |
| 03 | Long-only bounds imply A∈[0,1]; source public variance checks that domain. |
| 04 | Source capA=.4 reduces upper bound to.4. |
| 05 | Source capB=.6 reduces lower bound to.4. |
| 06 | Source rejects two.4 caps because maximum budget.8<1. |
| 07 | A minimum.3 is a lower bound; analytic bound-reduction review. |
| 08 | B minimum.2 implies A≤.8; analytic reduction. |
| 09 | Source A[.2,.6],B[.1,.7] reduces exactly to A[.3,.6]. |
| 10 | Source inverted minA.5/capA.3 rejects. |
| 11 | Reduced variance .04w²+.09(1−w)² matches source evaluation. |
| 12 | Source uncapped weight9/13 versus independent derivative. |
| 13 | Source capA.4 projects optimum to.4; SciPy independently checked. |
| 14 | Source capped variance97/2500=.0388. |
| 15 | Source uncapped variance9/325≈.0276923077. |
| 16 | Variance/turnover multiplier needs compatible units; conceptual, no turnover objective exported. |
| 17 | h(w)=sum(w)−1=0 is equality; analytic. |
| 18 | g(w)=wA−.4≤0 matches reduced KKT sign convention. |
| 19 | Source cap slack at.3=.1 versus rational expectation. |
| 20 | Source cap slack at.4=0, active. |
| 21 | Positive source slack at.3 implies inactive; negative at.5 exposes violation. |
| 22 | L=f+λh equality Lagrangian; conceptual sign convention. |
| 23 | Supplemental derivative/multiplier give reduced stationarity0; no source general KKT export. |
| 24 | Supplemental cap multiplier19/250≥0 under g≤0 convention. |
| 25 | Supplemental μg=0; positive multiplier implies active, active need not imply positive in general. |
| 26 | Source constraints/slacks and separate SciPy bound/budget checks establish only fixture feasibility. |
| 27 | PSD quadratic with linear bounds is convex; analytic global fixture interpretation. |
| 28 | Exactly five nonzero assets introduces nonconvex support choices; conceptual, unsupported here. |
| 29 | Sector sum cap is linear; conceptual, no sector-input engine. |
| 30 | Sum absolute turnover is convex under fixed old weights; conceptual, no trade engine. |
| 31 | Proportional absolute-trade fees are convex under stated assumptions; conceptual. |
| 32 | Sum absolute weights bounds gross exposure; conceptual. |
| 33 | Net sum1 alone does not bound gross exposure; conceptual. |
| 34 | [1.2,−.2] sums1 but gross1.4 and violates long-only; source variance rejects A1.2. |
| 35 | Fixed-mean return floor is linear; conceptual, no target-return constraint implemented. |
| 36 | With full investment, a finite long-only weighted average of means strictly below.08 is strictly below.08. Answer/prose tightened from 'may' to 'is infeasible' under those explicit assumptions. |
| 37 | Exact SciPy result independently checked for both weights, bounds/budget and rational objective. |
| 38 | Hard-bound source policy has no feasibility tolerance; SciPy comparison tolerances are explicitly recorded and not mandate approval. |
| 39 | Variance/currency cost scaling remains conceptual; covariance scale tests verify only numeric invariance. |
| 40 | Model, bounds, runtime, source hashes, slacks and raw outputs retained; no production/market approval. |

## Twelve lab steps and prerequisites

Prerequisites: Python, finite int/float risk inputs, valid two-asset PSD covariance, compatible single-period squared-return units, consistent long-only bounds, and callable finite objectives for grid. NumPy/SciPy optional for step11 and available here. No actual market history/as-of or currency conversion supplied. Return/sector/turnover/leverage constraints, calendars and costs remain outside these exports.

| Step | Actual evidence and scope |
|---|---|
| 1 | Verbatim reference saved isolated; interpreter and source/listing hashes retained. |
| 2 | Exact bound reduction and source default, capped and combined intervals checked. |
| 3 | Source two40% cap infeasibility, plus separate tiny actual gap rejection. |
| 4 | Source uncapped weights/risk versus9/13 and9/325. |
| 5 | Source capA=.4 specified explicitly. |
| 6 | Source capped weights.4/.6 and risk.0388. |
| 7 | Independent objective increase361/32500 retained. |
| 8 | Source slacks at.3/.4/.5 identify inactive/active/violating cap; implicit budget identity limitation disclosed. |
| 9 | Source1000-subinterval grid on[0,.4], spacing.0004,1001 evaluations, boundary winner.4/value.0388. Singleton grid separately evaluated once. |
| 10 | Source ordinary/tiny/large invalid PSD rejections; no scale-dependent absolute determinant threshold. |
| 11 | Exact NumPy/SciPy SLSQP snippet plus separate namespace inspection and independent rational checks. |
| 12 | Four exact commands,52 supplemental predicates and twelve existing methods pass; sixteen baseline failed predicates retained. |

## Limits and resume checkpoint

Local Linux CPython/NumPy/SciPy environment only. No general nonlinear/multivariate solver, source multipliers, economic covariance estimation acceptance, rounded-holdings optimization, production performance, arbitrary conditioning proof, broad shared-input integration, notebook/platform or external independent acceptance/certification. Source execution, supplemental rational/KKT derivations and conceptual designs remain separate above. F28/F32 and all unresolved tracker findings remain open.

Chapter17 has six core workflows and235 local answers scoped. Next: Section17.7 — Portfolio Optimization. Resume from fresh main without duplicating completed batches.
