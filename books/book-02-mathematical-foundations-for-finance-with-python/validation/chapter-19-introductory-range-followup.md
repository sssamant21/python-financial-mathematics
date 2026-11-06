# Section 19.1 introductory range and report follow-up

[Baseline source](https://github.com/sssamant21/python-financial-mathematics/tree/b8d5590794bdf2b32c4979081ca2887bdaed4fdf/books/book-02-mathematical-foundations-for-finance-with-python/chapter-19/code) · [Corrected source](https://github.com/sssamant21/python-financial-mathematics/tree/b8d9ad694136393a36aca2c06d9c0798062cb21c/books/book-02-mathematical-foundations-for-finance-with-python/chapter-19/code) · [Initial probes](chapter-19-introductory-range-baseline.md) · [Raw results and exact source blobs](chapter-19-introductory-range-followup.json).

The 39 checks found 21 mismatches on the baseline; replay produced the same results. An intermediate rerun found one remaining signed-zero mismatch at zero horizon. The final rerun passed all 39 cases. The JSON retains expected and actual values, exception classes and messages, and exits. Its counts are observations, including multiple assertions on the same assessment fields.

The growth, constant-flow and Euler entry points now evaluate complete balances with the existing chapter kernels. A zero-horizon account preserves the initial value. Balance underflow may round to signed zero. Effective-rate conversion raises `ValueError` for overflow and when the result rounds to the inverse's excluded endpoint of −1. The nearest valid effective rate above −1 remains accepted. The actual assessment now reports the absolute error for each Euler grid.

The checker uses high-precision Decimal exponentials, logarithms and geometric balances, exact rational Euler widths and affine steps, and explicit tests for signed zero, invalid inputs and true overflow. It also checks that reported errors equal the differences of the displayed balances and that both review flags remain false.

Run from `chapter-19/code` at the corrected revision: `python check_introductory_range.py`. To replay the failure, invoke the same pinned checker with one argument: the baseline checkout's absolute `chapter-19/code` path. [Full Linux candidate run](runtime-refresh-2026-11-06-r10.md).

Selected COV-84 evidence only. No exhaustive rounding claim, independent reviewer sign-off, supported-platform validation, release acceptance or canonical approval.
