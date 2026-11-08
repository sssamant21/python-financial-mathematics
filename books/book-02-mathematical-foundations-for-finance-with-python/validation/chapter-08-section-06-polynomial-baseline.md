# Section 8.6 polynomial range — retained initial screen

Pinned executable revision: `a02160a18fcb320ffb537ea5b5cf7bce8e64a3d3`. [Nine actual observations with exact source blob](chapter-08-section-06-polynomial-baseline.json) · [Runnable probe](chapter-08-section-06-polynomial-probe.txt).

```bash
python books/book-02-mathematical-foundations-for-finance-with-python/validation/chapter-08-section-06-polynomial-probe.txt .
```

Independent rational monomial sums use each represented binary64 coefficient and argument exactly, rounding only the final expectation. Falling-factorial coefficients derive derivatives directly instead of repeating the implementation's derivative loop. Four mismatches are retained, not four distinct defects: recoverable Horner intermediate overflow (exact rounded answer1e308), subnormal final rounding (exact rounded answer1e-323), and two nonfinite outputs where ValueError is a proposed final-output policy. Constant/ordinary/exact-zero and derivative-order controls remain distinct from failures. No fixes or corrected passes are claimed.

Next: reconcile complete-expression versus ordinary-Horner rounding guarantees, final finite/underflow/zero/error semantics and validation order before implementing corrections. Preserve one-shot coefficient consumption, nonempty/finite input checks, order0, order above degree and bool rejection; derive meaningful additional guards without an unbounded order loop. Then assess sampled-second differences separately. This screen is not the completed polynomial contract review, a new full runtime, a defect total or COV closure. Thirty-five selected categories remain partially addressed; reviewer/platform/resource/release/canonical limits remain open.
