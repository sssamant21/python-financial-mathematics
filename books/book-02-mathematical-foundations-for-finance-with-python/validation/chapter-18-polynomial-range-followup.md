# Chapter 18 — Complete polynomial interpolation range follow-up

**Date:** 2026-10-31  
**Executable revision:** `4d90b8d6a3fdd397c7d071582829d5384fa410ab`  
**Baseline:** `0c6adb3eee831bb109290c5c9e093a05cbdce19a`

Section 18.6 Lagrange evaluation could lose finite answers through overflow in knot differences, basis products, or cancellation between terms. The retained baseline regression fails even at a supplied knot. [Raw evidence](chapter-18-polynomial-range-followup.json) preserves four initial probes, the original failed regression, the first successful rerun, scoped outputs and source hashes.

The implementation now evaluates the complete rational polynomial of the represented finite inputs, then converts once to float. Exact zero is accepted; a nonzero result rounding to zero or a final overflow raises ValueError through the affine result guard. Increasing-knot validation and mathematical extrapolation behavior remain. This O(n²) rational evaluation serves small educational examples; it does not cure conditioning, data noise, high-degree oscillation or financial extrapolation risk.

[Runnable checker](../chapter-18/code/check_polynomial_range.py) uses independently known quadratic, cubic, quartic and constant formulas with 2500-digit Decimal references: 19 values including knot recovery, extreme scales, cancellation, subnormal knots and finite extrapolation. Two final-range and four invalid-input cases also pass. The oracle does not reproduce Lagrange's basis algorithm.

All **34 Chapter 18 Python files compiled and 24 check scripts passed** at the executable revision; scoped hashes match the tree and remain unchanged after execution. Run from chapter-18/code: `python check_polynomial_range.py` and `python check_linear_range.py`; the raw record lists every scoped command. [V-53](runtime-refresh-2026-10-31-r2.md) includes both fixes.

COV-80 remains partially addressed. This is assistant execution evidence on Python 3.12.14/Linux, not independent reviewer sign-off, supported-platform validation or release acceptance.
