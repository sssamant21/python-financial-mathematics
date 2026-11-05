# Book 02 — V-60 full runtime refresh

Date: 2026-11-05. Pinned executable revision: `9f2f2ae7297b44fa443a0fe70a5e2616a74a4536`.

Compiled **510 Python files**, passed **299 check/test scripts**, and matched **511 required source and fixture Git blob hashes before and after execution**. No failed exits or timeouts. Includes [time-varying forcing](chapter-19-time-varying-forcing-followup.md) and the [nonterminal jump correction](chapter-19-nonterminal-jump-followup.md).

[Raw evidence](runtime-refresh-2026-11-05-r2.json) records the exact manifest, runtime environment and per-script exits. Reproduce by verifying pinned Git blob hashes, compiling all listed Python files and running every listed check/test script from its own directory in a fresh interpreter with assertions enabled and a15-second timeout; verify all hashes again afterwards. Candidate Linux evidence only; counts overlap and do not measure independent coverage. Independent review, supported platforms and release approval remain pending.
