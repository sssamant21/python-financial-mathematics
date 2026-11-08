# Section18.14 — scoped project/lab/worked-answer review

Baseline `79b2bd3053d0099d7d1f8af7d8fb9c52d13781a3`. [Source](../../chapter-18/18.14-chapter-project-monte-carlo-financial-simulator.md). One project workflow,forty local-answer records,twelve lab steps,seven requirement records and seven separate acceptance-table records reviewed; zero new historical unique methods.

```bash
python books/book-01-python-foundations-for-financial-mathematics/qa/chapter-18-project-review/review.py
python books/book-01-python-foundations-for-financial-mathematics/qa/chapter-18-project-review/review.py 79b2bd3053d0099d7d1f8af7d8fb9c52d13781a3
```

Baseline command intentionally exits1. [Baseline](baseline.json) retains11 failed predicates, with [identical predicate replay](baseline-replay.json). [Corrected results](results.json):56 supplemental predicates and three exact-source commands passed (demo/12 existing methods,compile,quiet import). Counts are separate from the40 answers,12steps,7requirements,7acceptance records and zero new historical methods. Supplemental source calls include seeds42/7,alpha changes and installed Section18.12 contract comparisons. The latter shares risk arithmetic; it is an integration parity check, not an independent mathematical oracle.

## F187 — scoped project risk/input correction

The project copy overflowed ES tails even for finite averages, lost exact integer ES/loss identity, leaked TypeError/OverflowError for invalid iterables/huge numerics, and differed at decimal alpha rank boundaries. It now uses the documented Section18.12 displayed-decimal float/exact-integer/rational-tail/reporting contracts. Nearest-rank VaR retains the selected original observation; whole-number loss/ES preserve integer identity. Nonzero risk outputs below float range are explicitly rejected. Decimal-boundary and positive-underflow predicates are explicit policy adoption, not retroactive promise violations. Mean/SD remain Python statistics for nonnegative terminals; extreme-magnitude mean/SD/SE error is not certified by this discrete-model run. F187 resolved in this scope only.

F28/F32/F165/F185 remain open. Negative terminal rejection is retained; the supported three-state project values are nonnegative, so this integration succeeds without resolving the upstream signed normal-model interface. No clipping/dropping negative paths or forecast/calibration claim.

## Observer corrections retained

[Initial baseline observer](observer-initial-baseline.json) and [initial corrected-source observer](observer-initial-corrected.json) are retained separately. The first oracle converted a selected float VaR to its exact decimal integer; source VaR correctly retains the original float observation. That expected representation was corrected. An alleged ES-underflow case actually rounded to the smallest positive float; it was replaced by a three-observation case whose exact positive ES rounds to zero. Final baseline predicates were then replayed identically and corrected source rerun. These are observer changes, separate from source defects and policy adoption; baseline counts are not distinct defect totals.

## Independently derived expectations and limits

State masses1/4,1/2,1/4 imply E[V]=100,E[L]=0,Var(V)=200,P(L>0)=1/4. Theoretical IID mean SE at10000 is sqrt200/100. For losses[-10,0,20,40], alpha.75 selects20 and averages the top one observation40; alpha.625 integrates top1.5 equivalent observations to100/3. The oracle integrates each sorted quantile cell intersecting[alpha,1], rather than using the implementation's full/fractional-tail loop. The population discrete VaR at.75 is0 and ES20; empirical VaR can change across the boundary with realized counts. Exact decimal/integer risk arithmetic and Fraction are shared backends, not arithmetic-library certification. Discounted expectation2000/21 is supplemental, not a source pricing implementation.

Reports/state counts for two actual seeds are retained, with sample means/SD/SE recomputed from exact direct sums and centered squares. Standardized deviations and plug-in Bernoulli SE are descriptive; no predeclared replication acceptance, binomial coverage, quantile/ES intervals, model-risk coverage or market acceptance is claimed. No performance/native-memory/platform certification.

## Seven project requirement contracts

| Requirement | Prompt | Evidence / limits |
|---|---|---|
| 1 | Local generator | Source random.Random(seed), support/replay checked; independence is modeling/generator assumption, not proved |
| 2 | Mean/SD/SE | Sample reports checked against direct arithmetic at model-scale values |
| 3 | Loss frequency | Strict sign convention verified by exact state counts |
| 4 | VaR/ES | Equal-weight nearest rank/fractional tail; complete decimal/rational policy explicit |
| 5 | Configuration | Demo prints model/generator/seed/count/alpha; Python/source revision retained externally |
| 6 | Deterministic tests | Known moments, signs, tail examples and12 original methods checked |
| 7 | Invalid input | ValueError for malformed iterables, bool/huge numerics and unreportable risk output; no silent clipping |

## Seven separate acceptance-table records

| Record | Expected / disposition |
|---|---|
| 1 | Exact model mean100 independently derived |
| 2 | Exact model variance200 independently derived |
| 3 | Strict loss probability.25 independently derived |
| 4 | Deterministic alpha.75 VaR20/ES40 source/oracle agree |
| 5 | Deterministic alpha.625 ES100/3 source/oracle agree |
| 6 | Invalid count/alpha/nonfinite cases raise; expanded malformed-input cases corrected |
| 7 | Compatible seed/draw-order replay actual equality; no statistical-independence proof |

