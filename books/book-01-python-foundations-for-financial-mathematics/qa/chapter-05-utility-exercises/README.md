# Chapter5 — Section5.4 local utility exercises

Based on main `5f0e1a41` (recorded source hashes bind reviewed manuscript contents). [Eight answers](ANSWERS.md) · [Register](answer-register.json) · [Runner/supplements](review.py) · [Results](results.json)

CPython3.12.14 Linux: **28 source/supplement predicates passed**, **four command records passed**, including **nine existing original methods**. Counts remain separate; no additions to historical unique-method/workflow totals. Initial run passed; no unexpected failure or manuscript correction. Expected type/schema/domain failures record actual versus expected exceptions; no source error is hidden as an empty result.

Reproduce using standard library:

```bash
python3 -B books/book-01-python-foundations-for-financial-mathematics/qa/chapter-05-utility-exercises/review.py
```

Original Section5.4 utility fence is compiled unchanged for direct probes; exact core/runner/test files separately reconstructed in a temporary directory and source suite/USD runner executed. New EUR caller source retained in results and run independently; all callers import same original utility. Source/code SHA256 for Sections5.4 and5.3 retained. New events_before/count_events/adapt_canonical are QA supplements, not published API changes.

Independent expectations derive from explicit records/date comparisons: equal cutoff excluded for before operation; E0 before2028-01-15; E1zero andE2positive share a date and normalize by ID. Reversal invariant checked against explicit E0,E1,E2 ordering as well as original result. Count3/empty0 is cardinality, not an amount total. EUR selection retains both leap-day zero andpositive records without FX. No discounting/interest/market value calculation inferred.

Cross-section integration uses exact Section5.3 canonical parser output against Section5.4 public normalizer: wrapper/event field sets, exact date/Decimal types, leap-day dates, -1000/0/1040.00 values, parent identity and output ownership checked explicitly. Schema already matches; adapter validates/reconstructs/sorts rather than inventing conversion. Extra canonical metadata rejects instead of being discarded. Invalid records excluded by cutoff still block result.

All eight prompts have scoped answers. Multi-currency schema and compatibility-migration response remain design reviews; current-contract regression cases are executed, hypothetical revised policies are not. Prerequisites: original three sibling files, exact dates/Decimal and declared investor/single-currency input contracts. No static checker, Windows/macOS, notebook, external data/FX or independent review executed. F28/F32 remain open and F33 history retained.

34 of96 local prompts now reviewed;62 remain. Next: Section5.5 package exercises, then queue order; skip already recorded5.12-E2/E3 unless source changes.
