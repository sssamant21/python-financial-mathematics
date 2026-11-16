# V10 — Section18.7 aggregation and overlap: partial checkpoint

Pin `d62a1c118702ff64aca3c656c94ddb334a8443c8`. [Runnable independent observer](aggregation-oracle-r38.js.txt), [15 passing checks](aggregation-results-r38.json), [prepared native replay](aggregation-source-pending-r38.txt). JavaScript evaluation ran twice with identical results. Python source/checker/demo/compile execution remains unavailable;the prepared runner is unexecuted andnot syntax/runtime verified. This advances two external aggregation assumptions without completing §18.7 orV10. No source implementation change ornew numerical defect claimed.

## Exact fixtures and interpretation

Four equally weighted atomic P&Ls are10,2,−2,−10,with baseline100,one common fictional period/currency andzero fee. Their mean is0 andstrict-loss probability1/2.

| Input rows used for weighting | Group definitions | Mean P&L | Loss probability from row P&Ls | Interpretation |
|---|---|---:|---:|---|
|Atomic states|Four individual outcomes|0|1/2|Original finite model|
|Conditional group means6,4|Indices[0,1] and[0,2],eachweight1/2|5|0|Overlapping events change the modeled law|
|Conditional group means0,0|Disjoint indices[0,3] and[1,2],eachweight1/2|0|0|Mean preserved;loss events lost by replacing distributions with means|

The overlapping-event mixture expands to atomic masses1/2,1/4,1/4,0. Its group weights sum to1,but it double-counts the first atomic state andomits the last relative to the original model. It is a coherent *different* probability distribution,not evidence of the original distribution or a source arithmetic defect. Labels/normalized weights cannot establish mutual exclusivity/exhaustiveness.

The disjoint-group example preserves atomic masses1/4 each andthe overall mean. However,

E[1(P&L<0)] ≠ E[1(E[P&L|group]<0)]

for these groups:the left side is1/2 andright side0. The source's strict-loss summary on supplied row means cannot recover omitted within-group event probabilities. Supply atomic loss outcomes oraggregate conditional loss probabilities separately;do not substitute a conditional mean row for a full outcome law when estimating losses. That external modeling requirement is distinct from input numeric validation.

Checks cover original atomic mean/loss frequency,the normalized group weights,reference group means/strict-loss indicators,expanded atomic masses/mean reconciliation andthe two non-equivalence controls. Exact small integers andbinary-exact quarter weights are used;no Monte Carlo sampling,calibration,confidence intervals ordependence certification.

## Resume

Replay supplemental algebra with `node -p 'JSON.stringify(eval(require("fs").readFileSync("books/book-01-python-foundations-for-financial-mathematics/qa/v10-scenario-dependence/aggregation-oracle-r38.js.txt","utf8")),null,2)'`. Actual execution here was JavaScript evaluation,not a Node platform test.

When Python returns,run the prepared aggregation replay twice andretain actual output. It compares native weighted_summary on all three row sets to these references;passing would confirm the documented numeric behavior,**not approve overlapping-event orcollapsed-loss modeling**. Also finish the pending fee/dependence runner from the earlier checkpoint andprior formal command scope as justified. Next remains §18.7 runtime/completion,then18.8. No newanswers/workflows/labsteps/historicalmethod totals. F28/F32/F209/F165/F185,scenario metadata consistency,model/resource/platform/release/independent/canonical gates remain open;priorF179failures retained at originalscope.
