# V06 — Chapter 3 early section-exercise review

Date: 2026-10-29. Source baseline: `7b9ee5df7c2f091b3bf260e185189b5e839de5ec`.

**PASS (scoped): 25 exercises in Sections3.4–3.6 reviewed; all33 runtime predicates passed.** Discovery identified88 earlier section exercises (7 in3.4 and9 each in3.5–3.13). The remaining63 and full project/checklist review are pending; the separate20 Section3.15 answers and10 lab records retain their existing evidence. No full Chapter3 completion percentage is asserted.

| Evidence | Scope |
|---|---|
| [Answers](ANSWERS.md), [register](answer-register.json) | All25 prompts with contracts, explanations and source hashes |
| [Section exercise queue](section-exercise-queue.json) | All88 prompts inventoried;25 reviewed,63 pending |
| [Runner](review.py), [results](results.json) | Exact source labs/default definition; explicit supplemental probes and33 expected comparisons |
| [Required-timing teaching variant](required_timing_variant.py) | Complete temporary-interface exercise with updated calls; not replacement canonical code |

Exact guarded source functions are used for target detection, validation, timing, ownership and scenario checks. The three original labs execute unchanged before their functions are reused. The introductory default function is separately extracted as its exact definition with a documented Decimal prelude. The print-only function and required-timing lab are generated AST variants: no original manuscript function is silently rewritten.

The required-timing variant removes that keyword-only default and updates every lab call. Calls using **options merge a default timing before supplied overrides, so deliberate timing errors remain errors; existing assertions still pass. The generated standalone teaching file is explicitly supplemental. The print variant displays the computed value and returns None. Other helpers demonstrate signed differences, list aliasing, module/local binding, conditional failures, closures and explicit-rate alternatives. These teaching probes are not full external-input financial APIs.

All33 predicates passed on the first run. Numeric fixtures use hand-checkable expected values (including1000*.9*.9=810); semantic checks inspect identity, returned types/absence, exceptions and caller state. Conceptual items such as API compatibility and the proposed PV contract are prose reviews, not33 independently implemented exercises. Historical method/workflow totals are unchanged.

Reproduce from repository root: `python books/book-01-python-foundations-for-financial-mathematics/qa/chapter-03-early-section-review/review.py`. CPython3.12.14 on Linux x86_64; standard library only. No manuscript/code fence changed and no numerical source defect was identified. This batch supplies exercise answers where the companion explicitly limits itself to chapter-wide questions; it does not redefine optional extension tasks as prior authoring defects.

Next: the27 section exercises in3.7–3.9, then36 in3.10–3.13, followed by full Section3.14 project and definition/call/contract checklist review. Independent model/editorial/source acceptance, broader numerical/input/platform coverage and Book1 F28/F32 gaps remain open.


Follow-up: [Sections3.7–3.9](../chapter-03-middle-section-review/README.md) add27 reviewed prompts. The live exercise queue now records52 reviewed and36 pending; the25/63 counts above describe the original batch.
