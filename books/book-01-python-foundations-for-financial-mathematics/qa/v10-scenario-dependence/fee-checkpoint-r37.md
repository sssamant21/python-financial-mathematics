# V10 — Section18.7 fee/dependence boundary: partial checkpoint

Source pin `ecd8f947c1aaa69a905e220d86f8f5a2c55d9edd`. [Independent runnable oracle](fee-oracle-r37.js.txt), [36 passing arithmetic checks](fee-oracle-results-r37.json), [prepared source runner](resume-source-review.txt), [earlier dependence checkpoint](README.md).

The oracle was evaluated twice in JavaScript BigInt with identical results. Twelve exact finite-law fixtures combine the three earlier symmetric±10% joint laws with end-period fees0,2,10,11. This advances the fee/strict-loss assumption contract;it does not repeat the earlier population-variance study. The actual Python listing,ten existing methods,reference demo andcompilation remain unexecuted because the execution environment is unavailable. Source unchanged;no new implementation defect claimed.

For sign states a,b∈{−1,+1},the independent reference is P&L=6a+4b−fee,terminal=100+P&L. Equal model-state weights are explicit assumptions. Every fee reduces expected P&L once,independent of state count. Strict P&L<0 excludes exact ties,so increasing the fee can reveal joint-law differences hidden at fee0.

| Joint law | Fee0 loss probability | Fee2 | Fee10 | Fee11 | E(P&L),fee10 |
|---|---:|---:|---:|---:|---:|
|Same direction|1/2|1/2|1/2|1|−10|
|Independent|1/2|1/2|3/4|1|−10|
|Opposite direction|1/2|1/2|1|1|−10|

At fee10,the first two laws each have one zero-P&L state;the opposite law has none. Checks separately cover exact expected fee shift,monotonic strict-loss counts andexplicit tie-sensitive counts. These are exhaustive finite-model probabilities,not empirical observations,calibrated frequencies or statistical confidence claims. Source weighted_summary does not compute an automatic dependence model orvalidate metadata consistency.

Replay standalone supplemental algebra with `node -p 'JSON.stringify(eval(require("fs").readFileSync("books/book-01-python-foundations-for-financial-mathematics/qa/v10-scenario-dependence/fee-oracle-r37.js.txt","utf8")),null,2)'`. Actual checks used JavaScript evaluation,not a Node platform test.

The source runner is updated to the pinned current source andadds the12 saved fee fixtures to the earlier three native-call comparisons. It is still **unexecuted andnot syntax/runtime verified**. Run twice when Python returns,retain actual source mismatches andreruns,then evaluate whether the §18.7 V10 batch can advance to18.8. No new answer/workflow/step/historical-method totals. Existing F179/69 predicates/21 initial failures remain historical;F28/F32/F209/F165/F185 andbroader integration,resources,model,platform,release,independent/canonical acceptance remain open.
