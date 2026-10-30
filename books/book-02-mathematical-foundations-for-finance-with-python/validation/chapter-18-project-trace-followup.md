# Book 02 — Section 18.9 project trace audit follow-up

**Date:** 2026-10-30  
**Baseline:** `f0be6d824860db421ae25fb03ba2a7b5c7229843`  
**Pinned executable source:** `f431e9daabc74a3cb25b254a2c219573f1267144`  
**Disposition:** Selected COV-79 diagnostics checked; solver unchanged; independent review pending.

The earlier map identified absent independent project-trace evidence beyond lengths/final containment. The [new runnable checker](../chapter-18/code/check_project_trace.py) observes actual objective/derivative calls and independently audits every selected trace row. Its first run passed against the unchanged helper; no numerical defect or correction was demonstrated. This does not repeat Section18.8's separate bracket-audit change.

Ten cases cover safeguarded Newton, zero-derivative fallback, an interior exact proposal, exact lower/upper quarter proposals, an exact initial midpoint, an endpoint root, initially sufficient width, iteration exhaustion and adjacent-float stagnation. Callbacks evaluate exact rational polynomial expressions before final rounding. This separates solver update logic from avoidable polynomial-evaluation cancellation; it does not assess arbitrary financial callback accuracy.

For87 trace rows, the audit recomputes endpoint signs, the separately rounded quotient/subtraction proposal, strict middle-half test, raw residual, update and remaining sign bracket. It checks all200 objective calls and87 derivative calls against observed event logs, including termination-only evaluations. Final residuals are independently reevaluated. Exact-quarter proposals correctly fall back; initial-midpoint and endpoint roots do not require derivative calls. Two quadratic paths additionally use100-digit Decimal sqrt2 to check containment and midpoint half-width error. The adjacent-float case has a continuous affine root strictly between representable endpoints.

Five wrong reports are rejected: changed endpoint, out-of-contract proposal, function count, root residual and step kind. Strict JSON output is retained. [Machine record](chapter-18-project-trace-followup.json) contains the initial passing run, exact source manifest, environment, commands, full event logs, outputs and scoped rerun.

All22 Chapter18 sources compiled and12 check/test scripts passed on Python3.12.14/Linux, assertions enabled, timeout15 seconds, separate processes in the chapter-code directory. All22 source blob hashes match the pinned Git tree and remained unchanged after execution. Helper blob `522d815f22e4a11189be78f924e78c031f60eb74`; checker blob `ee951d81ec31bd3b1d04b61245ba4cf9e79a806e`.

This one-checker addition follows [V-47](runtime-refresh-2026-10-30-r11.md):482 compiled/271 scripts/483 required input hashes at its prior pin. The new pinned inventory is483 Python files/272 check-test scripts, not a new full execution. Manuscript/report/tracker writes after this executable pin are outside source inputs.

Scope is ten pure selected callback cases. Sign brackets remain conditional on continuity; logging does not prove arbitrary callbacks continuous or roots unique. Extreme proposals/evaluation exceptions, every financial range case, project nonfinite-derivative behavior and broader final applied scope remain open. COV-79 remains partially addressed. Twenty-eight selected categories remain partially addressed; none closed by the register. Independent mathematics/editorial review, supported environments, release acceptance and canonical approval remain pending.

Next substantive item: COV-80 Section18.5 multiple-root scan/refinement contract: exact-grid repeated roots, deduplication threshold and nearby distinct-root separation, with independently derived polynomial references and explicit nonexhaustive flags. Preserve the existing recorded solver-boundary regressions.
