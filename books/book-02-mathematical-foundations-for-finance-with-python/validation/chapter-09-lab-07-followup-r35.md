# V-218 — Section9.7 kink lab and exercise crosswalk

Source pin `c539a0d935facc2a11c510516c7fa3b23271806f`. [Runnable observer](chapter-09-lab-07-review-r35.txt), [baseline](chapter-09-lab-07-initial-r35.json), [baseline replay](chapter-09-lab-07-baseline-replay-r35.json), [corrected](chapter-09-lab-07-corrected-r35.json), [corrected replay](chapter-09-lab-07-corrected-replay-r35.json), [runtime delta](chapter-09-lab-07-runtime-delta-r35.json).

Run from repository root: `python books/book-02-mathematical-foundations-for-finance-with-python/validation/chapter-09-lab-07-review-r35.txt chapter-09-lab-07-corrected-r35`; append `--baseline` to test the pinned original manuscript. Baseline and replay retain63 passes/one static-markup failure. Eight escaped backticks repaired; status/checkbox links scoped runtime, preserving independent/canonical gates. Lab prose now distinguishes supplied fixed report from operational design fields:threshold/distance-to-threshold remain caller work. No numerical Python changes or new numerical defect invented.

Corrected64 predicates pass twice:24 CLI numerical/bool leaves,seven schemas,27 rounded-grid quotient fields,two trap comparisons,three payoff-identity values,one markup predicate. Each run compiles two exact Python files and passes three commands (CLI,existing checker,compile). Numerical comparison rtol5e-14/atol1e-12 applies to selected values;schema/bool/markup checks are exact. Actual outputs, source SHA256 and final manuscript SHA256 retained. Independent120-digit nominal-decimal exp(-.08) reference shares Decimal.exp withsource;sampled quotients independently use exact Fraction values of actual rounded coordinates/callback payoffs and nominal h, not ideal unrounded neighbors.

## Six lab units

| Unit | Actual scope |
|---|---|
| Setup | Standard library, positive-spot expiry payoffs, K100, caps/floors .02/.05,N1000,rate .04,time2;no market data or pre-expiry pricing model. |
| Execution | Exact pinned CLI/checker/compile, complete six-part CLI schema and numerical leaves checked. |
| Sided slopes | Call0/1,put−1/0,cap1000/0 andfalse differentiability flags at thresholds;fixed r,t discount factor scales slopes. |
| Step study | Caller-selected x99/100/101 and h2/.5/.1. At101,h2 crosses strike:centered quotient .75 vslocal derivative1;h.5 staysbranch andreturns1. Atstrike centered.5 persists withouta derivative. Rounded neighbors/nominalh convention preserved. |
| Scenarios | Complete up/down baseline,shocked,change,slope,flag fields checked;no automatic threshold distance, market delta or convergence guarantee. |
| Interpretation | Call-minus-put expiry identity,not fullmarketprice parity;formal physicalspot0extension limitation and finitefactor/payment gates remain as prior follow-ups. |

## Twelve prompt-to-answer dispositions

| Exercise | Derivation/execution boundary |
|---|---|
|1|Definition andequalfinite-limit criterion reviewed conceptually,not a finite-sample proof.|
|2|Callstrikeleft0/right1:CLI fields checked.|
|3|98/100/102 payoffs0/0/2 follow max(S−100,0);prior182-predicate direct payoff coverage retained at originalscope.|
|4|Putstrikeleft−1/right0:CLI fields checked.|
|5|h2 centered(2−0)/4=.5:CLI plusstepstudy;notordinaryderivative.|
|6|Capthresholdleft1000/right0:CLI fields;positivefloor at.02 irrelevant locally.|
|7|Belowfloor/interior/abovecap slopes0/1000/0 algebraicallyreviewed;priorbranchcoverage reused,notnewpredicates.|
|8|exp(−.08)=.923116346… andleft0:complete discountedCLI checked.|
|9|Two branch proof reviewed;nativepayoffdifference checked at98/100/102.|
|10|Expiry payoff omits timevalue/model;conceptual,notpreexpirypriceexecution.|
|11|Stepdomain/capcrossing/one-sidedslopes prerequisite reviewed;callladder concreteanalogue,notnewcapstepAPI.|
|12|Call-minus-put slopes both1 throughstrike bybranchidentity;sampledvaluesnotglobalproof.|

Prior182 payoff,111 sampled-quotient plus3 unequal-grid,130 scenario predicates retain original scope/failures/replays;not rerun/recounted as newunique methods. Physicalspot0flag isformal extension,notphysicaltwo-sided derivative. Broad numerical/resource/provenance/model/platform/release/independent/canonical acceptance remains open.

Fresh tree inventory642Python/429check-test scripts/643requiredblobs;642match V212 andonlyearlier V216check9.05differs. Latest full remains V212 at `2ee81822af67357087e2af6193348f2b3c5dbdf8`;this is scopedexecution,notnewfullruntime. Next9.8 sensitivity-report lab/exercise crosswalk.38selected COVcategories partial,noneclosed;not adefectcountorcompletionpercentage. Book1 separatelytracked.

Observer provenance:initial receipt comparison found unordered set text in schema expectations varied between processes. Four `chapter-09-lab-07-pre-order-*-r35.json` receipts retain the transition. Expected schema text now sorted;actual checks/counts unchanged. Final baseline/corrected pairs regenerated and row-equality checked. This was an observer serialization issue,not a source defect.
