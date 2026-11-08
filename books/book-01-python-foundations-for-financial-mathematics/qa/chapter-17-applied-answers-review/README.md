# Section 17.15 — scoped Chapter 17 assessment review

Baseline manuscript: `a029e1d587ac54836bdcc639905cdbcdab1fb2ed`. Reviewer: automated source execution and mathematical/prompt/step review, not external independent acceptance. One assessment workflow,50 chapter-wide answers and twelve lab steps. Exercises41–50 are ten applied-case records **within** those50 answers, not ten additional answers. Chapter17's555 earlier local answers remain a separate inventory.

[results.json](results.json) retains five successful exact-source command records,64 passing supplemental predicates, runtime/platform/SciPy, input/criteria records, the assessment snippet hash and six linked manuscript/listing hashes. The assessment contains no unittest suite; twelve existing Section17.14 project methods are rerun separately. Zero historical unique methods added. No substantive manuscript numerical/answer defect was found in this scope; the only manuscript change links this evidence and updates the execution disclosure. The compact snippet payload is unchanged.

From repository root:

```bash
python books/book-01-python-foundations-for-financial-mathematics/qa/chapter-17-applied-answers-review/review.py
```

Reproduce the unchanged-payload baseline and linked-source review (requires Git history):

```bash
python books/book-01-python-foundations-for-financial-mathematics/qa/chapter-17-applied-answers-review/review.py a029e1d587ac54836bdcc639905cdbcdab1fb2ed
```

[baseline.json](baseline.json) passes all64 final-observer predicates and five commands. This is scoped agreement/execution, not model or comprehensive certification. Criteria are fixed in the runner: ordinary relative1e−12, known-zero currency absolute1e−12, ordinary roots absolute1e−12, multiple-root absolute1e−10 and optional-snippet repricing currency absolute1e−10. Rounded presentation values are checked separately from full-precision source expectations.

## Retained observer correction F172

[initial-observer-baseline.json](initial-observer-baseline.json) retains the first65-predicate run with one failed observer assumption: I required exp(−1e−16)==1. In this runtime it is0.9999999999999999; naive1−exp(−1e−16)=1.1102230246251565e−16 is nonzero but inaccurate relative to expm1's1e−16. Downward/upward binary64 spacing near1 differs. [observer-primitive-correction.json](observer-primitive-correction.json) explains changing the complete-cancellation illustration to1e−20 and preserves the initial values. This is an observer selection/assumption correction, not a manuscript or standard-library defect.

An unrelated zero-flow NPV probe mislabeled as an unconstrained-quadratic exercise was removed rather than counted as optimization evidence. Exercises11/12 are now explicitly analytic square/derivative reviews, with no optimization export claimed from NPV. Final inventory64 differs from initial65; inventories are not added. F172 severity low, owner Book1 QA, decision correct/remove misleading observer probes, status resolved within this scope; final baseline and rerun pass.

## Exact-source and linked-source boundaries

Five isolated commands run the verbatim assessment SciPy snippet, the verbatim Section17.14 demonstration, its separate twelve-method test file, compilation of those three exact files, and silent project/test imports. A second unchanged-snippet execution enables independent root/repricing checks; stdout retained. The optional snippet is tested only on its supplied two-period fixture; its deliberately compact NPV is not claimed to have general domain/range safeguards.

The runner also compiles/imports six verbatim linked listings, without triggering their `__main__` suites, and calls their exports for lab checks. Exact source/hash provenance is recorded:

| Linked section | Executed scope |
|---|---|
|17.14 Financial solver | NPV, root reports, separate multiple brackets, coupon/two-period flows, finite1bp; twelve existing methods rerun. |
|17.7 Portfolio optimization | Two-asset mean-variance/volatility and invalid covariance rejection. No general optimizer/backtest acceptance. |
|17.12 Convergence/error | Two/four-panel trapezoids, distinct from limiting integral. Its eight embedded methods are not rerun/count-added here. |
|17.9 Interpolation | Linear-zero midpoint, interval forward and out-of-domain rejection. No market curve calibration. |
|17.11 Stability | Continuous annuity, guarded log return/log-sum-exp. No arbitrary-conditioning proof. |
|17.13 Validation | Coupon repricing residual and specified mixed tolerance. No production-use approval. |

