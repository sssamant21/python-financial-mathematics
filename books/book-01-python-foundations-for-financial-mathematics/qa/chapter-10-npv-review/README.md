# Section 10.12 — NPV review

Baseline `503edbdc3e622f98acabea861a53ac1581b9132f`. [Runner](review.py) · [Initial results](initial-results.json) · [Corrected results](results.json) · [Twelve answers](ANSWERS.md).

The two documented commands and twelve existing methods passed on both versions. Eight of 35 additional predicates initially failed; all 35 now pass. The runner extracts the sole Python fence verbatim, saves it as net_present_value.py, runs the demonstration and tests, then compiles it in isolation. Prepared Linux CPython 3.12.14, standard library only. No previous module, data files, installation or network access are needed. The demonstration prints 4.13.

F54: discount factor and nonzero payment underflow silently returned zero; PI overflow and underflow produced infinity and zero. F56: zero amounts triggered needless overflowing factors or powers in NPV and component reporting. Both now use the same checked terms, retaining periods for zero amounts. F59: PI discarded a nonfinite initial cost before validation, returning zero or NaN. The complete input is now validated before separating receipts. The eight regression cases are in an existing method; no historical unique methods were added. Run the same review against baseline source to reproduce initial failures.

Independent Fraction sums check NPV, components, PI, signs and rate sensitivity. The time-zero cost is the first element; later elements are one period apart, including explicit zero placeholders. The worked NPV is 500/121, rounded after summation. Decision, capital-rationing and dated-convention questions are conceptual, not recommendations or additional source workflows. No model inputs from real projects, dated NPV, fresh installation, notebook or platform acceptance were tested. Bounded float factors and extreme cancellation remain range limitations. F28, F32 and independent acceptance remain open.

```bash
python3 -B books/book-01-python-foundations-for-financial-mathematics/qa/chapter-10-npv-review/review.py
```

Next: Section 10.13.
