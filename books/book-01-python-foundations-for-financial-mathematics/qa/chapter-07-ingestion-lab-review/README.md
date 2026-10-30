# Chapter 7 — Sections 7.5–7.8 ingestion/conversion/coverage/cleaning review

Based on main `1273dc47b6df75c107047da28b81f2630a8a4546`. [Contracts](REVIEW.md) · [Four workflow/32 derived-unit records](workflow-register.json) · [Runner](review.py) · [Results](results.json) · [Exact-source cleaning audit](cleaning-audit.json)

CPython 3.12.14, pandas 2.2.3, NumPy 2.3.5, Linux: **17 command checks and 36 predicates passed** on the first run; **32 existing methods** passed (eight per section). No unexpected failure or manuscript change. Workflow records, derived units, commands, predicates and existing methods remain separate; these overlapping reruns add no historical unique methods or workflow cases. All 136 local prompts remain pending.

```bash
python3 -B books/book-01-python-foundations-for-financial-mathematics/qa/chapter-07-ingestion-lab-review/review.py
```

One prepared-runtime/options probe and four original demo/discovery/compileall/quiet-import groups produce 17 command records. Eight complete listings and the Section 7.5 CSV fixture are recreated unchanged in documented parent/sibling layouts. Demonstration comparisons preserve line/value/label order while allowing console whitespace; the CSV digest placeholder is resolved from the exact local fixture bytes. All source/fence/fixture hashes are retained. Tests run with FutureWarning as error.

All 3 explanatory fences run with explicit source prerequisites: pandas/NumPy names for 7.6/7.7, and the original cleaning function's captured normalized table for 7.8. That trace invokes original source, not a supplemental normalization implementation. Independent integer/rational arithmetic checks values; supplemental source probes distinguish LF/CRLF bytes, exact count bounds, explicit Boolean tokens, missing/absent coverage and local audit conservation. The retained audit records raw tokens, accepted/rejected records and every source ordinal; a partial accepted subtotal is never reported as full batch value.

**Setup remains PARTIAL**: preinstalled pinned versions are verified; fresh venv/install, shell activation, Windows/macOS, notebooks and cross-mode/platform acceptance are unexecuted. Copy-on-Write=False is observed, not assumed portable behavior. Hashes establish byte identity only; authenticity, source availability, intraday/currency completeness, transactional snapshots, exact monetary accuracy and independent acceptance remain open. F28/F32 and all earlier finding/failure history remain intact.

**8/17 Chapter 7 formal workflows now have scoped records; 9 remain.** Twenty chapter-wide answers remain separately scoped; 136 local prompts and project checklist/acceptance review remain pending. Next: **Sections 7.9–7.12 formal lab-step review**.
