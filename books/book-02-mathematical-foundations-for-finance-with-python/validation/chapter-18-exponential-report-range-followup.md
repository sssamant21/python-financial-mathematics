# Section 18.1 — Exponential report range

Baseline: `505aa5aedb4cad6c20fdc69f6e6bb9d36f71dfc3`. Corrected executable revision: `46aa9c5a32f9a3293bcd7926efa4c04c984a3258`.

The initial run failed eight of 44 checks. The approximation report now rejects a positive exponential reference that rounds to zero, rather than treating the reference as zero and returning an undefined relative error. Exponential overflow raises ValueError. The cancellation report still deliberately shows direct subtraction rounding to zero near the origin; a change rounding to −1 is valid when the underlying exponential is tiny.

[Runnable checker](../chapter-18/code/check_exponential_report_range.py) uses 900-digit Decimal exponentials and rational arithmetic on the reported operands. It checks selected subnormal changes, saturation, exponent and relative-error limits, and invalid inputs. All 44 checks passed. [Initial results and rerun](chapter-18-exponential-report-range-followup.json) retain outputs and exits. Run from chapter-18/code. These are selected checks, not universal rounding or platform guarantees.
