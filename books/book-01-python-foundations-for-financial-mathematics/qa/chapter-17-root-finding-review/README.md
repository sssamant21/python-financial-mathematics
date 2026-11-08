# Section 17.3 — scoped numerical root-finding review

Baseline: `c86a9b69ed67c1745401d17f0cdf4bca587a86fa`. Reviewer: automated source execution and mathematical/contract review; no external independent acceptance. One workflow, 40 local answer records and 12 lab-step records below. These inventories are separate from 53 supplemental predicates, four exact-source command records and twelve existing unittest methods. Zero historical unique methods added.

From repository root:

```bash
python books/book-01-python-foundations-for-financial-mathematics/qa/chapter-17-root-finding-review/review.py
```

Reproduce the unchanged-source baseline (expected nonzero exit; requires history):

```bash
python books/book-01-python-foundations-for-financial-mathematics/qa/chapter-17-root-finding-review/review.py c86a9b69ed67c1745401d17f0cdf4bca587a86fa
```

[results.json](results.json) retains actual commands, raw stdout/stderr, environment, source/listing SHA256 and expectations. Four successful commands execute the verbatim reference demonstration/twelve tests, silent import, compilation, and the separate verbatim SciPy snippet (SciPy 1.17.0 in this runtime). Printed sqrt/IRR demonstrations and assertions run, not merely a supplemental reimplementation. The 53 predicates separately call source exports or derive explicitly labeled mathematical expectations. Fractions and 80-digit Decimal sqrt(2) supply expectations without borrowing source solver results.

## Finding F160 and retained transitions

Severity: medium (educational numerical correctness); owner: Book 1 manuscript maintainers; decision: repair source and clarify contracts; affected baseline and reproduction above, corrected outcomes below.

[baseline.json](baseline.json) retains sixteen failed predicates under the final observer, although the original twelve tests passed. Corrections cover overflowing midpoint/secant differences, Newton's absolute derivative cutoff, update arithmetic with an otherwise finite destination, NPV integer cancellation/rate/power/output handling, all-zero IRR ambiguity, typed bound/callback/domain validation and explicit bisection stopping diagnostics. Secant stagnation now fails directly rather than reaching a misleading subsequent zero-slope error. Other guards that already passed remain passing; the baseline is not a claim of sixteen separate defects.

[observer-failure.json](observer-failure.json) retains the original observer traceback: rational actual values were not JSON serializable. The observer stores rational/Decimal actual values as strings; it does not change numerical predicates. [first-correction-rerun.json](first-correction-rerun.json) retains the initial 53-predicate corrected-source run with one failure. [observer-fixture-correction.json](observer-fixture-correction.json) explains its inconsistent piecewise Newton callback/derivative. The final differentiable probe uses f(x)=x/2+5e307, derivative 1/2, starting at 1e308 with exact root −1e308. The associated source update uses the stated displayed-decimal coordinate policy, and an unreportable last-step diagnostic is retained as an exact rational string. The final reports pass 53 predicates/four commands; transition inventories are not added together.

Cashflows are fictional common currency, t0 initial flow and equally spaced period-end flows; no dates, quote feeds or conventions other than periodic r>−1. Model fixture [-100,110] has analytic rate 110/100−1=1/10. For [-100,230,−132], multiplying by (1+r)^2 gives −100(r−.1)(r−.2), independently deriving both rates. Separate brackets isolate both; substituting rates checks original NPV. This is not an all-root search or economic choice among IRRs.

Bisection radius is conditional on continuity/accurate endpoint signs and accounts for rounded midpoint. Ten retained halvings, not ten midpoint evaluations, give width 1/1024 and midpoint bound 1/2048 from width 1. Newton/secant residual tolerance is not an x-error certificate. The tiny-scale linear demonstration deliberately accepts x=0 with root error 2 under default ftol; users must specify residual units and conditioning. A discontinuous step can meet the interval criterion with residual ±1 and no mathematical root. Callback zero also concerns the evaluated callback only. `converged` means the recorded numerical stopping rule was satisfied, not model validation.

## Forty local answers — prompt alignment and limits

