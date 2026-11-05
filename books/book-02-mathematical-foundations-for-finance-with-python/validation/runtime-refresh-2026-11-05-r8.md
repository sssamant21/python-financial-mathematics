# Book 02 — V-66 full runtime refresh

Date: 2026-11-05. Pinned executable revision: `552d14965ec893cb3022e7f9d1ee6e6596f9f7e5`.

Compiled **518 Python files**, passed **307 check/test scripts**, and matched **519 required source and fixture Git blob hashes before and after execution**. No failed exits or timeouts in this full run. Includes the [contribution-balance correction](chapter-19-contribution-balance-range-followup.md) and expanded checker.

**Execution-budget change:** this run uses60 seconds per script, following a recorded15-second scoped timeout in the unchanged rate-conversion checker. The final full run's slowest script took11.135988881 seconds. The earlier timeout and successful scoped rerun are retained in the correction evidence; this is not a runtime-performance acceptance claim.

[Raw evidence](runtime-refresh-2026-11-05-r8.json) records the exact manifest, environment, per-script exits and timings. Reproduce by verifying pinned Git blob hashes, compiling all listed Python files and running each listed check/test script from its own directory in a fresh interpreter with assertions enabled and a60-second timeout; verify all hashes again afterwards. Candidate Linux execution only. Counts overlap and do not measure independent coverage. Independent review, supported platforms and release approval remain pending.
