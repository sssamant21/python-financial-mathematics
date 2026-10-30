# Book 02 — Full pinned runtime refresh V-46

**Date:** 2026-10-30  
**Pinned executable source:** `df656dbbe59bda073bf662392c9f0348fc18cc83`  
**Disposition:** Candidate Linux execution passed; independent review and release acceptance pending.

This fifteenth refresh includes Section17.4's prior active-boundary correction/checker and the new degenerate-multiplier checker after V-45. Counts were derived from the pinned Git tree.

| Actual check | Result |
|---|---:|
| Python files compiled | 480/480 |
| check_/test_ scripts, separate processes | 269/269 zero exits |
| Required source/fixture Git blob hashes before execution | 481/481 |
| Same input hashes after execution | 481/481 |
| Failed scripts / timeouts | 0 / 0 |

[Complete machine record](runtime-refresh-2026-10-30-r10.json) retains the exact manifest, compiled paths, environment, commands, stdout/stderr/exits and times. Required inputs comprise every Book02 Python file plus `chapter-01/data/section-1.14-cases.json`. The full manifest was compared against the pinned Git tree; source reuse required exact Git blob hashes, checked again after execution. Later manuscript/report/tracker commits are outside executable inputs.

Python3.12.14/Linux x86_64, assertions enabled, no -O. Each script ran as `python <basename>` in its parent directory, timeout15 seconds. Summed script wall time: 8.303 seconds.

Reproduce at this revision: verify every manifest entry with Git blob hashing (SHA1 of the Git blob header plus exact bytes), compile listed Python files with `py_compile.compile(...,doraise=True)`, execute listed check_/test_ scripts using recorded commands/cwd/timeout, then reverify all inputs. Aggregate scripts repeat checks; totals do not measure independent substantive coverage.

[Boundary correction](chapter-17-active-boundary-followup.md) retains its original failure/rerun; [degenerate-family evidence](chapter-17-degenerate-multiplier-followup.md) retains its first passing run and exact rational references. G1 has candidate runtime evidence at this pin. G2–G8, independent mathematics/editorial review, supported-platform checks, final reviewed-release validation and canonical approval remain pending. Twenty-eight categories remain partially addressed; none closed by the register.
