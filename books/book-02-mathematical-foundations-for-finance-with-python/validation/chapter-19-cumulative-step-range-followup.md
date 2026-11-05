# Cumulative affine stepper and report range

Date: 2026-11-05. Baseline: `baf06212851ca7949fad4376e4b9857184fb1cb9`. Corrected executable revision: `e747c068bfebd0959444b62b31fe25fe784cfa46`.

The actual Section 19.10 Euler/RK4 wrappers now share Section 19.8's complete affine method steps after retaining the cumulative public type/time/count guards. This avoids losing a representable step increment through division underflow, derivative/stage overflow or weighted-sum overflow. The helper still returns only a terminal scalar. States round once per step; exact zero is allowed, and nonzero states rounding to zero or nonfinite states raise ValueError.

The independent whole-horizon oracle uses a rational finite geometric sum of the method amplification. With h=T/n and z=r*h, Euler has R=1+z and forcing multiplier h; RK4 has R=1+z+z²/2+z³/6+z⁴/24 and forcing multiplier h*(1+z/2+z²/6+z³/24). It sums powers of R for all forcing contributions, rather than reusing the state loop. The allowance is 4*n ulps of the final reference to accommodate per-state rounding. This is a reference for the method, not the exact ODE solution.

Thirty cases include 18 helper cases, six invalid controls and six actual assessment values at 10/20/40 steps. Error fields must equal the absolute difference from the report's exact-growth field. The baseline exit 1 retained nine failed cases; the corrected exit 0 passed all 30. Six observed shared-method calls additionally verify that assessment consumes injected Euler/RK4 values and computes its error fields from them. Both injected helpers are restored. All 40 chapter files compiled and 30 scripts passed, with matching before/after hashes.

Changing arithmetic order to the complete affine increment can change final rounding. This does not certify generic callback solvers, arbitrary coefficients, global ODE error or model suitability. Required representability applies at every method state; a formal whole-horizon result cannot authorize crossing an unrepresentable intermediate state.

[Raw initial failures, reruns and scoped manifests](chapter-19-cumulative-step-range-followup.json) · [Runnable checker](../chapter-19/code/check_cumulative_step_range.py)

Replay: use a clean repository checkout at the corrected revision, change to Book 02's chapter-19/code, and run `python check_cumulative_step_range.py` with assertions enabled. To reproduce the initial failures, retain that checker outside the checkout, select the stated baseline revision, overlay only the checker, then run it there. Record stdout, stderr and exit separately. For the chapter scope, compile every chapter-19/code/*.py using py_compile.compile(path,doraise=True), then execute every check_/test_ basename in its parent directory with a fresh Python process and a 60-second timeout. Verify the raw manifest Git blob hashes before and afterward. The expanded scope contains existing checkers, not only the new file.

Selected assistant-derived references and Python 3.12.14/Linux checks only. No independent reviewer sign-off, supported-platform validation, release acceptance, canonical approval, arbitrary-range accuracy or real financial model validation is established. COV categories remain partial.
