# Chapter 20 — Error magnitude range follow-up

**Date:** 2026-10-29
**Scope:** Section 20.5 error-reporting portion of COV-87.
**Status:** Confirmed range-reporting defect corrected; scoped runtime passed; independent review pending.

## Reproducer and contract

Before the change, errors(1e308,-1e308) returned (inf,inf), and errors(1,5e-324) returned (1.0,inf), although inputs passed finite validation. The helper now raises OverflowError with distinct absolute-error or relative-error messages when a computed magnitude is nonfinite.

The interface still returns (absolute, relative), with None for relative error against zero. Ordinary floating-point rounding/underflow remains possible; no high-precision magnitude API is promised. The manuscript now explains the numerical-range contract.

The separate close_to_reference function retains its exact Fraction comparison for represented binary floats. Its Boolean decision does not require converting the difference/threshold to a float, so it can still compare opposite-signed huge inputs whose absolute error cannot be returned by errors.

## Regression evidence

Six new unittest methods cover absolute-error overflow in both sign orders; relative overflow for positive and negative subnormal references; largest-float/zero/equal and subnormal finite cases; negative reference scaling; invalid/nonfinite/bool inputs; and continued exact-comparison behavior independently of error-report range.

The boundary expectations use exact powers/ratios and float.fromhex for the largest finite value. Section 20.5 now passes 20 unittest methods. These cases do not establish every duplicated validation contract, correctly rounded error reporting or all magnitude transitions.

## Runtime and publication

Baseline tree: `283df59f1f70e4d8b373f502607700baaae82b8c`. All 19 Chapter 20 Python sources were fetched at that revision; the local snapshot replaced only the Section 20.5 implementation and checker. Python 3.12.14/Linux: 19/19 files compiled with py_compile and 10/10 check scripts exited zero, with assertions enabled, code-directory working directories and a 15-second per-script timeout.

| File | Commit | Blob |
|---|---|---|
| [section_20_05.py](../chapter-20/code/section_20_05.py) | `5371e4b84a36df6734f548f277755790209cca61` | `72360096700472a2824305b3c87d2355d0ac5171` |
| [check_section_20_05.py](../chapter-20/code/check_section_20_05.py) | `2316470c3e5e26bac6e51661ee1a5c2ca0a1aa4c` | `fad230c0d373d7cd09571863067f553f195c255d` |
| [20.05-floating-point-tolerances.md](../chapter-20/20.05-floating-point-tolerances.md) | `61229d17e96658d2bd9804e30be9513eebf33f92` | `1b797e4672c206261f29fde14afee5f8e119f71d` |

This change follows the latest full-book refresh and has scoped runtime evidence only. COV-87 remains partially open for other duplicated numeric contracts, range cases and independent review.

[Chapter 20 map](coverage-chapter-20.md) · [Gap register](gap-remediation-register.md) · [Tracker](PROGRESS.md).
