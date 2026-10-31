# Chapter 7 — Section 7.6 conversion exercises

Based on main `62c4777599cf30ca874d69f1f88f8c465a824857`. [Eight answers](ANSWERS.md) · [Per-prompt register](answer-register.json) · [Runner](review.py) · [Results](results.json) · [Supplemental Y/N adapter](yn_adapter.py)

**Eight scoped answers; 4 command checks, 28 predicates and 8 existing methods passed on the first run.** CPython 3.12.14, pandas 2.2.3, NumPy 2.3.5, Linux; Copy-on-Write=False. Original demo/discovery/compileall plus one supplemental adapter caller run in the documented sibling layout with FutureWarning as error. Full stdout,source/listing/adapter hashes and expected rejection traces retained. No unexpected failure or manuscript change; overlapping reruns add no historical unique methods or prior workflow cases.

```bash
python3 -B books/book-01-python-foundations-for-financial-mathematics/qa/chapter-07-conversion-exercises/review.py
```

Exact source calls preserve another leading-zero ID,unknown counts and the Int64 bound. Supplemental diagnostics separate introduced coercion failures from original missingness,and show irrecoverable fractional truncation. E4 implements a narrow Y/N adapter with rejection checks while preserving the source converter's other contracts. Scaled cents and checked downstream aggregation/multiplication remain designs. Independent rational/integer expectations are executor derivations,not external independent acceptance.

**48/136 Chapter 7 local prompts have scoped records; 88 remain.** All 17 core workflows, 20 chapter-wide answers and 18 separate project records remain distinct. Fresh-install/platform/notebook,source context/precision and independent acceptance remain open; F28/F32 retained. Next: **Section 7.7 local exercises**.
