# Chapter 18 — Cent rounding across input and context ranges

Baseline: `5504f2cf019487dae61912e6b01bdb6440931307`. Corrected revision: `7b779924a288286a39a55a98f7383bdc4310989d`.

The original Section 18.1 cent formatter failed 18 of 32 observations across the default and a restricted caller context. Large finite amounts exceeded the default decimal precision, and a caller's settings could cause exceptions or alter its context flags. The formatter now uses a private half-even context with enough precision for 309 integer digits and two cent digits. Its policy remains rounding the float's shortest decimal text, preserving signed zero.

[Runnable checker](../chapter-18/code/check_money_cents_range.py) independently rounds exact rational cents with ties to even and checks both context isolation and the resulting text. All 30 amount cases and two caller-context checks passed. [Raw evidence](chapter-18-cents-range-followup.json) retains the initial failures, rerun and scope manifest. Run from chapter-18/code. All 41 Chapter 18 sources compiled and 31 scripts passed. This is scoped execution after [V-56](runtime-refresh-2026-11-04-r2.md); it does not replace the preceding full runtime evidence.
