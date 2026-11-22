# V264 — Partial Section 10.9 analytic exponential/rate contracts

Baseline pin: `0e5b5fc323732073c2164acbad2e30507e13a883`. [Observer](review.txt), [baseline](baseline.json), [baseline replay](baseline-replay.json), [corrected](corrected.json), [replay](replay.json), [chapter runner](native-runtime.txt), [chapter execution](chapter-runtime.json).

```bash
python books/book-02-mathematical-foundations-for-finance-with-python/validation/ch10-engine-exponential-2026-11-22/review.txt baseline baseline
python books/book-02-mathematical-foundations-for-finance-with-python/validation/ch10-engine-exponential-2026-11-22/review.txt baseline baseline-replay
python books/book-02-mathematical-foundations-for-finance-with-python/validation/ch10-engine-exponential-2026-11-22/review.txt candidate corrected
python books/book-02-mathematical-foundations-for-finance-with-python/validation/ch10-engine-exponential-2026-11-22/review.txt candidate replay
python books/book-02-mathematical-foundations-for-finance-with-python/validation/ch10-engine-exponential-2026-11-22/native-runtime.txt
```

Final baseline/replay: **10 pass /10 fail**. Nine numerical/value failures and one new shared-helper call contract, not ten independent defects. Corrected **20 predicates pass twice**, identical rows. Four final observer CLI/compile commands pass. The native Chapter 10 run compiles 21 files and passes eleven checkers plus ten CLIs; before/after source identities retained. Fresh pinned full-book inventory is **642 Python files /429 check-test scripts /643 required blobs**; only Section10.9 source/checker differ from V263. This is a scoped chapter run, not a new full runtime. [V263](../full-runtime-timing-2026-11-22/README.md) remains the preceding full run at `d70076db68175154442acfeb934c721bd438d6ab`.

Initial strict-equality observer results are preserved in [initial-strict-comparison.json](initial-strict-comparison.json): two ordinary one-ULP discrepancies were observer overprecision, not source defects. The final numerical comparator uses 2e−15 relative/zero absolute tolerance. Interim19 baseline/replay/corrected/replay records retain the first smaller batch. The final20 adds a genuinely lost shift: growth=base=1e16,shift=1,T=1 must have net exponent−1 and PV about .6321205588285577; the old rounded base+shift returned1.

## Complete-value and rate algebra

For integral c*integral(exp(k*t),t=0..T), the source now validates local scalar/horizon inputs then invokes the existing corrected Section10.5 internal helper with exact Fractions of validated binary floats. Constant/exponential analytic_pv forms base+shift and growth−base−shift exactly before the same helper, avoiding intermediate rate overflow or loss of the shift. These branches retain Stream/Curve type checks and flat-curve restriction. This creates a companion-file dependency: keep section_10_05.py beside section_10_09.py. Both exact source/dependency hashes are in each observer result; the integration spy verifies the actual call.

Independent 1800-digit integrated Taylor series (small exponent) and halving/Taylor/squaring exponentiation (otherwise) evaluate the complete integral directly, rather than the source stable scaled formula. Eleven standalone integral cases cover ordinary decay, a*T overflow with finite signed result, compensated growth exp(710)*1e−308, overflowing decay k*T with result1, zero amplitude/huge exponent, zero horizon, tiny duration, zero rate, true final overflow and final underflow. Six analytic cases check constant overflowing rate sum (result .5), exponential growth/discount algebra, overflowing decay difference (result .5), lost shift, ordinary shift and zero amplitude with huge rate difference. Two local invalid-input checks and one actual shared-call contract complete the20.

The shared helper retains its declared 800-digit Decimal precision, positive exponent>10000 rejection, large negative gap cutoff and final-underflow-to-zero policy. Thus this is not a proof of universal correct rounding or unrestricted exponent/resource support. Exact rate combinations refer to validated binary float inputs; manuscript decimal rates still require unit interpretation. Numerical quadrature is a different computational route and is not made robust by fixing analytic branches.

## Explicit unfinished scope

Next: Section10.9 weighted_integral and linear analytic PV range/cancellation contracts. Then Stream.rate/Curve.discount, Simpson grid/weights/resources, numerical/discrete/portfolio aggregation, parallel-shift derivative iterator/range contracts, full assessment/oracle/report/units and all exercise/lab assumptions. No claim that the entire engine is validated. All38 COV categories remain partially addressed, none closed; no new completion percentage. Broader model/data/platform/independent reviewer/release/canonical acceptance remains open. Local Linux CPython only; Book1 tracked separately.
