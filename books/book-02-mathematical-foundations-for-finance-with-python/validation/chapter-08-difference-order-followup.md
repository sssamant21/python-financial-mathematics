# Chapter 8 — Second-difference order and cancellation follow-up

**Date:** 2026-10-29 (America/New_York)
**Scope:** Section 8.6 portion of COV-49.
**Status:** Selected exact-error and cancellation cases passed; algorithm unchanged; independent review pending.

The checker now verifies the centered second-difference identity D2(x^4)=12x^2+2h^2 at x=0,0.5,1,-1 and h=2^-1 through 2^-5. These dyadic cases use exact equality: halving h gives error ratio four. Negative-step symmetry and exact quadratic curvature two are checked on the same grid.

At x=0 for x^6, D2=2h^4, giving ratio sixteen. This special cancellation of lower-order truncation terms is not a claim that the stencil is generically fourth order.

For x^2 at x=1 and h=2^-40, the inputs x+h and x-h are distinct and h^2 is representable, but rounding causes the returned stencil numerator to cancel to zero. The checker explicitly compares this zero estimate with the independent true derivative two and an accurate larger-step result. It documents existing numerical behavior; no automatic accuracy rejection or precision guarantee is added.

Temporary in-memory variants with denominator h instead of h^2 and an incorrect center coefficient were both detected. No mutant or algorithm change was published.

Baseline tree: `9f792d034343fc946783af2036c2006a44e49235`. All 21 Chapter 8 Python files were fetched at that revision; the local snapshot replaced only the Section 8.6 checker. Python 3.12.14/Linux: 21/21 files compiled and 11/11 scripts exited zero with assertions enabled, own-directory working directories and a 15-second per-script timeout.

Published [checker](../chapter-08/code/check_section_8_06.py): commit `4bf78fe5e3b8a9a1bf7e3160434e8efd8e297eb4`; blob `5b46254c42da72e81f6a843692e7aa6168a5044c`. The implementation remains at blob `cb05d8a24ea6c4d47d9d2a7503f2420af6c2451b`.

COV-49 remains partially open for other derivative helpers, noise/wrong-reference cases, arbitrary functions/ranges and independent review. This scoped checker change follows the recorded full-book run.

[Chapter 8 map](coverage-chapter-08.md) · [Gap register](gap-remediation-register.md) · [Tracker](PROGRESS.md).