Prior [clean Linux project setup/source evidence](../chapter-17-solver-project-review/setup-results.json) matches the current linked17.14 source hash, as recorded in results.json. It is prior scoped SciPy1.18.1 execution, not a newly created environment or fresh installation in this assessment run. Current commands use recorded Python3.12.14/SciPy1.17.0 and isolated temporary source directories. This does not close F28 notebook/platform or F32 broad shared-input integration gaps.

## Independent mathematical model and expectations

Fictional annual-effective periodic rates, common currency, initial t0 and integer-year-end future flows unless explicitly continuous. For[-100,110], NPV(r)=−100+110/(1+r), exact root1/10. Bracket[0,.2] has residuals10 and−25/3; at returned rate.101 residual−100/1101≈−.0908265213, rounding to−.090827. Initial width.2 after ten ideal halvings gives width1/5120 and midpoint bound1/10240=125/128 basis points≈.9766bp. These mathematical bounds require a retained continuous sign-changing bracket, not just a solver flag.

[-100,230,−132] becomes−100(r−.1)(r−.2)/(1+r)^2, hence separate roots.1/.2. For[-100,60,60], multiply by u² with u=1+r:100u²−60u−60=0. Positive admissible u=(3+sqrt69)/10 and r=(3+sqrt69)/10−1≈.1306623863. The optional snippet and linked project recover that root; original NPV is independently repriced with Fraction. At.1, the two-period NPV is500/121≈4.1322314.

Two-asset variances.04/.09 at equal weights give13/400=.0325 and volatility sqrt(13/400). Covariance.03 adds.015, giving19/400=.0475 and volatility sqrt(19/400). Covariance.07 violates c²≤.04*.09=.0036. Budget residuals are separate calculations; variance alone does not approve budget/mandates. Analytic f(x)=(x−3)^2+2 has unique unconstrained minimum(3,2); on[0,2], negative derivative forces boundary(2,3). These are proofs/reviews, not exported numerical optimization runs.

For ∫x² on[0,1], antiderivative gives1/3; finite trapezoids T2=3/8 and T4=11/32 have exact errors1/24 and1/96, ratio4. Continuous annuity100/year,T2,r.05 has PV2000(1−exp(−.1)), independently evaluated with Decimal200. Periodic annual coupon flows[0,5,105] at.05 give100; their separate-price residual is0. Continuous and annual-effective rates are not mixed.

Single payment110 at.11 prices11000/111≈99.0990990991. At.1001 it prices1100000/11001≈99.9909099173; finite+1bp change−100/11001≈−.00909008272. Currency scaling by1000 scales NPV, not the root. Position discrepancy.02×500000=10000; standard-error arithmetic20/sqrt10000=.2 assumes IID finite-variance sampling. No Monte Carlo paths are simulated here.

## Fifty chapter-wide answer records

