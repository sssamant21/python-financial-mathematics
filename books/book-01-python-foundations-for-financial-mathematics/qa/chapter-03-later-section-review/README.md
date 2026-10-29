# V06 — Chapter3 later section exercises

Date:2026-10-29. Baseline:`a1e3c960fa67d457585920d1bda626ff91de0344`.

**PASS(scoped):36 exercises reviewed;43 final predicates passed.** All88 earlier section-exercise prompts now have scoped answer records. This is separate from20 Section3.15 answers and10 lab records; project/checklist and independent acceptance remain open.

[Answers](ANSWERS.md) · [Register](answer-register.json) · [Runner](review.py) · [Final results](results.json) · [Initial retained result](initial-results.json) · [Updated queue](../chapter-03-early-section-review/section-exercise-queue.json)

The runner extracts exact Section3.10–3.13 lab code, calls original functions and runs all12 published test methods individually in fresh subprocesses. Their counts are reruns, not new unique reference methods. A separate temporary wrong-horizon copy causes the independent known-value method to fail as expected; failure stdout/stderr is retained. An in-memory precision6 copy demonstrates a policy change; canonical precision40 is unchanged.

The first42-predicate run had41 passes and one harness expectation failure:100/7 at precision3 happened to agree with multiplication by its rounded reciprocal. The retained initial result records this. The corrected hand-checkable fixture uses2/3=.667 versus2*(1/3)=.666 at precision3. A policy-revision probe was then added; final43 predicates pass. This was a fixture correction, not a manuscript defect or a tolerance relaxation.

Cases cover nominal/effective relations with an exact Fraction oracle, negative discount factors, type/domain rejections, staging at low precision, nested composition, caller-context preservation after success/failure, hidden globals, alias mutation, known PV, near−1 rates, actual return type, individual test execution and wrong-horizon detection. Conceptual conversion/metadata/tolerance/reproduction proposals are prose review records, not implemented production features or43 separate exercises. No universal numerical bound, full signal/branch/input range or platform coverage is claimed.

Reproduce from repository root: `python books/book-01-python-foundations-for-financial-mathematics/qa/chapter-03-later-section-review/review.py`. Standard library only; CPython3.12.14 Linux x86_64. Source paths/code hashes and actual subprocess outputs are retained. No manuscript source/fence changed; historical method/workflow totals remain unchanged.

Next: full Section3.14 project and definition/call/contract checklist review. Independent model/editorial/source/platform acceptance and Book1 F28/F32 remain open.
