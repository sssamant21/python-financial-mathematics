# V-221 — Section9.8 rational enclosure audit: partial checkpoint

Pin `d62a1c118702ff64aca3c656c94ddb334a8443c8`. [Runnable rational audit](chapter-09-lab-08-rational-audit-r38.js.txt), [104 passing results](chapter-09-lab-08-rational-audit-r38.json), [observer transitions](chapter-09-lab-08-rational-observer-transition-r38.json), [prior CLI reference](chapter-09-lab-08-cli-oracle-r37.json). The audit evaluated twice in JavaScript with identical results. Python source/runtime remains unexecuted because the executor is unavailable. No source change,independent reviewer sign-off orfull-book/runtime claim.

## New verification beyond precision agreement

The earlier80/100-digit reference agreement did not itself provide a mathematical enclosure. This audit builds exact rational bounds,independent ofDecimal.exp,JavaScript Math.exp andthe earlier fixed-point exponential implementation. Exact IEEE754 represented inputs are reconstructed before arithmetic. For0≤a≤1/8,the alternating series

exp(−a)=1−a+a²/2!−…

has decreasing term magnitudes. Its24th even partial sum is an upper bound and25th odd partial sum a lower bound. Exact rational interval operations propagate those enclosures through baseline values,complete endpoint/Taylor changes/errors andduration/convexity divisions. No floating tolerance substitutes for the enclosure predicates.

| Audit scope | Numeric reference fields |
|---|---:|
|Parallel baseline V,V′,V″,D,K|5|
|Nine parallel rows,ten value/change/error fields each|90|
|Nonparallel baseline andseven change/error fields|8|
|Total selected numeric fields|103|

For each nonzero saved reference,the entire exact enclosure lies strictly between its adjacent-double midpoint boundaries. Thus these selected mathematical quantities round to the saved binary64 reference under nearest rounding. Exact zero controls are checked as exact rational zero. This is a bounded selected-fixture mathematical check,not universal accuracy certification,source output verification orplatform acceptance. Metadata,bp conversions andtolerance booleans retain their earlier separate scopes rather than being counted as new transcendental proofs.

A104th predicate rejects a deliberately sign-flipped+100bp exact-change reference. The candidate numeric expectation is checked against an independently derived interval;no source orchecker mutation is executed. All103fields plus this control pass in both evaluations.

## Observer/resource provenance

An initial100/101-term uncached rational attempt was stopped without results after extended execution. No pass/fail/source defect was assigned to that attempt. A24/25-term cached version initially rejected a represented exponent slightly above nominal.1:exact represented rate+shock is not the decimal label. [Initial-domain source](chapter-09-lab-08-rational-domain-initial-r38.js.txt) and[two actual preflight rejections](chapter-09-lab-08-rational-domain-initial-r38.json) retain that transition. The domain was explicitly widened to1/8,where the same alternating-series bound holds,andthe corrected audit passed. These observer transitions are retained separately;neither is a Python manuscript failure.

Replay from repository root using Node:

~~~bash
node -e 'const fs=require("fs");const audit=eval(fs.readFileSync("books/book-02-mathematical-foundations-for-finance-with-python/validation/chapter-09-lab-08-rational-audit-r38.js.txt","utf8"));const input=JSON.parse(fs.readFileSync("books/book-02-mathematical-foundations-for-finance-with-python/validation/chapter-09-lab-08-cli-oracle-r37.json","utf8"));console.log(JSON.stringify(audit(input),null,2));'
~~~

Actual execution here used JavaScript evaluation;this command is a reusable replay path,not an executed Node/platform record.

## Outstanding source evidence

The [prepared completeCLI/tolerance source runner](chapter-09-lab-08-cli-resume-r37.txt) and[Exercise6/7 source fixture](chapter-09-lab-08-resume-r36.txt) remain unexecuted. Run them twice when Python is restored,retain actual source failures before fixes,andcompare native output to the now independently enclosed reference. No advancement past §9.8 is implied. Native resource/rounding/policy behavior outside these small fixtures is not established by reference arithmetic.

[Fresh tree delta](chapter-09-lab-08-runtime-delta-r38.json):642Python/429check-test scripts/643requiredblobs;642match latestfullV212 at `2ee81822af67357087e2af6193348f2b3c5dbdf8`;theonlydifference remains earlierV216check9.05. Source blob matches the priorpreparedCLIreference pin. This batch changes noPython/fixture-requiredblob. Nextremains §9.8 native replay/labcompletion,then9.9.38selectedCOVcategories partial,noneclosed;broaderprovenance/resource/model/platform/release/independent/canonical gates open. Book1 separate.
