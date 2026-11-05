# Section 20.6 rounded-term portfolio aggregate

Date: 2026-11-05. Baseline: `8c65a16ae2aee217438e45adc055202a666682b6`. Final executable revision: `8795c02e5bbe873cd6db42a26564cc9adc7a070e`.

The portfolio helper now sums the exact represented per-term PV values and rounds the final total once. This preserves finite cancellation across large rounded terms, independent of order, and keeps OverflowError for a genuinely overflowing final total. Input validation, term discounting, term-range failures, one-shot iterables and the empty-portfolio rate guard are unchanged. It is not exact valuation of unrounded mathematical terms.

An independent common-integer-scale dyadic sum covers permutations, large cancellations, subnormal residuals, rounding ties and the overflow midpoint. Additional checks exercise actual discounted terms, guards and observed per-term calls. The first baseline probe aborted at the call assertion because the old summation consumed only two terms before overflow. The harness's JSON parse failure is not a numerical case. Recording that assertion as a row produced seven failures across 27 baseline cases. Both corrected reruns pass all 27. The final chapter scope includes both corrected helpers and both checkers.

Final Chapter 20 scope: 31 compiled files and 20 passing scripts, with matching source hashes before and after. [Raw attempts, results and scoped hashes](chapter-20-metamorphic-aggregate-range-followup.json) · [Runnable checker](../chapter-20/code/check_metamorphic_aggregate_range.py).

Replay from Book 02's chapter-20/code at the final revision: run python check_metamorphic_aggregate_range.py with assertions enabled. To reproduce the baseline, save the checker externally, check out the stated baseline and overlay only the checker. For the 60-case discrete baseline omit the four added binary-tie probes; overlaying the full checker on the recorded intermediate revision reproduces the expanded probe. Compile each .py via py_compile.compile(path,doraise=True), run each check_/test_ basename from its parent directory in a fresh process with timeout=60, and verify the raw Git blob hashes before and after. Successful stdout is omitted from the scope summary.

COV-87 remains partial; 32 selected categories remain partially addressed and none closed. Selected assistant-run Linux evidence only. No independent sign-off, supported-platform validation, release acceptance or canonical approval.
