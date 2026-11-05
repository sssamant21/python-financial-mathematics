# Book 02 — V-64 full runtime refresh

Date: 2026-11-05. Pinned executable revision: `29e2c8fc93087cb58cf08f641f49c58e9ac33a05`.

Compiled **516 Python files**, passed **305 check/test scripts**, and matched **517 required source and fixture Git blob hashes before and after execution**. No failed exits or timeouts. Includes the [rate-conversion range correction](chapter-19-rate-conversion-range-followup.md) and its checker.

[Raw evidence](runtime-refresh-2026-11-05-r6.json) records the exact manifest, environment and per-script exits. Reproduce by verifying pinned Git blob hashes, compiling all listed Python files and running each listed check/test script from its own directory in a fresh interpreter with assertions enabled and a15-second timeout; verify hashes again afterwards. Candidate Linux execution only. Counts overlap and do not measure independent coverage. Independent review, supported platforms and release approval remain pending.
