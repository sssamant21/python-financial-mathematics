# Section 20.2 benchmark annuity range

Date: 2026-11-05. Baseline: `58301a4e13b618a3340b31524af89d92354c2b27`. Corrected executable pin: `825bca6fb21fec89f5598a26de3ee0c7745f1202`.

The explicit annuity previously rounded 1+rate before discounting, and formed unscaled powers before multiplying small payments. The closed helper multiplied payment*expm1 before the final division. These routes could erase a represented small rate, lose tiny payments, overflow before a finite final sum or silently return zero for a nonzero unrepresentable sum.

Both benchmark helpers now retain exact rational arithmetic for represented inputs until the final float conversion. The explicit helper accumulates discounted terms; the closed helper uses the finite geometric formula. Positive integer period counts are retained without converting them to float. Valid zero-period/payment identities follow type/domain validation. Nonfinite final amounts and nonzero amounts rounding to zero raise ValueError; signed payments and exact zero results remain valid.

The independently derived expectation works backward from a zero final liability: V=(V+payment)/(1+rate) once per payment. It does not call either helper or use the explicit term recurrence/closed power expression. Cases include subnormal payments, near-minus-one rates, finite results hidden by large intermediate powers, tiny represented rates, signed amounts, true final overflow/underflow, zero identities, invalid controls and actual assessment values. The declared allowance is two ulps with exact zero/nonzero classification.

All 62 cases pass after correction; the baseline exited 1 with 20 failed cases. These are selected case failures, not 20 adjudicated defects. All 20 Chapter 20 files compiled and all 11 scripts passed; all retained source hashes matched before/after. The initial result-summary wrapper additionally raised KeyError: inputs after saving the complete checker outputs, because the two assessment rows omit that field; this harness error is retained separately in the raw record.

The computational tradeoff is explicit: these are exact reference benchmarks for modest period counts. Rational numerator/denominator sizes and memory/runtime grow with the count; the closed algebraic expression is not a constant-cost large-horizon pricing implementation. A 1,075-payment selected case passes, and huge-count zero/zero-rate guards are checked; this is not a resource-bound guarantee for arbitrary nontrivial counts. No count cap or new financial-domain exclusion was introduced.

[Raw initial failures, rerun and scoped manifest](chapter-20-benchmark-annuity-range-followup.json) · [Runnable checker](../chapter-20/code/check_benchmark_annuity_range.py).

Replay from a clean checkout at the corrected pin: change to Book 02's chapter-20/code and run python check_benchmark_annuity_range.py with assertions enabled. For initial failures, save that checker externally, checkout the stated baseline, overlay only the checker and run it there. Compile chapter-20/code/*.py with py_compile.compile(path,doraise=True); execute all check_/test_ files separately from their parent directory, fresh Python per script, timeout=60. Compare Git blob SHA-1 values with the raw manifest before/after. Successful script stdout is omitted from the scoped summary.

COV-87 remains partially addressed for other helper copies/ranges and independent review. Thirty-two selected categories remain partial; none closed. Selected assistant-derived expectations and Python 3.12.14/Linux checks only; no independent reviewer sign-off, supported-platform validation, release acceptance, canonical approval or general numerical accuracy/model suitability certification.
