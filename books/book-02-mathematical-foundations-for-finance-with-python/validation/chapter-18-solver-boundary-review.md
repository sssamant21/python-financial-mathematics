# Book 02 — Chapter 18 Solver Boundary Review

**Date:** 2026-10-27  
**Scope:** Selected bisection and safeguarded Newton boundaries; not comprehensive numerical or independent mathematical review.

The tested local Chapter 18 code matched tree `96bebc11db9ea6bfa28097d4c33cd410a3314a98` except for six modified files and a new regression script. The code changes were published through `94a02f84458d2d5b8c6bf439cc7f68875c571e89`.

## Findings and fixes

1. Finite bracket endpoints can have a difference too large for a float. Five educational solvers now report OverflowError when the initial non-root bracket width is not representable. The four solvers with relative tolerances also reject an unrepresentable initial tolerance expression. This explicitly limits their domain; it is not a general arbitrary-range bisection solution.
2. Section 18.10 multiplied endpoint values to check signs, which can underflow to zero for nonzero opposite-sign values. It now compares signs directly.
3. Section 18.4 evaluated the derivative at an exact midpoint root. It now returns the exact root before evaluating the derivative. The existing non-finite derivative check was moved to a non-root midpoint to preserve its purpose.
4. A new `check_solver_boundaries.py` exercises wide brackets, tiny opposite signs, an exact root with an unavailable derivative, and an overflowing tolerance.

## Runtime evidence

On Python 3.12.14/Linux, the ten Section 18.1–18.10 check scripts and the new solver-boundary script all exited zero from the chapter code directory, each with a 15-second timeout. This is not a full book-wide rerun or cross-platform certification.

## Remaining work

- Independently review solver semantics, stopping criteria, accuracy and event handling, including endpoint roots and stagnation.
- Assess numerical range in interpolation, integration and derivative calculations, and whether explicit rejection or stable scaling is appropriate.
- Review test quality and manuscript examples beyond the selected cases; verify the final exact revision and supported environments.