| Exercise | Alignment and execution boundary |
|---|---|
|01 | Linked one-year PV100, exact analytical expectation. |
|02 | Linked project root versus1/10; NPV equation/domain reviewed. |
|03 | Linked endpoint residuals10/−25/3; continuity specified. |
|04 | Exact midpoint.1 and linked NPV0; does not imply every float callback returns exact0. |
|05 | Independent ideal width1/5120/bound1/10240; bound in bp125/128≈.9766. |
|06 | Linked invalid same-sign bracket rejects; no universal no-root claim. |
|07 | Linked residual at.101 versus−100/1101; printed−.090827 rounding verified. |
|08 | Rate and currency tolerances have different units; conditioning remains conceptual. |
|09 | Linked separate .1/.2 brackets checked; independent factorization. |
|10 | Linked endpoint root0. |
|11 | Analytic square≥0 gives unique x3,value2; not a source NPV/optimizer export. |
|12 | On[0,2],derivative2(x−3)<0, so boundary x2,value3; analytic review. |
|13 | Supplemental exact .4+.6−1=0. |
|14 | Supplemental .4+.61−1=.01; feasibility tolerance must be selected separately. |
|15 | Linked variance13/400 and Decimal volatility; printed.18028 rounded correctly. |
|16 | Linked correlated variance19/400 and Decimal volatility; printed.21794 rounded correctly. |
|17 | Linked PSD rejection for covariance.07; exact bound.06. |
|18 | Global/local optimum evidence reviewed conceptually; no general global proof. |
|19 | Objective/constraint units and coefficients require economic meaning; conceptual. |
|20 | Correlation/near-singular sensitivity is model/conditioning risk; no actual estimation study. |
|21 | Analytic integral1/3; source finite quadrature results kept distinct. |
|22 | Linked T2=.375 and exact1/24 error. |
|23 | Linked T4=.34375 and independent error ratio4. |
|24 | Linked continuous annuity versus Decimal PV; printed190.32516 rounded correctly. |
|25 | Direct/expm1 primitive illustration at1e−20, with initial observer assumption retained separately. |
|26 | Linked linear-zero midpoint.05; assumption stated. |
|27 | Linked default extrapolation rejection at year4; no authorized tail rule. |
|28 | Linked continuously compounded average forward.06; distinct from annual-effective coupon convention. |
|29 | Repricing calibration instruments required; no actual market calibration run. |
|30 | Quadrature estimate does not cover wrong cashflow/model assumptions; conceptual. |
|31 | Direct binary64(1e16+1)−1e16=0 observed. |
|32 | math.fsum([1e16,1,−1e16])=1 observed; no universal overflow guarantee. |
|33 | Linked log return versus Decimal ln1.01; printed.00995033 rounded correctly. |
|34 | Linked log-sum-exp versus1000+ln2; avoids direct exp1000. |
|35 | Supplemental absolute.02/relative.0002=.02%. |
|36 | Zero-reference absolute scale required; no universal tolerance approved. |
|37 | Linked mixed comparator rejects .02 error versus.015 threshold. |
|38 | Supplemental exact residual1e−6 versus root error.01. |
|39 | Stagnation does not establish success; conceptual, earlier scoped convergence evidence remains separate. |
|40 | Inputs/units/criteria/source/library/runtime/outputs/limits retained; external reviewer approval absent. |
|41 | Applied case: linked coupon price100 under simplified annual convention. |
|42 | Applied case: linked separate-price residual0; dates/settlement still require real-use verification. |
|43 | Applied case: linked PV11000/111, printed99.099099 rounded correctly. |
|44 | Applied case: linked bumped price and finite change; printed99.990910/−.009090 rounded correctly. |
|45 | Applied case: linked1000×currency NPV and unchanged root within stated budgets. |
|46 | Applied case: linked NPV500/121, printed4.13223 rounded correctly. |
|47 | Applied case: linked/optional-snippet root versus independent positive quadratic root, printed.130662 rounded correctly. |
|48 | Applied case: supplemental10000 aggregate discrepancy; no actual materiality approval. |
|49 | Applied case: supplemental SE.2; no simulated samples/confidence interval. |
|50 | Applied case: unresolved coupon dates prevent appropriate use approval despite numerical convergence. |

## Twelve assessment lab-step records

| Step | Actual evidence and boundary |
|---|---|
|1 | Current runtime/Python/SciPy recorded and exact files run in isolated temp directories; prior clean project environment evidence linked, not claimed as a fresh install. |
|2 | Verbatim Section17.14 implementation/test files used with explicit annual-effective,t0/integer-period convention; no supplemental replacement model. |
|3 | Linked one-period root/NPV,coupon PV and two-period NPV checked against independent expectations. |
|4 | Linked project roots plus exact optional SciPy snippet, with analytic1/10 and quadratic benchmarks. |
|5 | Independent original-equation Fraction repricing and preselected currency budgets. |
|6 | Linked separate brackets for.1/.2; no all-root enumeration. |
|7 | Linked variances/volatility for covariance0/.03 and rejection.07. |
|8 | Linked trapezoids n2/n4, independent finite-grid errors and ratio. |
|9 | Direct subtraction/expm1 example recorded; QA correction explicit. |
|10 | Linked project invalid rate/nonfinite flow and PSD/domain guards; compact snippet only supplied fixture. |
|11 | Five exact commands,64 final supplemental predicates and twelve existing linked methods pass; initial observer failure retained. |
|12 | All50 answers reviewed; numeric rounded presentations checked separately, source/supplemental/conceptual limits disclosed. |

## Limits and chapter checkpoint

Local Linux CPython/SciPy. No standalone general solver certification for compact snippet, new Monte Carlo/backtest, arbitrary optimizer/shape/conditioning proof, market calibration/calendar/schedule acceptance, production performance, platform/notebook matrix, broad shared-input integration or external independent review. Source execution, supplemental rational/Decimal derivations, analytic proofs and conceptual designs are separated above. F28/F32,F165 integrated-CDF tail limits and every unresolved finding remain open.

Chapter17's listed formal scope is now recorded: fourteen core/project workflows plus one assessment workflow,555 local answers and50 chapter-wide answers. This is scoped review completion, not comprehensive validation or certification. Next: Chapter18 Section18.1 — Simulation Fundamentals; resume from fresh main.
