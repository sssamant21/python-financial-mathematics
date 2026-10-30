# V06 — Chapter4 dictionary, set and nested-structure exercises

Date:2026-10-29. Baseline:`ac223164d72403638340a7ef60cd099ab30e5f8e`.

**PASS(scoped):27 exercises in4.4–4.6 reviewed;40 runtime predicates passed, zero failed.** Earlier section exercise records now cover54 of108 prompts, with54 pending. These are not percentages of full chapter acceptance.

[Answers](ANSWERS.md) · [Register](answer-register.json) · [Runner](review.py) · [Actual results](results.json) · [Live queue](../chapter-04-workflow-review/section-exercise-queue.json)

The exact source index_payments, reconcile_ids and flatten_portfolio implementations are extracted unchanged from their complete lab fences. Independent expected keys, sets, alias identities and exceptions are stated before checking results. Probes cover missing mandatory fields, duplicate/case-distinct IDs, deletion/reinsertion, unexpected duplicate membership, remove/discard, disjoint partition identities for four fixture classes, source preservation, invalid later nested records, missing versus empty positions and repeated mutable references. A supplemental empty-output wrapper preserves parent identity without changing the source flatten contract.

All40 checks passed on the first run. Conceptual source/correction/FX/lot/metadata and expanded field-table proposals are prose reviews, not implemented production extensions. These validators/reconciliation helpers do not convert currencies, calculate market value, establish transaction completeness or enforce durable/concurrent revisions. No source correction was identified.

Reproduce:`python books/book-01-python-foundations-for-financial-mathematics/qa/chapter-04-middle-section-review/review.py` from repository root. CPython3.12.14 Linux x86_64; standard library only. Source/code hashes, expected/actual outcomes and environment are retained. No manuscript/fence or historical method/workflow count changed. Full branch/input/platform and independent model/editorial/source acceptance remain open; F28/F32 remain open.

Next:27 exercises in4.7–4.9, then27 in4.10–4.12 and full4.13 project/checklist/extensions.
