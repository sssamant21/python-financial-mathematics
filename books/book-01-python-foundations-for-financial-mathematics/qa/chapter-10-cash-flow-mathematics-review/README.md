# Section10.1 — Cash-flow mathematics lab and answer review

Baseline `58301a4e13b618a3340b31524af89d92354c2b27`. [Runner](review.py) · [Results](results.json) · [Eight answer records](ANSWERS.md).

One core workflow and eight local prompts scoped. Two documented commands,23 supplemental predicates and eight existing methods passed. The complete single Python listing was extracted verbatim as cash_flow_mathematics.py, executed and compiled in an isolated temporary directory. Its exact console display is Example NPV:41.32 with the source's spacing retained in results.json. No manuscript defect was substantiated in this scope; source unchanged. No failures occurred in the retained run.

Prepared Linux CPython3.12.14, standard library only. Save-before-run, exact filename and self-contained imports hold. No preceding module, external data or network required. Times are nonnegative modeled years from a common reference; input rates are annual effective decimals greater than−1; constructor admits only int/float and rejects booleans. This is not a Fraction/Decimal input API; those types are used only in independent QA oracles. Local prompt8 is a conceptual audit answer. Valuation-date shifts are checked with a nonzero stream, not solely the original zero-NPV fixture. Both direct shifted-value and common-date identity agree with exact rational expectations. Same-date netting, empty generator, fsum cancellation, selected type/domain/range rejections and negative rates passed.

The source lab sequence is save, execute, compile; all feasible steps ran. Exact Fractions independently derive benchmark discounting, NPV and shifted values. Supplemental calls exercise original functions rather than replacement implementations. No financial-market return/forecast approval, arbitrary-domain coverage, calendar/day-count implementation, exact ledger rounding, installation, Windows or notebook validation is claimed. F28/F32, platform and independent acceptance remain open. The original historical reference-method total is unchanged.

```bash
python3 -B books/book-01-python-foundations-for-financial-mathematics/qa/chapter-10-cash-flow-mathematics-review/review.py
```

Next: Section10.2 formal lab and local answers.
