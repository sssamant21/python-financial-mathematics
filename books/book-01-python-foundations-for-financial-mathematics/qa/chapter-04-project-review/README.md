# Chapter 4 — project/checklists/extensions scoped review

Based on main `20c43970b5a9b00a65d258e25388a27eca6db935`. [Review and worked extensions](REVIEW.md) · [Machine-readable register](review-register.json) · [Runner](review.py) · [Final results](results.json) · [Initial results](initial-results.json)

Run with standard-library CPython:

```bash
python3 -B books/book-01-python-foundations-for-financial-mathematics/qa/chapter-04-project-review/review.py
```

CPython 3.12.14 Linux: **45 runtime predicates passed**, plus **three command records passed**: exact-source direct execution (10 existing test methods), exact-source demo, and silent import. Counts are separate. Initial run passed 35 predicates and the same three commands; ten price-record checks were then added and final run passed 45. No failures occurred; initial results are retained, manuscript unchanged. No historical unique-method/workflow count is increased by this rerun.

Both source Python fences are extracted unchanged into a fresh temporary directory, with SHA-256 retained. The test-runner stderr and demo stdout are in results. Expected values for S0→S1→S2→S3 were independently derived by appending C3, absolutely replacing A with20 and removing B0, not by calculating a monetary total. Every intermediate quantity/order/revision is compared to explicit literals. The source demo independently asserts A12.5/C3 active rows and unchanged S0.

The 45 review records comprise 12 contract rows, six derived workflow steps, ten acceptance-checklist rows, nine extension prompts and eight Section4.12 design-checklist answers. These numbers describe review coverage, not test totals. Learning objectives map to validation/reference contracts1–3, command contracts4–6, ownership8, revision9, reporting7 and workflow steps2–6. Section4.13 troubleshooting maps directly to the recorded command/reference/revision/report/valuation boundaries. Earlier lab and 108 section-exercise records remain separate evidence.

New supplemental APIs implement fresh lookup, full membership, multi-portfolio reports, metadata wrappers and strictly supplied price-record validation. They do not change published code. Price records require positive exact finite Decimal per-instrument-unit quotes at explicit UTC instants, matching catalog currency, and unique security/time identity. No arithmetic or FX is performed; as-of selection, staleness, completeness and valuation precision/rounding require a later model. Lot identity, command-batch atomicity policy and persistence/concurrency are specifications only. Historical-label reuse and competing successors are executed documented limits, not remediated defects.

Scope now recorded for Chapter4: all12 section lab/workflows, all108 earlier section exercises, all20 chapter-wide answers, this project/acceptance workflow, listed checklists and nine extension prompts. This is scoped instructional review, not comprehensive coverage or independent acceptance. No static checker, Windows/macOS, live prices, notebook, tax accounting, durable transaction or independent reviewer ran here. F28 notebook/platform and F32 shared-input integration remain open.

Next: Chapter5 formal lab-step/worked-answer review. Start by inventorying current prompts/labs/checklists and consulting existing Chapter5 runtime/installed-wheel evidence, retaining dependency and platform limits. Reassess changed source hashes before reusing this checkpoint.
