# Section18.8 — Monte Carlo estimation: scoped review

Reviewed2026-11-08 by Codex, not an external independent reviewer. Baseline `9a45c4e004cbb6ffee8a637421d3d5cd0eee5de2`; [source](../../chapter-18/18.08-monte-carlo-estimation.md). One workflow, forty local answers, twelve lab steps; no new historical unique methods.

Run from repository root:

```bash
python books/book-01-python-foundations-for-financial-mathematics/qa/chapter-18-estimation-review/review.py
python books/book-01-python-foundations-for-financial-mathematics/qa/chapter-18-estimation-review/review.py 9a45c4e004cbb6ffee8a637421d3d5cd0eee5de2
```

The baseline command intentionally exits1 and needs that git object. [Baseline](baseline.json) retains thirteen failed supplemental predicates. [Corrected results](results.json) retains104 passing predicates and three passing exact-source command records: complete verbatim reference demo/twelve existing methods, quiet import, compile. Source/listing SHA256, actual stdout/stderr, CPython3.12.14/Linux and sampler metadata are retained. Commands, predicates, exercise records, lab steps and historical methods are separate inventories. No observer correction was needed in this batch.

## Finding F180 and numeric contract

The original constant interval and zero-rate discount lose integer identity at`10**18+1`. Malformed noniterable observations leak TypeError and huge integers/SD reports leak OverflowError. Nonzero discounted payoffs can underflow silently; interval endpoints can be infinite even when mean and sample SD/SE are finite.

Source now accepts finite int/float inputs in finite float range, excludes booleans, uses displayed-decimal float/exact integer arithmetic, consumes observation iterables once, and raises ValueError for invalid or unreportable nonzero results. Rational mean/variance and Decimal square roots/interval calculations precede rounded reports. Constant interval endpoints retain exact integer identity. Every exported mean, SD, SE and endpoint must be reportable: a sample SD outside float range is rejected even when SE alone could fit. Tiny nonzero SD/SE remain nonzero where reportable. Finite reporting can still collapse a narrow interval; the source explicitly disclaims arbitrary-precision bounds or certified statistical coverage. All twelve original unittest methods remain unchanged and pass.

estimate_mean needs≥2 observations; event_frequency permits one but not zero; discount permits an empty iterable but still validates its rate. Signed finite payoffs/thresholds are allowed; event comparison is strictly below threshold. These functions neither validate IID assumptions nor construct binomial/sequential intervals. Such gaps remain open, not hidden by a numeric pass.

## Independent expectations and evidence separation

Exact-source execution is the verbatim fenced program per recorded revision and its module commands. Additional calls to source functions are supplemental probes. The three NumPy samplers below are supplemental implementations, **not execution of the source random.Random sampler**.

Independent rational derivation for X∈{80,100,120} with probabilities[1/4,1/2,1/4]: E[X]=100, Var(X)=200, SD=sqrt200≈14.1421 and mean SE atN10000=sqrt(200/10000)≈.14142. For observed[80,100,120], mean100, unbiased sample variance400 (N−1 denominator), sample SD20 and SE20/sqrt3≈11.547. These differ from the model population variance/SD. All printed roundings are checked. P(X<100)=1/4, indicator SEsqrt(3/160000)≈.00433; no binomial interval is implemented by source.

At annual effective5%, expected discounted payoff2000/21≈95.2381, population SDsqrt200/1.05≈13.4687 and theoretical SE≈.13469. Discounted source sample mean/SE are checked against the undiscouted source sample's independently scaled quantities. The source reports a nominal fixed-N normal interval mean±1.96SE, not exact finite-N coverage. The illustrative100.1±1.96(.14142) gives[99.8228168,100.3771832], rounding to[99.823,100.377]. Sample interval endpoints are recomputed with separate Fraction/Decimal arithmetic. Planning N=(1.96sqrt200/.5)²=3073.28 rounds upward to3074. MSE=variance+bias² illustrated with9+2²=13, not a source MSE API.

Arithmetic checks use rtol1e-12,atol0 or exact integer equality; they are **not statistical acceptance bands**. Sample mean, SD, SE, event frequency and normal endpoints are recomputed conditional on actual observations. No mandatory analytical/sample equality, monotonic improvement or multi-run coverage acceptance is asserted.

### Source sampler invocations

| Seed | N | Mean | Estimated SE | Nominal normal interval | P̂(X<100) | (mean−100)/SE |
|---|---:|---:|---:|---|---:|---:|
|42|10000|99.96|.1406051812050259|[99.68441384483815,100.23558615516185]|.2481|−.2844845|
|43|10000|100.002|.14013551796864218|[99.72733438478146,100.27666561521853]|.2454|.0142719|
|42|1000|100.38|.4450321939519136|[99.50773689985425,101.25226310014575]|.238|.8538708|

Different seeds are not proof of independent streams. Seed42/N1000 is a prefix of seed42/N10000, so the two are explicitly not independent replications. The smaller run's error/SE comparison is descriptive, not an anytime-valid stopping rule.

### Supplemental spawned-stream workflow

Lab step9 asks for several independent streams. The source has no spawning API. The observer therefore separately executes NumPy2.3.5 SeedSequence(2026).spawn(3), PCG64 workers0/1/2 with spawn keys[0]/[1]/[2]. Each generates10000 uniforms and applies the stated three-state thresholds in supplemental code; **source estimators** then summarize those samples. Mean/SE/frequency observations are100.048/.1417666370410817/.25,100.278/.14195170526859782/.245,99.926/.14024770708262646/.2477. Assignments, hashes and results are in JSON. This is designed stream separation under generator assumptions, not statistical independence certification or source-sampler execution. No actual distributed scheduling or platform replay tested.

