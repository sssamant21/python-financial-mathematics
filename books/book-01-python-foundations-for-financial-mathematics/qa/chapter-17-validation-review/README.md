# Section 17.13 — scoped numerical-results validation review

Affected baseline: `0e8bd0fcb5d2bd3e45262569342c152afbe44f52`. F170, severity medium (educational numerical correctness/specification), owner Book 1 manuscript maintainers; decision repair comparison/arithmetic/reporting defects and clarify timing/feasibility contracts. Reviewer: automated source execution and mathematical/prompt/step review, not external independent acceptance. Corrected revision is the containing publication commit.

One formal hands-on workflow,40 local answer records,twelve lab steps and ten separate process-control records are distinguished from four exact-source commands,47 supplemental predicates and **eight** existing unittest methods. Zero historical unique methods added. [results.json](results.json) retains raw stdout/stderr, actual values/tolerances, runtime/platform/SciPy, input fixtures/criteria and source/listing SHA256.

From repository root:

```bash
python books/book-01-python-foundations-for-financial-mathematics/qa/chapter-17-validation-review/review.py
```

Reproduce unchanged source (expected nonzero exit; requires history):

```bash
python books/book-01-python-foundations-for-financial-mathematics/qa/chapter-17-validation-review/review.py 0e8bd0fcb5d2bd3e45262569342c152afbe44f52
```

[baseline.json](baseline.json) retains12 failed predicates; original eight methods and the SciPy snippet already passed. Defects/contracts include integer/tiny-rate/discounted-flow loss in NPV, price residual rounding before subtracting price, signed variance overflow/cancellation to NaN, overflowed comparator intermediates giving a false pass, integer/float comparison loss, malformed/huge input exceptions, relaxed PSD boundary due to rounded square roots and silently erased positive risk. The exact displayed-decimal tolerance boundary is an explicit specification choice: a binary-expansion interpretation is different, not universally wrong. New source documents the chosen integer/displayed-decimal contract. Twelve predicates are not12 distinct defects. No observer failures occurred.

## Exact execution and independent expectations

Four isolated commands execute the verbatim tilde-fenced reference/eight methods, silent import, compilation and printed SciPy root snippet. A separate unchanged-snippet execution in a namespace supports two independent yield/repricing predicates; stdout retained. No supplemental solver substitutes for exact reference execution. Analytical/rational expectations and acceptance budgets are specified in the runner before the baseline run, not adjusted to make results pass.

Fictional annual-effective rate.1 and cashflows[-100,110],t0/t1, imply NPV0 and IRR1/10. Separate price-residual fixture price100,future_cashflows[0,110] subtracts price once; input t0 zero is explicit. PV110/1.1=100, zero-rate PV100, and NPV at.11=−100/111≈−.9009009. Currency residual budget1e−12, SciPy root absolute budget1e−12 and independent SciPy repricing currency budget1e−10 are recorded. No real instrument calendar/market data provided.

Analytic NPV expectations at rates0,.05,−.5,1e−308 are −100+110/(1+r), derived with Fraction, and doubled flows are checked against twice that expression. Appending a zero after the existing terminal period leaves PV unchanged. Inserting a period before110 changes it from one-year PV100 to two-year110/(1.1²)=1000/11. The manuscript invariant/answer now states this timing prerequisite rather than implying arbitrary zero insertion is harmless.

Mixed tolerance example actual100.02/reference100/atol.01/rtol.00005 has error1/50=.02 and threshold3/200=.015, hence fail. The boundary100.015 passes under documented displayed-decimal semantics. At actual1.79e308/reference−1.79e308/atol1.79e308/rtol.1, true difference3.58e308 exceeds threshold1.969e308, so fail: comparing float infinities originally returned true. An integer10^18+1 against float1e18 with zero tolerances retains difference1. Thresholds remain rational internally even beyond float reporting range; tolerances are never widened.

Two-asset covariance fixture diag(.04,.09),equal weights.5 yields13/400=.0325. Exact PSD requires nonnegative diagonals and c²≤v1v2; c=.04000000000000001 with v1=v2=.04 is invalid despite rounded sqrt products appearing equal. Signed weights[1e308,−1e308] under identical rank-one covariance cancel exactly to variance0; this is an algebraic stress case, not an investable portfolio. The variance function deliberately permits signed/nonunit weights; [.4,.4] gives13/625=.0208 but does not establish a fully invested budget. Feasibility/mandate rules remain separate.

Rational integer/displayed-decimal calculations precede float reporting for discounting, full price residual, comparison and quadratic forms. Required nonzero computed numeric reports reject on underflow; nonfinite outputs reject. Cashflow iterables are consumed once and nonempty. Exact model arithmetic does not restore already-rounded float observations, validate cashflow conventions, or preserve every increment in a large final float. A small residual does not certify root error, uniqueness, model suitability or external approval.

## Forty worked-answer records

