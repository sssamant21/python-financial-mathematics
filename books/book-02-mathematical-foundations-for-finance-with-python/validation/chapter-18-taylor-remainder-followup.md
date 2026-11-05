# Chapter 18 — Taylor remainder reference checks

**Date:** 2026-11-04  
**Scoped executable revision:** `9c77e189563fd2fc7bbcee7b43d2ee0c8a82b191`

[Runnable checker](../chapter-18/code/check_taylor_remainder.py) evaluates 11 actual Section 18.1 reports. For positive x, the omitted terms after x²/2 have successive ratios at most x/3, giving an upper bound of (x²/2)/(1−x/3). For negative x in the selected range, alternating terms bound the remainder between x²/2−|x|³/6 and x²/2. The checker compares 120-digit Decimal references and the observed errors with explicit allowances for rounding the exponential and the linear approximation.

At x=±2⁻⁴⁰ the report's rounded subtraction is zero even though the mathematical remainder is positive. The manuscript distinguishes these quantities. The first audit passed; no numerical helper changed. All 39 Chapter 18 files compiled and 29 scripts passed. [Raw scoped evidence](chapter-18-taylor-remainder-followup.json) lists source hashes, results and script exits. Run the checker from chapter-18/code. This is selected evidence, not a universal rounding bound or independent review. V-55 remains the preceding full runtime pass.
