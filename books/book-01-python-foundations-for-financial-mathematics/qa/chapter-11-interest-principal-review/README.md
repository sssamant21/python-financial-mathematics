# Section 11.5 — Interest and principal components review

Baseline `1665971077c73345080350fcca1352e70d4d0b28`. [Runner](review.py) · [Initial results](initial-results.json) · [Corrected results](results.json) · [Twelve answers](ANSWERS.md).

Both documented commands and twelve existing methods passed on each source version. Nine of 40 additional predicates initially failed; all 40 pass after correction. The runner saves the sole Python fence verbatim as interest_principal_components.py, executes the demonstration and tests, and compiles it in isolation on prepared Linux CPython 3.12.14. No earlier module, external package, data or network is required.

F68: three displayed cells in two rows of the worked table disagreed with the unrounded model and exact console output. F54: tiny or out-of-range amounts were silently lost or produced nonfinite results, and overflowing summary totals escaped as raw summation errors. F66: subtracting nearly equal interest and payment erased a positive principal portion and could leave a false closing balance. The corrected source uses the same prospective factor and direct principal identities as 11.3, with its original standalone dictionary interface. Unsupported values and totals now raise a range error. Seven regression cases are inside an existing method; no historical unique methods were added. Running this runner on baseline reproduces the nine failures.

An independent Fraction annuity sum and retrospective recurrence benchmark all 24 unrounded rows, the rounded three-row demonstration and the printed table separately. The twelve prompt records distinguish exact source execution from the conceptual negative-amortization explanation. The first-balance prompt now names its opening balance. No negative-amortization product, cent-rounded servicing schedule, fresh installation, notebook or alternate platform was tested. F28, F32 and independent acceptance remain open.

```bash
python3 -B books/book-01-python-foundations-for-financial-mathematics/qa/chapter-11-interest-principal-review/review.py
```

Next: 11.6.
