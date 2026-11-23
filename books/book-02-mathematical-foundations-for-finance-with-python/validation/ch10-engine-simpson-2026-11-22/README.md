# V267 — Partial Section10.9 Simpson weighted/grid/resource contracts

Pin: `9197db12d407f4adf756ba48d263121caeb0e88a`. [Observer](review.txt), [baseline](baseline.json), [baseline replay](baseline-replay.json), [corrected](corrected.json), [replay](replay.json), [chapter runner](native-runtime.txt), [chapter results](chapter-runtime.json), [retained scalar36](scalar-retention.json), [retained linear28](linear-retention.json), [retained exponential20](exponential-retention.json). Retention runners are the corresponding *-retention.txt files in this directory.

```bash
python books/book-02-mathematical-foundations-for-finance-with-python/validation/ch10-engine-simpson-2026-11-22/review.txt baseline baseline
python books/book-02-mathematical-foundations-for-finance-with-python/validation/ch10-engine-simpson-2026-11-22/review.txt baseline baseline-replay
python books/book-02-mathematical-foundations-for-finance-with-python/validation/ch10-engine-simpson-2026-11-22/review.txt candidate corrected
python books/book-02-mathematical-foundations-for-finance-with-python/validation/ch10-engine-simpson-2026-11-22/review.txt candidate replay
python books/book-02-mathematical-foundations-for-finance-with-python/validation/ch10-engine-simpson-2026-11-22/scalar-retention.txt candidate scalar-retention
python books/book-02-mathematical-foundations-for-finance-with-python/validation/ch10-engine-simpson-2026-11-22/linear-retention.txt candidate linear-retention
python books/book-02-mathematical-foundations-for-finance-with-python/validation/ch10-engine-simpson-2026-11-22/exponential-retention.txt candidate exponential-retention
python books/book-02-mathematical-foundations-for-finance-with-python/validation/ch10-engine-simpson-2026-11-22/native-runtime.txt
```

Baseline/replay: **26 pass /15 fail**. Six numerical/exception failures,five prematurely unreportable values plus a true-overflow exception mismatch;the other eight are explicit grid/underflow/callable/work support contracts,and one is a new actual-delegation probe. Counts are not fifteen independent defects. Corrected **41 predicates pass twice**,identical rows. Prior scalar36/linear28/exponential20 checks pass with current10.5/10.7 companion sources. Four final observer CLI/compile commands pass;three retention observers add six separate commands. Exact source/dependency hashes and outputs retained.

## Complete weighted sum

Engine simpson retains its horizon and positive-even-int n validation,then delegates to corrected Section10.7 integrate(f,0,T,n,'simpson'). This reuses complete exact represented-binary-sample weights and step scaling rather than overflowing4*f before the final finite integral. A constant1e308 over[0,1] yields1e308;constant±1e308 over[0,1e−308] gives the finite signed complete product;endpoint1e308/interior−5e307 has exact Simpson sum0. A two-panel tiny represented grid T≈1e−323 with callback1e308 has integral about9.881312916824931e−16. Genuine final overflow raises ValueError.

The independent2400-digit Decimal oracle constructs nominal nodes and sums returned binary callback values with Simpson coefficients before complete scaling. Sixteen degree0–3/n2,4,6,10 cases also compare with exact polynomial integrals. This is a fixed-grid quadrature contract,not universal truncation-error or model accuracy certification.

## Explicit support policies

The shared nominal step is exact in represented endpoints;each node is rounded once. On T=.1,n=6,the fifth interior point differs by one ULP from the old i*(rounded step);that is a declared grid convention,not an empirically established improvement for every function. Endpoints are called first,then increasing interior nodes,exactly once each. Distinct represented nodes are preflighted before callbacks;T=5e−324,n2 collapses and rejects ValueError. Zero horizon invokes no callable,but invalid noncallables now reject TypeError before the zero result.

The inherited **100000-panel budget** is an educational work/memory policy,not an optimal bound. Oversized baseline probes use a callback safety sentinel at the first evaluation (or fail float count conversion before it);they never run huge callback loops. Corrected versions reject before callbacks. Final nonzero integral underflow now rejects ValueError via the shared quadrature reporting policy,unlike scalar Stream/Curve final-underflow0. These policies are distinguished from the five lost finite results. Bool/odd n,negative horizon,callback bool/nonfinite values and user exceptions retain their tested behavior.

Section10.7 must now be kept beside10.9 as well as10.5. Actual delegation is observed;the existing10.7 source is unchanged. All three dependency hashes are recorded by the main/scalar/linear runners;the exponential retention also records its quadrature companion hash.

Chapter10 compiles21 files and passes11 checkers/10 CLIs with before/after source identity verification. Fresh pinned inventory remains642 Python files/429 check-test scripts/643 required blobs;three executable blobs differ from [V263 full runtime](../full-runtime-timing-2026-11-22/README.md):10.5 source plus10.9 source/checker. This is a scoped chapter run,not a new full-book run. Earlier baseline failures,scalar timeout and precision/cutoff/resource limits remain retained.

Next:10.9 complete numerical integrand product scaling,then discrete/portfolio aggregation,parallel-shift derivative and complete assessment/oracle/report/units/exercise/lab crosswalk. Individually unreportable stream/discount factors can still hide a finite combined integrand;the Simpson fix does not resolve that separate contract. All38 COV categories remain partial,none closed. No engine/book/model/platform/independent reviewer/release/canonical acceptance. Book1 tracked separately.
