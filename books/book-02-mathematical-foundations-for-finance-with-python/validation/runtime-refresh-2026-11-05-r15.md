# V-73 — Full Book 02 runtime refresh

Date: 2026-11-05. Exact executable revision: `5988dee92cf70f48f718bf8b96e0ae465d22ee42`.

All 534 Python files compiled, all 321 discovered check/test scripts exited zero, and all 535 required source/fixture Git blob hashes matched before and after execution. Counts derive from the pinned tree. The required non-Python fixture is chapter-01/data/section-1.14-cases.json. No script failed or timed out. Python: 3.12.14 (main, Aug 25 2026, 14:00:49) [Clang 22.1.3 ]. Platform: Linux-6.18.57-x86_64-with-glibc2.39. Assertions enabled; a fresh Python process, parent-directory cwd and 60-second timeout for each script.

Includes the [Section 20.3 quadratic/feasibility correction](chapter-20-invariant-matrix-range-followup.md), retaining 12 initial failed cases and a 36-case pass, and the [Section 20.2 two-by-two correction](chapter-20-benchmark-linear-range-followup.md), retaining seven initial failed cases and a 19-case pass. Their chapter scopes were 28 files/17 scripts and 29 files/18 scripts.

[Full source/fixture manifest and individual results](runtime-refresh-2026-11-05-r15.json).

Replay in a clean checkout at the stated revision. Verify SHA1(b'blob '+decimal_byte_length+b'\\0'+file_bytes) for each listed path, compile each .py via py_compile.compile(path,doraise=True), run each check_/test_ basename in a fresh Python process from its parent directory with timeout=60, then recheck every hash. The raw record contains compiled paths, script exits, stderr and timings; successful stdout is omitted. Cached inputs were reused only if their Git blob hashes matched; missing blobs were retrieved at the pin.

Thirty-two selected COV categories remain partially addressed; none closed. These are assistant-run candidate Linux checks, not independent sign-off, supported-platform validation, release acceptance or canonical approval. G2–G8 remain pending.

Publication verification at `b6af77a8ff3c9782d3981b761b1b3f5e83d80fa9` re-fetched all 17 changed files exactly, matched all 535 runtime hashes against current main and found no missing paths among 940 recognized local destinations in changed Markdown. [Pinned receipt](runtime-refresh-2026-11-05-r15-publication-verification.json). The receipt precedes this added link; this is a static path check, not rendered navigation or another runtime pass.
