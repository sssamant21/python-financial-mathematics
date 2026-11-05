# Section 10.8 — Perpetuities review

Baseline `b6af77a8ff3c9782d3981b761b1b3f5e83d80fa9`. [Runner](review.py) · [Initial results](initial-results.json) · [Corrected results](results.json) · [Twelve prompt records](ANSWERS.md).

Two documented commands and twelve existing methods passed on both source versions. Seven of 32 additional predicates initially failed; all 32 pass after correction. The exact sole Python listing was saved as perpetuities.py, executed with its PV demonstration and compiled in isolation. Filename, save/run/compile sequence and standalone imports hold under prepared Linux CPython 3.12.14. No earlier module, dependencies beyond the standard library, data files or network are required.

F54 recurred in a tiny-rate finite annuity, ordinary and finite PV underflow, and deferral factor and result underflow (five cases). Unit-factor-first evaluation prevents premature multiplication loss, and checked nonzero values now reject silent zero outputs. F56 recurred in due PV (ordinary payment rounded to zero before the time-zero contribution) and deferred PV (ordinary PV overflowed before discounting). The due branch uses a single monetary product at rates at least one and a quotient plus payment at smaller rates. Deferred valuation combines the unit discount and rate when representable, with a quotient-first fallback otherwise. Both repaired final values match independent rational benchmarks, and the tiny-rate finite deferred quotient remains supported. All seven regression assertions are inside an existing method; no historical unique methods were added. Reproduce the initial failures by running the same runner with baseline source.

Fraction sums independently value finite payments at counts 1, 20, 100 and 1000; first-term/ratio formulas check ordinary, due and deferred perpetuities. The exact remaining positive tail at n=1000 is less than 10^−16 in the fixture. Zero/negative rate rejections, signs, count/date conventions and genuine zeros are checked. Definition and convergence are conceptual reviews, while inverse arithmetic is supplemental and reconciled with source valuation: no inverse API exists. No calendar, contract rounding, market suitability, fresh installation, Windows or notebook execution is claimed. Bounded float factors do not support all representable final values. F28, F32, platform coverage and independent acceptance remain open.

```bash
python3 -B books/book-01-python-foundations-for-financial-mathematics/qa/chapter-10-perpetuities-review/review.py
```

Next: Section 10.9.
