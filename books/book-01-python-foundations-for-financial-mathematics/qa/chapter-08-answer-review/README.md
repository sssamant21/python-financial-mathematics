# Chapter 8 — Twenty chapter-wide prompt and companion reviews

Baseline `630462777b9d1cf5b9802c985392b3a28dca4618`. [Runner](review.py) · [Results](results.json) · [Observer log](observer.log) · [Worked answers](ANSWERS.md) · [Prompt register](answer-register.json) · [Initial runner](initial-review.py) · [Initial results](initial-results.json).

**Twenty chapter-wide answers reviewed. Three command checks and twenty-two additional predicates passed after the F45 harness correction.** The unchanged companion's twenty methods passed in its documented command and again in an instrumented observer run of those same methods. The separate unchanged Section 8.13 integration suite passed sixteen methods as required by Problem 20. Final successful method invocations are 20+20+16=56; no historical unique methods were added. Repeated development attempts and initial failures remain separate from this final-run count.

The observer uses Python tracing to retain method locals at return; no test predicates or implementation statements are modified. Prompt-derived fractions, integer bin assignments and 60-digit Decimal computations are compared with those executed source values. The companion is fixed-fixture reference work; its test predicates do not become general-purpose validators. The per-prompt register maps each original problem and companion answer, hashes both source files, and identifies scope.

**F45 (QA harness):** The initial separate dashboard test reconstruction omitted prices.csv, which the exact tests read at import time. The raw FileNotFoundError and initial runner are retained. Adding the exact published CSV resolved it; no manuscript change was needed. The first two companion command checks and observer succeeded even in that initial attempt. To reproduce the harness failure, run initial-review.py at this same relative path in a worktree of the baseline; it needs the earlier dashboard evidence directory.

Prepared Linux CPython 3.12.14, NumPy 2.3.5, pandas 2.2.3 and Matplotlib 3.10.8 were used; timezone tests used the available America/New_York rules. No fresh install or other platform execution. All listings are extracted from current manuscript source. Problem 20's small accounting case is distinct from its sixteen-method integration task, which is executed separately in the runner.

Six source figure objects (Problems 2, 3, 4, 5, 18, 19) were additionally exported by QA with titles/units and constrained layout. The QA display for Problem 4 adds distinguishing legend/styles; Problem 18 adds inversion, labels and a zero marker. These supplemental presentations were visually inspected for spacing, gaps, held-state semantics, sign cues and exported labels. They are not unchanged source exports, an accessibility certification or substitute for the thirteen complete labs. The runner regenerates them and records hashes. Problem 2 intentionally leaves its second panel empty.

```bash
python3 -B books/book-01-python-foundations-for-financial-mathematics/qa/chapter-08-answer-review/review.py
```

Chapter 8 has scoped records for thirteen core workflows, 104 local prompts and twenty separate chapter-wide answers, plus project deliverable/responsibility records. These counts are distinct. Broad source/data, platform/notebook and independent acceptance remain open, including F28/F32. Next: Chapter 9 formal lab-step and worked-answer review, beginning with Section 9.1.
