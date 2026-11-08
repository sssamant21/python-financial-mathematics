# Section 18.1 — scoped simulation fundamentals review

Affected baseline: `31c777e7b1e41eaa3913a5144a69c6cb56cf914a`. F173, severity medium (educational numeric/input/reporting contracts), owner Book1 manuscript maintainers. Decision preserve exact whole-number outcomes, guard reachable terminal reports/statistical summaries/discounting and disclose generator/statistical boundaries. Reviewer: automated execution and mathematical/prompt/step review, not external independent acceptance. Corrected revision is the containing publication commit.

One workflow,40 local answers,twelve lab steps and eight separate process-control records are distinguished from three exact-source command records,55 supplemental predicates and ten existing unittest methods. Zero historical unique methods added. [results.json](results.json) retains runtime/platform,raw stdout/stderr, model/seed/count metadata, sample hashes,summaries, independent expectations/tolerances and source/listing SHA256.

From repository root:

```bash
python books/book-01-python-foundations-for-financial-mathematics/qa/chapter-18-simulation-review/review.py
```

Reproduce unchanged source (expected nonzero exit; requires history):

```bash
python books/book-01-python-foundations-for-financial-mathematics/qa/chapter-18-simulation-review/review.py 31c777e7b1e41eaa3913a5144a69c6cb56cf914a
```

[baseline.json](baseline.json) retains ten failed predicates; the ten original methods already passed. Defects/contracts include lost unit increments in terminal values, unrepresentable positive terminal/discounted values silently becoming0, unchecked boolean/malformed summary inputs and wrong huge-input/unreportable-SD exception behavior. Evaluating only reachable outcomes is an explicit policy addition: original code rejected overflow in an impossible probability-zero branch. Model return/domain validation still applies to all parameters. Ten predicates are not ten distinct defects. No observer failures occurred.

## Exact execution, analytical moments and shared-generator replay

Three isolated commands save/run the verbatim demonstration/ten tests, import silently and compile. Separate calls execute the same imported listing for the seeded lab. No supplemental simulation engine replaces source execution.

Fictional initial100, simple one-year returns+.1/−.1, model probabilities.5/.5 give outcomes110/90, exact mean100, variance100, SD10, loss probability.5 under terminal<initial. Theoretical IID SE atN10000 is10/sqrt10000=.1 currency. Changing p to.6 gives model mean102 and variance96; these are distribution assumptions, not estimated facts about markets.

For a seeded sample with k upward observations and N draws, independently derive mean90+20k/N, sample variance400k(N−k)/(N(N−1)), SE sqrt(sample_variance/N), loss frequency(N−k)/N. Counts are replayed using the same Python `random.Random` generator and exact binary draw versus displayed probability comparison. That replay checks mapping/draw-order/arithmetic, **not independent randomness quality or distributional validity**. Rational count formulas and Decimal square roots are separate from source summary implementation; model mean/variance are analytically derived, not assumed equal to sample results.

Actual corrected lab observations:

| N | Seed | Up probability | Up count | Mean | Estimated SE |
|---:|---:|---:|---:|---:|---:|
|1000|42|.5|480|99.6|.3161327885|
|1000|43|.5|506|100.12|.3163632180|
|10000|42|.5|4990|99.98|.1000048004|
|1000|42|.6|580|101.6|.3123100023|

Same seed/parameters reproduce the sequence; selected seed43 differs from42; the local generator does not change global random state. Those are deterministic observations, not proofs of independence or all-seed uniqueness. No predicate requires the larger sample to be closer to the expectation, enforces a nominal confidence-interval coverage rate, or certifies rare-event probability accuracy. The observed improvement for seed42 is not a universal property.

Known sample[110,90,110,110] has mean105, sample variance100, sample SD10, SE5 and loss frequency1/4. Its upward proportion3/4 differs from model probability1/2. Source discounted110 at.1 gives100; discounted model expectation100/1.1=1000/11 assumes the stated discounting/measure model. Real-world expectation is not automatically risk-neutral value. Compound100*1.1*.9=99 is separate supplemental arithmetic, not a new path simulator.

## Numeric, policy and statistical boundaries

Inputs are finite Python int/float, booleans excluded. Model/summary/discount arithmetic preserves integer/displayed-decimal quantities rationally; whole-number outcomes/means retain integer identity within finite range. Thus initial10^18 with return1e−18 reports integer10^18+1, rather than losing the increment before summarization. Other values are float reports. Required nonzero computed reports must stay nonzero/finite or raise ValueError; a true−100% return gives a legitimate zero outcome.

Only positive-probability branches are evaluated for terminal reporting, so an impossible branch need not have a reportable terminal price. Summary accepts finite signed observations and a finite threshold; it is not a validator that all observations came from this asset model. Iterable samples are consumed once. Sample SD and SE come from separate square roots of exact sample variance and variance/N, with Decimal guards; all returned fields must be reportable. An unreportable sample SD rejects even if an alternative SE-only API could report a value. Numeric guards do not prove arbitrary correctly rounded statistics or repair already-rounded input observations.

`random.Random.random()` has finite53-bit resolution. Exact binary draws compared with displayed-decimal p still quantize arbitrary probability thresholds; extremely rare-event probabilities and independence/tail properties are not certified. The displayed IID SE/normal-approximation theory requires assumptions that the code cannot verify from a seed or finite sample. These remain statistical/model limitations, not closed by improved arithmetic. F28/F32 and F165's unrelated integrated-CDF tail gap remain open.

## Forty local-answer records

