# V-74 — Full Book 02 runtime refresh

Date: 2026-11-05. Exact executable revision: `8795c02e5bbe873cd6db42a26564cc9adc7a070e`.

All 536 Python files compiled, all 323 discovered check/test scripts exited zero, and all 537 required source/fixture Git blob hashes matched before and after execution. Counts derive from the pinned tree. The required non-Python fixture is chapter-01/data/section-1.14-cases.json. No script failed or timed out. Python: 3.12.14 (main, Aug 25 2026, 14:00:49) [Clang 22.1.3 ]. Platform: Linux-6.18.57-x86_64-with-glibc2.39. Assertions enabled; fresh Python process, parent-directory cwd and 60-second timeout for each script.

Includes [Section 20.4 discrete range](chapter-20-boundary-discrete-range-followup.md), retaining 22 original mismatches and three additional tie failures at an intermediate revision before the final 64-case pass, and [Section 20.6 portfolio aggregation](chapter-20-metamorphic-aggregate-range-followup.md), retaining seven baseline failures before the final 27-case pass. Final chapter scope: 31 compiled files and 20 passing scripts.

[Full source/fixture manifest and individual results](runtime-refresh-2026-11-05-r16.json).

Replay in a clean checkout at the stated revision. Verify SHA1(b'blob '+decimal_byte_length+b'\\0'+file_bytes) for each listed path, compile each .py via py_compile.compile(path,doraise=True), run each check_/test_ basename in a fresh Python process from its parent directory with timeout=60, then recheck every hash. The raw record contains compiled paths, script exits, stderr and timings; successful stdout is omitted. Cached inputs were reused only if their Git blob hashes matched; missing blobs were retrieved at the pin.

Thirty-two selected COV categories remain partially addressed; none closed. These are assistant-run candidate Linux checks, not independent sign-off, supported-platform validation, release acceptance or canonical approval. G2–G8 remain pending.

Publication verification at `10b0cfbfc900222cc43c05469ae6a9520fa066b7` re-fetched all 17 changed files exactly, matched all 537 runtime hashes against current main and found no missing paths among 951 recognized local destinations in changed Markdown. [Pinned receipt](runtime-refresh-2026-11-05-r16-publication-verification.json). The receipt precedes this added link; static path checks do not establish rendered navigation or another runtime pass.
