# V-76 — Full Book 02 runtime refresh

Date: 2026-11-05. Exact executable revision: `77a943c4ee6551431485c3a53d71f789691c2392`.

All 540 Python files compiled, all 327 discovered check/test scripts exited zero, and all 541 required source/fixture Git blob hashes matched before and after execution. Counts derive from the pinned tree. The required non-Python fixture is chapter-01/data/section-1.14-cases.json. No script failed or timed out. Python: 3.12.14 (main, Aug 25 2026, 14:00:49) [Clang 22.1.3 ]. Platform: Linux-6.18.57-x86_64-with-glibc2.39. Assertions enabled; fresh process, parent-directory cwd and 60-second timeout for each script.

Includes [capstone rate and valuation range](chapter-21-capstone-rate-range-followup.md), retaining ten baseline mismatches before the 53-case pass, and [analytic sensitivity and Taylor range](chapter-21-capstone-sensitivity-range-followup.md), retaining 17 baseline mismatches before the 32-case pass. Final Chapter 21 scope: 21 compiled files and 12 passing scripts.

[Full source/fixture manifest and individual results](runtime-refresh-2026-11-05-r18.json).

Replay in a clean checkout at the stated revision. Verify SHA1(b'blob '+decimal_byte_length+b'\\0'+file_bytes) for each listed path, compile each .py via py_compile.compile(path,doraise=True), run each check_/test_ basename in a fresh Python process from its parent directory with timeout=60, then recheck every hash. The raw record contains compiled paths, script exits, stderr and timings; successful stdout is omitted. Cached inputs were reused only when their Git blob hashes matched; missing blobs were retrieved at the pin.

Thirty-four selected COV categories are partially addressed; none closed. COV-90 now records selected conversion, valuation and analytic sensitivity evidence, with broader proofs, units and review still open. These are assistant-run candidate Linux checks, not independent sign-off, supported-platform validation, release acceptance or canonical approval. G2–G8 remain pending.