## Twelve lab-step contracts

| Step | Prompt | Evidence / limits |
|---|---|---|
| 1 | Document model | One hypothetical position, initial100, one-year horizon, specified teaching probabilities; no calibration or pricing-measure acceptance |
| 2 | Exact moments | E100,variance200,P(loss>0)=1/4 derived from three-state table |
| 3 | Mean SE | sqrt(200/10000); assumes independent finite-variance draws |
| 4 | Save/environment | Verbatim fence extraction; Python/platform/source SHA256/seed recorded |
| 5 | 10000 paths | Source demo command retained; supplemental records seeds42 and7 |
| 6 | Compare mean | Direct sample sums/centered-square sample variance independently recomputed; standardized deviation descriptive only |
| 7 | Compare loss frequency | State counts give adverse fraction and plug-in Bernoulli SE; no nominal interval coverage claim |
| 8 | Deterministic VaR/ES | Independent quantile-cell integral; integer/fractional boundaries |
| 9 | Different seed | Seed7 and42 reports/state counts retained; two replications are not tail calibration |
| 10 | Change alpha | Actual source calls .625,.75,.9; tail masses differ without monotone-noise claims |
| 11 | Tests/invalid input | 12 existing methods and invalid-input predicates executed; baseline failures/corrected reruns retained |
| 12 | Evidence/limits | This record separates source/supplemental/design scopes and keeps broader acceptance open |

## Forty prompt-to-answer records

| Exercise | Prompt | Reviewed answer / boundary |
|---|---|---|
| 1 | State probabilities | 1, exact rational sum |
| 2 | Down loss | 20 |
| 3 | Flat loss | 0 |
| 4 | Up loss | -20 |
| 5 | Expected terminal | 100 |
| 6 | Expected loss | 0 |
| 7 | Variance | 200, probability-weighted centered squares |
| 8 | Model SD | sqrt(200), about14.1421 |
| 9 | Theoretical mean SE | sqrt(200/10000), about.14142 |
| 10 | Loss probability | .25, strict adverse state only |
| 11 | Zero loss | Not included under loss>0 |
| 12 | Discounted expectation | 2000/21, about95.2381; supplemental arithmetic, source is undiscounted |
| 13 | Pricing measure | Not automatically a market price; risk-neutral/instrument conventions required |
| 14 | Nearest rank | ceil(.75*4)=3 |
| 15 | Deterministic VaR | 20 |
| 16 | Deterministic ES | 40 |
| 17 | Fractional tail mass | 1.5 observation-equivalents |
| 18 | Fractional ES | 100/3, independently integrated quantile cells |
| 19 | Population VaR | 0 at alpha.75: F(0)=.75 |
| 20 | Population ES | 20, upper quarter adverse state |
| 21 | Strict exceedance | Need not equal1-alpha at atoms |
| 22 | ES maximum | Not generally maximum loss; this population happens to have upper tail all20 |
| 23 | Mean SE versus VaR | Mean SE does not measure quantile uncertainty |
| 24 | Zero observed loss | Does not prove zero population probability |
| 25 | Fourfold paths | IID mean SE approximately halves |
| 26 | Model bias | Not removed by more samples |
| 27 | Seed | Replay under compatible generator/version/draw order |
| 28 | Duplicate streams | May understate uncertainty; no parallel implementation executed |
| 29 | Retained values | Source keeps/sorts observations for empirical order statistics |
| 30 | Batch replay | Draw/reduction order can change exact replay; no batching in this project |
| 31 | Quantile conventions | Package definitions differ; explicitly selected nearest rank/fractional ES |
| 32 | Invalid alpha | 1 rejected; endpoint domain(0,1) |
| 33 | Negative terminals | Rejected by this position model; F185 remains OPEN |
| 34 | Profit | Negative of loss for the stated no-cash-flow setup |
| 35 | Stress probability | No automatic probability |
| 36 | Costs | Fees/taxes/transaction costs absent |
| 37 | Backtest | Unit tests are not a backtest |
| 38 | Model risk interval | Sampling interval does not automatically cover model risk |
| 39 | Benchmarks | Independent model and deterministic targets |
| 40 | Evidence | Model/inputs/seed/versions/conventions/results/limits retained; no certification |

## Six extension proposals — conceptual/design review only

Configurable probabilities/costs, independent replications, suitable binomial intervals, weighted-scenario risk, joint portfolio and alternative quantile definitions each need a separate specification/test/model review. No implementation or acceptance of these extensions is claimed.

Next: Section18.15 chapter-wide Exercises and Applied Problems; Chapter18 and broader Book1 acceptance remain in progress.

Publication verified at `1c7aa7fb7d3fd229f77ef9d0a03584d010e9f9f2`: source/evidence blobs fetched and matched, with concurrent unrelated main work preserved via expected-head lease. This pins the corrected execution; the assessment follow-up has its own evidence and counts.
