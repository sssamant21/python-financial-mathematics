# Chapter 19 affine account-step range

Date: 2026-11-05. Baseline: `908a65f2cd68240d65ef70f8a86c63078660218e`. Corrected executable pin: `f60205d5025a2eb4a4055ad746074fe3a198f3c7`.

The Section 19.8 affine account Euler/RK4 helpers now retain the complete rational step and combined affine method increment before rounding the state once per step. This preserves finite method results when step division underflows or derivative/stage/weighted-sum arithmetic overflows. Valid zero-time inputs return the initial state after validation. Exact zero states remain allowed; nonzero method states rounding to zero and nonfinite states raise ValueError.

Independent expectations use the finite geometric accumulation of the method amplification R: Euler R=1+z; RK4 R=1+z+z²/2+z³/6+z⁴/24, with z=r*T/n. The constant forcing multiplier is h for Euler and h*(1+z/2+z²/6+z³/24) for RK4. The oracle sums the whole-horizon geometric powers; it does not call the implementation or reproduce its state loop. The allowance is 4*n ulps of the reference to accommodate state rounding, with exact zero/nonzero classification. Twelve fixtures per helper plus three invalid controls per helper give 30 cases.

The baseline failed 12 cases (exit 1); the corrected run passed all 30. All 38 Chapter 19 files compiled and 28 scripts passed at the corrected pin. These are autonomous affine account helpers, not the generic callback solvers. Exact combined-stage arithmetic changes floating-point operation order; method accuracy, stability and general ODE proofs are separate obligations. Per-step representability is required even if a later formal geometric sum would become finite.

[Raw failures and reruns](chapter-19-account-step-range-followup.json) · [Runnable checker](../chapter-19/code/check_account_step_range.py)

From a clean repository checkout, select the stated corrected revision with `git checkout <revision>` and run `python chapter-19/code/<checker>` from the Book 02 directory (or change to `chapter-19/code` and run its basename). To reproduce initial failures, overlay that checker onto the stated baseline checkout. Keep assertions enabled. Compile each scoped `chapter-19/code/*.py` with `py_compile.compile(path, doraise=True)`; run every `check_*.py`/`test_*.py` in a fresh Python process from its parent directory, with a 60-second timeout. Compare Git blob SHA-1 values with the raw evidence manifest before and after execution. Initial failures are expected only on the baseline.

Assistant checks on Python 3.12.14/Linux only. Selected fixtures do not establish arbitrary-range accuracy, model suitability, independent reviewer sign-off, supported-platform validation, release acceptance or canonical approval. COV categories remain partially addressed.
