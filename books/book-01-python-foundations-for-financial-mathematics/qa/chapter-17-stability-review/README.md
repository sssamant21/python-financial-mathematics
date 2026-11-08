# Section 17.11 — scoped numerical stability review

Affected baseline: `e7fabf3bcb43a6956461213703eb842e839d700d`. F168, severity medium (educational numerical correctness), owner Book 1 manuscript maintainers. Decision repair scale/cancellation/reporting defects while distinguishing printed binary64 demonstrations from guarded reference exports. Reviewer: automated source execution and mathematical/prompt/step review, not external independent acceptance. Corrected revision is the containing publication commit.

One workflow,40 local answers and twelve lab steps are separate from seven exact-source command records,55 supplemental predicates and twelve existing unittest methods. Zero historical unique methods added. [results.json](results.json) records runtime/platform/NumPy/SciPy, raw stdout/stderr, quantities/tolerances, model, source/listing SHA256 and primitive observations.

From repository root:

```bash
python books/book-01-python-foundations-for-financial-mathematics/qa/chapter-17-stability-review/review.py
```

Reproduce unchanged source (expected nonzero exit; requires history):

```bash
python books/book-01-python-foundations-for-financial-mathematics/qa/chapter-17-stability-review/review.py e7fabf3bcb43a6956461213703eb842e839d700d
```

## Retained failures and corrected rerun

[baseline.json](baseline.json) retains29 failed predicates under the final55-predicate observer; the original twelve methods and all printed examples/SciPy assertions already passed. Defects/contracts include tiny product loss and intermediate exponential overflow in annuities, zero-intensity overflow, extreme log-return ratios, signed sum overflow, NPV integer/tiny-rate/power loss, lost small log-sum-exp correction, scaled discriminant/root failures and wrong negative-discriminant decisions, nonfinite/underflowed reports, malformed/callback-coordinate handling and empty-NPV policy. Some invalid-input/empty-input cases are explicit contract additions;29 failed predicates are not29 distinct defects.

[first-correction-rerun.json](first-correction-rerun.json) retains the55-predicate run with two failures: even Decimal exponentiation can underflow to0 at an enormous negative exponent. The first guarded source therefore still returned0 for discount(rate1e308,tenor1) and compound(rate−.5,periods10^1000). `_exp_report` now rejects a zero Decimal exponential before float conversion. Final corrected source passes all55 predicates/seven commands. This is a retained source reporting failure/correction, not an observer error; no observer failures occurred. Inventories are not summed across runs.

## Exact execution versus independent benchmarks

Seven isolated command records execute the verbatim reference demonstration/twelve tests, silent import, compilation, epsilon fragment, summation fragment, contextual log-return fragment and SciPy/NumPy stability snippet. The contextual fragment is executed unchanged with only the explicitly required bindings P0=100,P1=101; it is not a standalone complete program. All raw outputs are retained. A second unchanged SciPy snippet execution in a namespace supports independent solution/tail/log-sum-exp checks.

For A=[[4,1],[1,3]],b=[1,2], exact solution is[1/11,7/11], derived by elimination/determinant11. SciPy logsumexp([1000,1000]) is compared with1000+ln2, and norm.sf(8) with independent standard-library erfc(8/sqrt2)/2. A positive survival probability here does not fix or certify Section17.8's zero-centered integrated CDF tail behavior; F165's disclosed limits remain open.

Fictional continuous annuity C100 currency/year,T2 years,r.05/year has PV2000(1−exp(−.1)). Independent Decimal1000 provides both this expectation and tiny-rate r1e−12 expectation. Coupled stress r1e−308,T1e−308,C1e308 is approximately1; the stable primitive alone cannot save a binary64 r*T that has already rounded to0. Negative-rate stress r−1000,T1,C1e−308 has finite PV1e−308*(exp(1000)−1)/1000 although its standalone exponential overflows binary64. Zero intensity/tenor returns0 without irrelevant exponentiation; a genuinely nonzero unreportable annuity rejects.

