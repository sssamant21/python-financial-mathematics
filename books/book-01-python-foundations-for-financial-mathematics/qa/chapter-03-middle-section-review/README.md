# V06 — Chapter 3 types, documentation and valuation section exercises

Date: 2026-10-29. Baseline: `00b7cd53ca165d1e7d684ce54d1ea09ea3f13701`.

**PASS (scoped): 27 exercises in Sections3.7–3.9 reviewed;34 predicates passed, zero failed.** Earlier section exercise coverage is now52 of88 prompts, with36 in3.10–3.13 pending. This count is separate from20 Section3.15 chapter-wide answers and10 lab records; no complete chapter-acceptance claim is made.

| Evidence | Scope |
|---|---|
| [Answers](ANSWERS.md), [hashed register](answer-register.json) | All27 prompt-aligned answers, including conceptual/proposed contracts |
| [Runner](review.py), [results](results.json) |34 predicates, exact source calls, supplemental typed helpers and temporary doc/horizon variants |
| [Updated exercise queue](../chapter-03-early-section-review/section-exercise-queue.json) |52 reviewed,36 pending, source hashes retained |

The runner extracts the exact3.7–3.9 labs into isolated in-memory modules. Only3.7 has top-level demonstrations; their output is recorded. Source functions handle the runtime guard and valuation fixtures. The supplemental signed-difference and keyword-only Literal-timing helpers are new teaching code; annotations alone are not described as runtime enforcement. The zero-principal doctest and horizon10 definition are in-memory variants; canonical horizon1000 remains unchanged. The signed-amount extension is documented but intentionally not silently implemented in the canonical nonnegative API.

Checks include wrong representation, NaN/Infinity, bool/negative/fractional periods, period0 versus None, cast identity, timing, an added zero-principal doctest, a reconciled temporary horizon with valid docstring examples, exact Fraction FV and independently known PV, negative rates, a mutually inverse wrong pair, restrictive Inexact behavior, caller-state restoration and display/quantization separation. The exact source's ordinary Decimal context is used; this is not the fixed-policy3.14 API. Conceptual rate/documentation/compatibility answers require prose review and are not relabeled as executable tests.

All34 final checks passed. An initial33-check harness also passed, then the temporary horizon text replacement was narrowed to avoid touching numeric example literals and a doctest regression check was added; the34-check result is authoritative. That was a harness refinement, not a manuscript correction. The exercise queue and trackers are updated; no manuscript/code fence changed. Existing unittest, doctest and unique workflow totals are unchanged.

Reproduce from repository root: `python books/book-01-python-foundations-for-financial-mathematics/qa/chapter-03-middle-section-review/review.py`. CPython3.12.14, Linux x86_64, standard library only. The selected local context probe restores caller precision/rounding/flags/traps; no exhaustive signal, magnitude, numerical-error or platform coverage is asserted.

Next:36 exercises in Sections3.10–3.13, then full project/definition/call/contract checklist review. Independent mathematical/model/editorial/source acceptance and Book1 F28/F32 gaps remain open.


Latest follow-up: [Sections3.10–3.13](../chapter-03-later-section-review/README.md) complete the scoped answer records for all88 earlier section exercises. The live queue records zero pending section exercises; project/checklist acceptance remains open.
