# Section 9.8 — Multiple cash flow lab and answer review

Baseline `03738cba6ff3df3e7969508f7a8b96c3b6274779`. [Runner](review.py) · [Initial failure](initial-results.json) · [Corrected results](results.json) · [Five answers](ANSWERS.md).

One workflow and five local answers reviewed. Two documented commands, sixteen additional checks and eight existing embedded methods passed after the F46 follow-up. The full listing is reconstructed verbatim as multiple_cash_flows.py, executed and compiled in isolation. Prepared Linux CPython 3.12.14; standard library only. No earlier module imports, external schedule or network. Fresh installation and Windows substitution were not exercised.

A nonzero Fraction event below float range formerly became zero before event-underflow validation. Initial failure retained; the validator now preserves the original scalar until conversion checks finish and rejects lost nonzero inputs. The existing range-test method includes a regression; historical unique method count is unchanged. Use this runner at the same relative path in a worktree of the baseline to replay the failure.

Independent fractions verify every audit field, PV total, common future/intermediate totals and all numerical practice answers. Exact source probes exercise event reversal, signed cancellation, zero versus empty records and careful summation. Practice 5's acquisition-price/profitability discussion is conceptual. Input completeness, currency normalization, financing availability, rate appropriateness and contractual rounding remain author-supplied assumptions; no real investment or account validation. Tables require no image. F28/F32, platform/notebook and independent acceptance remain open.

```bash
python3 -B books/book-01-python-foundations-for-financial-mathematics/qa/chapter-09-multiple-flows-review/review.py
```

Next: Section 9.9 formal lab and local answers.
