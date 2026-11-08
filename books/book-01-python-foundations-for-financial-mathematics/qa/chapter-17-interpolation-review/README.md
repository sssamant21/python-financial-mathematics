# Section 17.9 — scoped interpolation review

Affected baseline: `473cfcd129fe042c9f1ddcde4a8f81c869609add`. F166, severity medium (educational numerical correctness), owner Book 1 manuscript maintainers; decision repair interpolation/log/forward precision and finite/input/reporting contracts. Reviewer: automated source execution plus mathematical/prompt/step review, not external independent acceptance. Corrected revision is the containing publication commit.

One workflow,40 local answer records and twelve lab-step records are separate from four exact-source commands,45 supplemental predicates and twelve existing unittest methods. Zero historical unique methods added. [results.json](results.json) retains raw stdout/stderr, values/tolerances, runtime/platform/NumPy/SciPy versions, fixtures and source/listing SHA256.

From repository root:

```bash
python books/book-01-python-foundations-for-financial-mathematics/qa/chapter-17-interpolation-review/review.py
```

Reproduce unchanged-source baseline (expected nonzero exit, requires history):

```bash
python books/book-01-python-foundations-for-financial-mathematics/qa/chapter-17-interpolation-review/review.py 473cfcd129fe042c9f1ddcde4a8f81c869609add
```

## Failures, observer correction and reruns

[baseline.json](baseline.json) retains16 failed predicates under the final45-predicate observer; original twelve methods/SciPy snippet already passed. Recorded defects include wide-coordinate/ordinate differences, integer cancellation and knot identity, ratio overflow/underflow, erased tiny forwards (including close queries on a huge tenor span), malformed-input exceptions, nonboolean extrapolation policies and unreportable outputs. A strict boolean extrapolation argument is an explicit contract tightening. Sixteen predicates do not mean16 distinct defects.

[initial-observer-baseline.json](initial-observer-baseline.json) retains the first42-predicate run with16 failures, one caused by my incorrect SciPy cubic midpoint oracle307/6400. [observer-oracle-correction.json](observer-oracle-correction.json) records the independent rational four-point Lagrange derivation609/12800, matching the not-a-knot cubic. This was an observer error, not a SciPy/source defect. The corrected42-predicate baseline had15 source/contract failures.

[first-correction-rerun.json](first-correction-rerun.json) retains the subsequent45-predicate source rerun with one failure: piecewise forward on tenors[0,1e308], discounts[.9,.8], queries0/1e−308 returned0 instead of ln(1.125)/1e308≈1.17783035656e−309. Precision based only on the maximum input fraction length was insufficient for the combined coordinate scales. The corrected source sums input fraction digit lengths plus100 guard digits. The final baseline has16 failures; final corrected source45 predicates/four commands pass. These inventories are not added together; the earlier source hashes identify transitions.

## Exact execution and independent derivations

Four isolated commands run the verbatim reference demonstration/twelve tests, silent import, compilation and printed NumPy/SciPy interpolation snippet. A separate unchanged-snippet execution in a namespace supports four supplemental result/shape/domain checks, with its stdout retained. No supplemental curve implementation substitutes for source execution.

For linear interpolation at x2 between(1,2),(3,6), exact λ=1/2 and y4. Integer/displayed-decimal rational weights avoid wide-span/difference overflow and preserve supplied integer differences. Exact knots return the supplied ordinate/discount, including integer identity; interior/extrapolated reports use floats with finite/nonzero requirements. Nodes are reusable paired lists/tuples, strictly increasing; extrapolate must be bool and only generic linear interpolation permits explicit extrapolation.

For SciPy PCHIP nodes1,2,3,5 and rates.04,.045,.05,.055, the derivatives at2 and3 are1/200 and9/2600. The Hermite midpoint is(.045+.05)/2+(1/200−9/2600)/8=31/650≈.04769230769. The not-a-knot four-point spline equals the global interpolating cubic: rational Lagrange evaluation at5/2 yields609/12800=.047578125. The observer derives this polynomial value independently at runtime. Sampled monotonicity and outside-domain NaNs are finite fixture checks, not a general shape/arbitrage proof. The separate SciPy log-discount midpoint uses logs−.09/−.15, giving exp(−.12).

Fictional lab tenors[1,2,3] years and continuous annual zero rates[.04,.05,.06] produce supplied float discount observations exp(−.04),exp(−.10),exp(−.18). Source log-discount value at2.5 is exp(−.14), with recovered continuous zero.056; the average forward from1 to3 is.07. Outer-node-only comparison at2 intentionally removes the2y quote: linear-zero gives.05/DF exp(−.1), while log-discount gives exp(−.11). The full three-node curve preserves the actual2y quote; the differing experiment is not silent data removal.

Discounts.9/.81 have geometric midpoint sqrt(.729). Direct forwards use exact discount ratio then Decimal logarithm; piecewise forwards subtract interpolated log discounts before either discount report is rounded. Tests include ratio(10^18+1)/10^18, ratios1e±616, and huge-tenor/close-query cancellation. Scale-dependent Decimal precision mitigates those cases but is not arbitrary-conditioning/correct-rounding certification. Negative forward rates and discounts>1 remain valid under this convention. Supplied float observations may already contain rounding; exact arithmetic does not restore unavailable market precision.

## Forty worked-answer records

