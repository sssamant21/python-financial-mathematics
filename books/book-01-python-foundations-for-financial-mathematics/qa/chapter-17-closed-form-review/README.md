# Section17.2 — scoped closed-form versus numerical review

Baseline manuscript: `4f11563325b1b6c337cb8a35983f6e65ab06be29`. One core workflow, all40 local worked answers and twelve lab steps reviewed. Predicate, workflow, answer and historical unique method counts are separate.

Run from repository root:

```bash
python books/book-01-python-foundations-for-financial-mathematics/qa/chapter-17-closed-form-review/review.py
```

Reproduce unchanged-source failures (requires baseline in Git history; expected nonzero exit writes baseline.json):

```bash
python books/book-01-python-foundations-for-financial-mathematics/qa/chapter-17-closed-form-review/review.py 4f11563325b1b6c337cb8a35983f6e65ab06be29
```

Exact-source printed demonstration/twelve existing unittest methods, silent import and printed compileall execute in isolated temporary directories. Final results.json retains three successful commands,60 passing supplemental predicates, raw outputs, runtime/platform, hashes and independent rational/Decimal expectations/tolerances. No new historical unique methods. No SciPy backend executed.

## Baseline and observer records

baseline.json retains22 failed predicates under the final observer policy; the original twelve unittest methods already passed. F159 corrects inverse amount-ratio cancellation/overflow, future-value power overflow/underflow, NPV precision/power overflow, annuity intermediate exponential/power failures, scaled discriminant overflow/underflow, callback/coordinate stagnation and output/exception contracts. All-zero IRR now explicitly rejects as non-identifiable rather than selecting an arbitrary valid rate; this is a stated financial interpretation guard, not a claim that the zero function has no roots.

observer-failure.json retains the initial QA serialization traceback: baseline quadratic outputs included NaN in project metadata, which strict JSON could not encode. The observer now recursively stores nonfinite metadata values as repr strings; failed numerical predicates remain failed. This is observer evidence handling, not a source repair.

first-correction-rerun.json retains the first corrected-source57-predicate run with one failed comparison: IRR .10000000000013641 was within the requested absolute1e-12 rate tolerance but outside an accidentally stricter1e-12 relative budget at rate.1. observer-root-tolerance-correction.json records the comparison repair. Final baseline/final reports use absolute1e-12 for that root and add three ordinary quadratic branch checks, yielding60 predicates. The failed comparison is not counted as a source defect; inventories are not added together.

## Algorithms, reporting and independent checks

Forward compounding, NPV and the geometric annuity formula use integer/displayed-decimal rational arithmetic before finite float output. The direct annuity sum follows a separate finite payment-discounting path. Implied rate forms the exact amount ratio then uses Decimal log/exp with precision increased for small relative differences and period count; positive future amounts must not result in a reported rate−1. Quadratic discriminants use exact rational arithmetic, stable-q roots use80-digit Decimal with q/a and c/q, and repeated roots are handled directly. Both roots must be reportable.

All required nonzero results must stay nonzero and finite on reporting or raise ValueError. This policy avoids silent loss/overflow but does not establish conditioning or preserve every insignificant increment in a large float. Bisection/quadrature follow Section17.1's finite-float callback/coordinate rules and stagnation handling. Public bisect/irr retain scalar returns; independent residual substitution is recorded instead of claiming a complete public solver-status interface. Continuity, accurate callback signs, units and valid financial conventions remain caller responsibilities.

Independent reference annuity=sum(100/(21/20)^t,t=1..5) is rational, not just agreement between two source functions. Extreme negative-rate annuities use the independently derived geometric series2*payment*(2^n−1). Quadratic roots follow exact factorizations/scaling and stable reciprocal-root expectations; ordinary roots, zero-linear-term and repeated-root branches are checked. Trapezoid_N(x²)=1/3+1/(6N²) is the finite-grid oracle, distinct from the limiting integral. These references and conceptual examples are supplemental derivations, not additional source exports.

