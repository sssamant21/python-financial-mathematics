# Book 02 — Full pinned runtime refresh V-50

**Date:** 2026-10-30  
**Pinned executable source:** `54c73a8f98043676edad54efc5725e80f4af883c`  
**Disposition:** Candidate Linux runtime passed; independent review and release acceptance pending.

This nineteenth refresh includes the Section18.9 project-error checker and Section18.10 solver/curve integration/checker after V-49. Counts were derived from the pinned Git tree.

| Actual check | Result |
|---|---:|
| Python files compiled | 489/489 |
| check_/test_ scripts, separate processes | 278/278 zero exits |
| Required source/fixture Git blob hashes before execution | 490/490 |
| Same input hashes after execution | 490/490 |
| Failed scripts / timeouts | 0 / 0 |

[Complete machine record](runtime-refresh-2026-10-30-r14.json) retains the manifest, compiled paths, commands/environment and every script's stdout/stderr/exit/time. Required inputs comprise every Book02 Python file plus `chapter-01/data/section-1.14-cases.json`. The complete manifest was compared with the pinned Git tree; reused files required exact Git blob matches, rechecked after execution. Later manuscript/report/tracker writes are outside executable inputs.

Python3.12.14/Linux x86_64, assertions enabled,no -O. Each script ran as `python <basename>` in its parent directory,timeout15 seconds. Summed script wall time: 9.949 seconds.

Reproduce at the exact pin: verify each manifest entry using Git blob hashing (SHA1 of the Git blob header plus exact bytes), compile listed Python files with `py_compile.compile(...,doraise=True)`, execute listed check_/test_ scripts with recorded command/cwd/timeout, then reverify inputs. Aggregate scripts repeat checks; counts do not measure independent substantive coverage.

[Project-error evidence](chapter-18-project-errors-followup.md) retains its passing baseline and expected rejection records. [Final-method integration](chapter-18-final-method-integration-followup.md) preserves the initial missing-field failure and passing reruns. G1 has candidate runtime evidence at this pin; G2–G8,independent mathematics/editorial review,supported environments,final reviewed-release validation and canonical approval remain pending. Thirty categories remain partially addressed; none closed by the register.
