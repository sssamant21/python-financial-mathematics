# Book 02 — Full pinned runtime refresh V-51

**Date:** 2026-10-30  
**Pinned executable source:** `ae81661567a38edf78cac3a8c95bc0897819989a`  
**Disposition:** Candidate Linux runtime passed; independent review and release acceptance pending.

This twentieth refresh includes Section18.10's final sensitivity/PV study integration and shared periodic-valuation correction with two new checkers after V-50. Counts were derived from the pinned Git tree.

| Actual check | Result |
|---|---:|
| Python files compiled | 491/491 |
| check_/test_ scripts, separate processes | 280/280 zero exits |
| Required source/fixture Git blob hashes before execution | 492/492 |
| Same input hashes after execution | 492/492 |
| Failed scripts / timeouts | 0 / 0 |

[Complete machine record](runtime-refresh-2026-10-30-r15.json) retains the manifest,compiled paths,commands/environment and every script's stdout/stderr/exit/time. Required inputs comprise every Book02 Python file plus `chapter-01/data/section-1.14-cases.json`. The full manifest was compared with the pinned Git tree; reused files required exact Git blob matches,rechecked after execution. Later manuscript/report/tracker writes are outside executable inputs.

Python3.12.14/Linux x86_64,assertions enabled,no -O. Each script ran as `python <basename>` in its parent directory,timeout15 seconds. Summed script wall time: 16.158 seconds.

Reproduce at the exact pin: verify manifest entries using Git blob hashes (SHA1 of the Git blob header plus exact bytes),compile listed Python files with `py_compile.compile(...,doraise=True)`,run listed check_/test_ scripts with recorded command/cwd/timeout,then reverify inputs. Aggregate scripts repeat checks; totals do not measure independent substantive coverage.

[Final studies](chapter-18-final-studies-followup.md) preserves its missing-report failure and separately corrected checker import error. [Final NPV correction](chapter-18-final-npv-followup.md) retains original false-root reports and passing reruns. G1 has candidate runtime evidence at this pin; G2–G8,independent mathematics/editorial review,supported environments,final reviewed-release validation and canonical approval remain pending. Thirty categories remain partially addressed; none closed by the register.
