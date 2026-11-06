# Section 11.8 — Mortgages review

Baseline `c297157882e4419be0310a04c29f9220b1c7dd41`. [Runner](review.py) · [Initial results](initial-results.json) · [Corrected results](results.json) · [Fourteen worked answers](ANSWERS.md).

The runner saves the single Python fence verbatim as `mortgages.py` and runs the documented demo/test and compile commands on Linux CPython 3.12.14. A separate direct invocation of the same embedded suite confirms all 12 methods on both versions; 24 method invocations per version do not change the 12-method inventory. All three commands pass. Ten of 32 added predicates initially failed; all 32 pass after correction. One workflow and 14 local answer records are scoped. No historical unique methods were added.

A direct sum of exact rational discount factors gives the 15-year and 30-year installments. From those amounts the runner derives first principal, total interest and the illustrative housing allowance, and checks the exact demo output. The 30-year fixture displays 1,438.92 for principal and interest and 1,838.92 with illustrative taxes and insurance. Separate probes cover quarterly and fractional-year terms, LTV, financed fees, housing extras and positive amounts outside the supported float range.

F54 recurred at payment, rate conversion, LTV, purchase principal and housing-cost boundaries. The one-period branch and finite positive-result checks correct the witnessed cases. F71: a fractional decimal term could be accepted after the float product rounded to an integer. Count derivation now uses the term's decimal text and rejects nonintegral counts. It no longer calls a method on the product whose availability depends on the interpreter's integer API. The original integer-years demo did pass on Python 3.12; older interpreters were not run.

The workflow requires only Python and its standard library. The runner uses independent supplemental oracles; the executable lab is the extracted listing. ARM resets, official APR or payoff calculations, lending decisions, escrow administration, legal rules and real loan offers are outside the tested scope. F28, F32 and independent acceptance remain open.

```bash
python3 -B books/book-01-python-foundations-for-financial-mathematics/qa/chapter-11-mortgages-review/review.py
```

Next: 11.9 — Extra Payments and Prepayment.
