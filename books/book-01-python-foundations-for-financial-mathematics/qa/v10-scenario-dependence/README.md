# V10 — Section18.7 dependence crosswalk: partial checkpoint

Source pin `17a15f56db324709638d7fe5b7cc1500f9d0b2fa`; [manuscript](../../chapter-18/18.07-scenario-analysis.md), [prior formal review](../chapter-18-scenarios-review/README.md). Source blob `39fd28700fcab4e125d97ee5924c812a9cba20dd`.

The Python execution environment returned **“No usable execution environment is available.”** No Python source, reference demo, unittest method or compile command ran in this batch. This is a partial assumptions review, not completion of §18.7 or V10. Prior F179/69-predicate evidence and21 original failures remain at their recorded scope and revisions; they are not recounted as fresh passes.

## Verified supplemental joint-law arithmetic

[Runnable JavaScript BigInt observer](algebra.js.txt) was evaluated twice, yielding identical [18 passing algebra predicates](algebra-results.json). This is an independently constructed finite-law reference, not execution or translation of the Python listing. To replay with Node: `node -p 'JSON.stringify(eval(require("fs").readFileSync("books/book-01-python-foundations-for-financial-mathematics/qa/v10-scenario-dependence/algebra.js.txt","utf8")),null,2)'`.

Exposures60/40, one common fictional period/currency, each return marginal equally likely±10%, zero fee. Joint weights below are explicit model assumptions, not inferred frequencies.

| Joint law | Terminal outcomes | Equal state weights | E(terminal) | Population P&L variance | P(loss) | Mean loss conditional on loss |
|---|---|---|---:|---:|---:|---:|
|Same direction|110,90|1/2|100|100|1/2|10|
|Independent|110,102,98,90|1/4|100|52|1/2|6|
|Opposite direction|102,98|1/2|100|4|1/2|2|

Exact algebra:P&L=6a+4b for signs a,b. Every marginal, expected terminal and strict-loss probability agrees, but joint variance and conditional loss severity differ. Matching expected P&L or loss probability does not establish equivalent risk. Population variance and conditional loss severity are caller analyses, not fields exported by weighted_summary. These are exhaustive model states, not IID Monte Carlo observations or calibrated probabilities; no sample-SE or independence inference.

## Source/assumption crosswalk

| Contract | Static disposition |
|---|---|
|Fixed fully funded positions|Native value_scenario accepts nonnegative exposures and simple returns≥−1; short/leverage/derivative extensions remain outside scope.|
|Scenario frequency|Native weighted_summary normalizes accepted near-unit probabilities; it cannot establish likelihood calibration or state exhaustiveness.|
|Dependence|Source deterministic scenarios can encode the three proposed laws, but native calls against these new fixtures remain unexecuted.|
|Shared metadata|Common baseline, horizon, currency and P&L reconciliation are caller prerequisites; no metadata enforcement claimed.|
|Cost timing|Fixed nonnegative fee subtracted once at period end; no funding/transaction-cost/feasibility model inferred.|
|Evidence inventories|No new answer/workflow/lab-step/historical unique-method totals. Existing forty answers/twelve steps remain in prior formal review.|

## Resume without duplication

[Prepared source runner](resume-source-review.txt) is **unexecuted**. When Python returns, run it twice, retaining actual output and failures before repairs, then run prior formal review if required by source changes. It imports the exact pinned fence, compares all three proposed laws to the saved independent fixtures, and runs exact reference demo/ten existing methods plus compilation. Do not treat runner preparation as syntax/runtime verification. Source unchanged in this batch.

Next remains §18.7 source replay and completion of the V10 assumptions batch; only then proceed to §18.8. F28/F32/F209/F165/F185, broader integration, model, resource, platform, release, independent and canonical acceptance remain open. No certification.
