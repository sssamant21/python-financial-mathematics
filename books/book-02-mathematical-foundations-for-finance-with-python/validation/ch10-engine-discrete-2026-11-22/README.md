# V269 — Partial Section10.9 discrete signed grouping/iterator range

Pin: `ff67ac399441099d09200fd6cd26f65390cb32a3`. [Observer](review.txt), [baseline](baseline.json), [baseline replay](baseline-replay.json), [corrected](corrected.json), [replay](replay.json), [chapter runner](native-runtime.txt), [chapter results](chapter-runtime.json). Retained checks: [integrand22](integrand-retention.json), [Simpson41](simpson-retention.json), [scalar36](scalar-retention.json), [linear28](linear-retention.json), [exponential20](exponential-retention.json), [Section10.8 schedule27](schedule-retention.json);corresponding *-retention.txt runners are in this directory.

```bash
python books/book-02-mathematical-foundations-for-finance-with-python/validation/ch10-engine-discrete-2026-11-22/review.txt baseline baseline
python books/book-02-mathematical-foundations-for-finance-with-python/validation/ch10-engine-discrete-2026-11-22/review.txt baseline baseline-replay
python books/book-02-mathematical-foundations-for-finance-with-python/validation/ch10-engine-discrete-2026-11-22/review.txt candidate corrected
python books/book-02-mathematical-foundations-for-finance-with-python/validation/ch10-engine-discrete-2026-11-22/review.txt candidate replay
python books/book-02-mathematical-foundations-for-finance-with-python/validation/ch10-engine-discrete-2026-11-22/integrand-retention.txt candidate integrand-retention
python books/book-02-mathematical-foundations-for-finance-with-python/validation/ch10-engine-discrete-2026-11-22/simpson-retention.txt candidate simpson-retention
python books/book-02-mathematical-foundations-for-finance-with-python/validation/ch10-engine-discrete-2026-11-22/scalar-retention.txt candidate scalar-retention
python books/book-02-mathematical-foundations-for-finance-with-python/validation/ch10-engine-discrete-2026-11-22/linear-retention.txt candidate linear-retention
python books/book-02-mathematical-foundations-for-finance-with-python/validation/ch10-engine-discrete-2026-11-22/exponential-retention.txt candidate exponential-retention
python books/book-02-mathematical-foundations-for-finance-with-python/validation/ch10-engine-discrete-2026-11-22/schedule-retention.txt candidate schedule-retention
python books/book-02-mathematical-foundations-for-finance-with-python/validation/ch10-engine-discrete-2026-11-22/native-runtime.txt
```

Final baseline/replay **16 pass /19 fail**:fifteen complete-value/zero/exception probes,three new preflight/work contracts and one actual shared-call probe,not nineteen independent defects. Corrected **35 pass twice**,identical rows. Earlier22/41/36/28/20 engine predicates and27 Section10.8 schedule predicates pass. Four final main-observer CLI/compile commands pass;the six retention observers add twelve separate commands. All source/dependency hashes and raw outputs are retained.

## Complete signed payment values

Native Curve payments are validated in one bounded pass,then grouped by the exact binary-input affine exponent −(base+shift)*time−slope*time²/2. Rational payment coefficients cancel within identical exponent groups before exponential arithmetic. The existing corrected Section10.8 schedule sum is factored into private `_discounted_sum`;the public10.8 schedule input validation/formula are retained. Engine discrete_pv calls that shared complete sum instead of separately reporting each discount or payment product.

Independent2400-digit halving/Taylor/squaring exponentials sum explicit signed discounted payments,not source grouping. Twelve schedules run forward and reversed. Examples include1e−308*exp(710)≈2.233994766161711;equal-time±1e308 at growing time710 plus immediate3 yielding3;an overflowing immediate subtotal returning1e308 after cancellation;and1e308*exp(−1450) retaining a representable subnormal about1.9e−322 rather than0. Affine exponent cancellation,overflowing base+shift,tiny residuals,different-time signs,true final overflow and final underflow are included. Two additional identities cancel huge equal-time coefficients or a zero amount before unsupported exponent arithmetic. Thus some rows are alternate orders of the same defect case,not distinct defects.

Two-value row iterators remain accepted. Custom Curve subclasses retain their discount-method route;one actual custom result is tested. Their numerical range still depends on the custom implementation and final fsum behavior. Native grouping guarantees do not silently override subclass dispatch.

## Support and validation contracts

The inherited **10000-payment budget** is now enforced for engine schedules. At most10001 outer rows are pulled to detect overflow;up to10000 are validated. This is a declared ingestion/work policy,not a guarantee about arbitrary iterator or callback execution cost. A feasible10001-zero-payment baseline probe distinguishes the missing cap without attempting huge work. Shift is validated even for an empty schedule. All bounded rows are validated before exponential arithmetic,so a late bool amount is rejected before an earlier unsupported growing discount is evaluated. These three changes are explicit support/exception-priority policies,not numerical defect counts. Existing negative-time,bool-amount,bad-shape behavior is checked.

The shared sum retains2000-digit sorted-group arithmetic,exact zero-exponent aggregation,exponent>10000 rejection,exponent<−10000 omission,final-underflow0 and unresolved signed-zero rejection policies. No unrestricted resource/correct-rounding or arbitrary extreme-cancellation guarantee. Keep Section10.5,10.7 and now10.8 companion files alongside10.9.

The initial observer reused its output-label variable inside a validation loop and overwrote its run filename. The [surviving initial corrected record](initial-shadowed-label.json) and [original runner](initial-shadowed-label-runner.txt) remain. Original baseline files were overwritten by those later observer runs;the final baseline and baseline-replay reproduce the pinned source with distinct filenames (same16/19 counts),followed by distinct corrected/replay35/0 files. No financial-source failure is attributed to this observer filename bug;the final named evidence is verified before publication.

Chapter10 compiles21 files and passes11 checkers/10 CLIs,including10.8,with before/after source hashes verified. Fresh pinned inventory remains642 Python files/429 check-test scripts/643 required blobs. Four executable blobs differ from [V263 full runtime](../full-runtime-timing-2026-11-22/README.md):10.5 source,10.8 source,and10.9 source/checker. This is a scoped chapter run,not a new full-book runtime. Earlier failures,scalar timeout and precision/cutoff/resource limits remain retained. Next:10.9 portfolio aggregation,then parallel-shift derivative and complete assessment/oracle/report/units/exercise/lab crosswalk,followed by accumulated-code full runtime refresh. All38 COV categories remain partial,none closed. No engine/book/model/platform/independent reviewer/release/canonical acceptance. Book1 tracked separately.
