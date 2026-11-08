# Section18.5 — Return simulations: scoped review

Reviewed2026-11-08 by Codex, not an external independent reviewer. Baseline `992bc63dc9eb9ace107c19a44e040001966d9bcf`; [source](../../chapter-18/18.05-return-simulations.md). One workflow, forty local answers, twelve lab steps, no new historical unique methods.

Run from repository root:

```bash
python books/book-01-python-foundations-for-financial-mathematics/qa/chapter-18-returns-review/review.py
python books/book-01-python-foundations-for-financial-mathematics/qa/chapter-18-returns-review/review.py 992bc63dc9eb9ace107c19a44e040001966d9bcf
```

The baseline command intentionally exits1 and requires the baseline git object. [Baseline](baseline.json) retains fifteen failed supplemental predicates; [corrected results](results.json) retains all78 passing predicates, source/listing SHA256, runtime, actual stdout/stderr and seeded run records. Three exact-source commands pass in both revisions: verbatim reference demo/ten existing methods, quiet import and compile. The78 supplemental predicates are not additional unittest methods or exercises. CPython3.12.14/Linux, local random.Random/Mersenne Twister normalvariate; no cross-version or platform agreement claim.

## Finding F177 and support extension

Original zero-log terminal and analytical expectation calculations lose integer identity at initial`10**18+1`. Dividing rounded mean by initial erases a mean simple return of1e-18. Finite normal inputs can produce infinite draws; huge integer inputs leak OverflowError; noniterable returns/sample leak TypeError; an unreportable simple-return ratio can be infinity. These failures substantiate guarded output and input/reporting corrections.

Source now defines finite int/float input range, booleans excluded, displayed-decimal floats/exact integers, ValueError for invalid/unreportable nonzero results, guarded standard-normal affine sampling, exact zero-log identity and rational summary return before rounding the mean. Standard error is computed directly from rational variance/N, not by overflowing an intermediate sample variance/SD. Empty log-return iterables return an empty terminal list, while summarize requires at least two strictly positive terminal values and a positive initial.

**Two of the fifteen baseline failures are explicit support extensions:** initial1e-308 with L1000, and initial1e308 with L−1000, have finite final products despite unreportable intermediate exp(L). The earlier source explicitly disclaimed support for all representable combinations, so these are not retroactively claimed as violated promises. Decimal scaled exponentials now check the final product. Exponents outside±2000 cannot produce a reportable final result for positive finite-float-range initial values, so the source rejects them early. Precision is finite; this is not a certified arbitrary-precision algorithm. Guarded affine sampling/Decimal exponentiation can alter last-bit results and thus stream/output hashes relative to older source revisions. Original ten unittest methods remain unchanged and pass. No observer correction was needed in this batch.

## Independent expectations and evidence boundaries

Exact-source evidence is the unchanged fence per recorded revision plus its commands. All extra calls, algebra, central CDF series and sample-statistic computations are supplemental QA implementations, not chapter exports.

Simple-return algebra independently gives (110−100)/100=.1, (90−100)/100=−.1, zero-price return−1, and cumulative1.1×.9−1=−.01. Equal±.1 outcomes have mean0, variance.01, SD.1 and loss probability.5. Decimal ln1.1 verifies log return.0953102 to seven decimal places; log1p/expm1 at1e-20 illustrate stable near-zero transforms separately from source APIs.

For L=m+sZ, completing the square in the standard-normal integral gives E[exp(L)]=exp(m+s²/2). Median exp(L)=exp(m), since standard-normal median is0. Thus at m=.04,s=.2, the exponent is.06, mean terminal100exp(.06)≈106.18365, mean simple return≈.0618365 and median100exp(.04)≈104.08108. Decimal exponential expectations and displayed rounding are checked independently of the source implementation's helper, though both use Python Decimal as a shared arithmetic backend; this is not independent numerical-library certification.

Loss for s>0 is P(Z<−m/s)=Φ(−.2). A100-digit Decimal series integrates exp(−z²/2) from0 to.2 using60 terms and a recorded100-digit π constant, giving approximately.42074029056; rounded.42074 is checked. This **fixed central-point supplemental oracle does not resolve F165's general integrated-CDF tail limitations** or implement a source CDF. The s=0 case is handled as deterministic: m=.04 gives terminal104.0810774…, zero sample SE and zero strict losses; m=0 gives100 and no strict loss.

Given actual source terminal observations, independent Fraction(str(value)) arithmetic computes mean, simple-return ratio, unbiased variance and SE=sqrt(variance/N), and exact strict-loss counts. It checks arithmetic conditional on observed values, not independent normal distribution quality. Numerical predicates use rtol1e-12,atol0 and exact identity where appropriate; they are not statistical acceptance bands. Seed replay/global-state checks share the source generator. No requirement for exact analytical/sample means, monotonic improvement, independent seed certification or confidence-interval coverage is imposed.

## Twelve lab-step contracts

Prerequisites: Python standard library, save reference as return_simulations.py, distinguish dimensionless one-year log returns m/s from simple return and terminal-currency units. Initial100; uncalibrated fictional model, no external dataset/date, no risk-neutral dynamics or investment recommendation. Discount example is arithmetic at constant annual effective5%, not market-price acceptance.

