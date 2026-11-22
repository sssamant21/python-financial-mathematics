# V258 — Partial Section10.8 continuous-PV complete scaling

Baseline pin: `3394dadd805cd683c35c4e1232df2b7a1b01aff9`. [Observer](review.txt), [baseline](baseline.json), [baseline replay](baseline-replay.json), [corrected](corrected.json), [replay](replay.json), [Chapter10 runner](native-runtime.txt), [actual chapter execution](chapter-runtime.json).

```bash
python books/book-02-mathematical-foundations-for-finance-with-python/validation/ch10-continuous-comparison-2026-11-22/review.txt baseline baseline
python books/book-02-mathematical-foundations-for-finance-with-python/validation/ch10-continuous-comparison-2026-11-22/review.txt candidate corrected
python books/book-02-mathematical-foundations-for-finance-with-python/validation/ch10-continuous-comparison-2026-11-22/review.txt candidate replay
python books/book-02-mathematical-foundations-for-finance-with-python/validation/ch10-continuous-comparison-2026-11-22/native-runtime.txt
```

Baseline/replay **10 passes /eight failed predicates**;corrected **18 pass twice**,identical rows. Six failures concern complete-value/zero handling,one unsupported-growth exception contract,and one newly required shared-helper call (not a numeric defect). No eight-defect count. Original CLI/compilation already passed despite these uncovered inputs;initial failures remain reproducible at the pin.

Continuous c=1e308,r=1,T2 has finite PV8.646647167633874e307 despite c*T overflowing;negative c preserves sign. c=r=T=1e308 has reportable limiting PV1 although r*T overflows as a float. c=1e−308,r=−1,T710 has finite PV2.233994766161711 despite unscaled exponential overflow. Validated c0 or T0 returns0 without evaluating impossible growth. Final output overflow and positive-growth exponent beyond supported10000 reject ValueError;the existing final-underflow-to0 convention is retained explicitly,not changed to a nonzero-underflow error policy.

Correction preserves Section10.8 input validation then delegates continuous_pv to the existing corrected Section10.5 constant_pv. Both companion files are required (run from chapter-10/code);the observer stages and hashes the dependency. A spy verifies one actual shared call. This avoids another independently diverging duplicate integral. Section10.5 uses exact binary-input Fractions,800-digit Decimal exponential/scaling and declared cutoff conventions;its earlier failure/range/resource evidence retains scope. It is not a universal correct-rounding/resource certificate.

Independent1800-digit references use integrated Taylor series for small exponents and halving/Taylor/squaring for the remaining tested exponentials. For positive r*T>10000,exp(−rT) is below the reportable compensation range of validated floats,so c/r supplies the limiting reference. Tests also cover ordinary/zero rate,tiny horizon,nearzero rate,signed outputs,final range,invalid bool/NaN/horizon and helper integration. Reference code does not call the Section10.5 helper. Actual selected outputs match the independently reported floats exactly;no generic1800-digit precision claim for source output.

Chapter10:21 files compile,11 checkers and10 CLIs pass,21 code identities verify afterward;full outputs/status/timings retained. Fresh pinned Book2 inventory642 Python files /429 check-test scripts /643 required blobs;only Section10.8 source/checker differ from V257. This scoped run is NOT a new full-book pass.

**Next:**10.8 equal-payment finite sum,explicit schedule,ratio/range and full comparison/report contracts,then timing-order/limit/units/exercise/applied-lab crosswalk. Importing the corrected continuous helper does not fix or validate those other functions' complete-range behavior. V257 remains latest full runtime;refresh again when accumulated code/check changes justify it,before moving beyond the section as needed. All38 selected COV categories remain partial,none closed;not defect counts/percentages. Broader data/model/resource/platform/reviewer/release/canonical acceptance remains open. Book2 IN PROGRESS;Book1 separate.
