# Section18.10 — Confidence and simulation error: scoped review

Reviewed2026-11-08 by Codex, not an external independent reviewer. Baseline `84edbf7fcbe0766189e06159b700d9315d4a4bfa`; [source](../../chapter-18/18.10-confidence-and-simulation-error.md). One workflow, forty local answers, twelve lab steps; no new historical unique methods.

Run from repository root:

```bash
python books/book-01-python-foundations-for-financial-mathematics/qa/chapter-18-error-review/review.py
python books/book-01-python-foundations-for-financial-mathematics/qa/chapter-18-error-review/review.py 84edbf7fcbe0766189e06159b700d9315d4a4bfa
```

Baseline command intentionally exits1 and requires that git object. [Baseline](baseline.json) retains19 failed final-observer predicates; [corrected results](results.json) retains88 passing supplemental predicates and three passing exact-source commands: verbatim reference demo/twelve existing methods, quiet import, compile. Source/listing SHA256, actual stdout/stderr and CPython3.12.14/Linux retained. Commands, predicates, exercise records, workflow/steps and historical methods are separate inventories.

## Finding F182 and observer transitions

Original mean interval loses integer constant endpoints, can emit infinity, and computes an intermediate sample SD that may overflow although the requested SE and interval fit. Invalid huge inputs leak OverflowError; a noniterable sample leaks TypeError. Original Wilson lower endpoint can cancel to zero despite a positive reportable value (events1,trials10,z1e100 yields lower≈1e-201), and calculations on huge trial counts overflow even when the final endpoints fit. Planned count can underflow to0 for a positive theoretical requirement or overflow converting a large finite-input expression, and can lose integer precision.

Source now defines finite int/float observation/SD/width/z inputs in finite float range (no booleans), displayed-decimal float/exact integer arithmetic, ValueError for invalid or unreportable outputs, direct SE, Decimal mean bounds, stable Wilson quadratic-root products plus symmetry, closed boundary formulas, and exact rational planning before ceiling. Original twelve unittest methods are unchanged and pass. Wilson integer counts are formula arguments, not evidence those experiments ran. Source mean interval exports SE but not SD; it can therefore report a finite SE when intermediate sample SD would overflow. A large planned integer is not an executed simulation.

The **positive-endpoint reportability predicate** (events1,trials10,z1e200) is an explicit new policy: reject mathematically positive endpoints below float report range, rather than silently calling them exact zero. The original rounding clamp did not state this requirement, so that baseline failure is not retroactively called an existing promise violation. Rounded narrow intervals may still collapse; no certified arbitrary-precision or exact coverage guarantee.

Source Exercise13 previously asked for1.96×.14142 but answered.27719. Exact displayed-input multiplication gives.2771832, rounding to.27718 at five decimals. The answer.27719 is correct when using **unrounded** theoretical SEsqrt200/100. Both prose benchmark and prompt now explicitly use that unrounded SE; the exercise also gives the rounded-input result. The original assertion failure and corrected prompt are retained, not erased by changing an oracle tolerance.

[Initial observer baseline](initial-observer-baseline.json) and [transition note](observer-transitions.md) retain a bytes-literal SyntaxWarning and a mislabeled intermediate-SD fixture. The literal was replaced with direct UTF-8 encoding. The fixture changed from±1e308 (SD still finite) to±1.79e308 (SD exceeds float but SE fits); original source then fails that correctly scoped probe. Two additional general huge-count Wilson checks plus four constructed-interval arithmetic predicates brought the final inventory to88 predicates/19 baseline failures. Initial82/16 and intermediate82/17 inventories are transitions, not additional tests/methods or independent acceptance. No tolerance changed to obtain a pass.

## Independent numerical derivations and limits

Exact execution is the complete unmodified fence per revision plus its commands. All other calls and oracles are supplemental. There is **no source RNG, seed, sampler or replication workflow** in this section; none is invented or claimed executed.