Supplemental antithetic examples compute pair averages[100,100,100] from[(80,120),(120,80),(100,100)], and paired differences[2,2,2] from[(80,82),(100,102),(120,122)]. They illustrate independent analysis units if pairs are independent; source exports no antithetic/control-variate/comparison estimator. No universal variance-reduction promise.

## Twelve lab-step contracts

Prerequisites: Python standard library; NumPy present only for the explicitly supplemental step9. Save exact listing as monte_carlo_estimation.py. Target: expected fictional one-year payoff and P(X<100), units common currency, probabilities as above; constant5% annual effective discount. No actual market data, valuation date, calibrated probability measure or market-price approval. Source hash/command/environment/seed/N retained.

| Step | Actual action and scoped outcome |
|---|---|
|1|Estimand, event threshold/strict inequality, one-year payoff horizon, currency and three-state probabilities recorded.|
|2|Independent exact mean100 and variance200.|
|3|Theoretical mean SEsqrt(.02)≈.14142 atN10000, distinct from outcome SD14.1421.|
|4|Exact reference saved/executed in fresh temporary directory; Python/generator/seed/source hashes recorded.|
|5|N10000,seed42 source estimates/interval retained in table/JSON; twelve existing methods run.|
|6|Standardized error−.2844845 for seed42, .0142719 for seed43; descriptive only, not acceptance of nominal coverage.|
|7|Source frequency.2481/.2454 versus exact.25; strict threshold and single-observation cases checked.|
|8|Source-discounted payoffs/estimates compared with rational100/1.05 and sample scaling; probability/discount consistency is a model prerequisite.|
|9|Three documented supplemental spawned NumPy streams and source-estimator summaries executed, with worker assignments. Source API lacks spawning; statistical independence and cross-platform/parallel scheduling remain unverified.|
|10|Seed42/N1000 versusN10000 SE.44503219/.14060518; nested samples explicitly labeled. No requirement that a larger run always be closer.|
|11|Invalid input/report cases, all twelve original methods and quiet import/compile pass after fix; thirteen original failed predicates retained.|
|12|Evidence and assumptions/limitations recorded; no binomial/sequential interval, dependence/model validation or independent acceptance claimed.|

## Forty prompt-to-answer alignment records

All forty local prompts/answers read in source order. Conceptual rows are review records, not extra callable tests.

| Answer | Scoped disposition |
|---|---|
|1|E[X] model expected payoff, correct estimand definition.|
|2|Sample mean as a rule is estimator, distinct from realized estimate.|
|3|Exact mean100, weighted rational sum.|
|4|Exact population variance200, weighted squared deviations.|
|5|SDsqrt200≈14.1421, Decimal root/rounding.|
|6|N10000 mean SE≈.14142, variance/N root.|
|7|Known sample mean100, source/reference.|
|8|Known sample variance400, N−1 calculation; source SD² consistent.|
|9|Known sample SD20, source/reference.|
|10|Known sample SE20/sqrt3≈11.547, source/reference/rounding.|
|11|Model eventX<100 probability.25, exact state sum.|
|12|Equality100 gives indicator0, source strict-threshold probe.|
|13|Indicator SE≈.00433, exact Bernoulli formula/rounding, no source interval API.|
|14|Zero events do not provep0, correct statistical limit.|
|15|Discounted expectation≈95.2381, source/reference/rounding.|
|16|Discounted SD≈13.4687, independent scaling/rounding.|
|17|Discounted mean SE≈.13469, independent scaling/rounding.|
|18|FourfoldN halves theoretical SE under same variance/IID, algebraic factor.|
|19|HalfSE needs4timesN, squared inverse relationship.|
|20|Illustrative interval[99.823,100.377], exact decimal calculation/rounding.|
|21|Fixed mean not random after observing interval in frequentist model, correct interpretation.|
|22|Nominal95% not guaranteed for every sample/model, correct limit; selected intervals are not coverage proof.|
|23|Normal approximation not universally reliable at smallN, correct.|
|24|More paths do not remove model bias, correct distinction.|
|25|MSE=variance+bias² when moments exist, supplemental9+4=13 illustration.|
|26|N−1 corrects sample-variance bias under IID assumptions, appropriate qualifier.|
|27|Constant sample estimated SE0, source check; no claim of zero population uncertainty.|
|28|IID SE not blindly valid under dependence, correct.|
|29|Duplicated streams overstate effectiveN, correct design concern; no independence inferred from seeds.|
|30|Independent pair average is unit when pairs independent, supplemental pair-average illustration.|
|31|Comparison uncertainty uses paired differences, supplemental difference illustration.|
|32|Planning exact3073.28→ceil3074, rational calculation.|
|33|Fixed-N coverage need not survive sequential stopping, correct; no anytime-valid procedure implemented.|
|34|Seed supports replay, not correctness, source replay/global-state checks separate.|
|35|Analytical benchmark helps detect defects, independent formulas versus source statistics retained.|
|36|Any expected payoff is not automatically a market price, correct measure/discount requirement.|
|37|Normal interval not always suitable for rare events, correct; binomial methods remain outside source.|
|38|Variance reduction not universal, correct design limit.|
|39|Mean SE differs from individual outcome volatility, separate200/SD/SE benchmarks.|
|40|Inputs/model/generator/seed/N/version/estimates/limits recorded for scoped fixture; external acceptance remains.|

## Remaining scope / resume

Next: **Section18.9 — Convergence**. Chapter18 now has eight scoped workflows and320 local answers. F28 notebook/platform, F32 shared-input integration, F165 CDF tails, dependence/rare-event/coverage/sequential methods, broader input/branch tests, financial model/editorial/copyright and external independent acceptance remain open. No certification, production or external messaging action.
