# Section18.9 — Monte Carlo convergence: scoped review

Reviewed2026-11-08 by Codex, not an external independent reviewer. Baseline `c15a77dc7e9058d418581ac284bda95b80450747`; [source](../../chapter-18/18.09-convergence.md). One workflow, forty local answers, twelve lab steps, no new historical unique methods.

From repository root:

```bash
python books/book-01-python-foundations-for-financial-mathematics/qa/chapter-18-mc-convergence-review/review.py
python books/book-01-python-foundations-for-financial-mathematics/qa/chapter-18-mc-convergence-review/review.py c15a77dc7e9058d418581ac284bda95b80450747
```

The baseline command intentionally exits1 and requires that git object. [Baseline](baseline.json) retains twelve failed supplemental predicates; [corrected results](results.json) retains88 passing predicates and three passing exact-source commands: complete verbatim reference demo/twelve existing methods, quiet import, compile. Source/listing SHA256, actual stdout/stderr and CPython3.12.14/Linux are retained. Commands, predicates, workflow/step records, answers and historical unique methods remain separate inventories. No observer correction needed in this batch.

## Finding F181 and numerical scope

Original summary rounds an exact half-unit error to0 for observations[10**18,10**18+1] versus reference10**18. It can report infinite absolute error from finite inputs, and an intermediate SD can overflow although the requested SE is reportable (two values±1.79e308 have SE1.79e308). Malformed iterables leak TypeError; huge numeric inputs leak OverflowError. Theoretical SE can fail while converting a large integer count to float, including the zero-SD case, or fail with the wrong exception when its nonzero result underflows.

Source now uses finite int/float observations/reference/SD inputs within finite float range, booleans excluded, exact integer/displayed-decimal float arithmetic, guarded mean/error reports, and SE computed directly from rational variance/N with Decimal sqrt. Absolute error is computed before rounding the reported mean. Invalid or unreportable nonzero results raise ValueError. This source exports SE but **not sample SD**, so it can accept a reportable SE whose intermediate SD exceeds float range; Section18.8's SD-exporting API legitimately requires both reports to fit. Contracts are not conflated.

Two baseline predicates exercise **numerical count support**: theoretical_se(10,10**400)≈1e-199 and theoretical_se(0,10**1000)=0. These are algebraic computations without allocating or generating those sample counts, not execution evidence for enormous simulations. Count must be an arbitrary positive integer; theoreticalN1 is valid for a known population SD, while sample summary needsN≥2. Source documents this support range explicitly. The original twelve unittest methods remain unchanged and pass.

Prefix samples/sizes may be one-pass iterables. Sizes must be nonempty, strictly increasing distinct integers, between2 and sample length. Only values in requested prefixes are validated: unused trailing None in[80,100,None] with sizes[2] remains ignored and is explicitly tested/documented. This does not approve that trailing record for a later study. No streaming-summary, confidence-sequence or independence-assessment implementation added.

## Independent expectations and separation of evidence

Exact-source execution consists of the whole unmodified reference fence per recorded revision, its demo/tests, quiet import and compile. Extra source function invocations and all analytical/reference calculations are supplemental probes. NumPy stream construction and discount transformations below are supplemental implementations, not source sampler exports.

For X∈{80,100,120}, probabilities1/4,1/2,1/4 give mean100 and variance200. Independent Fraction/Decimal calculations verify SDsqrt200≈14.1421 and theoretical SEsqrt(200/N):1.41421 at100,.70711 at400,.14142 at10000,.07071 at40000. Both table and exercise rounding are checked. FourfoldN halves theoretical SE; halving SE needs fourfoldN under the fixed-variance/IID assumptions. Known sample[80,100,120] has unbiased sample variance400 and SE20/sqrt3; population and sample variance are separate.