For payoff80/100/120 with probabilities1/4,1/2,1/4, independent rational arithmetic gives E[X]=100, Var(X)=200 and mean SEsqrt(200/10000). Decimal roots verify.14142 and unrounded half-width1.96sqrt(.02)≈.27719. Separately, SD20,N10000 gives SE.2 and half-width.392; estimate100.1 gives exactly[99.708,100.492]. Event probability.25 gives SEsqrt(3/160000)≈.00433. Discounting the hypothetical one-year expectation at constant annual-effective5% gives2000/21≈95.2381 and scales SE by1/1.05. No calibrated measure or market-price claim.

For actual sample[80,100,120], sample variance400, SE20/sqrt3=11.547005383792515, source mean100 and interval[77.36786944776667,122.63213055223333]. This is a fixed-sample normal teaching interval; finite formula correctness is not suitability or coverage for this small discrete sample.

Wilson is independently checked by score-quadratic inversion: A=N(N+z²), B=N(2k+z²), C=k², with roots(B±sqrt(B²−4AC))/(2A). The reference's lower root uses2C/(B+sqrt(discriminant)) to avoid cancellation. This is independently written algebra, but shares Decimal as an arithmetic backend with source, so it is not arithmetic-library certification. Ordinary, boundary, rare-count, large-z and huge-N cases are retained. Zero-event closed upper=z²/(N+z²), all-event lower=N/(N+z²). Results include:

| Events/trials | z | Source Wilson interval |
|---|---:|---|
|0/100|1.96|[0,.03699480747600191]|
|100/100|1.96|[.9630051925239981,1]|
|50/100|1.96|[.40382982859014716,.5961701714098528]|
|1/1000|1.96|[.00017654182905727149,.00564270296016047]|
|2500/10000|1.96|[.24161004081807774,.2585819654208055]|
|1/10|1e100|[1e-201,1]|
|0/10**300|1.96|[0,3.8416e-300]|
|1/10**300|1.96|[1.7652001428425675e-301,5.665079985715743e-300]|

Boundedness, order and complement symmetry checked. Numerical comparisons use rtol1e-12,atol0, plus exact boundary/integer comparisons; these are not coverage acceptance thresholds. z is caller-supplied1.96, not an inferred confidence level or a Student-t quantile implementation.

Planning exactly(1.96×20/.5)²=6146.56 gives ceil6147. Positive tiny requirements round to1, not0; SD0 mathematically yields planned0. That is not permission to estimate sample variance from zero/one observations: mean_interval still requires≥2 and actual sample design is external. Very large theoretical planned counts are computed algebraically only.

## Twelve lab-step contracts

Prerequisites: Python standard library; save exact source as simulation_error.py. Estimands are model mean and independent Bernoulli event probability. Units fictional common currency; discounted example paid in one year at5%. No market data/date or specified calibrated probability measure. Caller must justify IID units, critical value/method, sample size and stopping rule. No seed exists for deterministic source functions; a future stochastic caller must retain its stream metadata.

| Step | Actual review/execution and scope |
|---|---|
|1|Estimand/units/sample design assumptions recorded. Source accepts deterministic observations and does not verify IID design.|
|2|Independent three-state mean100/variance200.|
|3|Theoretical mean SEsqrt(.02)≈.14142, distinct from outcome SD.|
|4|Hypothetical100.1 centered on unrounded theoretical SE gives bounds100.1±1.96sqrt(.02); formula evaluated in observer, not a source API taking arbitrary mean/SE. Rounded-input distinction explicitly corrected. A supplemental two-point fixture100.1±theoreticalSE is passed to source mean_interval; its sample mean/SE/endpoints are checked. This is an arithmetic fixture, not an appropriate small-sample coverage demonstration.|
|5|Frequentist repeated-sampling interpretation reviewed; no empirical or exact95% coverage run/acceptance.|
|6|Theoretical event SEsqrt(.25×.75/10000)≈.00433 independently derived.|
|7|Zero-event plug-in SE0 contrasted with actual source Wilson0/100 interval[0,.03699480747600191]. Not proof of zero event risk.|
|8|Source planned_count(20,.5)=6147 versus exact6146.56 ceiling; mathematical zero/huge-count limits explicit.|
|9|Supplemental pair averages[100,100,100] illustrate independent units if pairs independent; source has no antithetic estimator.|
|10|Optional-stopping coverage warning reviewed as design contract; no sequential method implemented/executed.|
|11|Twelve existing methods and all source commands run; final19 baseline failures and corrected88-predicate rerun retained, observer transitions separate.|
|12|Inputs, method/critical value, formulas, hashes/commands/runtime and limits retained. Seed marked inapplicable to this deterministic API, not fabricated.|

