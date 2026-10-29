# Chapter 20 — Metamorphic PV numeric-contract follow-up

**Date:** 2026-10-28 (America/New_York)
**Scope:** Section 20.6 portion of COV-87.
**Status:** Selected input/output contract gaps addressed; scoped runtime passed; independent review pending.

## Contract and changes

The PV helper previously used math.isfinite directly, accepting booleans as numbers, and returned amount*exp(-rate*years) without checking result finiteness. It now validates finite real numeric inputs excluding booleans, converts them to floats and retains the nonnegative-time restriction.

Wrong numeric types raise TypeError. Nonfinite inputs or values that cannot convert to finite floats raise ValueError. A nonfinite discount exponent, exponential overflow or nonfinite PV result raises OverflowError. Rejecting a nonfinite exponent is an explicitly stated range policy, including the positive-rate case where exp(-inf) previously returned zero. Ordinary underflow from a finite exponent is still allowed and documented.

Portfolio valuation now validates rate before consuming flows, including an empty portfolio. Valid empty portfolios return zero; invalid rates are no longer silently ignored. Generator cash flows remain supported. No new all-range summation guarantee is introduced: math.fsum can raise on intermediate overflow.

## Added cases

Seven new unittest methods cover boolean inputs at all three coordinates; strings/None/complex and out-of-range integers; NaN/infinities at every coordinate; exponential/product/exponent overflow; documented underflow and zero amount; empty portfolio rate validation; generator inputs and portfolio summation overflow.

The original nonzero analytical benchmark and twenty bounded generated scaling cases remain. Passing metamorphic checks alone still cannot establish valuation correctness or a universal numerical property.

## Runtime and publication

Baseline tree: `105b19bb3fc790ad6e02367a35ef325210cf3b09`. All 19 Chapter 20 Python files were fetched at that revision; the local snapshot replaced only the Section 20.6 implementation and checker. Python 3.12.14/Linux: 19/19 files compiled and 10/10 check scripts exited zero, with assertions enabled, own-directory working directories and a 15-second per-script timeout. Section 20.6 passed 19 unittest methods.

| File | Commit | Blob |
|---|---|---|
| [section_20_06.py](../chapter-20/code/section_20_06.py) | `4ac9d9dcee0c9c510a855a1da111e7d0f99d5aaf` | `c4b41dae13b6899a4dc53408d508f66ea9f4659d` |
| [check_section_20_06.py](../chapter-20/code/check_section_20_06.py) | `16115720ea4a5f476cddc3aeb8469e19660f1b48` | `5cc023867be43734ffd938fe139c39a0f34edef1` |
| [20.06-property-and-metamorphic-checks.md](../chapter-20/20.06-property-and-metamorphic-checks.md) | `7db66564bb1e681686a5a4b65e8b79cb26e46ddb` | `806b00891d3cd07e161161022e92c992772477da` |

This scoped change follows the latest full-book refresh. COV-87 remains partially open for other duplicated contracts/ranges, underflow interpretation and independent mathematical/editorial review.

[Error-range follow-up](chapter-20-error-range-followup.md) · [Chapter 20 map](coverage-chapter-20.md) · [Gap register](gap-remediation-register.md) · [Tracker](PROGRESS.md).
