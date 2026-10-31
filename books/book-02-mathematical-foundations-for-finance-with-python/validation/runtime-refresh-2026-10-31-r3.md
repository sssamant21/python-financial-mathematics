# Book 02 — Full-book runtime refresh V-54

**Date:** 2026-10-31  
**Pinned source revision:** `228a2ce79ca4d14cd4c6196238ba2e5a112ea8f5`  
**Environment:** Python3.12.14 / Linux x86_64, assertions enabled, no optimization.

The twenty-third refresh compiled **498/498 Python files** and ran **287/287 check_/test_ scripts successfully**, with zero failed exits or timeouts. **499/499 required source/fixture Git blob hashes matched before and after execution**. Counts derive from the pinned recursive tree and include the Section1.14 JSON fixture. Summed script wall time: 10.055107 seconds.

Since [V-53](runtime-refresh-2026-10-31-r2.md), three checkers were added: [bisection bounds/counts](chapter-18-bisection-bounds-followup.md), [observed Newton order/safeguards](chapter-18-newton-order-followup.md), and [tiny discount changes](chapter-18-discount-change-followup.md). No numerical helper changed in this refresh. The Newton record distinguishes its corrected initial test-fixture failure from an implementation defect.

[Raw full execution](runtime-refresh-2026-10-31-r3.json) retains exact manifest, interpreter/environment, per-script commands, working directories, outputs and timings. To reproduce, check out the pin, verify every listed Git blob hash, compile every listed .py using py_compile.compile(doraise=True), and run each basename beginning check_ or test_ in a fresh Python process from its parent directory with assertions enabled and a15-second timeout. Re-verify the manifest hashes afterwards. No script was skipped. Counts overlap and do not measure independent coverage.

G1 is refreshed for this candidate Linux snapshot only. Thirty selected COV categories remain partially addressed; none closed by the register. Independent mathematical/editorial review, supported platforms, release acceptance and canonical approval remain pending.
