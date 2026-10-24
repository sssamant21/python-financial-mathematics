# Chapter 9 — Time Value of Money with Python

| Section | Title | Status |
|---|---|---|
| 9.1 | [The Time Value of Money](9.01-the-time-value-of-money.md) | Canonical / Complete |
| 9.2 | [Financial Timelines](9.02-financial-timelines.md) | Canonical / Complete |
| 9.3 | [Simple Interest](9.03-simple-interest.md) | Canonical / Complete |
| 9.4 | [Compound Interest](9.04-compound-interest.md) | Canonical / Complete |
| 9.5 | [Present Value](9.05-present-value.md) | Canonical / Complete |
| 9.6 | [Future Value](9.06-future-value.md) | Canonical / Complete |
| 9.7 | [Discount Factors](9.07-discount-factors.md) | Canonical / Complete |
| 9.8 | [Multiple Cash Flows](9.08-multiple-cash-flows.md) | Canonical / Complete |
| 9.9 | [Net Present Value](9.09-net-present-value.md) | Canonical / Complete |
| 9.10 | [Effective vs. Nominal Rates](9.10-effective-vs-nominal-rates.md) | Canonical / Complete |
| 9.11 | [Compounding Frequency](9.11-compounding-frequency.md) | Canonical / Complete |
| 9.12 | [Continuous Compounding](9.12-continuous-compounding.md) | Canonical / Complete |
| 9.13 | [Solving for Rate](9.13-solving-for-rate.md) | Canonical / Complete |
| 9.14 | [Solving for Time](9.14-solving-for-time.md) | Canonical / Complete |
| 9.15 | [Python TVM Functions](9.15-python-tvm-functions.md) | Canonical / Complete |
| 9.16 | Chapter Project — Time Value of Money Engine | Planned |
| 9.17 | Exercises and Applied Problems | Planned |

**Canonical manuscript progress:** 9.1–9.15 complete (15/17 sections).  
**Chapter status:** In progress.  
**Next:** 9.16 — Chapter Project — Time Value of Money Engine.

## Publication Policy

Follow the locked Book 1 Master TOC v1.0 and Draft → Technical + Source Review → Production + Copyright Review → Revised Final / Canonical Edition. Section 9.1 includes a standalone standard-library lab with eight passing reference tests and a successful compilation check. Original examples use explicit periodic rates, matching whole-period terms, common valuation dates, and stated numerical limits. Author review is not independent certification.

Section 9.2 adds a standalone financial-timeline lab with event retention, period netting, explicit completeness assumptions, and eight passing reference tests; compilation succeeds.

Section 9.3 adds a standalone simple-interest lab with matching rate/time units, explicit fixed day bases, rollover distinctions, and eight passing reference tests; compilation succeeds.

Section 9.4 adds a standalone compound-interest lab with a retained-interest schedule, closed-form reconciliation, composition checks, and eight passing reference tests; compilation succeeds.

Section 9.5 adds a standalone signed single-payment present-value lab with inverse accumulation, common-date comparisons, negative-rate boundaries, and eight passing reference tests; compilation succeeds.

Section 9.6 adds a standalone future-value lab with explicit start/target coordinates, common-future-date comparisons, signed equivalents, and eight passing reference tests; compilation succeeds.

Section 9.7 adds a standalone discount-factor lab with reciprocal accumulation, interval composition and factor ratios, signed payments, and eight passing reference tests; compilation succeeds.

Section 9.8 adds a standalone multiple-cash-flow lab with event-level audit rows, same-date netting, common-target reconciliation, and eight passing reference tests; compilation succeeds.

Section 9.9 adds a standalone NPV lab with explicit initial-cost handling, break-even pricing, rate scenarios, incremental comparison, and eight passing reference tests; compilation succeeds.

Section 9.10 adds a standalone nominal/effective rate-conversion lab with reverse conversion, equivalent balances, common-basis comparison, and eight passing reference tests; compilation succeeds.

Section 9.11 adds a standalone compounding-frequency lab with fixed-nominal versus fixed-effective comparisons, annual-to-daily schedules, limiting behavior, and eight reference tests.

Section 9.12 adds a standalone continuous-compounding lab with exponential accumulation, discounting, rate-convention conversion, numerical boundary checks, and eight reference tests (execution verification pending).

Section 9.13 adds a standalone rate-solving lab with periodic, effective annual, nominal annual, and continuous inversions, boundary validation, and eight reference tests (runtime verification pending).

Section 9.14 adds a standalone logarithmic time-solving lab with periodic, effective, nominal, and continuous conventions, feasibility checks, and eight reference tests (runtime verification pending).

Section 9.15 adds a reusable standard-library TVM module with discrete and continuous valuation, rate conversions, inverse solvers, signed cash-flow NPV, and eight reference tests (runtime verification pending).