Periodic NPV fixture[-100,110],rate.1,t0/t1 has exact displayed-decimal value0; absolute1e−12 currency budget retained for the original float baseline. Rational expectations cover integer cancellation, tiny rates and high-rate discounted cashflows. Compound.01/12 equals1.01^12. Log returns for ratios1e±616 have finite logarithms±616ln10 even though binary64 ratios overflow/underflow. Stable-q quadratic cases use exact factorizations/scaled(1,−3,2), reciprocal large/small roots, repeated root and b0 branches; tiny negative discriminants reject before square root.

The mathematical small log-sum-exp correction ln(1+exp(−40)) is independently computed with high-precision Decimal; the original log(fsum(1,exp(−40))) returned0. Revised max-shift excludes one maximum before `log1p`, retaining this correction. Deep exponential weights below binary64 subnormal range are discarded; zero-maximum/nonreportable positive corrections reject. This is scoped float transcendental evaluation, not arbitrary correctly rounded log-sum-exp proof.

## Numeric and interpretation boundaries

Printed epsilon, `log1p`, `expm1`, `math.fsum` and non-associative binary64 demonstrations remain unchanged. Reference exports now use exact integer/displayed-decimal rational arithmetic for model sums/NPV/ratios/discriminants and scale-aware Decimal guards for log/exp/annuity/quadratic operations before finite float reporting. This is a disclosed extension of the original binary64-only reference, not a claim that ordinary primitives alone solve every coupled-range problem. Required nonzero computed reports reject if lost on conversion; Decimal underflow is checked for positive exponentials. Mathematical conditioning and model validity remain separate.

Input types are finite Python int/float with booleans excluded. Iterable terms are consumed once; empty sum returns0, empty NPV/log-sum-exp rejects explicitly. Callback residual validates coordinate/function/value, but arbitrary callback exceptions propagate and a residual does not certify root error/uniqueness. Supplied floats may already be rounded; finite reporting cannot preserve every small increment in a huge number. No market calibration or actual data inputs are supplied.

## Forty worked-answer records

| Exercise | Alignment and execution boundary |
|---|---|
| 01 | Exact epsilon fragment runs; recorded runtime spacing2^-52. Not universal accumulated error bound. |
| 02 | Direct(1e16+1.0)−1e16=0 observed, distinct from actual built-in sum implementation. |
| 03 | Exact fsum example recovers1; source stable_sum also checked. Built-in sum output retained, not assumed across versions. |
| 04 | x1e−16 lost in1+x; observed cancellation/log example. |
| 05 | Printed contextual log1p fragment runs with P0/P1 bindings; supplemental x1e−16 comparison shows advantage. |
| 06 | Supplemental expm1(x)>0 while exp(x)−1=0 at1e−16. |
| 07 | −expm1(−rT) identity reviewed; reference annuity additionally protects r*T and amount scaling via Decimal. |
| 08 | Source zero-rate annuity200. |
| 09 | Source positive-rate annuity versus independent Decimal formula. |
| 10 | Source log return100→101 versus ln1.01. |
| 11 | Contextual float formula is suitable locally but not universally range-safe; reference extreme-ratio tests separate. |
| 12 | Source compound versus exact-form Decimal1.01^12; zero periods returns1. |
| 13 | Source NPV0, periodic t0/t1 and currency residual budget recorded. |
| 14 | exp(−t log1p(r)) mathematical identity reviewed; source NPV uses rational integer-period discounting to avoid early exponential loss. |
| 15 | Direct binary64 exp(−1000) can underflow; guarded reference reports ValueError for unreportable positive discount. |
| 16 | Direct exp(1000) may overflow; guarded finite-report failure separated from mathematical existence. |
| 17 | Source/printed SciPy log-sum-exp≈1000+ln2, plus independently checked small correction. |
| 18 | Consistent currency scaling reviewed; numeric range probes not a general optimizer conditioning proof. |
| 19 | Meaningful residual scale needed; conceptual, no universal normalization export. |
| 20 | Absolute tolerance has units; known-zero NPV uses1e−12 currency budget. |
| 21 | Relative tolerance near zero needs meaningful scale; oracle comparison explicitly records absolute/relative choices. |
| 22 | Mixed tolerance formula reviewed; no blanket financial acceptance threshold inferred. |
| 23 | Problem conditioning differs from algorithm defect; conceptual. |
| 24 | Backward stability means solving a nearby input problem; no formal backward-error proof for all reference exports. |
| 25 | Small derivative can magnify root uncertainty; conceptual, no root solver exported. |
| 26 | Nonconventional signs can produce multiple IRRs; conceptual, NPV is not all-root enumeration. |
| 27 | Naive small quadratic root cancellation observed; source stable-q independently checked across ordinary/huge/tiny scales. |
| 28 | Near-singular covariance affects sensitivity; conceptual, no covariance estimator/regularizer here. |
| 29 | Exact SciPy linear solve snippet and independent[1/11,7/11] oracle; residual alone not conditioning certificate. |
| 30 | Log-discount representation reviewed; curve implementation not exported in this section. |
| 31 | Log differences preferable when available; conceptual, no forward-rate export here. |
| 32 | Tiny tenor-gap conditioning remains separate from stable arithmetic. |
| 33 | Exact SciPy sf8 positive and independently compared to erfc; Section17.8 tail gap remains open. |
| 34 | Finite-difference h/cancellation tradeoff reviewed; no derivative implementation here. |
| 35 | Quadrature refinement eventually faces roundoff; conceptual, no quadrature export here. |
| 36 | Objective/penalty scaling must respect units; conceptual, no optimizer exported. |
| 37 | Runtime/platform versions recorded; no cross-platform/BLAS acceptance. |
| 38 | Report-boundary rounding policy explicit; no intermediate currency-cent rounding imposed. |
| 39 | Decimal helps precision with explicit context, not model/conditioning proof; guarded Decimal underflow failure retained. |
| 40 | Inputs/units/algorithms/outputs/tolerances/hashes/versions retained; external independent approval absent. |