| Exercise | Alignment and execution boundary |
|---|---|
| 01 | Specification conformance is verification; conceptual, scope of current source tests. |
| 02 | Fitness for purpose is model validation; remains external/model-specific acceptance. |
| 03 | Source one-year PV100 versus rational110/1.1. |
| 04 | Source NPV0 at.1 within stated currency budget. |
| 05 | Source zero-rate PV100. |
| 06 | Positive future-flow PV decreases as valid rate rises; source checked. |
| 07 | Source doubled cashflows compared with independent analytic2×NPV across four rates. |
| 08 | Source appended terminal zero preserves timing/PV; inserted period has distinct1000/11 PV. Wording corrected. |
| 09 | Source specified mixed tolerance fails, with independent error/threshold. |
| 10 | Near-zero absolute scale needed; known-zero checks use explicit absolute currency budget. |
| 11 |5%=.05 decimal, rate convention reviewed. |
| 12 |1bp=.0001 decimal, unit definition. |
| 13 | Supplemental .11−.10=.01=100bp. |
| 14 | Source calculated100.03−price100 at zero rate=.03. |
| 15 | Small price residual can coexist with inaccurate yield; conceptual conditioning limit. |
| 16 | NPV[-100,110] includes purchase price at t0. |
| 17 | Source price_residual input[0,110] excludes price; separate price subtracted once before reporting. Caller schedule cannot be inferred automatically. |
| 18 | Source rate−1 rejects. |
| 19 | Source comparator NaN rejects. |
| 20 | Source comparator infinity rejects. |
| 21 | Integral1/3 analytical benchmark reviewed; no quadrature export in this section. |
| 22 | Two-grid agreement can share bias; conceptual, no rigorous refinement certifier. |
| 23 | Optimizer success need not mean global optimum; no optimizer export. |
| 24 | Supplemental exact budget residual1.001−1=.001; not verified by variance API. |
| 25 | Source variance13/400=.0325. |
| 26 | Source exact PSD inequality without rounded sqrt-bound relaxation. |
| 27 | Conditioning can magnify solution error despite residual; conceptual. |
| 28 | One IRR does not prove uniqueness; SciPy one-period root not general enumeration. |
| 29 | Explicit SciPy bracket[0,.2] retained in exact snippet; source NPV itself has no solver. |
| 30 | Source negative future flow reverses PV monotonicity; positive-flow premise explicit. |
| 31 | Wrappers sharing a solver are not fully independent; rational analytical oracles separate from source wrappers. |
| 32 | IID finite-variance SE scales1/sqrtN; no Monte Carlo run or error estimator here. |
| 33 | Seed supports reproducibility, not validity; conceptual. |
| 34 | Statistical interval does not automatically cover model bias; no simulated intervals claimed. |
| 35 | Source NPV at.11 versus exact−100/111. |
| 36 | Exposure determines materiality; no production mandate/tolerance approval. |
| 37 | Settlement/day count examples remain unsupported conventions, not tested production bond features. |
| 38 | Baseline failures retained; fixes investigated without widening acceptance budgets. |
| 39 | Revalidation after relevant change is a process requirement; this batch hashes reviewed source. |
| 40 | Eight unit methods do not certify production model; all limits explicit. |

## Twelve lab-step records

Prerequisites: Python, finite typed quantities, periodic annual-effective rate>−1, explicit t0/list timing, nonempty cashflow iterable, nonnegative tolerances, compatible two-asset PSD covariance. Weights may be signed/nonunit in the variance function; mandate checks separate. SciPy installed for printed example. Fictional common currency, no actual calendar/as-of inputs.

| Step | Actual evidence and scope |
|---|---|
| 1 | Recorded rate/timing/sign/units and separate NPV versus price-residual fixtures. |
| 2 | Source PV110/1.1=100 independently checked. |
| 3 | Source NPV0 with preselected1e−12 currency budget. |
| 4 | Source .11 NPV−100/111;100bp perturbation interpreted. |
| 5 | Source doubled-flow linearity, appended-zero invariant and inserted-period contrast. |
| 6 | Source zero rate and−1 rejection. |
| 7 | Source equal-weight variance.0325. |
| 8 | Source ordinary/near-boundary invalid PSD rejects; signed/range reporting stress separate. |
| 9 | Source specified mixed-tolerance fail, exact displayed boundary pass, overflow false-pass correction. |
| 10 | Exact reference/eight existing methods, import and compilation outputs retained. |
| 11 | Exact SciPy snippet plus independently derived.1 yield and rational repricing. |
| 12 | Four exact commands,47 supplemental predicates,eight existing methods and12 baseline failures retained; no external approval. |

## Ten process-control records — not ten independent approvals

| Control | Scoped disposition |
|---|---|
| 1 Intended use/assumptions | Fictional periodic/PV/variance teaching model explicit; real-use approval absent. |
| 2 Independent reference | Rational analytical one-period/variance/threshold expectations; not a second wrapper around source solver. |
| 3 Acceptance criteria | Numeric budgets encoded before baseline; model/data/business thresholds not approved. |
| 4 Input domains | Finite/typed/rate/PSD/shape checks exercised; calendar/market completeness not supplied. |
| 5 Known/boundary/invariant | Ordinary/extreme arithmetic, appended-flow/linearity/monotonicity cases executed. |
| 6 Status/residual/constraints | Exact SciPy convergence and repricing checked; budget/mandate validation deliberately separate from variance. |
| 7 Methods/sensitivity | Analytic cross-check and10→11% perturbation executed; no optimizer/MC or market schedule analysis. |
| 8 Failure investigation |12 baseline predicate failures retained, source repaired; comparator semantics explicitly specified rather than hidden tolerance changes. |
| 9 Evidence/reproducibility | Raw outputs/model/versions/hashes retained; no real sensitive/market dataset. |
| 10 Revalidation | Source-bound results/checkpoint saved; external review and future dependency/data/use changes still require appropriate review. |

## Limits and resume checkpoint

Local Linux CPython/SciPy only. No production bond schedules, general root/optimizer/integration/Monte Carlo implementation, full mandate/budget checks, real data/model approval, arbitrary-conditioning/correct-rounding proof, production performance, broad shared-input integration, notebook/platform or external independent acceptance/certification. Source execution, supplemental rational derivations and conceptual process controls are separate above. F28/F32, F165 integrated-CDF tail limits and all unresolved tracker findings remain open.

Chapter17 has thirteen core workflows and515 local answers scoped. Next: Section17.14 — Chapter Project — Financial Numerical Solver. Resume from fresh main without duplication.
