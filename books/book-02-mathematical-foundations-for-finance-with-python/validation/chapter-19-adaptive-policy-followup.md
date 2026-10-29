# Chapter 19 — Adaptive RK4 policy follow-up

**Date:** 2026-10-29
**Scope:** Section 19.6 portion of COV-82.
**Status:** Selected stage, rejection and controller checks passed; solver unchanged; independent review pending.

## Reference method

For \(y'=y\), an RK4 step of length \(h\) multiplies the state by the stability polynomial

\[
R(h)=1+h+\frac{h^2}{2}+\frac{h^3}{6}+\frac{h^4}{24}.
\]

The checker evaluates this polynomial with Fraction arithmetic, independently of the solver's stage helper. Starting at one with a unit trial step, the full result is \(R(1)=65/24\) and the two-half-step result is \(R(1/2)^2=(211/128)^2\). Their difference divided by 15 determines the expected estimator.

The reference also predicts a retry length from \(0.9(\mathrm{scale}/\mathrm{error})^{1/5}\), and predicts the accepted state from the polynomial at that retry length. Selected callback arguments expose actual stage times/states without adding trace instrumentation to the solver.

## What is asserted

- The first full step's four time/state callback arguments.
- A tolerance case that accepts only when scale uses max(abs(old),abs(two-half)), rather than abs(old) alone.
- Acceptance of the two-half-step value, rather than the full-step value.
- A forced rejected attempt: zero accepted steps, one rejected step, 12 evaluations, unchanged time/state.
- Rejection followed by a retry from the same time/state, with the independently expected retry length and accepted state.
- Lower step-factor clipping at 0.2 and upper clipping at 5 for nonzero error.
- Rejection followed by step_too_small, preserving the old state/time.
- An exactly zero RHS, ensuring the estimator is exactly zero: fivefold step growth, final-horizon clipping and unchanged state.

The initial constant nonzero-RHS experiment could have a tiny rounding discrepancy between full and half paths. It was replaced with an exact-zero RHS to discriminate the dedicated zero-error branch reliably.

## Discrimination experiments

Temporary in-memory solver variants were rejected for all nine intentional errors: divisor 16 instead of 15; old-state-only scale; accepting the full step; advancing time after rejection; changing state after rejection; exponent 1/4 instead of 1/5; lower clip 0.3; upper clip 4; and zero-error growth factor 4. No mutation or solver change was published.

These tests inspect selected local controller behavior. They do not establish a global error bound, correctness for arbitrary ODEs, stiffness handling, extreme floating-point range or all failure modes.

## Runtime and publication

Baseline tree: `ad21fb037bae4cc40d334c493704c99232b8e7c8`. All 21 Chapter 19 Python files were fetched at that revision. Only the Section 19.6 checker was replaced locally.

Python 3.12.14/Linux: 21/21 sources compiled and 11/11 check scripts exited zero, from their code directory with assertions enabled and a 15-second per-script timeout. After refining the zero-error case, that checker was recompiled and rerun successfully; the other unchanged scripts retain the same scoped pass.

Published checker commit: `bef990e0fec55bcd760848c5552e42a2bd8eb97e`; blob: `45e9eb2d28ba1f7874714ec9b116b7a89271fdd8`. The solver remains at blob `8a9bac4c4b973db41c0274e0f7ada06ec131d71a`.

COV-82 is partially addressed for these selected cases; broader adaptive integration, range and independent mathematical/editorial review remain open. The historical full-book run is unchanged.

[Checker](../chapter-19/code/check_section_19_06.py) · [Chapter 19 map](coverage-chapter-19.md) · [Queue](substantive-coverage-index.md) · [Tracker](PROGRESS.md).
