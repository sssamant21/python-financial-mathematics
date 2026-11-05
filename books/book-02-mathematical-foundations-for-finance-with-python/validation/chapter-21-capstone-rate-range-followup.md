# Section 21.3 rate conventions and fractional-horizon valuation

Date: 2026-11-05. Baseline: `2f860f73540630ea58b1bd75616ebfa38e003980`. Corrected executable revision: `239085a0580b7a97db6787e415c36f20d11f706c`. Final Chapter 21 revision: `77a943c4ee6551431485c3a53d71f789691c2392`.

Section 21.3 now evaluates the complete scaled term before rounding, then exactly accumulates represented terms before final conversion. The standalone factor retains its own range; a finite scaled amount need not have a representable standalone factor. True term or total overflow raises OverflowError and underflow may return zero. The rate, time and convention checks remain separate; an empty portfolio still validates the rate/convention. Individually overflowing terms are not combined before term rounding.

Independent high-precision effective gross powers and continuous exponential references cover negative rates, fractional horizons, tiny effective rates, separately unrepresentable factors, sign and cancellation. A separate conversion reference probes the rounded effective-minus-one boundary near -54 log(2). The conversion functions did not change: the selected controls already passed. The actual capstone cash-flow field and callable identity are checked without promoting pending report flags. Comparisons allow one ulp for nonzero floats and distinguish zero and range errors.

The baseline had ten mismatches in 53 rows, including precision-only differences. The corrected run passes all 53. Initial chapter scope: 20 compiled files and 11 passing scripts. The longer-term high-precision implementation is not a proof of correct rounding for every input.

Final Chapter 21 scope: 21 files compiled, 12 scripts passed, and matching source hashes before and after. [Raw baseline, rerun and scoped hashes](chapter-21-capstone-rate-range-followup.json) · [Runnable checker](../chapter-21/code/check_capstone_rate_range.py).

Replay from Book 02's chapter-21/code at the corrected revision: run python check_capstone_rate_range.py with assertions enabled. For the baseline, save the checker externally, check out the stated baseline and overlay only that checker. Compile each .py via py_compile.compile(path,doraise=True), run check_/test_ basenames in separate Python processes from their parent directories with a 60-second timeout, and verify the raw Git blob hashes before and after. Successful stdout is omitted from the scope summary.

COV-90 receives selected partial evidence only; none of its broader proof, units, scope or independent review obligations are closed. Selected assistant-run Linux evidence only; not independent reviewer sign-off, supported-platform validation, release acceptance or canonical approval.
