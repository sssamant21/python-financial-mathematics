# V260 — Partial Section10.8 explicit schedule PV

Baseline pin: `3c23b8721b0e2fa5a936438fd9cb0fa1aa4e0fbe`. [Observer](review.txt), [baseline](baseline.json), [baseline replay](baseline-replay.json), [corrected](corrected.json), [replay](replay.json), [native chapter runner](native-runtime.txt), [chapter execution](chapter-runtime.json), [continuous18](continuous-retention.json), [equal-payment39](equal-retention.json).

```bash
python books/book-02-mathematical-foundations-for-finance-with-python/validation/ch10-schedule-2026-11-22/review.txt baseline baseline
python books/book-02-mathematical-foundations-for-finance-with-python/validation/ch10-schedule-2026-11-22/review.txt candidate corrected
python books/book-02-mathematical-foundations-for-finance-with-python/validation/ch10-schedule-2026-11-22/review.txt candidate replay
python books/book-02-mathematical-foundations-for-finance-with-python/validation/ch10-schedule-2026-11-22/continuous-retention.txt candidate continuous-retention
python books/book-02-mathematical-foundations-for-finance-with-python/validation/ch10-schedule-2026-11-22/equal-retention.txt candidate equal-retention
python books/book-02-mathematical-foundations-for-finance-with-python/validation/ch10-schedule-2026-11-22/native-runtime.txt
```

Final baseline/replay **seven passes /20 failed contract predicates**;corrected **27 pass twice**,identical rows. The initial23-probe runner/results remain in interim23-*;final27 adds compensated subnormal residual and final-underflow controls. One cap probe inspects absence of a declared cap on baseline rather than executing an infinite iterator;one validation-priority probe specifies full-row preflight. Ordinary last-bit reporting differences are reference-strengthening probes,not necessarily standalone defects. Counts are not20 independent bugs. Prior V258/V259 failures,policies,18/39 predicates and support limits retain scope.

Independent2200-digit halving/Taylor/squaring references cover twelve selected schedules,each in original/reversed order,plus a finite generator,invalid-later-row priority and bounded-ingestion probe. Cases include zero-rate signed sums that overflow fsum before cancelling,small cash flows compensated by exp(710),exact cancellation at identical huge-growth times,zero cash flow at impossible growth,huge decay,negative amounts,different times,unreportable final sum,empty schedule,a residual of one least subnormal despite opposing1e308 payments,and retained final underflow0. The reference does not call source Decimal.exp;exact same-exponent cancellation is performed before reference exponentiation.

## Corrected source contract

Validate rate and every bounded row before exponential arithmetic. Rows must be two-item lists/tuples with finite amount and nonnegative finite time. Bounded generators remain supported;at most10000 payments are consumed successfully,and attempting the10001st raises ValueError. This is a declared ingestion budget,not a bound on an arbitrary iterator's next() execution time. No transactional rollback of iterator effects is claimed.

Amounts and discount exponents use exact binary-input Fractions. Equal-exponent amounts combine/cancel exactly before any exponential;zero groups disappear. Zero-rate/zero-exponent aggregate reports once from the exact rational total. Remaining terms evaluate in a fixed exponent order under a2000-digit Decimal context,then report one finite float. This preserves selected compensated values and signed cancellation and normalizes final overflow to ValueError. Zero amounts no longer force impossible exponent evaluation. All rows validate first,so a later invalid time cannot be masked by an earlier exponent failure.

Noncancelled exponents>10000 reject as outside the supported growth range;this is an explicit limit for signed schedules,not a proof that every possible cross-time cancellation beyond that limit is unreportable. Terms with exponents<−10000 are dropped under the declared final-underflow convention. A nonempty supported signed-term sum that collapses to Decimal zero raises an unresolved-precision ValueError rather than silently asserting cancellation. Exact grouped cancellation and an entirely negligible-decay schedule may return0;final nonzero float underflow remains0. Fixed2000-digit precision is not universal correctly-rounded aggregation or a general resource/cancellation proof.

Chapter10: **21 files compile /11 checkers and10 CLIs pass**,all21 code identities verify afterward. Retained V25818 and V25939 predicates pass on the corrected source. Full outputs/status/timings retained. Fresh pinned Book2 inventory642 Python files /429 check-test scripts /643 required blobs;only10.8 source/checker differ from V257. This is NOT a new full-book runtime pass.

**Next:**10.8 timing-ratio complete range and full comparison/report fields,then timing-order/limit/units/14-exercise/applied-lab crosswalk and full refresh after accumulated changes. Schedule correction does not validate unchanged ratio/report functions or arbitrary feeds/security/model provenance. All38 COV categories remain partial,none closed;not defect counts/percentages. Book2 IN PROGRESS;broader data/model/resource/platform/reviewer/release/canonical gates open. Book1 separate.
