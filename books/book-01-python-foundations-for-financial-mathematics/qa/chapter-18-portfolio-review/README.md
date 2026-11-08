# Section18.11 — Portfolio simulation: scoped review

Reviewed2026-11-08 by Codex, not an external independent reviewer. Baseline `8b19aac86aaf9d590f94d826628d0e8f9dc4c885`; [source](../../chapter-18/18.11-portfolio-simulation.md). One workflow, forty local answers, twelve lab steps, no new historical unique methods.

Run from repository root:

```bash
python books/book-01-python-foundations-for-financial-mathematics/qa/chapter-18-portfolio-review/review.py
python books/book-01-python-foundations-for-financial-mathematics/qa/chapter-18-portfolio-review/review.py 8b19aac86aaf9d590f94d826628d0e8f9dc4c885
```

Baseline command intentionally exits1 and needs that git object. [Baseline](baseline.json) retains fifteen failed supplemental predicates; [corrected results](results.json) retains90 passing supplemental predicates and three passing exact-source command records: verbatim reference demo/twelve existing methods, quiet import, compile. SHA256 of source/listing, actual stdout/stderr, CPython3.12.14/Linux, generator/seed/rows/outputs retained. Predicates, commands, exercise records, workflow/lab steps and unique historical methods remain separate inventories. No observer correction needed in this batch.

## Finding F183 and explicit policies

Original analytical variance overflows when two huge, perfectly negatively correlated contributions exactly offset. Simulation loses integer identity for a zero-volatility mean; tiny returns can lose a nonzero terminal increment. Nonzero terminal/variance values can underflow silently. Oversized inputs leak OverflowError; malformed outer/inner row iterables leak TypeError; the finite predicate itself raises on oversized integers.

Source now uses finite int/float inputs within finite float range, no booleans, displayed-decimal floats/exact integers, ValueError for invalid/unreportable nonzero outputs, exact whole-number reports, guarded correlation residual scale, and rational arithmetic before rounding. Analytical variance is evaluated as(a+rho*b)²+(1−rho²)b², a=w1*sd1,b=w2*sd2, preserving PSD nonnegativity and exact cancellation before output checks. Every exported variance/SD/SE must fit: tiny nonzero analytical variance below float range raises rather than pretending zero risk. Source joint returns/portfolio return are calculated before rounding reports; exact last-bit equality with old binary operations is not promised. All twelve original unittest methods unchanged and pass.

**Two baseline predicates establish a normalization policy:** nonnegative weights accepted within the existing1e-12 sum tolerance are normalized exactly to sum1 in both analytical and simulate. The original unstated choice is not retroactively called a universal promise violation; the source now documents it. Normalization is not position/calibration approval.

The source deliberately **retains normal simple returns below−1 and mathematically negative terminal values**. They diagnose the model's limited-liability inconsistency; no clipping, resampling or zero-floor was introduced. Exact total loss returns a legitimate zero terminal, while nonzero numeric underflow is rejected. The summary trusts supplied third-field portfolio returns, because it receives no weights/horizon/currency metadata to reconcile them. A fixture with asset returns0/0 but supplied portfolio return.1 is intentionally accepted and recorded as an **external integration requirement**, not a validated economic row. F32 and broader shared-input/model acceptance remain open.

## Independent expectations and execution boundaries

Exact execution is the complete verbatim reference fence per source revision and module commands. Extra calls are supplemental probes. Four rows are compared with independently written100-digit Decimal joint-normal mapping driven by the **same** standard-library normal stream; this validates algebra/order, not random quality or path independence.

Independent rational two-asset calculations: weighted deterministic return.6(.1)+.4(−.05)=.04, terminal104/profit4 at initial100. Means.08/.04 give portfolio mean.064. Covariance rho*sd1*sd2=.25×.2×.1=.005. Full quadratic variance.6²(.2²)+.4²(.1²)+2(.6)(.4)(.005)=.0184, SD≈.13565. Expected terminal106.4, terminal SD≈13.565, and theoretical mean SE at10000≈.13565. The numerical equality of return SD and currency mean SE here is due to initial100 and sqrt(N)=100, not equivalence of their meanings/units. At rho0 variance.016. Zero-volatility return is.064 deterministically. Stress−.2/−.1 gives portfolio return−.16 and P&L−16.

