# Book 02 — Full pinned runtime refresh V-52

**Date:** 2026-10-31  
**Pinned executable source:** `5396db3f4b64acb358f08ccfd89b13427ae33268`  
**Disposition:** Candidate Linux runtime passed; independent review and release acceptance pending.

This twenty-first refresh includes Sections18.7/18.10 quadrature grid/range corrections and the continuous-stream PV correction with two new checkers after V-51. Counts were derived from the pinned Git tree.

| Actual check | Result |
|---|---:|
| Python files compiled | 493/493 |
| check_/test_ scripts, separate processes | 282/282 zero exits |
| Required source/fixture Git blob hashes before execution | 494/494 |
| Same input hashes after execution | 494/494 |
| Failed scripts / timeouts | 0 / 0 |

[Complete machine record](runtime-refresh-2026-10-31.json) retains the manifest,compiled paths,commands/environment and every script's stdout/stderr/exit/time. Required inputs comprise every Book02 Python file plus `chapter-01/data/section-1.14-cases.json`. The complete manifest was compared with the pinned Git tree; reused files required exact Git blob matches,rechecked after execution. Later manuscript/report/tracker writes are outside executable inputs.

Python3.12.14/Linux x86_64,assertions enabled,no -O. Each script ran as `python <basename>` in its parent directory,timeout15 seconds. Summed script wall time: 9.147 seconds.

Reproduce at the exact pin: verify manifest entries using Git blob hashes (SHA1 of the Git blob header plus exact bytes),compile listed Python files with `py_compile.compile(...,doraise=True)`,run listed check_/test_ scripts with recorded command/cwd/timeout,then reverify inputs. Aggregate scripts repeat checks; totals do not measure independent substantive coverage.

[Quadrature evidence](chapter-18-quadrature-range-followup.md) and [continuous-PV evidence](chapter-18-continuous-pv-range-followup.md) preserve original failures and scoped reruns. G1 has candidate runtime evidence at this pin; G2–G8,independent mathematics/editorial review,supported environments,final reviewed-release validation and canonical approval remain pending. Thirty selected categories remain partially addressed; none closed by the register.