| Exercise | Alignment and execution boundary |
|---|---|
| 01 | Source linear midpoint4. |
| 02 | Exact affine weight(2−1)/(3−1)=1/2, analytic derivation. |
| 03 | Source left endpoint2. |
| 04 | Source right endpoint6; additional integer knot identity checked without float-coercing expectation. |
| 05 | Source explicit linear extrapolation8; default rejects. |
| 06 | Source duplicate-node rejection. |
| 07 | Source rejects unsorted pairs; caller must sort paired observations, not x alone. No automatic sorting export. |
| 08 | Missing-value interpolation is model assumption, not discovery of true quote; conceptual. |
| 09 | Slope(6−2)/(3−1)=2, analytic. |
| 10 | Shared knot values establish piecewise continuity; exact node preservation exercised. |
| 11 | Unequal neighboring slopes permit derivative jumps; conceptual, no smoothness guarantee for generic linear curves. |
| 12 | Three distinct nodes uniquely determine degree≤2 polynomial; conceptual, no polynomial export in standard-library listing. |
| 13 | Exact SciPy spline example run; cubic continuity/boundary dependence reviewed. |
| 14 | Overshoot risk reviewed; monotone sampled fixture is not proof of arbitrary spline behavior. |
| 15 | Exact SciPy PCHIP result compared with independent Hermite oracle and finite monotone samples. |
| 16 | Source linear-zero outer-node interpolation gives.05. |
| 17 | Supplemental zero-to-discount exp(−.1); standard listing has no zero-to-DF export. |
| 18 | Source continuous zero recovery from supplied exp(−.1) observation≈.05. |
| 19 | Source geometric midpoint sqrt(.729)≈.8538149682. |
| 20 | Linear log-DF slope implies constant interval instantaneous forward; analytic, piecewise average forwards executed. |
| 21 | Source forward from exp(−.05)/exp(−.1)≈.05. |
| 22 | Discounts>1/negative rates allowed; source negative-forward case executed. |
| 23 | Source nonpositive-discount rejection. |
| 24 | Positive forward implies declining D under matching continuous convention; analytic. |
| 25 | Source increasing discounts give negative forward; not automatically invalid. |
| 26 | Smoothness alone does not establish arbitrage-free pricing; conceptual/market acceptance open. |
| 27 | All fixture tenors explicitly years; no month/year-fraction conversion implementation. |
| 28 | ACT365/ACT360 conventions alter t; no calendar/day-count engine here. |
| 29 | Supplemental rational coupon PV5*.9+105*.81=1791/20=89.55, not a source pricing export. |
| 30 | Sparse interpolation/extrapolation model risk remains conceptual. |
| 31 | Source default out-of-range rejection and explicit generic-linear extrapolation exercised; log curves reject outside range. |
| 32 | Flat-forward extension conceptually differs from flat-zero; no such extrapolator exported. |
| 33 | Quote bump/rebuild/PV sensitivity remains design, not an executed market risk system. |
| 34 | Bootstrap/repricing consistency required conceptually; no market calibration engine here. |
| 35 | Known affine-function values supply held-out exact benchmarks; no estimate of real unobserved market error. |
| 36 | Leave-one-out is a diagnostic; controlled outer-node experiment illustrates withheld interior quote, not prediction-quality acceptance. |
| 37 | Runge-type global polynomial instability reviewed conceptually; no high-degree implementation tested. |
| 38 | Natural spline endpoint second derivatives differ from default SciPy not-a-knot used here; distinction explicit. |
| 39 | Ordered nodes/units/method/extrapolation/runtime/hashes retained; no real day-count or approvals. |
| 40 | Forward sign assumptions and market repricing acceptance remain caller/external responsibilities. |

## Twelve lab-step records

Prerequisites: Python; finite int/float inputs with booleans excluded; reusable paired strictly increasing nodes; common year fractions/quote units; positive discount factors/nonnegative log-curve tenors. NumPy/SciPy installed for the separate snippet. All data fictional, without market/as-of/calendar assumptions beyond stated years and continuous annual compounding.

| Step | Actual evidence and limit |
|---|---|
| 1 | Exact reference saved isolated; runtime/source/listing hashes retained. |
| 2 | Source simple linear midpoint4. |
| 3 | Source endpoints2/6 plus exact integer and supplied-discount knot preservation. |
| 4 | Source duplicate and unsorted errors retained. |
| 5 | Source default rejection versus explicit extrapolation8; strict boolean policy separately checked. |
| 6 | Explicit three-node zero table[1,2,3]/[.04,.05,.06]. |
| 7 | Supplemental math.exp converts to supplied discount observations; no hidden zero-to-DF source export. |
| 8 | Source log-discount at2.5 on full table versus exp(−.14), and separate outer-node midpoint experiment. |
| 9 | Source recovered2.5y zero.056, plus known2y recovery.05. |
| 10 | Source full-table average forward1→3=.07, constant-rate.05 fixture and negative-forward case. |
| 11 | Outer-node-only comparison exp(−.1) versus exp(−.11) distinct from full quote-preserving curve; printed SciPy families separately checked. |
| 12 | Four commands,45 supplemental predicates and twelve existing methods pass;16 final-observer baseline failures plus separate initial oracle/source-precision transitions retained. |

## Limits and resume checkpoint

Local Linux CPython/NumPy/SciPy only. No market bootstrap, calendar/day-count reconciliation, arbitrary arbitrage/shape/conditioning proof, flat-forward extrapolator, standard-library spline/PCHIP export, coupon-pricing or quote-risk engine, production performance, broad shared-input integration, notebook/platform or external independent certification. Source execution, supplemental exact/Decimal derivations and conceptual controls are separate above. F28/F32, F165 CDF-tail limits and all unresolved tracker findings remain open.

Chapter17 has nine core workflows and355 local answers scoped. Next: Section17.10 — Curve Construction Concepts; resume from fresh main without duplicating this batch.