| Exercise | Review result and execution boundary |
|---|---|
| 01 | x²−4=(x−2)(x+2): roots ±2; analytic review. |
| 02 | Continuous x²−2 has endpoint signs −1/+2; source bisection lab verifies the positive root. |
| 03 | Supplemental exact midpoint 3/2, residual 1/4, next bracket [1,1.5]. |
| 04 | Supplemental midpoint 5/4, residual −7/16, next bracket [1.25,1.5]. |
| 05 | Exact width 1/1024 after ten retained halvings; terminology corrected. |
| 06 | Exact midpoint error bound 1/2048 after those halvings, conditional on containment. |
| 07 | Existing source endpoint test returns root 1 at zero midpoint evaluations. |
| 08 | Source rejects x²+1 on [−1,1]; no real root algebraically. |
| 09 | Source rejects even-root bracket [0,2] despite root 1; sign-change requirement is not necessity of existence. |
| 10 | 1/x discontinuity defeats IVT. Conceptual singularity review; separate source discontinuous-step probe illustrates interval stopping without a root. |
| 11 | Newton update x−(x²−2)/(2x), x≠0; derivation reviewed. |
| 12 | Supplemental exact first update 3/2; source full Newton lab executed. |
| 13 | Supplemental second update 17/12; source full Newton lab executed. |
| 14 | Source zero derivative guard triggered at x=0 for x²+1. |
| 15 | Source Newton domain rejects update below −1 with boolean callback. |
| 16 | Secant update derived by intercept of line through two points; source full secant lab executed. |
| 17 | Source equal function values reject zero slope. |
| 18 | Source NPV(.1,[-100,110]) agrees with exact −100+110/(1.1)=0. |
| 19 | Source bracketed IRR within absolute rate tolerance 1e−12 of 1/10. |
| 20 | P(y)−Pm=0 correctly states yield residual; design only, no bond engine supplied here. |
| 21 | Both exact rates .1/.2 substituted; source separate brackets recover each within 1e−12. |
| 22 | Source NPV rejects r=−1; denominator zero. |
| 23 | Supplemental rational residual at 7/5 is −1/25. |
| 24 | Supplemental Decimal absolute error sqrt(2)−1.4≈.01421356237. |
| 25 | Source scaled linear callback accepts residual below default ftol while root error is 2; small residual not root accuracy. |
| 26 | .01/1=.01 versus .01/1e9=1e−11; units/scales reviewed, no observed prices. |
| 27 | Conditional bisection width halves; local convergence review, no empirical universal rate claim. |
| 28 | Newton quadratic convergence requires simple root, sufficient smoothness and suitable start; source sqrt lab only. |
| 29 | Secant local order (1+sqrt(5))/2≈1.618 under appropriate assumptions; analytic review. |
| 30 | Newton on (x−1)² has error update e/2, so linear; conceptual derivation, source is not all-root enumerator. |
| 31 | Bisection/Newton/secant unchanged-coordinate failures exercised; unmet criterion does not certify convergence. |
| 32 | Existing bisection iteration-limit method plus supplemental budget probe executed; solver raises failure. |
| 33 | Existence under continuity and sign change does not imply uniqueness; conceptual review. |
| 34 | Initial guesses affect basins; nonconvex/multiple-root claim reviewed, no basin enumeration implemented. |
| 35 | A rate close to −1 is negative, not huge in magnitude; wording corrected. Source rejects invalid or unreportable results and preserves finite extreme NPV. |
| 36 | Central difference has O(h²) smooth-function truncation and roundoff amplification as h shrinks; conceptual, no finite-difference routine exported. |
| 37 | Exact SciPy brentq/root_scalar snippet executed and assertions passed. |
| 38 | Exact SciPy Newton/root_scalar snippet executed and assertions passed; not arbitrary domain robustness. |
| 39 | Source NPV substitution, rate domain and separate multiple-root brackets checked. Searching all plausible roots remains caller task. |
| 40 | Source/listing hashes, platform, solver results, commands, tolerances and baseline retained. Callback continuity/market appropriateness remains review responsibility. |

## Twelve lab steps — prerequisite and output contracts

Prerequisites: installed Python; SciPy installed for optional step 11 (available here); finite typed input quantities; callable residual/derivative; boolean domain decision; valid periodic discount domain; model continuity and appropriate residual units. No interactive notebook or platform installation acceptance is inferred.

| Step | Actual evidence and scoped limit |
|---|---|
| 1 | Verbatim listing saved in isolated temporary directory, hashes/environment retained. |
| 2 | Source bisection on [1,2] for x²−2; Decimal sqrt(2) oracle. |
| 3 | Full root/residual/iterations/bracket/termination/radius record retained in lab_results. Midpoint evaluations separated from interval halvings. |
| 4 | Source Newton from 1; supplied derivative 2x, independent sqrt(2) expectation. |
| 5 | Source secant from 1/2; independent sqrt(2) expectation. |
| 6 | All three estimates and original residuals compared within explicit 1e−10 absolute lab budget; iteration counts retained. Counts alone are not fair timing or cost benchmarks because derivative/function costs differ. |
| 7 | Source x²+1 bracket failure, plus even multiplicity and separate discontinuity checks. |
| 8 | Source zero derivative rejection; scaled nonzero derivative separately validated without an absolute cutoff. |
| 9 | Source original NPV and bracketed IRR versus rational 1/10 expectation. |
| 10 | Separate source brackets [.05,.15]/[.15,.25] and NPV substitutions at .1/.2; no uniqueness certification. |
| 11 | Verbatim SciPy snippet executes both methods and assertions with installed version recorded. No extra SciPy financial calibrations or cross-version tests. |
| 12 | Twelve existing source methods, silent import and compilation pass; 53 supplemental predicates pass. All initial transitions retained separately. |

## Remaining scope and resume

Local Linux CPython/SciPy environment only. No global root/uniqueness proof, safeguarded Newton implementation, arbitrary callback error certification, irregular-date cashflows, bond/day-count or option/vega implementation, market-input acceptance, performance benchmark or independent reviewer certification. F28 notebook/platform and F32 broader shared-input integration remain open with all other unresolved tracker findings. Numeric finite-range policy is explicit but does not solve conditioning or validate the model.

Chapter 17 now has three core workflows and 115 local answers scoped. Next: Section 17.4 — Solving Yield and IRR Problems. Continue that source from fresh main; do not duplicate this batch.