For normal portfolio return, independent central CDF integration evaluates Phi(−.064/sqrt(.0184))≈.3185296858674, rounding to.3185. An80-term Decimal integral series with recorded100-digit pi is a **fixed central-point supplemental oracle**, not an exported general-tail CDF or resolution of F165 tail limitations.

Conditional on actual source rows, independent Fraction/Decimal arithmetic recomputes mean return, unbiased return SD, mean terminal, terminal SE, strict loss frequency and count of paths with either asset return<−1. Observed asset covariance/correlation are supplemental diagnostics, not summary exports or hard moment-acceptance thresholds. Both source and observer use Fraction/Decimal backends; independent algebra is not independent arithmetic-library certification. Numeric checks use rtol1e-12,atol0 and exact integer/singular-coupling equality. They are not statistical coverage bands.

| Run | N | Mean terminal | Terminal mean SE | Mean return / sample return SD | Loss frequency | Observed asset correlation | Paths with asset return<−1 |
|---|---:|---:|---:|---|---:|---:|---:|
|seed42,rho.25|10000|106.49022794706603|.13571761623558326|.06490227947066025 / .13571761623558326|.3155|.25808523060633537|0|
|seed43,rho.25|10000|106.42924179752723|.13457606206997397|.06429241797527233 / .13457606206997397|.3171|.24429746095921717|0|
|seed42,rho0|10000|106.48050301368608|.1266474082438444|.06480503013686074 / .1266474082438444|.3021|.013691769189369759|0|
|seed42,zeroSDs|10|106.4|0|.064 / 0|0|undefined|0|

Different seeds do not certify independence. Changing rho uses the same underlying seed intentionally as a sensitivity fixture, not independent replications or a paired-SE calculation. Zero tail count among10000 paths does not prove the model cannot produce returns<−1. Explicit deterministic tail fixtures retain negative terminals and count one below−1 path in two rows; count/frequency(.5) and strict inequality are checked separately from sampled observations.

## Twelve lab-step contracts

Prerequisites: Python standard library; save exact reference as portfolio_simulation.py. Fixture initial100 fictional common currency, beginning weights.6/.4, one common model period, simple-return means.08/.04, SDs.2/.1, rho.25. No actual period duration, market valuation date/dataset or calibrated probability measure supplied; all parameters must refer to the same period. Long-only fully invested, no fees/cash flows/rebalancing, no time-series paths. Normal simple returns are an illustrative mathematical model, not valid limited-liability prices in its lower tail.

| Step | Actual action and scoped outcome |
|---|---|
|1|Initial/period/units/weights/means/SDs/rho recorded, with unspecified actual duration/valuation data explicitly limited.|
|2|Exact weight sum1; accepted-near-one normalization policy also tested.|
|3|Independent mean.064, covariance.005, variance.0184 versus source analytical function.|
|4|Expected terminal106.4 and theoretical terminal mean SE≈.13565, independent formulas/rounding.|
|5|Exact reference demo/tests run; Python/generator/seeds42/43 and hashes retained.|
|6|Sample moments/table compared descriptively with theoretical values; independent conditional arithmetic verified. No hard moment band or independence acceptance.|
|7|Source count0/10000 in sampled runs, frequency0 for 'either asset return<−1'. Explicit tail fixtures count1/2 and retain negative terminals. Zero sampled events not proof of zero probability.|
|8|Actual source simulation at rho0 retained plus analytical variance.016; observed correlation need not equal0 exactly.|
|9|Zero-volatility source runN10 gives mean.064, terminal106.4, SD/SE0; singular rho±1/offsetting-return cases separately checked.|
|10|Independent stress−16%/−16 currency, source analytical zero-SD stress mean compared. No probability assigned to the deterministic stress.|
|11|Twelve original methods, invalid input/report cases, quiet import/compile pass; fifteen original failed predicates retained, including two policy probes.|
|12|Measure/tails/sampling/units/metadata/rebalancing and summary-reconciliation limits retained; no platform or independent model acceptance.|

