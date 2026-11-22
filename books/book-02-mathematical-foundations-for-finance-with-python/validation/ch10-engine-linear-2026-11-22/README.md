# V265 — Partial Section10.9 weighted factor/complete linear analytic PV

Pin: `d14c02c65f67b92ce6dd4e27be877d400b784f0f`. [Runner](review.txt), [baseline](baseline.json), [baseline replay](baseline-replay.json), [corrected](corrected.json), [replay](replay.json), [Chapter10 runner](native-runtime.txt), [Chapter10 execution](chapter-runtime.json), [retention runner](exponential-retention.txt), [retained20](exponential-retention.json).

```bash
python books/book-02-mathematical-foundations-for-finance-with-python/validation/ch10-engine-linear-2026-11-22/review.txt baseline baseline
python books/book-02-mathematical-foundations-for-finance-with-python/validation/ch10-engine-linear-2026-11-22/review.txt baseline baseline-replay
python books/book-02-mathematical-foundations-for-finance-with-python/validation/ch10-engine-linear-2026-11-22/review.txt candidate corrected
python books/book-02-mathematical-foundations-for-finance-with-python/validation/ch10-engine-linear-2026-11-22/review.txt candidate replay
python books/book-02-mathematical-foundations-for-finance-with-python/validation/ch10-engine-linear-2026-11-22/exponential-retention.txt candidate exponential-retention
python books/book-02-mathematical-foundations-for-finance-with-python/validation/ch10-engine-linear-2026-11-22/native-runtime.txt
```

Baseline/replay **15 pass /13 fail**:eleven value/exception failures plus two new shared-call contracts,not13 independent defects. Corrected **28 predicates pass twice**,identical rows. Retained V26420 predicates also pass against the current source and current companion dependency. Source hashes,raw CLI/compile outputs,Python/platform and scoped limits are retained. Four final main-observer CLI/compile commands pass;retention adds two separate commands.

Chapter10 compiles21 files and passes11 checkers/10 CLIs,including existing Section10.5 checks. The fresh pinned inventory remains642 Python files/429 check-test scripts/643 required blobs;three executable blobs differ from [V263 full runtime](../full-runtime-timing-2026-11-22/README.md):10.5 source plus10.9 source/checker. This is a scoped chapter run,not a full-book refresh.

## Complete arithmetic and dependency contract

`weighted_integral` validates local inputs then delegates to corrected10.5 `time_weighted_factor`. The existing10.5 `linear_pv` arithmetic is factored into private `_linear_pv(a,b,r,t)` on already validated exact rational inputs;the public10.5 function retains its validation and unchanged complete formula. Engine `analytic_pv` passes exact binary-input a,b,base+shift and T to that private helper. Both terms are combined before final float reporting,so cancellation and coefficient scaling are not discarded through independently unreportable moments. The companion10.5 file must remain alongside10.9. Actual calls are verified separately from numerical correctness.

Independent **2400-digit** integrated power series for small exponent and direct antiderivative/halving-Taylor-squaring exponential otherwise evaluate complete integrals. Comparisons use3e−15 relative/zero absolute tolerance,so falsely zeroing a representable subnormal fails. Nine weighted-factor cases include finite huge-duration decay(result1),huge decay(final underflow0),zero-rate finite/overflow,zero/tiny horizons,small rate and true growing-result overflow(ValueError). Fourteen linear cases include zero-rate exact cancellation,coefficient-rescued tiny/decay moments,huge duration,exact growth cancellation,zero coefficients/horizon,overflowing rate sum,negative/zero/small rates and true final overflow. Three invalid-input cases and two actual-call probes complete28.

Concrete failures: a=1e308,b=−1e308,r=0,T=2 has complete PV0 although separate terms overflow;a=0,b=1e308,T=1e−308,r=0 has PV5e−309 although unscaled T² underflows;a=0,b=1e308,r=1e308,T=1 has PV1e−308 although the bare weighted factor underflows. For a=709,b=−1,r=−1,T=710,the upper antiderivative coefficient is exactly0 and the complete PV is−710;separate growing terms are unreportable. These are deterministic arithmetic tests,not market calibration.

Shared limits remain explicit:800-digit weighted-factor/2000-digit linear arithmetic,large-exponent cutoff policies,final-underflow0,finite float inputs. The existing large-decay truncation and unsupported huge-growth branches are retained;no unrestricted exponent/resource/correct-rounding claim. Factoring the public10.5 wrapper does not assert new support for all10.5 model contracts.

Next:10.9 Stream.rate/Curve.discount complete-value/range contracts,then Simpson grid/weights/resources,numerical/discrete/portfolio aggregation,parallel-shift derivative and complete assessment/oracle/report/units/exercise/lab crosswalk. All38 COV categories remain partially addressed,none closed. No full engine/book/model/platform/independent reviewer/release/canonical acceptance. Book1 tracked separately.
