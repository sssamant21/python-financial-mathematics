# Book 02 — Full pinned runtime refresh V-45

**Date:** 2026-10-30  
**Pinned executable source:** `0e2f5e4eebc9b3e0328a3bba2c6e0d7f88954db3`  
**Disposition:** Scoped candidate execution passed; independent review and release approval pending.

This fourteenth refresh covers the normalized loss corrections in Sections16.9/16.10 and the new Section16.8 rank-deficient lab, plus their two checkers after V-44. Counts were derived from the pinned Git tree.

| Actual check | Result |
|---|---:|
| Python files compiled | 478/478 |
| check_/test_ scripts, separate processes | 267/267 zero exits |
| Required source/fixture Git blob hashes before execution | 479/479 |
| Same input hashes after execution | 479/479 |
| Failed scripts / timeouts | 0 / 0 |

[Complete machine record](runtime-refresh-2026-10-30-r9.json) retains the exact manifest, compiled paths, command/environment and every script's stdout/stderr/exit/time. Required inputs comprise all Book02 Python files plus `chapter-01/data/section-1.14-cases.json`. The complete runtime manifest was compared against the pinned tree; files were reused only when their required Git blob hash matched. All inputs were reverified after execution. Later manuscript/report/tracker writes are not represented as executable inputs.

Environment: Python3.12.14/Linux x86_64, assertions enabled, no `-O`; each script ran as `python <basename>`, cwd its parent, timeout15 seconds. Summed script wall time: 8.565 seconds.

Reproduce from the exact revision: verify each manifest entry with Git blob hashing (`SHA1("blob "+byte_length+"\\0"+bytes)`), compile listed Python paths with `py_compile.compile(..., doraise=True)`, run listed check_/test_ scripts with the recorded command/cwd/timeout, then reverify inputs. Aggregate scripts repeat checks; counts do not measure independent substantive coverage.

The [normalized-loss report](chapter-16-normalized-loss-followup.md) and [identifiability lab report](chapter-16-identifiability-followup.md) retain initial failures and scoped reruns. Earlier runtime records remain historical. G1 has scoped candidate evidence at this pin; G2–G8, independent mathematics/editorial review, supported environments, final reviewed-release validation and canonical approval remain pending. Twenty-eight categories remain partially addressed; none is closed by the register.