## Forty prompt-to-answer alignment records

All forty source prompts/answers read in order. Conceptual/design statements are not additional source APIs or tests.

| Answer | Scoped disposition |
|---|---|
|1|Weights sum1, exact fractions.|
|2|Weighted return.04, independent calculation.|
|3|Terminal104, algebraic map.|
|4|Profit4, independent subtraction.|
|5|Mean.064, source analytical versus weighted means.|
|6|Covariance.005, exact rho*SD1*SD2.|
|7|Variance.0184, source versus full quadratic independent formula.|
|8|Volatility≈.13565, Decimal sqrt/rounding.|
|9|Expected terminal106.4, independent initial*(1+mean).|
|10|Terminal SD≈13.565, independent scaling/rounding.|
|11|N10000 theoretical terminal mean SE≈.13565, independent variance/N formula.|
|12|rho0 variance.016, source analytical/reference and actual sensitivity run.|
|13|Loss≈.3185, supplemental fixed central normal integral, not source tail API.|
|14|Rp0 is not strict loss, source summary.|
|15|Stress return−.16, source analytical zero-SD/reference.|
|16|Stress P&L−16 at100, exact multiplication.|
|17|rho1 residual coefficient0, actual source singular coupling.|
|18|rho−1 residual0, actual source opposite coupling and offset portfolio.|
|19|rho1.1 invalid, source rejection/original method.|
|20|ZeroSD asset returns modeled mean, source deterministic run and integer identity probe.|
|21|Normal simple return can be below−1, retained deterministic tail fixtures; no truncation introduced.|
|22|Clipping changes normal model, correct design distinction; source does not clip.|
|23|Zero observed invalid-model draws not proof of impossible tail, correct sampling limit.|
|24|Zero correlation not generally independence, correct; special joint-normal property does not extend universally.|
|25|Diversification does not guarantee no loss, correct model distinction.|
|26|Correlation changes covariance/variance generally, .0184→.016 comparison.|
|27|Buy-and-hold weights drift as asset values change, correct; no multi-period source implementation.|
|28|Fixed beginning weights reset each period imply rebalancing under assumptions, correct conceptual distinction.|
|29|No fees in reference, source inspection; not silently added.|
|30|Initial0 invalid in summary, source rejection/original method.|
|31|Shorts unsupported, nonnegative-weight guard.|
|32|Covariance matrix must be PSD, correct general condition; source only two assets with validSD/rho.|
|33|Ordinary Cholesky not always applicable to singularPSD, correct design condition; no factorization API claimed.|
|34|Seed does not prove model validity, replay separate from acceptance.|
|35|More paths do not remove parameter uncertainty, correct.|
|36|SE is estimator variability, not portfolio volatility; numeric equality in fixture explained above.|
|37|Stress not automatically probabilistic, correct conditional interpretation.|
|38|Normal model not necessarily accurate for extremes, correct tail/calibration limit.|
|39|Measure defines modeled probability/valuation interpretation, recorded as uncalibrated illustrative model.|
|40|Inputs/weights/model/seed/versions/outputs/benchmarks/limits retained; no independent acceptance invented.|

## Remaining scope / resume

Next: **Section18.12 — Risk Simulation**. Chapter18 has eleven scoped workflows and440 local answers. F28 notebook/platform, F32 shared-input integration, F165 CDF tails, joint-tail/calibration/metadata consistency, coverage/dependence, broader branch/input tests, multi-period/rebalancing and model/editorial/copyright/external independent acceptance remain open. No certification, production or external messaging action.
