# Book 02 — Section 18.9 project evaluation-error contract

**Date:** 2026-10-30  
**Baseline:** `8cbba0741fd27713b7cf67b2c5d97c558a1b6e04`  
**Pinned executable source:** `0939286f031fc23b7b86f25b2f6dc80cb0bda807`  
**Disposition:** Selected COV-81 contract evidence; solver unchanged; independent review pending.

The manuscript correctly distinguishes nonfinite derivative errors from zero-derivative fallback, but the earlier project suite did not directly assert this rejection. The [new runnable checker](../chapter-18/code/check_project_errors.py) supplies direct error-path and callback-order evidence. Its first run passed against the unchanged solver; no solver defect or correction was demonstrated.

Nine invalid relative-tolerance/iteration controls reject before any callback. Five nonfinite/non-numeric derivative values reject after the independently expected objective endpoint/current-point sequence, without fallback. Fifteen objective-error cases cover each of five evaluation positions, including the terminal midpoint reevaluation, for NaN, infinity and Boolean returns.

Three early-stop paths never call an unneeded invalid derivative. Two affine cases with supplied zero or smallest-positive derivative reach the exact root3/8 through proposals1/2,1/4,3/8, with exactly8 objective and3 derivative calls. The tiny supplied slope makes the Newton proposal nonfinite and correctly triggers bisection; this does not certify that the supplied slope is the mathematical derivative.

Two user callback exceptions propagate unchanged. The endpoint contract is eager: both initial endpoint evaluations occur before an endpoint root is returned; a nonfinite upper evaluation is still rejected when the lower value is zero. No partial diagnostic result is returned for these exceptions. Two wrong policies (swallowing evaluation errors and coercing iteration budgets) are detected.

[Machine evidence](chapter-18-project-errors-followup.json) retains expected exception classes/messages, actual callback events, the initial passing checker run, exact manifest and scoped outputs. All27 Chapter18 sources compiled and17 scripts passed on Python3.12.14/Linux, assertions enabled, separate processes, timeout15 seconds. All27 source hashes match the pinned Git tree and remained unchanged after execution. Section18.9 solver blob `522d815f22e4a11189be78f924e78c031f60eb74`.

This one-checker addition follows [V-49](runtime-refresh-2026-10-30-r13.md), the earlier full487-file/276-script/488-required-hash run. Current pinned inventory is488 Python files/277 check-test scripts, not a new full execution. COV-81 is newly partially addressed, bringing selected partial categories to30; none closed by the register. Gap categories are not defect counts or completion percentages. Continuity/uniqueness, broad financial/error/scale cases, independent review, supported platforms and release acceptance remain open.

Next substantive item: COV-81 Section18.10 actual safeguarded-Newton versus bisection comparison and all three interpolation-convention outputs, currently absent from the final report. Integrate actual Section18.9/18.6 helpers with independent references and injected wrong-output checks; preserve broader applied-study obligations.
