# Book 02 — Full pinned runtime refresh V-43

**Date:** 2026-10-30  
**Pinned executable source:** `b5b04e9fbee6367d5d81136d47d9475c96a2dea5`  
**Disposition:** Scoped candidate execution passed; independent review and release acceptance pending.

This twelfth refresh covers the Section 16.8 calibration-range correction and subsequent Sections 16.9/16.10 normalized-copy corrections, plus both new checkers after V-42.

| Actual check | Result |
|---|---:|
| Python sources compiled | 474/474 |
| check_/test_ scripts, separate processes | 263/263 zero exits |
| Required source/fixture Git blob hashes before execution | 475/475 |
| Same input hashes after execution | 475/475 |
| Failed scripts / timeouts | 0 / 0 |

[Complete machine record](runtime-refresh-2026-10-30-r7.json) retains exact input hashes, compiled paths, command/environment and every script's stdout/stderr/exit/time. Required inputs are all Book 02 Python files plus `chapter-01/data/section-1.14-cases.json`. The complete manifest was compared with the pinned Git tree; snapshot bytes were reused only when their required Git blob hash matched. All hashes were reverified after execution. Subsequent report/manuscript/tracker writes are not represented as executable inputs.

Environment: Python 3.12.14/Linux x86_64, assertions enabled, no `-O`; each script ran as `python <basename>` with its parent as cwd and a 15-second timeout. Summed script wall time: 8.072 seconds.

Reproduction: check out the exact revision, verify the manifest using Git blob hashing (`SHA1("blob "+byte_length+"\\0"+bytes)`), compile listed Python files with `py_compile.compile(..., doraise=True)`, invoke listed check_/test_ scripts under the recorded command/cwd/timeout, and reverify the input hashes. Aggregate scripts repeat checks; counts do not measure independent substantive coverage.

The [raw-price calibration report](chapter-16-calibration-range-followup.md) and [normalized-copy report](chapter-16-normalized-calibration-followup.md) retain original failures and scoped reruns. Earlier runtime records remain historical. G1 has scoped candidate evidence at this exact pin; G2–G8, independent review, declared supported environments, final reviewed-release validation and canonical approval remain pending. Twenty-eight categories remain partially addressed; none is closed by the register.
