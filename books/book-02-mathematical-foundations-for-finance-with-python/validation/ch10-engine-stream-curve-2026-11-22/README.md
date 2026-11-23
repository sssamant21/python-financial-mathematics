# V266 — Partial Section10.9 Stream/Curve scalar range

Pin: `3938c931d4abccfc314e197e1ed2f75afe0acca4`. [Observer](review.txt), [baseline](baseline.json), [baseline replay](baseline-replay.json), [corrected](corrected.json), [replay](replay.json), [chapter runner](native-runtime.txt), [chapter results](chapter-runtime.json), [linear28 retention](linear-retention.json), [exponential20 retention](exponential-retention.json). Retention runners are linear-retention.txt and exponential-retention.txt in this directory.

```bash
python books/book-02-mathematical-foundations-for-finance-with-python/validation/ch10-engine-stream-curve-2026-11-22/review.txt baseline baseline
python books/book-02-mathematical-foundations-for-finance-with-python/validation/ch10-engine-stream-curve-2026-11-22/review.txt baseline baseline-replay
python books/book-02-mathematical-foundations-for-finance-with-python/validation/ch10-engine-stream-curve-2026-11-22/review.txt candidate corrected
python books/book-02-mathematical-foundations-for-finance-with-python/validation/ch10-engine-stream-curve-2026-11-22/review.txt candidate replay
python books/book-02-mathematical-foundations-for-finance-with-python/validation/ch10-engine-stream-curve-2026-11-22/linear-retention.txt candidate linear-retention
python books/book-02-mathematical-foundations-for-finance-with-python/validation/ch10-engine-stream-curve-2026-11-22/exponential-retention.txt candidate exponential-retention
python books/book-02-mathematical-foundations-for-finance-with-python/validation/ch10-engine-stream-curve-2026-11-22/native-runtime.txt
```

Final baseline/replay: **26 pass /10 fail** (eight complete-value/identity failures,two wrong exception types;not ten independent defects). Corrected **36 pass twice**,identical rows. Prior28 linear and20 exponential predicates pass against current source/dependency. Four final observer CLI/compile commands pass;the two retention observers add four separate commands. Exact source/dependency hashes and raw outputs are retained.

## Complete scalar values

Stream.rate now forms a+b*t exactly from validated binary float inputs before reporting. Exponential streams combine the coefficient with the exponential before final float reporting,so exp(710)*1e−308 remains about2.233994766161711 instead of overflowing first. Signed scales,zero scale/huge exponent,zero time,subnormal/underflow and genuine overflow are covered. Validation of nonfinite/bool parameters and negative time is retained;methods operate on float-validated field values as the rest of the engine does.

Curve.discount forms the complete affine integrated exponent −(base+shift)*t−slope*t²/2 with exact Fractions before exponentiation. Cases include base=−1e308,slope=1e308,t=2 giving exponent0/discount1 despite separately overflowing terms;an additional shift cancellation and overflowing base+shift at t0 also give1. Huge positive/negative exponents have explicit finite-result/ValueError behavior. This fixes scalar arithmetic,not discount-curve calibration.

The local scaled-exponential helper uses800-digit Decimal scaling for difficult values. Exact zero scale/exponent identities precede exponent limits. Exponent>10000 rejects ValueError;exponent<−10000 and final underflow return0. Ordinary |exponent|<=1 and 1e−200<=|scale|<=1e200 use a bounded math.exp fast path,avoiding a high-precision exponential at every quadrature node. No universal correct-rounding or unrestricted-resource claim. Independent2400-digit halving/Taylor/squaring references use complete binary-input expressions,with3e−15 relative/zero absolute tolerance. Four final boundary probes test±1 and the adjacent float outside each exponent boundary;other cases cover ordinary/extreme coefficients and affine cancellations. There are19 stream cases,ten curve cases and seven validation cases.

## Initial runtime failure retained

The first all-Decimal implementation passed32 scalar predicates twice and retained28/20 analytic predicates,but the Chapter10 runner aborted when check_section_10_09.py exceeded60 seconds. [Failure record](slow-runtime-failure.json), [slow source](slow-scalar-source.txt), [slow checker](slow-scalar-checker.txt), and interim32-* passing records remain. This was a real local runtime limit,not a passing chapter result. [Optional replay](slow-runtime-replay.txt) reconstructs that exact slow source with the pinned10.5 dependency;it is provided but was not executed again here,and whether it times out on another host is not asserted. Final source adds the bounded ordinary fast path and reruns all checks instead of relaxing the timeout.

Final Chapter10 run compiles21 files and passes11 checkers/10 CLIs within each60-second limit,with source hashes verified before/after. Fresh pinned inventory remains642 Python files/429 check-test scripts/643 required blobs. Three executable blobs differ from [V263 full runtime](../full-runtime-timing-2026-11-22/README.md):10.5 source plus10.9 source/checker. This is a scoped chapter rerun,not a new full-book run. Earlier V264/265 failures and precision/cutoff/underflow policies remain retained.

Next:10.9 Simpson grid/weighted-sum/resource contracts,then numerical product scaling,discrete/portfolio aggregation,parallel-shift derivative and full assessment/oracle/report/units/exercise/lab crosswalk. A finite full integrand may still require combining individually unreportable stream/discount factors;fixing the separate scalars does not resolve that product contract. All38 COV categories remain partial,none closed. No full engine/book/model/platform/independent reviewer/release/canonical acceptance. Book1 tracked separately.
