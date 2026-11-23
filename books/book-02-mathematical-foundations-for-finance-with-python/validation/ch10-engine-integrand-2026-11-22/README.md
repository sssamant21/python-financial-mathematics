# V268 — Partial Section10.9 complete discounted-rate product

Pin: `534485e5c34a2e8892aa85ec6471d24daa08681c`. [Observer](review.txt), [baseline](baseline.json), [baseline replay](baseline-replay.json), [corrected](corrected.json), [replay](replay.json), [chapter runner](native-runtime.txt), [chapter results](chapter-runtime.json). Retained checks: [Simpson41](simpson-retention.json), [scalar36](scalar-retention.json), [linear28](linear-retention.json), [exponential20](exponential-retention.json);corresponding *-retention.txt runners are in this directory.

```bash
python books/book-02-mathematical-foundations-for-finance-with-python/validation/ch10-engine-integrand-2026-11-22/review.txt baseline baseline
python books/book-02-mathematical-foundations-for-finance-with-python/validation/ch10-engine-integrand-2026-11-22/review.txt baseline baseline-replay
python books/book-02-mathematical-foundations-for-finance-with-python/validation/ch10-engine-integrand-2026-11-22/review.txt candidate corrected
python books/book-02-mathematical-foundations-for-finance-with-python/validation/ch10-engine-integrand-2026-11-22/review.txt candidate replay
python books/book-02-mathematical-foundations-for-finance-with-python/validation/ch10-engine-integrand-2026-11-22/simpson-retention.txt candidate simpson-retention
python books/book-02-mathematical-foundations-for-finance-with-python/validation/ch10-engine-integrand-2026-11-22/scalar-retention.txt candidate scalar-retention
python books/book-02-mathematical-foundations-for-finance-with-python/validation/ch10-engine-integrand-2026-11-22/linear-retention.txt candidate linear-retention
python books/book-02-mathematical-foundations-for-finance-with-python/validation/ch10-engine-integrand-2026-11-22/exponential-retention.txt candidate exponential-retention
python books/book-02-mathematical-foundations-for-finance-with-python/validation/ch10-engine-integrand-2026-11-22/native-runtime.txt
```

Baseline/replay **10 pass /12 fail**:eleven complete-value/zero-identity failures and one new actual-callback-route probe,not twelve independent defects. Corrected **22 pass twice**,identical rows. Earlier41/36/28/20 predicates pass with current10.5/10.7 companion sources. Four final main-observer CLI/compile commands pass;four retention observers add eight separate commands. Source/dependency hashes and raw outputs retained.

## Combined native integrand

For exact native Stream/Curve objects,`_discounted_rate` forms one exact binary-input coefficient and exponent before calling the existing scaled-exponential helper. Constant/linear streams use coefficient a or a+b*t;exponential streams add growth*t to the integrated discount exponent. Thus the exponential exponent is (growth−base−shift)*t−slope*t²/2. numerical_pv actually routes its Simpson callbacks through this helper;the integration spy observes all three n2 nodes.

This avoids separately reporting a huge linear rate or discount factor when their product is finite. Examples include (1e308+1e308*2)*exp(−2)≈4.060058497098381e307;constant1e−308 times exp(710)≈2.233994766161711;and growth=base=1e308 at t=1e308 yielding coefficient1e−308 instead of separately unreportable factors. Zero coefficients remain0 even when the unused discount/growth exponent is huge. Lost-shift behavior is covered with growth=base=1e16,shift1,t1 giving exp(−1).

Subclass behavior is preserved through the original rate(t)*discount(t,shift) method route. Two actual numerical_pv checks verify overridden stream/curve methods. Custom subclasses do not acquire the fused native-field range guarantee. This is an explicit compatibility boundary,not silently bypassed dispatch.

Independent2400-digit halving/Taylor/squaring references form the complete coefficient/exponent directly. Thirteen point probes include signs,extreme cancellation,zero,ordinary affine examples and true final scalar overflow. Six actual numerical_pv probes compare with independent Decimal Simpson weights of independently referenced once-rounded nodes,including a finite≈1.4496804596937922e308 linear-rule result and a constant compensated huge-growth/rate result≈1. These are finite-grid quadrature references,not a claim of continuous-integral accuracy for all models. Two subclass probes and one actual-route probe complete22. Numerical comparisons use4e−15 relative/zero absolute tolerance.

## Limits and progression

The existing800-digit scaled-exponential precision,bounded ordinary fast path,exponent cutoffs and final scalar-underflow0 policies remain. The shared Simpson grid/panel/nonzero-integral-underflow rejection policies also remain. A combined integrand must still be representable at each callback node;an unreportable point with a potentially finite integral is not resolved. Extreme subclass products,zero-horizon parameter preflight,unrestricted resources,universal correct rounding and rigorous model/truncation error are not claimed. Earlier scalar timeout and all baseline failures remain retained.

Chapter10 compiles21 files and passes11 checkers/10 CLIs with before/after source hashes verified. Fresh pinned inventory remains642 Python files/429 check-test scripts/643 required blobs. Three executable blobs differ from [V263 full runtime](../full-runtime-timing-2026-11-22/README.md):10.5 source plus10.9 source/checker. This is a scoped chapter run,not a new full-book runtime. Next:10.9 discrete-PV complete-value/grouping/iterator contracts,then portfolio aggregation,parallel-shift derivative and complete assessment/oracle/report/units/exercise/lab crosswalk,followed by an accumulated-code full runtime refresh. All38 COV categories remain partial,none closed. No engine/book/model/platform/independent reviewer/release/canonical acceptance. Book1 tracked separately.
