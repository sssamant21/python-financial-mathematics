# V261 — Partial Section10.8 timing ratio and complete fixed report

Baseline pin: `83322aff81c8a0fa62a1cd0787e6cad96acf56e0`. [Observer](review.txt), [baseline](baseline.json), [baseline replay](baseline-replay.json), [corrected](corrected.json), [replay](replay.json), [chapter runner](native-runtime.txt), [chapter execution](chapter-runtime.json), [continuous18](continuous-retention.json), [equal39](equal-retention.json), [schedule27](schedule-retention.json).

```bash
python books/book-02-mathematical-foundations-for-finance-with-python/validation/ch10-ratio-report-2026-11-22/review.txt baseline baseline
python books/book-02-mathematical-foundations-for-finance-with-python/validation/ch10-ratio-report-2026-11-22/review.txt candidate corrected
python books/book-02-mathematical-foundations-for-finance-with-python/validation/ch10-ratio-report-2026-11-22/review.txt candidate replay
python books/book-02-mathematical-foundations-for-finance-with-python/validation/ch10-ratio-report-2026-11-22/continuous-retention.txt candidate continuous-retention
python books/book-02-mathematical-foundations-for-finance-with-python/validation/ch10-ratio-report-2026-11-22/equal-retention.txt candidate equal-retention
python books/book-02-mathematical-foundations-for-finance-with-python/validation/ch10-ratio-report-2026-11-22/schedule-retention.txt candidate schedule-retention
python books/book-02-mathematical-foundations-for-finance-with-python/validation/ch10-ratio-report-2026-11-22/native-runtime.txt
```

Baseline/replay **59 passes /20 failed contract predicates**;corrected **79 pass twice**,identical rows and complete fixed reports. Three probes inspect absence of a ratio count-size guard in the pinned function rather than executing oversized counts. They are explicit support-policy probes,not numeric defects. Other failures include overflowing expm1/step products despite representable ratios,huge-n conversion and nonfinite comparison metadata. Counts are not20 independent defects. The initial76-probe runner/baseline remain in interim76-*;final79 adds x1500 ratio probes with zero absolute tolerance,including a representable subnormal midpoint result.

## Complete timing ratio

Let x=rT/n,offset=0,.5,1 and phi(u)=(1−exp(−u))/u with phi(0)=1. For x>0,the ratio is exp(−x*offset)/phi(x);for x<0 it is exp(−abs(x)*(1−offset))/phi(abs(x)). This cancels the original overflowing factors before float reporting. Source now forms x exactly from represented binary inputs,uses the existing stable phi helper and800-digit Decimal exponential/scaling,then reports one finite float. Zero x yields1. A ratio count has the same declared4096-bit budget as equal-payment counts.

Tests include x±710,±1e308,1500,overflowing full r*T,zero rate and n10^400. For positive x710,beginning ratio is about710 despite overflowing expm1;mid/end ratios may be tiny but finite. At x1500,the midpoint ratio is subnormal and must not be discarded before scaling. Huge decay returns0 when the full result underflows;unreportable growing ratio outputs reject ValueError. The exponent<−10000 cutoff and final-underflow0 convention are declared support policies,not universal correctly-rounded arithmetic or resource proofs.

Independent2200-digit halving/Taylor/squaring exponentials evaluate the direct quotient,not source phi. Ratio comparisons use3e−15 relative and zero absolute tolerance so a false zero cannot pass for a tiny nonzero reference. Extremely large-|x| asymptotic cases and huge-n controls are separately labelled;three bit-budget probes are distinct from numerical cases.

## Entire fixed comparison report

All four global fields and every field in all four prescribed scenarios(n2,8,24,730) are accounted for: schema,continuous reference,false native certification/reviewer flags,row count,n,payment amount,nominal total,three PVs and three signed differences. The independent reference uses2200-digit direct geometric quotients and integrated exponential arithmetic;reported differences use an independent complete Decimal subtraction of the reported binary PVs. Moderate report PV comparisons allow3e−15 relative/1e−12 absolute tolerance;nominal metadata and reported-difference fields are exact float comparisons.

A parameterized comparison with c1e308,r1,T2 has finite continuous and discrete PVs but unreportable nominal total2e308. The source now validates exact Fraction nominal metadata before assembling the report and raises ValueError,so it cannot publish infinity in required fields. Payment amounts derive from the complete exact c*T/n. This is a report representability requirement,not a rejection of the separate finite continuous-PV result.

Chapter10:21 files compile,11 checkers and10 CLIs pass;all21 executable identities verify afterward. Retained continuous18/equal39/schedule27 predicates pass. Actual outputs/status/timings retained. Fresh pinned Book2 inventory642 Python files /429 check-test scripts /643 required blobs;only10.8 source/checker differ from V257. This scoped run is NOT a new full-book runtime.

**Next:**10.8 timing-order/Riemann-limit/units/14-exercise/applied-lab crosswalk,then full pinned refresh before10.9 after accumulated corrections. The numerical ratio/report checks do not supply independent mathematical signoff,curve/cashflow provenance,financial/model/platform/release/canonical acceptance or arbitrary precision/resource guarantees. All38 COV categories remain partial,none closed;not defects/percentages. Book2 IN PROGRESS;Book1 separate.
