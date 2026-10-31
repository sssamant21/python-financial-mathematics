# Chapter 7 — Section 7.7 missingness exercises

Based on main `8cbba0741fd27713b7cf67b2c5d97c558a1b6e04`. [Eight answers](ANSWERS.md) · [Per-prompt register](answer-register.json) · [Runner](review.py) · [Corrected results](results.json) · [F37 failure/rerun](FAILURE-AND-RERUN.md) · [Unimplemented policy tests](DESIGN.md)

**Eight scoped answers; corrected rerun passes 3 command checks, 24 predicates and 8 existing methods.** CPython3.12.14,pandas2.2.3,NumPy2.3.5,Linux;Copy-on-Write=False. Original source demo/discovery/compileall run unchanged in documented sibling layout;full stdout comparison allows whitespace only. Initial QA shadowing error aborted before source execution and is retained separately. Manuscript unchanged;historical unique methods and earlier workflow cases not increased by overlapping reruns.

```bash
python3 -B books/book-01-python-foundations-for-financial-mathematics/qa/chapter-07-missingness-exercises/review.py
```

Exact source distinguishes absent versus explicitNaN,observedzero,emptyreturns and completecoverage. Independent fractions give partial3/50,renormalized3/35 and complete9/200,with different interpretations. Supplemental fill mechanics use prior/later observations without endorsing imputation. Quote-age and zero-weight exception policies/tests remain designs;strict zero-weight behavior is actually executed for comparison. Source/listing hashes,expectedrejection traces,initial runner and corrected outcomes retained.

**56/136 Chapter 7 local prompts have scoped records; 80 remain.** All 17 core workflows, 20 chapter-wide answers and 18 separate project records remain distinct. F28/F32,platform/input/numerical and independent acceptance remain open. Next: **Section 7.8 local exercises**.
