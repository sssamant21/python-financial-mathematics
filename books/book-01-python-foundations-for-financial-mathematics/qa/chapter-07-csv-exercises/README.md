# Chapter 7 — Section 7.5 CSV exercises

Based on main `831a0185aad6afe873f717d099d8f4bbca288492`. [Eight answers](ANSWERS.md) · [Per-prompt register](answer-register.json) · [Runner](review.py) · [Results](results.json) · [Snapshots](snapshots.json) · [Unimplemented extension designs](DESIGN.md)

**Eight scoped answers; 3 command checks, 22 predicates and 8 existing methods passed on the first run.** CPython 3.12.14, pandas 2.2.3, NumPy 2.3.5, Linux; Copy-on-Write=False. Original demo/discovery/compileall run unchanged in the documented folder layout with the exact CSV fixture and FutureWarning as error. Source/listing/payload hashes,raw outputs and expected rejection traces retained. No unexpected failure or manuscript change. Historical unique methods and earlier workflow cases unchanged by overlapping reruns.

```bash
python3 -B books/book-01-python-foundations-for-financial-mathematics/qa/chapter-07-csv-exercises/review.py
```

Exact source calls preserve leading-zero IDs,expose the missing-whole-record coverage limit,reject mismatched context/empty numbers and compare LF/CRLF/reordered files. Independent arithmetic reconciles original1000 and omitted/zero-BETA700. Retained bytes: [LF](holdings-lf.csv), [CRLF](holdings-crlf.csv), [renamed ID](holdings-renamed.csv), [omitted record](holdings-omitted.csv), [reordered records](holdings-reordered.csv). E7 expected-set tests and E8 chunked duplicate controls remain designs; no new ingestion API or streaming workflow was implemented or accepted.

**40/136 Chapter 7 local prompts have scoped records; 96 remain.** All 17 core workflows, 20 chapter-wide answers and 18 separate project records remain distinct. Fresh-install/platform/notebook,source completeness/authenticity,numerical and independent acceptance remain open; F28/F32 retained. Next: **Section 7.6 local exercises**.
