# V-70 — Full Book 02 runtime refresh

Date: 2026-11-05. Exact source revision: `e1364e25cf09cadb7210372c24d2cf8ef4ab0f67`.

All 526 Python files compiled, all 315 discovered check/test scripts exited zero, and all 527 required source/fixture Git blob hashes matched before and after execution. The required fixture is chapter-01/data/section-1.14-cases.json. Counts derive from this pinned tree. There were no failed scripts or timeouts. Python: 3.12.14 (main, Aug 25 2026, 14:00:49) [Clang 22.1.3 ]. Platform: Linux-6.18.57-x86_64-with-glibc2.39. Assertions enabled; fresh Python process, parent-directory cwd and a 60-second timeout for every script. Slowest script: check_rate_conversion_range.py, 4.741 seconds.

Includes both [Section 20.2 annuity corrections and checks](chapter-20-benchmark-annuity-range-followup.md), which retain 20 initial failed cases and a 62-case pass, and [Section 20.5 vector/residual design evidence](chapter-20-vector-residual-design-followup.md), whose six initial cases passed without scalar implementation changes. Their chapter scopes were 20 files/11 scripts and 21 files/12 scripts respectively. These counts are execution inventories, not independent review or coverage percentages.

[Full manifest and individual results](runtime-refresh-2026-11-05-r12.json).

Replay from a clean checkout at the pinned source revision. Load the JSON manifest and verify SHA1(b'blob '+decimal_byte_length+b'\\0'+file_bytes) for every listed path. Compile every .py using py_compile.compile(path,doraise=True). Run every basename beginning check_ or test_ in a fresh Python process from its parent directory, assertions enabled, timeout=60. Verify all source/fixture hashes afterward. The raw evidence retains compiled paths, source/fixture hashes, exit codes, stderr and timings; successful stdout is omitted. Snapshot reconstruction reused cached blobs only when exact expected hashes matched and retrieved other blobs at the pin, followed by full before/after verification.

The exact rational annuity benchmarks trade growing integer sizes and memory/time for represented-input arithmetic; the selected checks do not guarantee resource bounds for arbitrary period counts. Vector/residual cases are fixed design exercises, not a general vector/solver API. Thirty-two selected COV categories remain partially addressed; none closed. Assistant-run Python 3.12.14/Linux checks do not establish independent reviewer sign-off, supported-platform validation, release acceptance, canonical approval or financial model suitability. G2–G8 remain pending.
