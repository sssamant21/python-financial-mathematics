# Book 02 — Full pinned runtime refresh V-44

**Date:** 2026-10-30  
**Pinned executable source:** `692e8ffd8425c2fab1a0695f8c647b4fc5a128d7`  
**Disposition:** Scoped candidate execution passed; independent review and release approval pending.

This thirteenth refresh includes the Section16.10 per-candidate assessment and cumulative-objective additions plus both checkers after V-43. Counts were derived from the pinned Git tree.

| Actual check | Result |
|---|---:|
| Python files compiled | 476/476 |
| check_/test_ scripts, separate processes | 265/265 zero exits |
| Required source/fixture Git blob hashes before execution | 477/477 |
| Same input hashes after execution | 477/477 |
| Failed scripts / timeouts | 0 / 0 |

[Complete machine record](runtime-refresh-2026-10-30-r8.json) retains exact hashes, compiled paths, command/environment and every script's stdout/stderr/exit/time. Required inputs comprise all Book02 Python files plus `chapter-01/data/section-1.14-cases.json`. The full manifest was compared to the pinned tree; snapshot bytes were reused only when their required Git blob hashes matched. All inputs were reverified after execution. Later report/manuscript/tracker writes are not represented as executable inputs.

Environment: Python3.12.14/Linux x86_64, assertions enabled, no `-O`; each script ran as `python <basename>`, cwd its parent, timeout15 seconds. Summed script wall time: 8.026 seconds.

Reproduce from the exact revision: verify every manifest entry using Git blob hashing (`SHA1("blob "+byte_length+"\\0"+bytes)`), compile listed Python paths with `py_compile.compile(..., doraise=True)`, invoke listed check_/test_ files with the recorded command/cwd/timeout, then reverify input hashes. Aggregate scripts repeat tests; counts do not measure independent substantive coverage.

The [candidate-assessment report](chapter-16-final-candidate-followup.md) and [exercise-objective report](chapter-16-cumulative-objective-followup.md) preserve initial failures and scoped reruns. Earlier full records remain historical. G1 has scoped candidate evidence at this pin; G2–G8, independent mathematics/editorial review, supported environments, final reviewed-release validation and canonical approval remain pending. Twenty-eight categories remain partially addressed; none is closed by the register.
