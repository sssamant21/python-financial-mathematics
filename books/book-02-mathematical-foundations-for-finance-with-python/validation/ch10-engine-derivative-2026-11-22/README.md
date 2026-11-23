# V271 — Partial Section10.9 parallel-shift derivative contracts

Pin: `d2e0b72758c3bb81321b0786021d28ff70ed25d0`. [Observer](review.txt), [baseline](baseline.json), [baseline replay](baseline-replay.json), [corrected](corrected.json), [replay](replay.json), [chapter runner](native-runtime.txt), [chapter results](chapter-runtime.json). Retained checks: [portfolio35](portfolio-retention.json), [discrete35](discrete-retention.json), [integrand22](integrand-retention.json), [Simpson41](simpson-retention.json), [scalar36](scalar-retention.json), [linear28](linear-retention.json), [exponential20](exponential-retention.json), [Section10.8 schedule27](schedule-retention.json);corresponding *-retention.txt runners are in this directory.

```bash
python books/book-02-mathematical-foundations-for-finance-with-python/validation/ch10-engine-derivative-2026-11-22/review.txt baseline baseline
python books/book-02-mathematical-foundations-for-finance-with-python/validation/ch10-engine-derivative-2026-11-22/review.txt baseline baseline-replay
python books/book-02-mathematical-foundations-for-finance-with-python/validation/ch10-engine-derivative-2026-11-22/review.txt candidate corrected
python books/book-02-mathematical-foundations-for-finance-with-python/validation/ch10-engine-derivative-2026-11-22/review.txt candidate replay
python books/book-02-mathematical-foundations-for-finance-with-python/validation/ch10-engine-derivative-2026-11-22/portfolio-retention.txt candidate portfolio-retention
python books/book-02-mathematical-foundations-for-finance-with-python/validation/ch10-engine-derivative-2026-11-22/discrete-retention.txt candidate discrete-retention
python books/book-02-mathematical-foundations-for-finance-with-python/validation/ch10-engine-derivative-2026-11-22/integrand-retention.txt candidate integrand-retention
python books/book-02-mathematical-foundations-for-finance-with-python/validation/ch10-engine-derivative-2026-11-22/simpson-retention.txt candidate simpson-retention
python books/book-02-mathematical-foundations-for-finance-with-python/validation/ch10-engine-derivative-2026-11-22/scalar-retention.txt candidate scalar-retention
python books/book-02-mathematical-foundations-for-finance-with-python/validation/ch10-engine-derivative-2026-11-22/linear-retention.txt candidate linear-retention
python books/book-02-mathematical-foundations-for-finance-with-python/validation/ch10-engine-derivative-2026-11-22/exponential-retention.txt candidate exponential-retention
python books/book-02-mathematical-foundations-for-finance-with-python/validation/ch10-engine-derivative-2026-11-22/schedule-retention.txt candidate schedule-retention
python books/book-02-mathematical-foundations-for-finance-with-python/validation/ch10-engine-derivative-2026-11-22/native-runtime.txt
```

Baseline/replay **16 pass /13 fail**:six numerical/exception probes,three dependent call-presence consequences,two payment-snapshot failures and two bounded-read policy probes;not thirteen independent defects. Corrected **29 pass twice**,identical rows. Earlier35/35/22/41/36/28/20 engine predicates and27 Section10.8 schedule predicates pass. Four final main-observer CLI/compile commands pass;the eight retention observers add sixteen separate commands. Source/dependency hashes and raw outputs retained.

## Complete quotient versus exact derivative

The finite-difference result is now (Fraction(up)−Fraction(down))/(2*Fraction(bump)),followed by one scalar float report. Individually finite portfolio reports can differ by more than the float range while the quotient remains finite;the denominator need not be a representable float either. Five controlled report cases independently specify up/down/bump and exact quotient,including finite rescued quotients,true final overflow,zero and final underflow0. These are patched valuation-report probes,not genuine financial source evaluations. Call-count consequences are recorded separately.

Genuine source checks include signed payments−1.3e308 at0 and8.5e307 at1 with bump1;the two complete finite prices give derivative estimate about−9.989210145972312e307 despite the overflowing float subtraction. A time-zero payment with bump1e308 has exactly zero sensitivity. Four ordinary single-payment bumps.1/.05/.025/.0125 match independent2400-digit halving/Taylor/squaring central-difference references. They also satisfy a Taylor third-derivative bound plus1e−8 report-rounding allowance for that single smooth model. These finite differences are approximations to the true parallel-rate derivative,not a universal accuracy certificate.

Main controlled quotients use exact reported-float equality. Genuine central-difference and snapshot comparisons use4e−11 relative/zero absolute tolerance to allow cancellation of separately rounded prices,including the small.0001 bump. The native signed-price regression also compares its well-conditioned h1 case at4e−15 relative tolerance. The model here is deterministic parallel continuously compounded rate shifting;not quote-rebuilt,stochastic or calibrated curve sensitivity.

## Revaluation data and bounded work

Shared validated-stream/payment helpers preserve existing portfolio/discrete contracts. The derivative preflights horizon/panel support before ingestion,collects at most10000 streams and10000 payments,and pulls at most10001 items from each producer to detect overflow. Finite10005-item baseline producers demonstrate the former eager unbounded snapshot;no truly infinite producer is executed.

Payment rows are normalized to immutable finite scalar pairs before both valuations. This fixes a one-shot iterator within a payment row and isolates caller-owned mutable rows:an otherwise constant custom stream that overwrites the caller's amount cannot change the copied payment value used by either valuation. Stream objects themselves are only outer-snapshotted;arbitrary stateful subclass models or concurrent mutations of custom objects are not made pure or thread-safe. Actual custom model dispatch remains supported under its existing numerical limitations.

Finite positive bump and distinct finite represented base±bump checks remain. No automatic bump selection,unrestricted precision/resource guarantee or recovery of discarded PV rounding is claimed. The scalar result still permits final underflow0;finite-component/report and quadrature limits remain.

## Initial legacy-boundary failure retained

The first chapter run compiled21 files but failed check_cashflow_boundaries.py:test_denominator_overflow because it still required OverflowError when2*bump overflowed. [Initial runtime](initial-chapter-runtime.json) contains that exact failed output/hash manifest;[old boundary checker](initial-check-cashflow-boundaries.txt) and [initial runner](initial-native-runtime.txt) remain. The five-method boundary suite keeps its method count;its denominator fixture now checks a genuine time-zero cash flow with known shift-invariant PV and expected derivative0. This updates a superseded intermediate-denominator exception contract using an independent identity,rather than treating the old test as an oracle. The corrected chapter run passes.

Final Chapter10 compiles21 files and passes11 checkers/10 CLIs with before/after source hashes verified. Fresh pinned inventory remains642 Python files/429 check-test scripts/643 required blobs. Five executable blobs differ from [V263 full runtime](../full-runtime-timing-2026-11-22/README.md):10.5/10.8/10.9 sources,10.9 checker and cash-flow boundary checker. This is a scoped chapter run,not a new full-book runtime. Next:complete10.9 assessment/report/oracle/units/exercise/lab crosswalk,then accumulated-code full pinned runtime refresh. All38 COV categories remain partial,none closed. No engine/book/model/platform/independent reviewer/release/canonical acceptance. Book1 tracked separately.
