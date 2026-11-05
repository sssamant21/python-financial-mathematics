# Chapter 19 project transition range

Date: 2026-11-05. Baseline: `c8c7a10dc8a2e74e11f32a0b517a242387b12bb6`. Corrected executable pin: `908a65f2cd68240d65ef70f8a86c63078660218e`.

The project transition now delegates to Section 19.8's complete continuous accumulation. Independent expectations separately evaluate exponential growth and the constant-flow integral at 1,600 decimal digits, with exact rational zero-rate and equilibrium identities. Twelve transition cases and seven simulator/report scenarios cover signed flow, finite scaled growth/decay, equilibrium cancellation, zero/time identities, actual jump logs, post-jump depletion and rejection of nonzero terminal underflow. Final balance allowance is four ulps; event fields and policy metadata are checked directly.

The baseline failed 14 of 19 cases (exit 1); the corrected run passed all 19. The final checker additionally injects one observable shared transition result and verifies the simulator consumes it; the later scoped and full runs execute that final checker. This injected assertion was added after the isolated 19-case rerun. All 37 Chapter 19 sources compiled and 27 scripts passed at the corrected pin, with matching retained blobs. Event ordering and the terminal policy are unchanged.

[Raw failures and reruns](chapter-19-project-transition-range-followup.json) · [Runnable checker](../chapter-19/code/check_project_transition_range.py)

From a clean repository checkout, select the stated corrected revision with `git checkout <revision>` and run `python chapter-19/code/<checker>` from the Book 02 directory (or change to `chapter-19/code` and run its basename). To reproduce initial failures, overlay that checker onto the stated baseline checkout. Keep assertions enabled. Compile each scoped `chapter-19/code/*.py` with `py_compile.compile(path, doraise=True)`; run every `check_*.py`/`test_*.py` in a fresh Python process from its parent directory, with a 60-second timeout. Compare Git blob SHA-1 values with the raw evidence manifest before and after execution. Initial failures are expected only on the baseline.

Assistant checks on Python 3.12.14/Linux only. Selected fixtures do not establish arbitrary-range accuracy, model suitability, independent reviewer sign-off, supported-platform validation, release acceptance or canonical approval. COV categories remain partially addressed.
