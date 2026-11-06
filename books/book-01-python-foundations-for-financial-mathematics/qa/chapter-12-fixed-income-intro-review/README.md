# Section 12.1 — Introduction to fixed income review

Baseline `89c8370b1aa1eb2a4519c4eb9a441dc58b8c4154`. [Runner](review.py) · [Initial results](initial-results.json) · [Corrected results](results.json) · [Answer and project mapping](ANSWERS.md).

The runner extracts the sole Python fence verbatim, runs the documented demo and 12 existing methods, then compiles the same file in isolation. Both commands passed at baseline and after correction on Linux CPython 3.12.14. Nine of 26 supplemental predicates initially failed; all 26 passed after correction. This is one workflow, 16 local answer records and one separately tracked mini-project; no historical unique methods were added.

The benchmark directly discounts the six exact promised payments. The source uses a geometric annuity factor. Source calls cover the complete five-yield project, cash-flow count, periodic conversion, zero coupon and zero yield. The demo itself prints only the 3%, 5% and 7% examples. This distinction is recorded in the answer review.

F78: a tolerance accepted fractional decimal period counts, including a count rounded to zero, and classified materially discounted small-face bonds or distinct near-par values as par. The count now requires an exact positive integer under the decimal-text convention, and classification compares exact model values before float reporting. F54 recurred in intermediary float overflow, discount-factor underflow and nonrepresentable outputs. The source uses rational pricing and rejects unsupported result ranges.

Python 3.9+ and the standard library are specified; no prerequisite file is needed. Negative yields, default probability, day count, settlement, credit, liquidity, callable bonds and other instruments are outside this executed model. Conceptual risk and perspective questions were reviewed separately. F28, F32 and independent acceptance remain open.

```bash
python3 -B books/book-01-python-foundations-for-financial-mathematics/qa/chapter-12-fixed-income-intro-review/review.py
```

Next: 12.2 — Bond Cash Flows.
