# Chapter 18 — Tiny discount-change accuracy references

**Date:** 2026-10-31  
**Checker revision:** `228a2ce79ca4d14cd4c6196238ba2e5a112ea8f5`  
**Unchanged implementation inspected at:** `148ea600804bd4c3ce69699862e6f2cd7eac7c61`

[Runnable checker](../chapter-18/code/check_discount_change_accuracy.py) evaluates59 represented-input cases using the independent1200-digit formula (1+r)^(-n)-1 in Decimal, rather than reproducing log1p/expm1. Cases include positive/negative rates from minimum subnormal through1e-12, zero rate, selected integer periods and fractional periods. Fractional periods describe the implemented analytic extension, not a discrete annuity payment convention.

The actual helper agrees with each reference within four ulps of its rounded float, with explicit sign and zero/nonzero checks. The naive binary expression (1+r)^(-n)-1 returns a false zero in46 cases. Three zero/sign/naive variants are rejected. This replaces a permissive absolute tolerance with a scale-sensitive benchmark; it does not establish correct rounding or all-range accuracy.

The initial oracle passed without an implementation correction. [Raw evidence](chapter-18-discount-change-followup.json) retains that first audit, current outputs, reference/error/allowance values, commands, environment and scoped source hashes. All37 Chapter18 files compiled and27 scripts passed; scoped hashes match the executable revision and remain unchanged after execution. Run `python check_discount_change_accuracy.py` from chapter-18/code. [V-54 full refresh](runtime-refresh-2026-10-31-r3.md) includes this checker plus the preceding Newton and bisection oracles.

Input/product/result range, annuity extreme scaling and broader stability/model reasoning remain separate open obligations. Thirty selected COV categories remain partially addressed; none closed by the register. Assistant candidate Linux execution is not independent review, supported-platform validation or release acceptance.
