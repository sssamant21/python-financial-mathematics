# V-156 — Section9.2 complete point/arc/rate elasticities

Based on `55b8ebef2ca9338976fa27b140aae386e7e0d82b`. [Checker](../chapter-09/code/check_section_02_rational_elasticities.py),[observer](chapter-09-rational-elasticity-observer.txt),[scope runner](chapter-09-rational-elasticity-runner.txt),[actual scope results](chapter-09-rational-elasticity-results.json).

```sh
python books/book-02-mathematical-foundations-for-finance-with-python/validation/chapter-09-rational-elasticity-observer.txt . baseline
python books/book-02-mathematical-foundations-for-finance-with-python/validation/chapter-09-rational-elasticity-observer.txt . corrected
python books/book-02-mathematical-foundations-for-finance-with-python/validation/chapter-09-rational-elasticity-runner.txt .
```

[Baseline](chapter-09-rational-elasticity-baseline.json):31 passes/13 failed predicates,actual child exit1;[actual replay](chapter-09-rational-elasticity-baseline-replay.json) is identical. [Corrected](chapter-09-rational-elasticity-corrected.json):44/44 pass/exit0. Observer exit0 means child output recorded,not a numerical pass by itself.

Independent1800/2400-digit Decimal complete products/quotients agree at float reporting precision for9 point cases,8 arc cases and their8 reversed endpoint cases,7 rate cases and12 invalid/priority controls. Relative4e−15/zero absolute slack;exact zero signs are explicit reporting-policy checks,not unique mathematical signs. Cases include large-product rescue,tiny-product rescue,subnormal midpoint rounding,midpoint-sum overflow,signed baselines,zero numerators,endpoint reversal and true final overflow.

Point computes x*d/y from exact represented values. Arc computes (y2−y1)*(x1+x2)/((x2−x1)*(y1+y2)) while explicitly preserving x1!=x2,nonzero x midpoint and nonzero y midpoint domains. Rate computes−r*t with final finite reporting and zero-horizon sign preservation. No nonzero supplied-baseline requirement is removed;analytical model normalization in Section9.1 is a distinct contract.

The three[original OPEN probes](chapter-09-elasticity-resume-initial.json),[actual before-fix replay](chapter-09-elasticity-resume-before-fix-replay.json) and[explicit mapped dispositions](chapter-09-elasticity-resume-disposition.json) remain separate. Those three selected contracts are RESOLVED (scoped):point rescue,arc midpoint rescue and final rate-overflow ValueError. No whole Section9.2 or COV-54 closure is claimed. [Source comparison](chapter-09-rational-elasticity-scope-comparison.json) confirms model/centered helper function text unchanged;behavior through calls to the improved point helper can still differ and requires its own review.

Three files compiled,three commands passed (demo+two checkers),three input hashes verified before-after. Existing Section9.2 checker passes unchanged. Fresh610 Python files/397 check-test scripts/611 required source-fixture blobs is inventory,not full execution;the pinned full refresh records actual execution separately. All36 selected COV categories remain partial,none closed. Independent mathematical/editorial/platform/release/canonical acceptance pending.

Next:Section9.2 constant/linear/income model helper complete-range and near-zero contracts,then centered-elasticity preflight/sampled report/callback contracts. Book1 tracked independently.

Executable source/checker revision:`2f3595ce24acb024f48ce9682d357863be8826bd`. [Pinned three-input manifest and concurrent-main preservation](chapter-09-rational-elasticity-publication-verification.json).

[Remaining-helper resume checkpoint](chapter-09-model-helper-resume-initial.json),[runnable probes](chapter-09-model-helper-resume-probes.txt) retain three OPEN model numeric cases and a separate executed callback-consumption observation. The latter returns0 for a constant function but invokes it at infinity;the desired finite-preflight/consumption rule is pending contract review,not a claim that the numeric constant derivative is wrong. No remaining helper was fixed in this batch.
