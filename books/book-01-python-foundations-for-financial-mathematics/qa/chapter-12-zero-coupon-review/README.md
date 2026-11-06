# Section 12.4 — Zero-Coupon Bonds review

Baseline: `151f57aedd541dd1de9128b43fcb7614f8b5356d`. [Runner](review.py) · [Initial results](initial-results.json) · [Corrected results](results.json) · [Answers](ANSWERS.md).

The runner executes the single extracted Python fence verbatim and compiles it in isolation. Both documented commands and 12 existing test methods passed on both versions in the recorded Linux CPython environment. Eight of 39 additional predicates failed initially; all 39 passed after correction. Counts: one workflow, 18 local answers, one separate mini-project, no new historical unique methods.

The benchmark uses exact rational integer powers for the 16 project cases and high-precision symmetric finite differences for derivatives. It also checks rounded versus theoretical price inversion and independent one-payment ratio identities at both range extremes. The standalone demo prints one example; the runner calls the exact listing for the full matrix.

F54 recurred in intermediate discount underflow and unsupported output range. F81: implied yield could overflow or underflow the intermediate face-to-price ratio; sensitivity functions accepted booleans and could lose finite results through intermediate overflow. A local Decimal context now preserves the range until float reporting. Yields that round to the model's lower bound are explicitly rejected.

No files or dependencies outside Python's standard library are needed. Fractional maturities follow a model exponent, not an actual day-count convention. No bill quotation, settlement calendar, credit model, platform portability or independent acceptance was tested. F28 and F32 remain open.

```bash
python3 -B books/book-01-python-foundations-for-financial-mathematics/qa/chapter-12-zero-coupon-review/review.py
```

Next: 12.5.
