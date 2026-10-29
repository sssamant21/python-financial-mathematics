# Chapter 10 — Quadrature order and estimator follow-up

**Date:** 2026-10-29 (America/New_York)
**Scope:** Section 10.7 portion of COV-55.
**Status:** Selected convergence/estimator oracles passed; quadrature algorithm unchanged; independent review pending.

For the signed error estimate-minus-integral on [0,1], the checker uses exact composite identities: midpoint on x^2 gives -1/(12n^2), trapezoid on x^2 gives 1/(6n^2), and Simpson on x^4 gives 2/(15n^4). At n=2,4,8,16, these independently check signed errors, coarse/fine ratios and the fine-error estimator. Error identities and ratios use 1e-8 relative tolerance, with 1e-15 absolute tolerance for signed errors.

The checker also verifies reversed bounds and missing estimator fields for nondoubled consecutive grids [2,6,12]. For exp(x), the independent integral is exp(1)-1; ratios and estimator/actual-error agreement are checked within one percent at n=8,16,32,64. This is selected smooth-integrand evidence, not a general convergence proof.

Temporary in-memory variants with Simpson order two, estimator denominator 2^p instead of 2^p-1, and an estimator emitted for any increasing grid were all detected. No mutant or algorithm change was published.

Baseline tree: `e0f9cfdd30ce42f576fee3760fc86254be2bbdb7`. All 21 Chapter 10 Python files were fetched at that revision; only the Section 10.7 checker was replaced locally. Python 3.12.14/Linux: 21/21 files compiled and 11/11 check scripts exited zero with assertions enabled, own-directory working directories and a 15-second per-script timeout.

Published [checker](../chapter-10/code/check_section_10_07.py): commit `03d81547ea7e14b3b9180b43bf5c3008e078b265`; blob `c2314c8778361620f1e742e908d598f877ea60d3`. The quadrature source remains at blob `330346a51bfd5a5d5ae5c0395b8b74e15091a55b`.

COV-55 remains partially open for other report/error obligations and independent review. These cases do not turn the financial integrand's high-resolution shared-rule reference into an independent analytical oracle, nor establish arbitrary integrand regularity, floating-point range or universal error bounds. This scoped change follows the latest full-book run.

[Chapter 10 map](coverage-chapter-10.md) · [Gap register](gap-remediation-register.md) · [Tracker](PROGRESS.md).