## Forty prompt-to-answer alignment records

All forty prompts/answers read. Conceptual review is not a fictitious runtime test.

| Answer | Scoped disposition |
|---|---|
|1|Outcome SD20, correct interpretation distinct from mean SE.|
|2|SE20/sqrt10000=.2, exact arithmetic.|
|3|FourfoldN halves theoretical SE under fixed variance/IID, algebra.|
|4|1.96×.2=.392, exact fraction.|
|5|100.1±.392=[99.708,100.492], exact arithmetic.|
|6|Fixed model mean not random after observed interval in frequentist setup, correct.|
|7|Nominal confidence does not guarantee each interval covers, correct.|
|8|Higher critical value widens fixed-method interval, source z1 versusz3 comparison.|
|9|Sampling interval does not automatically quantify model risk, correct.|
|10|Three-state mean100, independent weighted sum.|
|11|Variance200, independent squared deviations.|
|12|Theoretical SE≈.14142, Decimal root/rounding.|
|13|Prompt corrected to unrounded theoreticalSE, answer.27719; literal rounded-input multiplication separately.27718.|
|14|Model event probability.25, exact state sum.|
|15|Theoretical probability SE≈.00433, independent root/rounding.|
|16|Zero events not proofp0, correct.|
|17|Plugin SE0 inadequate as full uncertainty statement, supplemental arithmetic/source Wilson contrast.|
|18|Wilson0/100≈[0,.0370], source versus independent closed form/rounding.|
|19|Discounted model expectation≈95.2381, separate exact arithmetic. No source discount API.|
|20|Positive constant discount factor scales SD/SE, independent algebra.|
|21|Real-world expected payoff not automatically risk-neutral price, correct measure requirement.|
|22|Planning ceil6146.56=6147, source/reference.|
|23|Planning not a coverage guarantee, correct approximation limit.|
|24|Fixed-N interval not automatically valid under optional stopping, correct.|
|25|Student-t exact classical interval under IID normal/unknown variance assumptions, correct conceptual statement; not implemented by source.|
|26|Normal approximation not universally reliable under skew, correct.|
|27|IID SE not blind substitute for dependent-sample estimator, correct.|
|28|Independent pair average when pairs independent, supplemental illustration only.|
|29|Paired differences determine comparison uncertainty, supplemental constant-difference illustration only.|
|30|Duplicated paths can understate uncertainty, correct stream-design concern; no workers deployed.|
|31|Seed not proof of model correctness, correct; source deterministic, no seed invented.|
|32|Unbiased IID sample variance usesN−1, actual source/reference calculations.|
|33|Ordinary sample SD undefinedN1, mean_interval rejects short sample.|
|34|Constant sample estimated SE0, source; does not prove population uncertainty0.|
|35|LargeN does not remove discretization bias, correct error-budget distinction.|
|36|Confidence interval concerns estimand, not individual payoff range, correct.|
|37|Units necessary for materiality/replay, scoped hypothetical currency recorded.|
|38|Variance-reduction improvement not universal, correct.|
|39|Analytical case supplies comparison target, independent formulas versus source retained.|
|40|Method/inputs/assumptions/N/interval/version/limits retained; source has no seed, caller responsibility documented.|

## Remaining scope / resume

Next: **Section18.11 — Portfolio Simulation**. Chapter18 has ten scoped workflows and400 local answers. F28 notebook/platform, F32 shared-input integration, F165 CDF tails, exact/empirical interval coverage, dependent/sequential/Student-t methods, broader input/branch tests, model/editorial/copyright and external independent acceptance remain open. No certification, production or external messaging action.
