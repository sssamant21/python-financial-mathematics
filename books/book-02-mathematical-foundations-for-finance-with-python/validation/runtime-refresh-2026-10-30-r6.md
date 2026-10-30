# Book 02 — Full pinned runtime refresh V-42

**Date:** 2026-10-30  
**Pinned executable source:** `c42fb1965a8febe91dc9ed310b2db9b0d0cb9ca2`  
**Disposition:** Scoped candidate execution passed; independent review and release acceptance pending.

This eleventh refresh includes the Section 16.8 residual metric correction, Section 16.9/16.10 shared-helper integration and two new checkers after V-41.

| Actual check | Result |
|---|---:|
| Python files compiled | 472/472 |
| check_/test_ scripts, separate processes | 261/261 zero exits |
| Required source/fixture Git blob hashes before execution | 473/473 |
| Same hashes after execution | 473/473 |
| Failed scripts / timeouts | 0 / 0 |

[Complete raw record](runtime-refresh-2026-10-30-r6.json) retains the pinned-tree manifest, compiled paths, environment/command and every script's stdout/stderr/exit/time. Required inputs are all Book 02 Python files plus `chapter-01/data/section-1.14-cases.json`. The complete manifest was compared to the pinned Git tree; each reused snapshot file matched its required blob hash. All input hashes were checked again after execution. Subsequent manuscript/report/tracker writes are not claimed as executable inputs.

Environment: Python 3.12.14/Linux x86_64, assertions enabled, no `-O`. Each script ran as `python <basename>`, cwd its parent, timeout 15 seconds. Summed script wall time: 7.880 seconds.

Reproduce from the exact revision: verify every manifest entry using Git blob hashing (`SHA1("blob "+byte_length+"\\0"+bytes)`), compile listed Python files with `py_compile.compile(..., doraise=True)`, run listed check_/test_ scripts with the recorded command/cwd/timeout, then reverify the input hashes. Aggregate scripts repeat checks; script counts do not measure independent coverage.

The [residual metric report](chapter-16-residual-metric-followup.md) preserves original failures and scoped reruns. Earlier runtime records remain historical. G1 has candidate evidence at this pin; G2–G8, independent mathematical/editorial review, supported platforms, reviewed release validation and canonical approval remain open. Twenty-eight categories are partially addressed; none is closed by the register.
