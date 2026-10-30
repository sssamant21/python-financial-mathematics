# Book 02 — Full pinned runtime refresh V-47

**Date:** 2026-10-30  
**Pinned executable source:** `60cd09c1072aec6d6f437b62961d0b4e50cad50c`  
**Disposition:** Candidate Linux runtime passed; independent review and release acceptance pending.

This sixteenth refresh includes Section17.9's report-contract source/checker and Section17.10's computed LP integration/checker after V-46. Counts were derived from the pinned Git tree.

| Actual check | Result |
|---|---:|
| Python files compiled | 482/482 |
| check_/test_ scripts, separate processes | 271/271 zero exits |
| Required source/fixture Git blob hashes before execution | 483/483 |
| Same input hashes after execution | 483/483 |
| Failed scripts / timeouts | 0 / 0 |

[Complete machine record](runtime-refresh-2026-10-30-r11.json) retains the exact manifest, compiled paths, commands/environment and every script's stdout/stderr/exit/time. Required inputs are every Book02 Python source plus `chapter-01/data/section-1.14-cases.json`. The runtime manifest was compared with the pinned Git tree; all reused files required an exact Git blob hash match, checked again after execution. Later manuscript/report/tracker writes are outside executable inputs.

Environment: Python3.12.14/Linux x86_64, assertions enabled, no -O. Each script ran as `python <basename>`, cwd its parent directory, timeout15 seconds. Summed script wall time: 9.095 seconds.

Reproduce from the exact pin: verify manifest entries with Git blob hashing (SHA1 of the Git blob header and exact source bytes), compile listed Python files with `py_compile.compile(...,doraise=True)`, execute listed check_/test_ scripts with recorded command/cwd/timeout, then reverify inputs. Aggregate scripts repeat checks; counts do not measure independent substantive coverage.

[Report contract](chapter-17-report-contract-followup.md) and [LP integration](chapter-17-final-lp-integration-followup.md) retain their initial missing-field failures and scoped reruns. G1 has candidate runtime evidence at this pin. G2–G8, independent mathematics/editorial review, supported environments, final reviewed-release validation and canonical approval remain pending. Twenty-eight categories remain partially addressed; none closed by the register.
