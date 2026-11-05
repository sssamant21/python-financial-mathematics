# Section 18.2 — Decimal-text cent rounding

Baseline: `1cdc4c891bd443dbbc5303d2f5715b26350da7bc`. Corrected executable revision: `3bb510f1715d9f734bc5e73ea19783e73f0ac4bf`.

The [checker](../chapter-18/code/check_decimal_text_cents.py) independently derives cents from exact rational decimal text and tests half-even ties, signed zero, malformed input, nonfinite values, and a carry beyond the output limit. The initial run failed 16 of 32 observations across default and restricted caller contexts. A private context now keeps the original default limit of 26 integer digits in the rounded output, leaves caller settings and flags unchanged, and reports invalid text or excess magnitude with ValueError.

All 32 observations passed on rerun. [Raw evidence](chapter-18-decimal-text-cents-followup.json) retains both runs and the exact Chapter 18 source manifest. Run the checker from chapter-18/code. The scoped run compiled 43 files and passed 33 scripts; [V-57](runtime-refresh-2026-11-04-r3.md) is the preceding full pass.
