# V06 — Chapter 2 project and checklist review

Date: 2026-10-29. Reviewed baseline: `fc18c1b2178751f9b8c5a179df01057e73f52551`.

**PARTIAL — project/checklist review recorded; 33 controlled project cases passed and one additional open-limitation probe confirmed the shared-input type precondition.** All 256 harness predicates matched their expected outcomes, including the expected AttributeError observation; that observation is not a successful project validation case. The total is 34 fresh subprocesses, not 34 passing project cases.

| Evidence | Scope |
|---|---|
| [Project requirements](REQUIREMENTS.md), [JSON](requirements.json) | 24 derived review units with passing, design, partial and open dispositions |
| [Chapter checklists](CHECKLISTS.md), [JSON](checklist-register.json) | 53 review units from four sections (2.8,2.9,2.10,2.11); not 53 tests/labs |
| [Runner](review.py), [actual outputs/state](results.json) | Exact Section2.12 script in fresh processes, declared AST input overrides, stdout, state, exceptions and predicates |

The project code is extracted from its sole Python fence; only declared top-level fixture assignments are replaced. Validation, projection, classification, storage, assertions and output logic are unchanged. Each child records original scenario representations so the expected accepted/rejected count does not mistake external numeric strings for Decimal values. The runner fails if any override cannot be applied.

Cases include baseline, period0, zero contribution/return, supported negative return, -100% and below, just above -100%, NaN/signalingNaN/infinities, representation rejection, empty scenarios, first/final-year crossing, tiny final miss, display-rounding mismatch, horizon1/100, classification at/after10, reversed/duplicate scenarios and shared field/horizon rejections. Fraction closed-form accumulation and annuity terms independently determine first crossing and terminal balance, using fixture bound max(1,|oracle|)*1e-26 for 28-digit Decimal output. This is not a universal tolerance or error proof.

F32 remains OPEN: shared monetary inputs are initialized as Decimal literals and call is_finite directly. A string initial investment raises AttributeError instead of a validation diagnostic. This is outside the typed example's supported path, but prevents treating it as a complete arbitrary external-input validator. Scenario inputs do have explicit representation guards. The probe's actual exception is retained in results.json; no original failure was discarded or relabeled as a supported success. External parsing, broader Decimal/resource limits, financial plausibility, scale and platform/independent acceptance remain open.

The review records design applicability explicitly. Section2.12 reports every scenario but does not rank earliest ties; that optional behavior is supplied by Exercise45/59's separate supplement. Calendar dates and stable-growth r>g relationships are not requirements of this annual ordinal savings recurrence. Reconciliation assertions verify internal consistency and can be disabled; they are not substitutes for external validation.

Reproduce from the repository root: `python books/book-01-python-foundations-for-financial-mathematics/qa/chapter-02-project-review/review.py`. Standard library only; CPython3.12.14, Linux x86_64. All 256 predicates matched on the first run and after strengthening representation metadata. Source manuscript/code is unchanged. Earlier 60/106/133 exercise predicates and historical methods/workflows are kept separate; do not add overlapping reruns as unique coverage.

All 60 Section2.13 exercise records and these project/checklist records now exist, with the listed open dispositions retained. Chapter2 is reviewed to this scoped level, not comprehensively accepted. Next: Chapter3 formal lab-step and answer review. Retain F32 and Chapter1 notebook/platform gaps in the cross-book follow-up queue.
