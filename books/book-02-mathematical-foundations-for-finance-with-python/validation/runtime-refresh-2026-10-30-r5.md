# Book 02 — Full pinned runtime refresh V-41

**Date:** 2026-10-30  
**Pinned source:** `a10a3efdbc8c69abb68089855216f70f070996da`  
**Disposition:** Scoped candidate execution passed; independent review and release approval pending.

This tenth full refresh covers both subsequent Section 16.6 corrections (secant threshold/callback contracts and combined Newton update range) and their two checkers after V-40.

| Actual check | Result |
|---|---:|
| Python sources compiled | 470/470 |
| check_/test_ scripts, each a separate process | 259/259 zero exits |
| Required input Git blob hashes before execution | 471/471 |
| Required input Git blob hashes after execution | 471/471 |
| Failed scripts / timeouts | 0 / 0 |

[Complete machine record](runtime-refresh-2026-10-30-r5.json) retains the pinned-tree manifest, exact hashes, compiled paths and every script's stdout/stderr/exit/time. Required inputs comprise all Book 02 Python sources plus `chapter-01/data/section-1.14-cases.json`. The complete runtime manifest was compared with the pinned Git tree; the snapshot reused only bytes matching each required blob hash, then reverified all hashes after execution. Subsequent manuscript/report/tracker writes are not represented as executable inputs.

Environment: Python 3.12.14/Linux x86_64, assertions enabled, no `-O`. Each script ran as `python <basename>` with its parent as cwd and a 15-second timeout. Summed script wall time: 9.847 seconds.

Reproduction: check out the exact source revision, verify each manifest entry with Git blob hashing (`SHA1("blob "+byte_length+"\\0"+bytes)`), compile all listed Python paths with `py_compile.compile(..., doraise=True)`, invoke each listed check_/test_ script under the stated command/cwd/timeout, and reverify the same input hashes. Aggregate scripts repeat tests; these counts do not measure independent substantive coverage.

[Newton range evidence](chapter-16-newton-range-followup.md) and [secant boundary evidence](chapter-16-secant-boundary-followup.md) preserve original failures and scoped reruns. Previous runtime records remain historical. G1 has candidate evidence at this exact revision; G2–G8, independent review, declared supported platforms, final reviewed release revision and canonical approval remain pending. Twenty-eight categories remain partially addressed; none is closed by the register.