| Step | Action, actual output and scoped limit |
|---|---|
| 1 | Recorded Python/platform, generator, seed42/43, N10000, one-year horizon, parameters/source hashes in JSON. |
| 2 | Simple100→110 return.1; independent Decimal log ln1.1≈.0953102; source terminal mapping also covered by original method. |
| 3 | Equal±10% model expectation0, variance.01, volatility.1, terminal expectation100 and loss.5; algebraic review, not a discrete source sampler. |
| 4 | Exact reference demo/ten tests ran; source generated10000 log returns and terminal values. |
| 5 | Independent exp(.04+.2²/2) mean106.1836546545… versus source expectation; numerical/printed rounding checks pass. |
| 6 | Seed42 mean106.1983037392661, estimated SE.21806875180228977. Descriptive comparison with analytical mean; no statistical pass criterion inferred. |
| 7 | Independent median104.0810774192…; lognormal right skew means mean>median when s>0. |
| 8 | Seed42 loss4237/10000=.4237 versus fixed central analytical probability.42074029056…. Recorded variation, not tail/coverage certification. |
| 9 | Seed43 mean106.34067423336751, SE.21317643380242254, loss4171/10000=.4171; actual run preserved without claiming independent replications merely from differing seeds. |
| 10 | s0,m.04,seed42: all deterministic terminal values, mean104.08107741923882, SE0, loss0; m0/s0 exact terminal100 checked. |
| 11 | Invalid input/output cases and original methods run; fifteen original failed predicates and corrected pass retained, two support extensions labeled. |
| 12 | Assumptions, units, scope, commands, source hashes and actual evidence retained; broader limits below. |

## Forty prompt-to-answer alignment records

Every local prompt/answer read in source order. Conceptual statements are not counted as callable source tests.

| Answer | Scoped disposition |
|---|---|
| 1 | Simple up return.10, independent rational ratio. |
| 2 | Simple down return−.10, independent ratio. |
| 3 | R.05 gives105, algebraic map. |
| 4 | Profit5 for100→105, subtraction. |
| 5 | Terminal0 gives simple return−1, ratio. |
| 6 | No finite log100→0, logarithm domain; source rejects nonpositive summary terminals. |
| 7 | ln1.1≈.0953102, Decimal logarithm/rounding. |
| 8 | exp0−1=0, exact special case. |
| 9 | +10% then−10% cumulative−1%, multiplicative exact fractions. |
| 10 | Equal±.1 mean0, weighted sum. |
| 11 | Variance.01, exact squared deviations. |
| 12 | SD.10, Decimal root. |
| 13 | Loss.5, state-probability algebra. |
| 14 | Normal simple return can be below−1, correct unbounded-support statement; source specifically samples log returns. |
| 15 | Clipping changes distribution, correct conceptual distinction; no clipping introduced. |
| 16 | exp(L)>0 in exact arithmetic, correct; source guards reportability. |
| 17 | Finite exponentiation can overflow/underflow, explicit source/probe cases. |
| 18 | Mean simple return exp(.06)−1≈.0618365; Decimal and displayed rounding. |
| 19 | Mean terminal≈106.18365, source versus independent model expectation. |
| 20 | Median≈104.08108, independent formula and displayed rounding. |
| 21 | LossΦ(−.2)≈.42074, fixed central integral series oracle; tail limits retained. |
| 22 | Zero volatility gives deterministic100exp(.04), source generated/terminal sample. |
| 23 | Zero drift/volatility gives100, source exact expectation and existing method. |
| 24 | Equality100 is not strict loss, source summary check. |
| 25 | Sample mean need not equal analytical mean, actual runs differ. |
| 26 | SD20,N10000 gives SE.2, exact arithmetic. |
| 27 | Fourfold N halves theoretical SE under same variance/IID assumptions, factor checked. |
| 28 | More draws cannot remove model bias, correct conceptual statement. |
| 29 | Seed supports compatible replay, source list-equality probe and original method. |
| 30 | Different-seed results not generally identical, selected outputs observed; no universal inequality/independence proof. |
| 31 | √12 scaling conditional, correct time/dependence requirement; no universal annualization API. |
| 32 | Real-world probabilities not automatically risk-neutral, correct measure limitation. |
| 33 | Discount100/1.05≈95.2381, exact rational arithmetic; no source discount API claimed. |
| 34 | log1p preferred near zero, supplemental1e-20 illustration. |
| 35 | expm1 preferred near zero, supplemental1e-20 illustration. |
| 36 | Negative volatility invalid, source rejection and original method. |
| 37 | Initial0 invalid for simple-return division, source terminal/summary domain. |
| 38 | Independent draws do not automatically model correlated assets, correct model distinction; no joint model executed. |
| 39 | Analytical expectations can detect implementation/sampling issues, correct purpose; arithmetic consistency does not certify model. |
| 40 | No simulated return is guaranteed, correct interpretation. |

## Remaining scope / resume

Next: **Section18.6 — Price-Path Simulation**. Chapter18 has five scoped workflows and200 local answers. Remaining workflows/answers, F28 notebook/platform, F32 shared-input integration, F165 CDF tails, statistical independence/rare-event/coverage, broader branch coverage, model/editorial/copyright and external independent acceptance remain open. No certification, production or external messaging action.
