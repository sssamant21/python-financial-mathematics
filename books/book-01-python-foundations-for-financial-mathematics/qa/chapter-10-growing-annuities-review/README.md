# Section 10.7 — Growing annuities review

Baseline `5988dee92cf70f48f718bf8b96e0ae465d22ee42`. [Runner](review.py) · [Initial results](initial-results.json) · [Corrected results](results.json) · [Twelve prompt records](ANSWERS.md).

The two documented commands and fourteen existing methods passed on both source versions. Eight of 30 additional predicates initially failed; all 30 now pass. The runner extracts the sole Python fence verbatim as growing_annuities.py, executes it and compiles it in isolation. Save/run/compile, exact filename and standalone imports were verified with prepared Linux CPython 3.12.14 and the standard library. No external files, package installation or network are needed.

F54 recurred in two tiny-rate valuations, unchecked equal-rate overflow, and three nonzero-value losses (closed-form PV, timeline payment and FV). Forming unit factors before monetary multiplication and guarding supported factors/results addresses these six cases. F56 recurred in two avoidable intermediate overflows: first×count in the equal-rate PV, and the PV used to derive a finite FV. The equal-rate unit factor is now computed first. Direct FV factors the larger base out of the finite accumulation sum and does not call PV. Timeline PV validates independently of the closed form. The eight regression assertions are in an existing method; no new historical unique methods were added. The unchanged near-equal regression and extreme-ratio fallback passed, as did additional exact represented-rate comparisons in both directions. F11's broader range limits remain.

Independent Fraction sums discount and accumulate each payment directly. The two payment-list answers use supplemental rational arithmetic because the source provides valuations, not a schedule-output API. The equal-rate explanation is conceptual, with equal-rate valuation separately executed. No alternative application implementation or external reviewer acceptance is claimed. Intermediate factor bounds can reject a mathematically finite value; full range, platform, notebook, calendar and contractual rounding validation remain open. F28 and F32 are unaffected.

```bash
python3 -B books/book-01-python-foundations-for-financial-mathematics/qa/chapter-10-growing-annuities-review/review.py
```

Reproduce the initial failures using the same runner against the baseline source. Next: Section 10.8.
