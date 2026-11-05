# V-68 — Full Book 02 runtime refresh

Date: 2026-11-05. Exact source revision: `908a65f2cd68240d65ef70f8a86c63078660218e`.

521 Python files compiled; all 310 discovered check/test scripts exited zero; all 522 required source/fixture Git blob hashes matched before and after. The required fixture is chapter-01/data/section-1.14-cases.json. Counts come from this pinned tree, not earlier totals. No failures or timeouts occurred. Python: 3.12.14 (main, Aug 25 2026, 14:00:49) [Clang 22.1.3 ]. Platform: Linux-6.18.57-x86_64-with-glibc2.39. Assertions enabled; fresh subprocess for each script, parent-directory cwd, 60-second timeout. Slowest script: check_rate_conversion_range.py, 4.830 seconds.

Includes the prior project-depletion adapter/checker and the project-transition correction/checker. The subsequent Section 19.8 account-step correction/checker at `f60205d5025a2eb4a4055ad746074fe3a198f3c7` has 38-file/28-script Chapter 19 scoped evidence and is outside this full-run pin. The later inventory is 522 Python files and 311 scripts, not another full run.

[Manifest and individual results](runtime-refresh-2026-11-05-r10.json) · [Project transition](chapter-19-project-transition-range-followup.md) · [Later account-step scope](chapter-19-account-step-range-followup.md)

Replay: use a clean checkout at the source revision above. Load the JSON manifest, verify each path's Git blob hash as SHA1(b'blob '+decimal_byte_length+b'\\0'+file_bytes), compile every manifest .py with py_compile.compile(path,doraise=True), then run every basename beginning check_ or test_ in a fresh Python process from its parent directory with assertions enabled and timeout=60. Verify every manifest hash again afterward. The JSON retains all source paths/hashes, compiled paths, exit codes, stderr and timings; successful stdout is omitted. Snapshot reconstruction used hash-verified cached blobs plus exact-pin changed blobs, followed by complete before/after verification.

Assistant checks on Python 3.12.14/Linux only. Selected fixtures do not establish arbitrary-range accuracy, model suitability, independent reviewer sign-off, supported-platform validation, release acceptance or canonical approval. COV categories remain partially addressed.

Publication re-fetch at `4334877cd9c965ecb9984f6732cd79e3239c2020` matched all 17 changed files exactly; 870 recognized local destinations in changed Markdown resolved to existing paths. Current inventory is 522 Python files/311 scripts; only the account-step source and new checker differ from the full-runtime manifest. [Pinned verification receipt](runtime-refresh-2026-11-05-r10-publication-verification.json). This is static path verification, not a new runtime or rendered-navigation result.
