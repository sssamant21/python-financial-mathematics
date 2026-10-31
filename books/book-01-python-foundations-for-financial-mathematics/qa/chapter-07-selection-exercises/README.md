# Chapter 7 — Section 7.4 selection exercises

Based on main `497e1892a8bc08b353d711a092f40ddada9531bf`. [Eight answers](ANSWERS.md) · [Per-prompt register](answer-register.json) · [Runner](review.py) · [Results](results.json) · [Supplemental unknown-condition guard](known_condition.py)

**Eight scoped answers; 4 command checks, 21 predicates and 8 existing methods passed on the first run.** CPython 3.12.14, pandas 2.2.3, NumPy 2.3.5, Linux; Copy-on-Write=False. Three original demo/discovery/compileall commands plus one supplemental guard caller; full stdout comparison allows whitespace only. Source/listing/supplement hashes and raw outputs retained. No unexpected failure or manuscript change; overlapping reruns add no historical unique methods or earlier workflow cases.

```bash
python3 -B books/book-01-python-foundations-for-financial-mathematics/qa/chapter-07-selection-exercises/review.py
```

Source calls check selected axes/rank, absent-key policy and copy isolation. Supplemental pandas mechanics show positional-mask population changes and the BETA90 repricing total970 from independent scalar arithmetic. E5 explicitly rejects unknown conditions before selection under stated preconditions. E8 probes documented stale-value and NaN permissiveness; financial context remains the caller's responsibility.

**32/136 Chapter 7 local prompts have scoped records; 104 remain.** All 17 workflows, 20 chapter-wide answers and 18 separate project records remain distinct. Fresh-install/platform/notebook,numerical/context and independent acceptance remain open; F28/F32 retained. Next: **Section 7.5 local exercises**.
