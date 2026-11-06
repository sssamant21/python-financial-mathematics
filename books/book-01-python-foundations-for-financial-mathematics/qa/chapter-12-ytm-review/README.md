# Section 12.6 — Yield to Maturity review

Baseline: `3592c4f94b1b63b476c7af2f75c550111ae7bd37`. [Runner](review.py) · [Initial results](initial-results.json) · [Corrected results](results.json) · [Worked answers and project](ANSWERS.md).

The runner extracts the sole Python fence verbatim and executes the documented demo, all 12 existing test methods and compilation. Both commands passed on both versions in the recorded Linux CPython runtime. Fourteen of 35 supplemental predicates failed at baseline; all 35 passed after correction. This is one workflow, 18 local answers and one separately scoped mini-project. No historical unique methods were added.

An independent high-precision Newton iteration evaluates the individual discounted flows and their derivative for the five market prices. A separate rational sum checks repricing, the 4.75% round trip and negative yields. The exact demo prints only three prices; the runner invokes the listing at all five and checks current yield and monotonicity. One-payment and par identities independently check range boundaries.

F83: the old price residual had an absolute floor, the positive bracket stopped at an arbitrary ceiling, and the solver could return an unchecked root. Tolerance and current-yield inputs also lacked checks. The new solver bisects the positive discount factor with a maturity-flow upper bound, resolves the bracket, and checks the returned yield's relative repricing residual. F54 recurred in intermediate range loss and unrepresentable outputs.

The listing is standalone Python 3.9+ and standard library only, with decimal-text model inputs and float results. This is an equal-period promised-cash-flow model for teaching-sized terms. It does not validate settlement conventions, issuer performance, reinvestment outcomes or independent acceptance. F28 and F32 remain open.

```bash
python3 -B books/book-01-python-foundations-for-financial-mathematics/qa/chapter-12-ytm-review/review.py
```

Next: 12.7 — Yield and Price Relationships.