Every actual prefix mean, unbiased sample variance/N SE and absolute error is recomputed with Fraction/Decimal independently of source summary. Numerical predicates use rtol1e-12,atol0 or exact equality; these are not statistical acceptance bands. A constructed source prefix[80,120,80,80] has errors0 atN2 and10 atN4, explicitly demonstrating non-monotonic observed error without a random-quality claim.

### Actual source nested stream

Seed42/random.Random generates40000 payoffs once; requested prefixes share observations. The exact reference demo itself uses only10000. The extra40000 source-sampler call is a supplemental invocation, not a newly exported workflow.

| Prefix N | Mean | Estimated SE | Absolute error |
|---:|---:|---:|---:|
|100|98.6|1.4285685425656274|1.4|
|400|100.15|.7237079057410387|.15|
|10000|99.96|.1406051812050259|.04|
|40000|100.048|.0706191693287093|.048|

Estimated SE roughly halves from10000 to40000, but observed error increases .040→.048. This does not contradict LLN/CLT. The prefix is verified to match a shorter replay of the same seed; it is not an independent replication.

For the Section6 discounted-payoff instruction, the observer transforms each payoff with exact rational division by1.05 then float reporting (supplemental transform), and applies source prefix_study/summary against reference2000/21≈95.2381. Each mean and SE is checked against the corresponding terminal statistic divided by1.05; full discounted rows are in JSON. No source discount API or risk-neutral valuation approval implied.

### Supplemental replications and rare-event illustration

NumPy2.3.5 SeedSequence(2026).spawn(3)/PCG64 workers0/1/2 use keys[0]/[1]/[2], each generate10000 uniforms and a supplemental three-state map. Source prefix/summary functions analyze them. Mean/SE/error rows:100.048/.1417666370410817/.048;100.278/.14195170526859782/.278;99.926/.14024770708262646/.074. Assignments/hashes retained. These deliberately reuse Section18.8's documented child-stream fixtures; they are not new independent evidence merely because this is another batch. Designed spawning is not a proof of mathematical independence, normality, nominal coverage or distributed scheduling correctness.

Independent rare-event arithmetic: p.001,N1000 implies expected count1, while probability of zero events is(.999)^1000≈.36769542477, using100-digit Decimal power. Thus zero events do not provep0. The true Bernoulli frequency SE is sqrt(.001×.999/1000)>0 even though the plug-in SE at observed0 is0. This is a fixed supplemental algebraic illustration, not an executed source rare-event/binomial-interval API or resolution of general tail gaps.

## Twelve lab-step contracts

Prerequisites: Python standard library; NumPy present only for the explicitly supplemental stream workflow. Save exact source as monte_carlo_convergence.py. Fixture: expected hypothetical currency payoff100 under the three-state model; discount example is one-year at constant annual effective5%. No actual market dataset/date or calibrated real-world/risk-neutral measure. Predetermined sample sizes[100,400,10000,40000], no adaptive stopping.

| Step | Action and actual evidence |
|---|---|
|1|Exact model mean100/variance200 derived independently.|
|2|Theoretical SE for100/400/10000 plus40000 derived; source theoretical_se compared.|
|3|Exact code saved/executed in isolated temporary directory; version/generator/seed42/source hashes retained.|
|4|Exact demo prefix output retained; additional40000 source-sampler prefix table above.|
|5|Absolute errors1.4,.15,.04,.048 observed, including an increase at largerN. No tolerance tuning or monotonicity requirement.|
|6|Prefixes share observations by construction; shorter same-seed replay confirms nesting. No independent-replication label.|
|7|Three supplemental spawned NumPy samplers/source summaries executed and mapped to workers; source lacks spawning API. Independence certification/parallel scheduling unverified.|
|8|Independent discounted model mean2000/21 and supplementary sample-discount transform/source-prefix estimates retained; no automatic market-price claim.|
|9|Rare-event expected count1; exact-probability zero-count illustration also recorded.|
|10|Zero-count probability≈.3677 explains why no events is not proof of zero probability; no rare-event coverage accepted.|
|11|All twelve original methods, invalid input/report probes, quiet import/compile pass; twelve original failed predicates retained.|
|12|Sampling/model/parameter/monitoring/numerical/stream limitations recorded; no finite run proves LLN/CLT or external acceptance.|

