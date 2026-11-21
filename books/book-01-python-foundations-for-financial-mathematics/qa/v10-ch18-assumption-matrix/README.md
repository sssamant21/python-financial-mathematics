# V10 — Chapter18 remaining exercise/lab assumption matrix

Source pin: `99b03b4ce334912f4731ee730d8fbdf60f06bb6a`. [Runnable review](review.py), [first](first.json), [replay](replay.json), [unchanged assessment/project sources](source-identity.json).

```bash
python books/book-01-python-foundations-for-financial-mathematics/qa/v10-ch18-assumption-matrix/review.py first
python books/book-01-python-foundations-for-financial-mathematics/qa/v10-ch18-assumption-matrix/review.py replay
```

Both runs pass **29 predicates** with identical rows. They cover Exercises31–44/47–48 using native path, portfolio, risk and performance functions plus explicitly labeled caller arithmetic. An independent100-term/100-digit exponential series gives the GBM model expectation; rational formulas derive covariance, portfolio returns, FX quote conversion, time steps and memory. Numeric tolerance is rtol5e-14/atol1e-12; native lists/state comparisons and decisions are exact.

A selected fine path [100,80,100] hits barrier90 while its coarse endpoints [100,100] do not. This is a deterministic information-loss example, not a sampled GBM bridge or continuous-monitoring accuracy test. Analytical portfolio variance.0184 uses the specified correlation; stress−.16 uses one deterministic scenario, not an assigned probability. Weight33/52 after buy-and-hold differs from initial.6; no rebalancing implementation is added. The FX example is caller arithmetic in USD for a USD/EUR quote, not a new native FX workflow.

Native batching runs the exercise's exact100001-path/10000-batch case and matches its documented serial stream state; caller partition arithmetic has ten full batches plus one. Storage202400000bytes≈193.0MiB is element storage only. Full native demo timings remain illustrative, not a measured speedup, peak-RSS or native-memory certification.

Each run executes four complete verbatim source demos and their suites, then compilation. Source18.6 has ten existing methods;18.11/18.12/18.13 each have twelve. Across both runs: ten command records and92 invocations of46 existing methods. No new historical unique methods, answer, workflow or lab-step totals are added. No source failure or financial source change occurred in this batch.

## Exercise assumptions, evidence and limits

These ranges reconcile the existing [fifty formal prompt/answer records](../chapter-18-applied-review/README.md) with V10 follow-ups. They do not recount fifty newly executed answers.

| Exercises | V10 evidence / prerequisite contract | Remaining limit |
|---|---|---|
|1–4|[Finite-model expectations](../v10-simulation-foundations/README.md), [outcome thresholds](../v10-outcome-thresholds/README.md); sample mean is descriptive, not automatically its model mean|Exercise2 is an alternative model; Exercise3's comparison uses Exercise1|
|5–10|[Generator resolution](../v10-generator-resolution/README.md), [partition/replay](../v10-reproducibility-partitions/README.md), [scenario runtime](../v10-scenario-runtime-2026-11-21/README.md)|Stress probability, stream independence and model suitability are not established by a seed|
|11–20|[Return laws](../v10-return-distribution/README.md), [fee/thresholds](../v10-outcome-thresholds/README.md)|Normal simple-return negative terminals remain F185; pricing measure and cost timing need caller context|
|21–30|[Paired estimates](../v10-paired-estimation/README.md), [nested convergence](../v10-nested-convergence/README.md), [finite Wilson coverage](../v10-wilson-coverage/README.md)|Finite variance/IID units and fixed-N assumptions; no monotone-error/optional-stopping/model-risk coverage|
|31–34|This run plus [path monitoring](../v10-path-monitoring/README.md)|Grid-time GBM expectation is not continuous barrier monitoring|
|35–38|This run plus [joint moments/tails](../v10-portfolio-moments-tails/README.md)|Fixed weights, costs, dependence and nonnegative-terminal interfaces remain model choices|
|39–42|This run plus [risk aggregation](../v10-risk-aggregation/README.md)|Displayed-decimal nearest-rank/fractional ES, equal weights; mean SE is not VaR/ES uncertainty|
|43–44|This run plus [performance order](../v10-performance-order/README.md)|Element bytes and serial ordering, not universal performance or peak memory|
|45|[Information-loss counterexample](../v10-exercise45-information/README.md)|Moments do not identify quantiles; initial observer correction remains retained|
|46|[Paired-unit laws](../v10-paired-boundary/README.md)|Pairing may increase or decrease variance; independence is between modeled pairs|
|47–48|This run; direct stress/FX calculations|No automatic scenario probability, quote inversion or transaction-cost model|
|49–50|[Zero-event/model decision](../v10-paired-boundary/README.md)|Zero observations do not prove p=0; precision/replay is not independent model acceptance|

## Twelve lab contracts

|Step|Crosswalk and disposition|
|---|---|
|1|Explicit three-state one-year teaching model/seed in [project review](../v10-project-integration/README.md); no calibration|
|2|Exact model mean100, variance200, loss probability.25; project/finite-model evidence|
|3|Theoretical mean-SE uses independent units, not outcome dispersion or tail uncertainty|
|4|Prior complete18.14 project execution retained; project source identity unchanged here|
|5|Prior exact report moments and selected finite coverage; no universal acceptance band|
|6|This run and independent atom-tail project/risk follow-ups align39–41|
|7|Prior seeds/replay evidence; distinct seeds do not prove independence/non-overlap|
|8|This run verifies.0184 variance/−.16 stress at stated model inputs|
|9|Fine/coarse selected barrier counterexample; no continuous bridge correction|
|10|This run verifies element bytes/exact partial batch, excludes overhead|
|11|Prior project methods remain retained; this run reruns four sibling suites only|
|12|Model, units, measure, dependence, numerical/resource and independent limits remain explicit|

The selected Chapter18 V10 assumption crosswalk is now recorded across all fifteen sections. **V10 and Book1 remain IN PROGRESS.** Broader generator/tail/dependence/model and independent acceptance are not closed. Next: inventory V10 sampler/uncertainty interfaces outside Chapter18, beginning the installed Chapter21.12 simulation with21.11 statistical contracts, preserving earlier wheel evidence. F28/F32/F209/F165/F185 remain open; F185/F32 interface/model decisions are not silently resolved by selected compatible examples. No independent sign-off, supported-platform, release or canonical acceptance is claimed.
