# Section 12.15 — Forward Rates review

Baseline: `726d007a18647764a0e6c93b94807ea1583501d7`. [Runner](review.py) · [Initial results](initial-results.json) · [Corrected results](results.json) · [Answers](ANSWERS.md).

The runner executes and compiles the exact extracted Python listing. Both documented commands and all 12 existing methods passed on the baseline and corrected listing in the recorded Linux CPython runtime. Eight of 56 supplemental predicates failed initially; all 56 passed after correction. This is one workflow, 18 local answers, one separately scoped mini-project and no additions to historical unique methods.

The independent benchmark raises rational growth factors to the integer node maturities, then takes independent high-precision interval powers. It checks every base and +50-bp shifted row, all reconstructions, and equivalent continuous quotes. The source demo prints the four base rows; the shift and conversion are driven separately by the observer. A quarterly example checks nominal periodic conversion.

F92: time-zero factor normalization and validation of an explicitly supplied start quote were missing; tiny forwards vanished when calculated via rounded spot factors, and a rate could round to the excluded lower bound. F54 recurred in range loss from intermediate discounts or reconstructed prices. The source now uses checked log-growth calculations and reports the requested value after scaling.

The lab is standalone Python 3.9+ and standard library only. This is a supplied single-curve educational model; no calibration, contractual day count, market data, independent acceptance or additional platform was tested. F28 and F32 remain open.

```bash
python3 -B books/book-01-python-foundations-for-financial-mathematics/qa/chapter-12-forward-rates-review/review.py
```

Next: 12.16 — Bond Analytics Engine project.