| Exercise | Alignment and execution boundary |
|---|---|
|01 | Model is specified representation/assumptions; conceptual. |
|02 | Monte Carlo repeats draws under a model; seeded source calls executed. |
|03 | Deterministic stress need not have assigned probability; no stress engine export. |
|04 | A path is a time sequence; current source generates terminal outcomes only. |
|05 | Payoff derived from outcome/path; current terminal value and discounted value scope explicit. |
|06 | Source all-up terminal110; integer arithmetic now exact for this fixture. |
|07 | Source all-down terminal90. |
|08 | Independent distribution mean100, not every sample mean. |
|09 | Source known sample mean105. |
|10 | Source known sample loss1/4 under strict terminal<100. |
|11 | Analytic model loss1/2; generated sample proportions not required exactly.5. |
|12 | Analytic p.6 expectation102; source sample101.6 retained separately. |
|13 | Source discounted110/.1=100. |
|14 | Source discounted mean1000/11≈90.9091 under stated assumptions. |
|15 | Measure/discount choice not justified by real-world expectation; conceptual/external validation. |
|16 | Analytic distribution variance100/SD10; separate from sample SD estimator. |
|17 | Analytic SE.1 at10000; actual estimated SE≈.1000048004 recorded. |
|18 | Fourfold IID samples roughly halve SE under assumptions; no deterministic guarantee imposed. |
|19 | Larger run need not be closer; no monotonic-error predicate. |
|20 | Source repeated seed sequence equality; generator/environment/draw order controlled. |
|21 | Seed does not prove model validity; no approval inferred. |
|22 | Runtime/generator versions and sample hashes retained; no cross-platform guarantee. |
|23 | Source probability1.1 rejection. |
|24 | Source simple return<−1 rejects; exact−1 zero accepted. |
|25 | Normal simple-return tails can be below−100%; conceptual, no normal model implemented. |
|26 | More samples do not remove model misspecification; conceptual. |
|27 | More paths do not remove time-step bias; no time-discretized paths implemented here. |
|28 | Nominal interval omits model risk; no interval coverage test or estimator here. |
|29 | IID SE not valid blindly for dependence; source cannot detect it. |
|30 | Independent analytical/count-based references executed; shared RNG replay not fully independent statistical reference. |
|31 | Source initial200/all-up220; analytic down180/expectation200 under equal probabilities. |
|32 | Source p1 all110. |
|33 | Source p0 all90; impossible branch reporting policy separately probed. |
|34 | Source constant sample SE0, not proof model variance is truly0. |
|35 | Source equality at threshold is not loss. |
|36 | Supplemental exact two-period compound99; no multiperiod source simulator added. |
|37 | Product1.1*.9=.99, not return to initial value; arithmetic mean and compound outcome differ. |
|38 | Source count/sample minimum2 required for N−1 sample SD. |
|39 | Simulated outcome is not guaranteed forecast; conceptual. |
|40 | Model/units/generator/seed/count/versions/output hashes/criteria/limits retained; external acceptance absent. |

## Twelve lab-step records

Prerequisites: Python, finite typed model quantities, positive initial value, returns≥−1, p∈[0,1], count integer≥2, integer seed; standard error interpreted under IID finite-variance assumptions. Fictional same-currency one-year model, no market/as-of input or calibrated probability measure.

| Step | Actual evidence and boundary |
|---|---|
|1 | Exact reference saved isolated; runtime/source/listing hashes retained. |
|2 | Fixed model/units and analytic expected terminal100. |
|3 | Analytic loss.5/SD10/theoretical SE.1 at10000, separate from sample. |
|4 | Source1000 draws/seed42, counts/mean/loss/hash retained. |
|5 | Source same-seed full sequence equality. |
|6 | Source seed43 differs for selected case; no statistical independence proof. |
|7 | Source10000/seed42 summary and exact-count SE oracle, not forced equality with theoretical.1. |
|8 | Larger-run improvement observed only for retained run; no universal closeness rule. |
|9 | Source p.6 seed42 sample and separate exact model mean102. |
|10 | Source discounted exact model expectation1000/11; probability measure suitability open. |
|11 | Invalid probability/rate/returns/seed, nonfinite/boolean/malformed summaries and output limits exercised. |
|12 | Three exact commands,55 supplemental predicates and ten existing methods pass;ten baseline failed predicates retained. |

## Eight process-control records

| Control | Scoped disposition |
|---|---|
|1 Question/horizon/units | Expected terminal value and strict-loss frequency, fictional one-year currency model. |
|2 Model/distribution | Two-point p.5/.6 specified; no empirical distribution/measure calibration. |
|3 Parameters/dependence | Domain/typed checks executed; IID assumption stated, not statistically proven. |
|4 Generator/seed/count | Local random.Random, seeds42/43,counts1000/10000 recorded. |
|5 Outcomes/payoffs | Exact source terminal values, strict-loss indicators and separate discount helper executed. |
|6 Summary/uncertainty | Sample mean/SD/conditional IID SE/frequency checked using exact-count formulas; no coverage certification. |
|7 Benchmarks | Independent analytical distribution moments and shared-generator replay clearly distinguished. |
|8 Sensitivity/limits | Changed p,seed,initial and numeric ranges checked; arbitrary robustness/rare-event/model approval remains open. |

## Limits and resume checkpoint

Local Linux CPython only. No arbitrary random-generator quality/independence or rare-tail guarantee, dependent/weighted uncertainty estimator, variance reduction, path time-discretization, risk-neutral calibration, market-model approval, production performance, broad shared-input integration, notebook/platform or external independent certification. Exact source execution, analytical/count references, shared-generator replay and conceptual/statistical controls remain separate above. All unresolved tracker findings retained.

Chapter18 now records one formal workflow and40 local answers scoped. Next: Section18.2 — Random Number Generators; resume from fresh main without duplication.
