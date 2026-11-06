# Section 13.1 — Measuring Investment Returns review

Baseline: `51ec8d8c2bd8aa7ebf6859ed8f00def6272e55df`. [Runner](review.py) · [Initial](initial-results.json) · [Corrected](results.json) · [Answers](ANSWERS.md).

The runner extracts the sole Python fence verbatim, runs the demo and all 12 existing methods, checks isolated import, and compiles the same file. All three commands passed on both versions in the recorded Linux CPython runtime. Eleven of 40 supplemental predicates initially failed; all 40 passed after correction. One workflow, 18 local answers, one separate mini-project and zero historical unique additions are recorded.

Independent rational arithmetic checks the project rows and continuity of 1,000 → 1,048 → 1,014 → 1,086. The linked return is 8.60% under the clarified account-value convention; it does not imply asset reinvestment. A separate Decimal log calculation checks log transforms. The demo is distinct from the mini-project, which the observer drives by calling the exact source.

F95: tiny gains cancelled during gross/real calculations, the unlevered helpers accepted losses below 100%, and the project mixed account wealth with reinvestment language. F54 recurred in intermediate overflow and unsupported float results. Rational operations and checked reporting now preserve representable values.

Use standalone Python 3.9+ and standard library only. No external cash-flow performance engine, asset price reconstruction, taxes, data source, other platform or independent acceptance was exercised. F28 and F32 remain open.

```bash
python3 -B books/book-01-python-foundations-for-financial-mathematics/qa/chapter-13-investment-returns-review/review.py
```

Next: 13.2 — Simple Returns.
