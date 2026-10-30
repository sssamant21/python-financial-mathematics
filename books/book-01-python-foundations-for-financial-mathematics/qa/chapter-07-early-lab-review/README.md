# Chapter 7 — Sections 7.1–7.4 lab-step review

Based on main `d913780ef0e5a6731dbfb19ebab24f8bdc1ad07b`. [Contract review](REVIEW.md) · [Four workflow/32 derived-unit records](workflow-register.json) · [Runner](review.py) · [Results](results.json)

CPython 3.12.14, pandas 2.2.3, NumPy 2.3.5, Linux: **17 command checks and 38 predicates passed** on the first run; **32 existing methods** passed (eight per section). No unexpected failure or manuscript change. Four workflow records and 32 derived review units do not add unique methods or historical workflow cases. All 136 local prompts remain pending; this batch does not claim their exercise answers reviewed.

```bash
python3 -B books/book-01-python-foundations-for-financial-mathematics/qa/chapter-07-early-lab-review/review.py
```

The 17 commands are one environment/options probe plus, per lab, the original demo/discovery/compileall commands and a quiet import check. The runner recreates documented parent/sibling layouts and hashes all eight complete source/test listings unchanged. Demonstration comparison preserves line order, values and labels while allowing whitespace differences in pandas console alignment. FutureWarning is an error. Compilation artifacts are confined to owned temporary directories.

All 13 explanatory Python fences also execute unchanged in dependency order with hashes/stdout retained. Section 7.4 uses the explicitly documented t precondition, initialized through the original fixture(); other snippets supply their own earlier dependencies. Supplemental predicates call unchanged APIs, use independent rational/hand values, and check ownership, missingness and intentional boundary differences. No new financial implementation replaces source code.

Series/holdings zero values remain allowed without imposing a weight denominator. The selector's NaN/stale-field acceptance is intentional and directly probed; it is not misreported as valuation validation. Original pandas Copy-on-Write setting is False in this environment; no cross-mode storage promise is inferred. Formatting, exact monetary precision and upstream identity/time/currency correctness remain separate.

**Setup is PARTIAL**: prepared runtime versions/options pass, but fresh venv/install/shell activation, Windows/macOS, notebooks, supported-platform and independent acceptance are unexecuted. F28/F32 and earlier finding history remain intact. The numerical, inference, concurrency, financial/model and conceptual-only limits in the chapter tracker persist.

**4/17 Chapter 7 formal section workflows now have scoped records; 13 remain.** Twenty chapter-wide answers remain separately scoped; 136 local prompts and project checklist/acceptance review remain pending. Next: **Sections 7.5–7.8 formal lab-step review**.
