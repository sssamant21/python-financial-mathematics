# Chapter 7 — Section 7.10 screening exercises

Based on main `1400cfa136ac844d097b13aaa8413caddde6b1e6`. [Eight answers](ANSWERS.md) · [Per-prompt register](answer-register.json) · [Runner](review.py) · [Results](results.json)

**Eight scoped answers; 3 command checks, 18 predicates and 8 existing methods passed on the first run.** CPython 3.12.14, pandas 2.2.3, NumPy 2.3.5, Linux; Copy-on-Write=False. Original commands use unchanged source listings in the documented sibling layout with FutureWarning as error. Full stdout comparison allows whitespace only. Source/listing hashes,raw outputs and expected rejection traces retained. No unexpected failure or manuscript change;historical unique methods and prior workflow-case counts unchanged.

```bash
python3 -B books/book-01-python-foundations-for-financial-mathematics/qa/chapter-07-screen-exercises/review.py
```

Original single-sector screen remains unchanged. Supplemental authored two-sector query/isin mechanics run on the validated fixture;this does not add a multi-sector public API. E5 retains the original maximum-row/tie-break policy. E8 proposes richer status/provenance fields without implementing a report writer or changing failure semantics.

**80/136 Chapter 7 local prompts have scoped records; 56 remain.** All 17 core workflows,20 chapter-wide answers and18 separate project records remain distinct. Fresh-install/platform/notebook,source context/numerical and independent acceptance remain open; F28/F32 and earlier findings/failures retained. Next: **Section 7.11 local exercises**.
