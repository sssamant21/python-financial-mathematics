# Section 10.14 — Cash-flow engine project review

Baseline `12c27a352a0ecf906967bf362091daa15aa4b95a`. [Runner](review.py) · [Initial results](initial-results.json) · [Corrected results](results.json) · [Answers and acceptance records](ANSWERS.md).

Both documented commands and all twelve existing methods passed on both versions. Fifteen of 48 additional predicates initially failed; all 48 pass after correction. The runner extracts the sole Python fence verbatim, saves it as cash_flow_engine.py, executes the demonstrations and tests, and compiles it in isolation. Prepared Linux CPython 3.12.14 and its standard library were used. The exact console prints NPV 4.13 and IRR 0.130662. The file is standalone: no earlier module, package installation, external data or network is required. Reproduce baseline failures with this runner against the baseline source.

- F54/F56: nonzero discounted and growing payments could silently underflow. Zero payments or rates triggered avoidable factor overflow, and a growing schedule formed a standalone power that overflowed before a finite payment was computed. The engine checks terms, handles exact zeros after validation, and builds growing amounts by recurrence.
- F60/F61: the project solver repeated premature residual-based stopping, underflowing sign products, unsafe midpoints and invalid settings. It now checks finite settings, compares signs directly and uses rate half-width or a computed zero.
- F62: opposite amounts on the same date netted to an identically zero NPV and were assigned a spurious unique IRR. The engine rejects streams with exactly zero net amounts at every period, using Fraction only for that check.
- F63: malformed IRR records could fail through attribute access, empty schedules bypassed payment checks, and growing arithmetic converted boolean first payments before validating them. These inputs now receive explicit validation.

Regression cases are inside an existing method. No historical unique methods were added. One project workflow, twelve local prompts and six project acceptance records are separate counts. Independent rational timeline sums, algebraic roots and a 100-digit Decimal quadratic benchmark check the worked scenario; no spreadsheet was executed. Signed values and exact timing were checked at several horizons. Same-sign, endpoint, multiple-root and indeterminate cases have separate evidence. Range rejection is bounded; the growth recurrence accumulates float rounding, and a computed zero is not an exact-real proof.

No real transaction completeness, application-specific thresholds, date/CSV/Decimal accounting extensions, cross-version or platform acceptance, notebook execution, or independent editorial certification was performed. F28 and F32 remain open.

```bash
python3 -B books/book-01-python-foundations-for-financial-mathematics/qa/chapter-10-engine-project-review/review.py
```

Next: Section 10.15, chapter-wide applied problems.
