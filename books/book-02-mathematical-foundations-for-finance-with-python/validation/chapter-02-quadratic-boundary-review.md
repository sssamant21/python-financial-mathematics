# Book 02 — Chapter 2 Quadratic Boundary Review

**Date:** 2026-10-28  
**Status:** Focused source review and runtime follow-up passed; independent review pending.

## Scope and revision

Reviewed the nine Chapter 2 implementation modules, focusing on equation classification, domain exclusions, interval endpoints and approximate roots. Runtime used the 19 chapter Python files at `c6fab5c672bcc9b821667e815dde03e3e9bd22a2`, plus the modified Section 2.5 implementation and the new cancellation regression. Code and regression published through `aead22cb3d11b6dd7558374abbc119f45b1dfad7`.

## Reproduced finding and correction

For x² + 10^50 x + 1 = 0, the previous 40-digit Decimal center-minus/plus-spread evaluation returned a zero small root. Its true magnitude is approximately 10^-50. Precision lost in subtracting nearly equal values cannot be restored by Decimal representation alone.

The irrational-root branch now chooses the root with reinforcing center and spread signs, then recovers the other using the exact rational product c/a converted to Decimal. Results remain sorted; exact rational roots, repeated-root and no-real-root branches retain their classifications. The manuscript now explains this evaluation choice.

## Evidence

Python 3.12.14 on Linux. All 20 Python files compiled using `py_compile.compile(path, doraise=True)`. All 11 `check*.py` scripts exited zero when invoked individually from the code directory, with captured output and a 15-second timeout per script.

The new [regression](../chapter-02/code/check_quadratic_cancellation.py) contains two unittest methods: eight separated-root sign combinations checked against 160-digit direct-formula references, with relative root error and normalized polynomial residual at most 10^-38; plus symmetric-root and exact classification checks. The separated-root cases passed. An initial symmetry assertion used context-rounded unary negation outside the function; it was corrected to an explicit absolute tolerance before the successful full rerun.

## Remaining work

This is scoped numerical evidence, not independent mathematical review or exhaustive manuscript validation. Review Decimal exponent limits, very large rational conversion, root accuracy near repeated roots, the Section 2.4 endpoint-ratio supported range, and exercise solutions. Final-revision and supported-platform runs remain pending. The chapter is not certified.
