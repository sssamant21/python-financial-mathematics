# V06 — Chapter4 early section exercises

Date:2026-10-29. Baseline:`9c65d890d0549f9b38fe0393a8af04bf27a86a48`.

**PASS(scoped):27 exercises in4.1–4.3 reviewed;22 final runtime predicates passed.** The earlier section queue now records27 reviewed and81 pending out of108. These counts are separate from20 chapter-wide answers and source test-method counts.

[Answers](ANSWERS.md) · [Register](answer-register.json) · [Runner](review.py) · [Actual results](results.json) · [Live queue](../chapter-04-workflow-review/section-exercise-queue.json)

The exact source payment validator and period-pair selector are exercised. Supplemental list/index/tuple probes use independently stated expected structures and exception classes. The new indexed_positive helper validates all amounts before returning original indices, accepts empty input, rejects wrong/nonfinite entries and preserves period metadata. The positive-receipt list and observed-zero selection list are explicitly separate fixtures. A prepublication fixture refinement made all four introductory future receipts positive; the final22-check run passed, as did the prior run. No source defect was inferred.

Schema/source-ID and collection/correction rules, nested-copy changes, signed-valuation adapters, FX prerequisites and expanded named records are documented designs. They are not misreported as implemented production features. Ownership, mutation, empty pop, wrong unpacking, tuple item assignment, upper period1000, equal-valued event identity and index-preserving selection have actual execution evidence. Not every conceptual exercise is a runtime test.

Reproduce:`python books/book-01-python-foundations-for-financial-mathematics/qa/chapter-04-early-section-review/review.py` from repository root. CPython3.12.14 Linux x86_64; standard library only. Canonical source and historical method/workflow totals remain unchanged. Independent model/editorial/source/platform acceptance and F28/F32 remain open.

Next:27 exercises in4.4–4.6, then remaining section exercises and4.13 project/checklist/extensions.