## Forty prompt-to-answer alignment records

All forty local prompts and answers read in source order. Conceptual reviews are not invented runtime methods.

| Answer | Scoped disposition |
|---|---|
|1|Sample mean targets specified model mean, correct estimand.|
|2|LargerN need not improve observed error, constructed/actual nested counterexamples.|
|3|Convergence does not validate model, correct distinction.|
|4|Mean100, independent weighted sum.|
|5|Population variance200, independent squared-deviation sum.|
|6|SDsqrt200≈14.1421, Decimal/rounding.|
|7|SE100≈1.4142, exact formula and source theoretical_se/table rounding.|
|8|SE400≈.7071, same.|
|9|SE10000≈.14142, same.|
|10|FourfoldN approximately halves SE, algebra under same IID variance.|
|11|HalfSE needs fourfoldN, inverse-square relation.|
|12|Single error need not halve, actual .04→.048 example.|
|13|Nested estimates dependent, shared input prefixes explicitly recorded.|
|14|Multiple streams assess variation, supplemental designed streams/summary records; no certified independence.|
|15|Different seeds do not prove independence, correct; source replay separate.|
|16|Finite positive variance standard IID CLT condition, correct conceptual condition; no theorem proved by runs.|
|17|IID SE not always applicable under dependence, correct limit.|
|18|More paths do not fix wrong assumptions, correct model distinction.|
|19|100 at5% PV≈95.2381, exact rational calculation and sample transform.|
|20|Discounted expectation not automatically market price, correct measure requirement.|
|21|p.001,N1000 expected count1, exact rational multiplication.|
|22|Zero events does not implyp0, zero-count probability .367695… illustration.|
|23|Plug-in SE0 misses boundary uncertainty, independent true-SE comparison.|
|24|Normal CI does not automatically include model error, correct. No source interval API.|
|25|Repeated fixed-N checks do not preserve coverage automatically, correct; no sequential stopping implementation.|
|26|More paths do not fix monitoring error, correct distinction.|
|27|Barrier may cross between observations, correct path-model limit, no bridge source executed.|
|28|GBM exact update is at grid times under constant parameters, correct qualifier.|
|29|Paired grids require independent paired differences as units, correct design, no grid-coupling implementation in this source.|
|30|Pairing not universally variance reducing, correct covariance-dependent claim.|
|31|Unbiased IID sample variance denominatorN−1, used in independent/source calculations.|
|32|Constant sample SE0 without proving population variance0, source constant check.|
|33|Units necessary for interpretation/replay, hypothetical currency/horizon recorded.|
|34|Analytical mean is benchmark, independent formulas versus summaries.|
|35|Usual sample variance cannot useN1, source summary rejects; known-population theoretical_se allowsN1.|
|36|More samples do not necessarily fix overflow, guarded output probes; numerical count support not enormous simulation execution.|
|37|Strong law: IID finite absolute mean gives sample-mean almost-sure convergence, correctly qualified conceptual theorem.|
|38|Convergence in probability: deviation probability tends0 for each epsilon>0, correct definition/theorem context.|
|39|Generator and software version beyond seed, retained.|
|40|Supplied tests are not executed evidence until run; all twelve methods actually ran in this batch.|

## Remaining scope / resume

Next: **Section18.10 — Confidence and Simulation Error**. Chapter18 has nine scoped workflows and360 local answers. F28 notebook/platform, F32 shared-input integration, F165 CDF tails, dependence/rare-event/sequential/monitoring and coverage methods, broader branch/input tests, financial model/editorial/copyright and external independent acceptance remain open. No certification, production or external messaging action.
