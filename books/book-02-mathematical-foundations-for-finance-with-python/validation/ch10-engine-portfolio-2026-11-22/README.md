# V270 — Partial Section10.9 finite portfolio-report aggregation

Pin: `f4c6b28094883b23c8bf79de51da540e904e3443`. [Observer](review.txt), [baseline](baseline.json), [baseline replay](baseline-replay.json), [corrected](corrected.json), [replay](replay.json), [chapter runner](native-runtime.txt), [chapter results](chapter-runtime.json). Retained checks: [discrete35](discrete-retention.json), [integrand22](integrand-retention.json), [Simpson41](simpson-retention.json), [scalar36](scalar-retention.json), [linear28](linear-retention.json), [exponential20](exponential-retention.json), [Section10.8 schedule27](schedule-retention.json);corresponding *-retention.txt runners are in this directory.

```bash
python books/book-02-mathematical-foundations-for-finance-with-python/validation/ch10-engine-portfolio-2026-11-22/review.txt baseline baseline
python books/book-02-mathematical-foundations-for-finance-with-python/validation/ch10-engine-portfolio-2026-11-22/review.txt baseline baseline-replay
python books/book-02-mathematical-foundations-for-finance-with-python/validation/ch10-engine-portfolio-2026-11-22/review.txt candidate corrected
python books/book-02-mathematical-foundations-for-finance-with-python/validation/ch10-engine-portfolio-2026-11-22/review.txt candidate replay
python books/book-02-mathematical-foundations-for-finance-with-python/validation/ch10-engine-portfolio-2026-11-22/discrete-retention.txt candidate discrete-retention
python books/book-02-mathematical-foundations-for-finance-with-python/validation/ch10-engine-portfolio-2026-11-22/integrand-retention.txt candidate integrand-retention
python books/book-02-mathematical-foundations-for-finance-with-python/validation/ch10-engine-portfolio-2026-11-22/simpson-retention.txt candidate simpson-retention
python books/book-02-mathematical-foundations-for-finance-with-python/validation/ch10-engine-portfolio-2026-11-22/scalar-retention.txt candidate scalar-retention
python books/book-02-mathematical-foundations-for-finance-with-python/validation/ch10-engine-portfolio-2026-11-22/linear-retention.txt candidate linear-retention
python books/book-02-mathematical-foundations-for-finance-with-python/validation/ch10-engine-portfolio-2026-11-22/exponential-retention.txt candidate exponential-retention
python books/book-02-mathematical-foundations-for-finance-with-python/validation/ch10-engine-portfolio-2026-11-22/schedule-retention.txt candidate schedule-retention
python books/book-02-mathematical-foundations-for-finance-with-python/validation/ch10-engine-portfolio-2026-11-22/native-runtime.txt
```

Final baseline/replay **19 pass /16 fail**. Six numerical/exception probes,four unavailable-report-field consequences of the same failures,and six preflight/work-policy probes are distinguished;not sixteen independent defects. Corrected **35 pass twice**,identical rows. Earlier35/22/41/36/28/20 engine predicates and27 Section10.8 schedule predicates pass. Four final main-observer CLI/compile commands pass;seven retention observers add fourteen separate commands. Exact source/dependency hashes and outputs retained.

## Sum of finite report fields

portfolio_pv now sums exact Fractions of the already reported finite continuous components and discrete field before a single final float report. Thus [1e308,1e308,−1e308] and its signed counterpart return finite±1e308 despite old fsum intermediate overflow. Combining two1e308 continuous fields with discrete−1e308 also returns1e308. Forward/reverse orders,tiny subnormal residuals,exact cancellation,true final overflow and preserved component/discrete fields are tested. True final overflow now raises ValueError through the scalar report guard.

The independent oracle exactly sums the represented report values. Unit-horizon,zero-rate constant streams make those component values equal their validated inputs;there is no shared numerical integration oracle. A separate one-shot constant/linear/discrete example gives exact4+6+3=13. A subclass rate override and report key contract are retained.

Each continuous component and the discrete aggregate must still be individually reportable because they are explicit report fields. Opposite components whose separate PVs overflow do not become a valid report merely because an unreported mathematical total would cancel. A dedicated rejection probe retains this boundary. The total is the complete sum of float report fields,not a claim to recover rounding discarded within component valuations or universal split/merge invariance.

## Preflight and resource support

Curve,horizon,shift and positive-even panel count are checked even for an empty portfolio. The inherited100000-panel limit also applies to the empty case. Streams are collected/validated in one bounded pass before their valuation;the educational **10000-stream limit** bounds report size and stream count. At most10001 outer items are pulled to detect overflow;arbitrary iterator/callback runtime is outside that bound. The source consumes stream/payment one-shot iterators once. All stream types are checked before the first continuous calculation,so a late invalid stream is not masked by an earlier unreportable component. These are explicit support/exception-priority policies,not numerical defect counts.

Payment-row validation still occurs in discrete_pv after continuous component valuation;this batch does not claim whole-portfolio atomic validation of every payment before any continuous calculation. Existing discrete schedule bounds,subclass numerical limitations,quadrature policies and precision/resource limits remain.

Initial observer baseline/replay used result-dependent inclusion of component/discrete checks:19 pass/12 fail across31 rows. [Original runner](initial-variable-predicates-review.txt), [initial baseline](initial-variable-predicates-baseline.json) and [initial replay](initial-variable-predicates-baseline-replay.json) are retained. Final fixture-defined35-row selection records missing report fields consistently on both baseline and candidate;it adds four downstream field consequences,not four newly discovered financial defects. Final19/16 and35/0 records are separately verified.

Chapter10 compiles21 files and passes11 checkers/10 CLIs,with before/after source hashes verified. Fresh pinned inventory remains642 Python files/429 check-test scripts/643 required blobs. Four executable blobs differ from [V263 full runtime](../full-runtime-timing-2026-11-22/README.md):10.5 source,10.8 source,and10.9 source/checker. This is a scoped chapter run,not a new full-book runtime. Next:10.9 parallel-shift derivative difference/denominator/iterator/resource contracts,then full assessment/oracle/report/units/exercise/lab crosswalk and accumulated-code full runtime refresh. All38 COV categories remain partial,none closed. No engine/book/model/platform/independent reviewer/release/canonical acceptance. Book1 tracked separately.
