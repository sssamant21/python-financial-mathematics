# V10 — Section18.7 native runtime completion

Reviewed2026-11-21 at pinned current source `468fcff19ca47c9090945fd29cc746a0a5ee891f`, CPython3.12.14/Linux. The earlier executor blocker is resolved for this run. This completes the scoped18.7 V10 dependence/fee/aggregation replay;V10 andBook1 remain in progress. Next18.8 Monte Carlo-estimation assumptions crosswalk.

Run from repository root:

```bash
python books/book-01-python-foundations-for-financial-mathematics/qa/v10-scenario-runtime-2026-11-21/review.py first
python books/book-01-python-foundations-for-financial-mathematics/qa/v10-scenario-runtime-2026-11-21/review.py replay
```

[First driver](first-driver.json),[replay driver](replay-driver.json),[source identity](source-identity.json). The driver executes the existing prepared observers without changing their source calls or predicates;only their repository evidence output filenames are redirected into this directory. Exact temporary reference files remain permitted. Assertions must be enabled. Original prepared pins differ,so current-source byte identity to all three older pins is explicitly verified;no stale-source equivalence is assumed.

## Actual source outcomes

| Evidence per run | Verified outcome |
|---|---|
|[Dependence/fees](first-dependence-fees.json) · [replay](replay-dependence-fees.json)|15 scenario-group records:three zero-fee joint laws and12 fee/law fixtures.40 direct value_scenario calls and15 direct weighted_summary calls match independently saved integer outcomes/means/strict-loss frequencies.|
|[Aggregation](first-aggregation.json) · [replay](replay-aggregation.json)|Three native weighted_summary records match atomic,overlapping-mixture andcollapsed-group references. These verify row arithmetic,not approval ofoverlapping scenarios orreplacing loss distributions byconditional means.|
|[Retained regression](first-regression.json) · [replay](replay-regression.json)|69 existing supplemental predicates pass;complete exact reference demo/ten existing methods,quiet import andcompilation pass. OriginalF179 baseline21failures remain inprior review,not overwritten.|

First/replay rows agree exactly. Dependence observer also runs the complete reference demo/ten existing methods andcompilation. Thus each run hasfive source-command records(two prepared plus three regression);across two runs,ten command records and40 invocations ofthe same10 existing unittest methods. No newhistorical unique methods,answers,labsteps orworkflow totals are claimed. Native dictionary/list assertions are distinct from69 recorded regression predicates andthe earlier18/36/15 independent algebra checks;do not add them into a misleading unique-test total.

The supplied independent finite-law references predict identical±10% marginals/mean100 butdifferent joint-law variance/conditional severity. Afee10 givesexpectedP&L−10 across laws butstrict-loss probabilities1/2,3/4,1. Overlapping conditional-mean mixtures producea differentmodel mean5;disjoint group meanspreserve mean0butsuppress within-group loss events. Actualsourcecalls now matchthose numericreferences. Population variance/conditional severity andmodel-validity interpretation remaincaller analyses,not native summary fields. Normalized weights do not validate calibration,state exhaustiveness,commonmetadata orIID uncertainty.

## Observer provenance and limits

[Initial driver source](initial-driver.txt) and[actual initial failure](initial-driver-failure.json) retain an overstrict output guard rejecting creation ofthe temporary verbatim reference file. The corrected wrapper allows temporary writes outside therepository andredirects only explicitlynamed repository output files. This was aQA wrapper failure,not a manuscript/source defect. Corrected first/replay receipts arefinal;the earlier failed wrapper attempts are not source-test failures or newunique methods.

No financial Python implementation changed. Source/older prepared identities verified after execution;original mathematical,resource,rounding andinput-policy limits retained. F28/F32/F209/F165/F185,broader metadata/integration,model/platform/release andindependent/canonical acceptance remain open. No production operations orindependent certification.