## All40 local answers

| Answers | Scoped review and execution boundary |
|---|---|
| 1–3 | Source FV100→121 at.1/two periods, inverse rate.1; supplemental discount121/(1.1²)=100. |
| 4–6 | Source zero-rate PV500; geometric annuity and direct payment sum independently match exact rational five-payment expectation≈432.9476671. Tiny positive rate, extreme negative rate with1100 periods and large positive-rate/amount models are separate scale probes, not empirical forecasts. |
| 7–12 | Source NPV≈0 within1e-12 dollars and IRR≈.1 within absolute1e-12 rate; separate .1/.2 roots for[−100,230,−132]. Source quadratic(1,−3,2) roots1/2, no-real-root rejection, huge/tiny scaled coefficients and negative tiny discriminant checked. |
| 13–19 | Conditional sign-change existence, midpoint/halving width and original-equation substitution reviewed/executed. Supplemental Newton step1.5; singular derivative failure conceptual. No Newton solver exported. Stagnation is a failure, not convergence. |
| 20–23 | Source linear integral.5 and quadratic N10=.335/N20=.33375, with exact error ratio4. Analytic integral1/3 remains separate from finite-grid result. |
| 24–28 | Supplemental unconstrained optimum.3, constrained optimum.5 and portfolio variance.0325; constrained portfolio/calibration formulations reviewed. No optimizer, interpolation or calibration export in this reference. |
| 29–33 | Residual versus root units, conditioning, currency scale, cancellation and binary .1+.2 demonstration reviewed; scale failures tested. Exact arithmetic does not cure a wrong or ill-conditioned model. |
| 34–36 | Curve interpolation conventions, irregular-date IRR and nonuniqueness reviewed. Source cashflows remain periodic; no curve/XIRR or all-root enumerator implemented. |
| 37–40 | Constraint rejection, wrong conventions, discretization and coupon-schedule model/input error reviewed conceptually; no actual mandate or market-data acceptance. |

## Twelve lab steps

Prerequisites: finite int/float quantities/callbacks, periodic compounding domain r>−1, positive amounts for inverse rate, integer periods, continuity for bracket interpretation, real-root existence and absolute error units. Fictional common USD cashflows occur at t0 and equally spaced period ends, no actual dates or instrument conventions supplied.

| Step | Evidence and limit |
|---|---|
| 1 | Exact isolated listing and runtime/hash records retained; standard library only. |
| 2–3 | Source FV121 and inverse rate.1, cross-checked with rational forward/discount identities. |
| 4–5 | Source geometric formula and direct sum at payment100/rate.05/n5 checked independently; source zero-rate500. |
| 6–7 | Source NPV known-zero dollar budget and numerical IRR absolute rate budget, not an accidental tighter relative tolerance. |
| 8 | Source separate brackets[.05,.15]/[.15,.25] isolate .1/.2. This does not prove unique or economically preferable IRR. |
| 9 | Stable source quadratic roots1/2; additional scale/zero-linear/repeated-root probes separated from ordinary lab. |
| 10 | Source quadratic trapezoids N10/N20 match1/3+1/(6N²), error decreases by4. |
| 11 | Bad brackets, invalid rates, no-real roots, output limits and exhausted float coordinates reject/raise as recorded. |
| 12 | Three commands/twelve existing tests,60 final predicates, baseline/source and observer records retained. Corrected source revision is containing publication commit. |

## Limits and resume checkpoint

Local Linux CPython standard library only. Exact source execution is separate from supplemental rational/Decimal expectations and conceptual financial designs. No actual market/as-of inputs, day-count/coupon/accrual implementation, irregular-date cashflows, all-root enumeration, SciPy/backend run, arbitrary conditioning proof, production performance, platform coverage, independent reviewer acceptance or certification. F28 notebook/platform, F32 broader shared-input integration and newer unresolved findings remain open.

Chapter17 now records two core workflows and75 local answers within scope. Next: Section17.3 — Numerical Root Finding.
