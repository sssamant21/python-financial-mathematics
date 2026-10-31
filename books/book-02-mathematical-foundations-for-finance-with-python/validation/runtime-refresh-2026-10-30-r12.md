# Book 02 — Full pinned runtime refresh V-48

**Date:** 2026-10-30  
**Pinned executable source:** `f02d9dc8de4198e2804737313a0ef9e05dcff50d`  
**Disposition:** Candidate Linux runtime passed; independent review and release acceptance pending.

This seventeenth refresh includes the Section18.9 trace checker and Section18.5 root-scan correction/checker after V-47. Counts were derived from the pinned Git tree.

| Actual check | Result |
|---|---:|
| Python files compiled | 484/484 |
| check_/test_ scripts, separate processes | 273/273 zero exits |
| Required source/fixture Git blob hashes before execution | 485/485 |
| Same input hashes after execution | 485/485 |
| Failed scripts / timeouts | 0 / 0 |

[Complete machine record](runtime-refresh-2026-10-30-r12.json) retains the manifest, compiled paths, commands/environment and every script's stdout/stderr/exit/time. Required inputs comprise every Book02 Python file plus `chapter-01/data/section-1.14-cases.json`. The complete manifest was compared against the pinned Git tree; source reuse required exact Git blob hash matches, checked again after execution. Later manuscript/report/tracker writes are outside executable inputs.

Python3.12.14/Linux x86_64, assertions enabled, no -O. Each script ran as `python <basename>`, cwd its parent directory, timeout15 seconds. Summed script wall time: 12.600 seconds.

Reproduce from the exact pin: verify manifest entries using Git blob hashes (SHA1 of the Git blob header plus exact bytes), compile listed Python files with `py_compile.compile(...,doraise=True)`, run listed check_/test_ scripts with recorded command/cwd/timeout, then reverify inputs. Aggregate scripts repeat checks; totals do not measure independent substantive coverage.

[Root-scan evidence](chapter-18-root-scan-followup.md) preserves original NPV/grid failures and reruns. [Project trace evidence](chapter-18-project-trace-followup.md) retains its selected passing baseline. G1 has candidate runtime evidence at this pin; G2–G8, independent mathematics/editorial review, supported environments, final reviewed-release validation and canonical approval remain pending. Twenty-nine selected categories are partially addressed; none closed by the register.
