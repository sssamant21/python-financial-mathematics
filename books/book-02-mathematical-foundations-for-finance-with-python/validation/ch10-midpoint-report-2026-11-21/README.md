# V-238 — Section10.4 midpoint and fixed assessment contracts

Baseline: `cdf2679391b0060db8465c0de08c09c632d658e6`. [Runnable review](review.txt), [baseline](baseline.json), [baseline replay](baseline-replay.json), [corrected](first.json), [replay](replay.json), [PV support](pv-support.json), [kernel/full ordinary-report support](kernel-support.json), [Chapter10 support](chapter-support.json). Matching support .txt runners retain their original baseline pins.

```bash
python books/book-02-mathematical-foundations-for-finance-with-python/validation/ch10-midpoint-report-2026-11-21/review.txt baseline --baseline
python books/book-02-mathematical-foundations-for-finance-with-python/validation/ch10-midpoint-report-2026-11-21/review.txt first
python books/book-02-mathematical-foundations-for-finance-with-python/validation/ch10-midpoint-report-2026-11-21/review.txt replay
python books/book-02-mathematical-foundations-for-finance-with-python/validation/ch10-midpoint-report-2026-11-21/pv-support.txt pv-support
python books/book-02-mathematical-foundations-for-finance-with-python/validation/ch10-midpoint-report-2026-11-21/kernel-support.txt kernel-support
python books/book-02-mathematical-foundations-for-finance-with-python/validation/ch10-midpoint-report-2026-11-21/chapter-support.txt chapter-support --chapter
```

Both baseline runs retain **24 passes/nine failed predicates**: zero-width callback policy, selected overflowing/canceling or underflowed products, final-overflow exception normalization, wide intervals and explicit representable-interior grid/pre-callback policies. These are not nine independent financial-model bugs. Both corrected runs pass **33 predicates** identically:23 midpoint/input/callback/numeric contracts and10 fixed-report schema/model/CLI-agreement checks.

The midpoint implementation adopts the selected10.2 contract: exact rational endpoint/sample preflight, strict interior rounded points and a zero-width no-callback result after validation. Exact callback-value×signed-width products and their full sum report once. This preserves a minimum-subnormal final integral even when two individually rounded products would each become zero, and selected cancellation/wide-interval results. True final overflow→ValueError; underflow0 allowed; caller exceptions propagate and already-evaluated callback effects are not rolled back. Invalid grids reject before callbacks. Preflight is O(n) storage plus exact-arithmetic costs, not arbitrary-count/resource acceptance.

Independent linear/quadratic integral identities, orientation, exact represented endpoint differences and sample positions supply expectations. Unrepresentable tiny/adjacent-endpoint grids are deliberately rejected, even for constant functions; this is an explicit policy rather than a universal mathematical integration limitation. Numeric tolerance is rtol5e-14/atol0; zero/list/schema/exception checks exact. The algorithm matches an existing reviewed source policy, while test oracles remain separate closed-form arithmetic.

The existing assessment has no parameters: five fixed rates, fixed a1000/b100/T2/n1000. Its complete numerical output already passes the independent35-field/schema/flag review within55 support predicates. New checks verify exact report/row key sets, negative/zero/positive-rate invariants and CLI/function equality. No hypothetical generalized report-input API is invented. absolute_difference measures reported analytical/quadrature discrepancy, not a rigorous error bound. Runtime/reviewer flags stay false. The assessment implementation itself did not require a source change.

Each scoped run executes CLI, strengthened native checker and compilation (three commands). Eight native regression assertions are added. Earlier21 complete-PV and55 kernel/report predicates pass. Chapter support passes33 earlier predicates, compiles/verifies21 Python files and executes11 checkers/10CLI labs (22 commands). Candidate Git blob SHA/SHA256 identify the tested source/checker; baseline pin does not contain fixes. Exercise/lab records remain separate from predicates.

Next: publish the accumulated10.4 source/checker batch, then full pinned runtime refresh before10.5. The latest full run remains V234 until that refresh; this scoped record does not claim a new full execution. Selected contracts do not close resource/continuous-model/all-float numerical obligations. All38 selected COV categories remain partial, none closed. Book2 and numerical/provenance/model/supported-platform/release/independent/canonical acceptance stay open; Book1 has separate trackers.
