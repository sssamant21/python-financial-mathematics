# Book 02 — Full pinned runtime refresh V-49

**Date:** 2026-10-30  
**Pinned executable source:** `e5780915662a4c69e0ef7acbbb961eadc16f2237`  
**Disposition:** Candidate Linux runtime passed; independent review and release acceptance pending.

This eighteenth refresh includes the Section18.6 interpolation checker, Section18.7 order/step checker and Sections18.7/18.10 complete-stencil correction/checker after V-48. Counts were derived from the pinned Git tree.

| Actual check | Result |
|---|---:|
| Python files compiled | 487/487 |
| check_/test_ scripts, separate processes | 276/276 zero exits |
| Required source/fixture Git blob hashes before execution | 488/488 |
| Same input hashes after execution | 488/488 |
| Failed scripts / timeouts | 0 / 0 |

[Complete machine record](runtime-refresh-2026-10-30-r13.json) retains the manifest, compiled paths, commands/environment and every script's stdout/stderr/exit/time. Required inputs comprise every Book02 Python file plus `chapter-01/data/section-1.14-cases.json`. The complete manifest was compared with the pinned Git tree; file reuse required exact Git blob matches, checked again after execution. Later manuscript/report/tracker writes are outside executable inputs.

Environment: Python3.12.14/Linux x86_64, assertions enabled, no -O. Each script ran as `python <basename>` in its parent directory, timeout15 seconds. Summed script wall time: 9.146 seconds.

Reproduce at this pin: verify manifest entries using Git blob hashes (SHA1 of the Git blob header and exact bytes), compile listed Python files with `py_compile.compile(...,doraise=True)`, run listed check_/test_ scripts with recorded command/cwd/timeout, then reverify inputs. Aggregate scripts repeat checks; totals do not measure independent substantive coverage.

[Difference-range evidence](chapter-18-difference-range-followup.md) retains original probes, failed regression and scoped reruns. [Order/step evidence](chapter-18-order-step-followup.md) and [interpolation evidence](chapter-18-interpolation-bound-followup.md) retain their selected passing baselines. G1 has candidate runtime evidence at this pin; G2–G8, independent mathematics/editorial review, supported environments, final reviewed-release validation and canonical approval remain pending. Twenty-nine categories remain partially addressed; none closed by the register.
