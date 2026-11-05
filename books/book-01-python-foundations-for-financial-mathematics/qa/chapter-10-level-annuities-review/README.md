# Section10.3 — Level-annuity lab and local answers

Baseline `bad500a1e19b0e30a844757f7ba251f7700a9eb6`. [Runner](review.py) · [Initial failures](initial-results.json) · [Corrected results](results.json) · [Ten answer records](ANSWERS.md).

One workflow and ten local prompts scoped. Two documented commands,26 supplemental predicates and ten existing methods passed after F54 correction. The single Python listing was extracted verbatim as level_annuities.py, executed and compiled in isolation. Exact demonstration output is PV:399.27 and FV:586.66 with original spacing captured in results.json. Prepared Linux CPython3.12.14, standard library only; no prior imports, data or network needed. Save/run/compile prerequisites and filename contracts hold.

**F54:** the original PV/FV formulas multiplied payment .1 by an expm1 result at rate5e-324 before dividing by that rate, returning0 instead of a representable payment near.1. Zero-rate PV/FV returned infinity for1e308 paid twice, bypassing finite-result checks. Timeline discount-factor and nonzero term underflow each returned0 silently. All six initial failures are retained; the original ten methods passed even then. Factor calculation now precedes multiplication; zero-rate paths share final range checks; timeline factors/terms reject unsupported loss. Regressions were added within the existing invalid-input method, so no historical unique methods were added. Reproduce initial failures by placing this runner at the same relative path against baseline source.

Independent exact finite sums derive PV, FV, shifted timelines and signed-payment cases; 100-digit Decimal summation checks a small periodic rate. These are QA oracles, not replacement source implementations. All executed values are calls to the exact listing. Prompt1's definition is conceptual; prompt6's nominal-monthly conversion is an exact-rational supplement because this module has no rate-conversion function. Fractional payment counts, negative schedule start, invalid periodic factor and bool payment are rejected. Empty schedules are distinct from unsupported nonzero-value underflow. PV/FV identities and payment intervals have consistent units; no early rounding in the benchmarks.

Float factor-first ordering can reject an intermediate factor even when a differently arranged formula might produce a finite final value; arbitrary-range support and exhaustive branch/domain coverage are not claimed. No ledger rounding, real contract/day-count/calendar model, fresh installation, Windows or notebook workflow was validated. F28/F32, platform and independent acceptance remain open.

```bash
python3 -B books/book-01-python-foundations-for-financial-mathematics/qa/chapter-10-level-annuities-review/review.py
```

Next: Section10.4 formal lab and local answers.
