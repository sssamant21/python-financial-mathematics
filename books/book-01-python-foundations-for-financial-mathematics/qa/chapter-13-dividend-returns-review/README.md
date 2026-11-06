# Section 13.7 — Dividends and Total Return review

Baseline: `09c430f339cd81a3801d365962dd8857cd1f9108`. [Runner](review.py) · [Initial](initial-results.json) · [Corrected](results.json) · [Answers](ANSWERS.md) · [Supplemental ledger](project-ledger.csv).

The observer executes the exact source, checks isolated import and compiles the standalone file. All three commands and the 12 existing methods passed on both versions in the recorded Linux CPython runtime. Nine of 33 supplemental predicates initially failed; all 33 passed after correction. Counts: one workflow, 18 local answers, one separately scoped project and no historical unique additions.

Independent rational share and cash arithmetic checks the source reinvestment, cash-held alternative, split neutrality and linked returns. Reinvesting the 40 dividend at 48 gives 20⅚ ending shares worth 1,125 and 12.5% return; holding the cash gives 1,120 and 12%. The supplemental ledger uses event labels because the project does not supply calendar dates. Its dividend receipt and reinvestment offset, leaving no remaining dividend cash in the reinvested valuation.

F101: tiny dividends could disappear before net-return calculation, and a positive residual holding could report as complete loss. F54/F95 recurred in large-notional, scaled, or tiny linked calculations. The source uses rational intermediates and checks reported outputs.

Standalone Python 3.9+ and the standard library suffice. No actual dividends, brokerage trades, withholding workflow, corporate-action feed, other platform or independent acceptance was tested. F28 and F32 remain open.

```bash
python3 -B books/book-01-python-foundations-for-financial-mathematics/qa/chapter-13-dividend-returns-review/review.py
```

Next: 13.8 — Arithmetic vs. Geometric Mean Return.
