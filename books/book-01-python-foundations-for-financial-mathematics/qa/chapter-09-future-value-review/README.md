# Section 9.6 — Future value lab and answer review

Baseline `ca167e595204cc0b37162d09fe46fe1f657fcc05`. [Runner](review.py) · [Initial failure](initial-results.json) · [Corrected results](results.json) · [Five answers](ANSWERS.md).

One new workflow and five local answers reviewed. Two documented commands, fifteen additional predicates and eight existing embedded methods passed after the F46 follow-up correction. The full listing is extracted verbatim, executed as future_value.py and compiled in an isolated directory. Prepared Linux CPython 3.12.14; standard library only. No prior lab imports, external market data or network. Windows substitution and fresh installation were not executed.

The same nonzero-to-zero scalar-conversion flaw found in9.1/9.3/9.4/9.5 was reproduced in9.6 with Fraction(1,2**2000). Initial failure retained; the helper now rejects lost nonzero inputs and an assertion was added within its existing first method. F46 is extended to this section; no new historical method is claimed. Use this runner at the same relative evidence path in a worktree of the baseline to reproduce the original failure.

Independent rational powers verify the worked amount/growth, all numerical practice answers, common-target comparison, elapsed-term difference and signs. The target label is not used as an exponent: start2 to target5 is three periods. Practice5 is a conceptual requirements review; the function does not infer dates, rate units or reinvestment terms. Tables require no image. Subnormal precision, extreme rearrangement, contractual rounding, fractional periods and real rate selection remain outside scope. F28/F32, platform/notebook and independent acceptance remain open.

```bash
python3 -B books/book-01-python-foundations-for-financial-mathematics/qa/chapter-09-future-value-review/review.py
```

Next: Section9.7 formal lab and local answers.
