# V-233 — Section10.3 finite stencil and complete secant quotient

Baseline: `878d165ae1d5ea05ff93b19a5963059fd1cf45ce`. [Runnable review](review.txt), [baseline](baseline.json), [baseline replay](baseline-replay.json), [corrected](first.json), [replay](replay.json), [polynomial support](polynomial-support.json), [composition support](composition-support.json), [Chapter10 support](chapter-support.json). Corresponding support .txt runners are retained in this directory and preserve their original baseline pins.

```bash
python books/book-02-mathematical-foundations-for-finance-with-python/validation/ch10-ftc-centered-2026-11-21/review.txt baseline --baseline
python books/book-02-mathematical-foundations-for-finance-with-python/validation/ch10-ftc-centered-2026-11-21/review.txt first
python books/book-02-mathematical-foundations-for-finance-with-python/validation/ch10-ftc-centered-2026-11-21/review.txt replay
python books/book-02-mathematical-foundations-for-finance-with-python/validation/ch10-ftc-centered-2026-11-21/polynomial-support.txt polynomial-support
python books/book-02-mathematical-foundations-for-finance-with-python/validation/ch10-ftc-centered-2026-11-21/composition-support.txt composition-support
python books/book-02-mathematical-foundations-for-finance-with-python/validation/ch10-ftc-centered-2026-11-21/chapter-support.txt chapter-support --chapter
```

Both baseline runs retain **17 passes/five failed predicates**: one explicit actual-span affine policy, two selected complete-quotient range extensions, and two finite-stencil/pre-callback policy checks. These are not five independent financial-model defects. Both corrected runs pass **22 predicates** with identical rows.

The source validates nominal t±h points as finite and strictly bracketing t before callbacks. It calls right then left, validates both returned values and combines their exact represented difference divided by the exact actual rounded stencil span before float reporting. True final overflow raises ValueError; underflow0 is permitted. Caller exceptions propagate; callback side effects during evaluation are not rolled back. Invalid stencils have no callback side effects.

Using the actual span is an explicit secant policy change from nominal2h: for t=1e16,h=3, rounded endpoints differ by8 rather than6, so the identity function returns1 rather than4/3. This does not guarantee an exactly centered stencil or derivative accuracy. Independent affine/quadratic/cubic identities, large-range constant-slope cases, subnormal points, type/finite guards and callback order are checked. A cubic at1,h=.5 yields3.25, distinct from the exact derivative3; the predicate intentionally tests finite-difference truncation, not an exact derivative claim. Arithmetic tolerance5e-14/atol0; exceptions/lists/zero exact. No arbitrary-domain, discontinuity, noisy-callback, resource or correctly-rounded universal guarantee is claimed.

Each scoped run executes CLI, strengthened native checker and compilation (three commands). Six native regression assertions extend the checker. Earlier27 polynomial and24 composition predicates pass (three commands each). Chapter support passes33 earlier10.2 predicates, compiles/verifies21 Python files and executes11 checkers/10CLI labs (22 commands). Candidate Git blob SHA/SHA256 identities are retained; baseline commit does not contain fixes. Fourteen prior exercise/six lab dispositions remain separate from new predicates.

Next: publish the coherent10.3 source/checker corrections, then full pinned Book2 runtime refresh before10.4. Latest full runtime remains V230 until then; no new full execution is claimed by this scoped record. All38 selected COV categories remain partial, none closed. Book2 and broader numerical/resource/provenance/model/supported-platform/release/independent/canonical gates remain open. Book1 has separate trackers.