## Twelve lab-step records

Prerequisites: Python, finite typed quantities, positive prices for log return, periodic rate>−1 and integer periods for compound/NPV, nonnegative continuous tenor, valid real quadratic discriminant; NumPy/SciPy installed for separate snippet. Cashflows fictional with compatible period/continuous-rate units. No market timestamps or platform-installation acceptance.

| Step | Actual evidence and limit |
|---|---|
| 1 | Verbatim reference saved isolated, runtime and source/listing hashes retained. |
| 2 | Exact printed epsilon fragment runs; independent2^-52 predicate. |
| 3 | Direct non-associative operations observed. |
| 4 | Exact sum/fsum fragment and actual version-dependent outputs retained. |
| 5 | Context fragment gets only P0=100,P1=101; separate x1e−16 naive/log1p values retained. |
| 6 | exp(x)−1/expm1 at1e−16 retained as supplemental primitive observations. |
| 7 | Source ordinary/tiny/zero/scaled annuities independently checked, with output-range failure paths. |
| 8 | Source100→101 log return/.01 for12 periods, extreme ratios and zero-period controls. |
| 9 | Naive small-root cancellation and source stable-q/scaled/repeated/b0 tests. |
| 10 | Source large-argument log-sum-exp, printed SciPy snippet and small-correction oracle. |
| 11 | Source periodic NPV known-zero and integer/tiny-rate/discount-scale probes; no root accuracy/uniqueness claim. |
| 12 | Seven exact commands,55 supplemental predicates and twelve existing methods pass;29 baseline failures and a separate two-failure Decimal reporting transition retained. |

## Limits and resume checkpoint

Local Linux CPython/NumPy/SciPy only. No general root/optimizer/integration/curve/matrix/tail implementation, arbitrary-conditioning/correct-rounding certification, real financial data/model acceptance, production performance, broad shared-input integration, notebook/platform or external independent review. Exact source, supplemental derivations and conceptual controls are separate above. F28/F32, F165 integrated-CDF tail limits and all unresolved tracker findings remain open.

Chapter17 has eleven core workflows and435 local answers scoped. Next: Section17.12 — Convergence and Error; resume from fresh main without duplication.
