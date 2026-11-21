# V-232 — Section10.3 composition contracts, partial checkpoint

Baseline: `99b03b4ce334912f4731ee730d8fbdf60f06bb6a`. [Runnable review](review.txt), [baseline](baseline.json), [baseline replay](baseline-replay.json), [corrected](first.json), [replay](replay.json), [polynomial support](polynomial-support.json), [polynomial runner](polynomial-support.txt), [chapter support](chapter-support.json), [chapter runner](chapter-support.txt), [full-runtime delta](runtime-delta.json).

```bash
python books/book-02-mathematical-foundations-for-finance-with-python/validation/ch10-ftc-composition-2026-11-21/review.txt baseline --baseline
python books/book-02-mathematical-foundations-for-finance-with-python/validation/ch10-ftc-composition-2026-11-21/review.txt first
python books/book-02-mathematical-foundations-for-finance-with-python/validation/ch10-ftc-composition-2026-11-21/review.txt replay
python books/book-02-mathematical-foundations-for-finance-with-python/validation/ch10-ftc-composition-2026-11-21/polynomial-support.txt polynomial-support
python books/book-02-mathematical-foundations-for-finance-with-python/validation/ch10-ftc-composition-2026-11-21/chapter-support.txt chapter-support --chapter
```

Both baseline runs retain **twelve passes/twelve failed predicates**. They cover lost low-order balance amounts, premature primitive reporting, unguarded true final overflow, reused one-pass coefficients, complete endpoint-product cancellation, rounded-away rolling windows and rolling primitive cancellation. Four cases are explicitly complete-expression range extensions; failed predicates are not twelve independent financial-model bugs.

Both corrected runs pass **24 predicates** with identical rows. Source polynomial value/amount helpers now have internal exact-expression variants. Balance combines the initial value with the entire integral before reporting; endpoint derivatives consume coefficients once and combine both rate-weighted endpoint expressions before conversion. Rolling amount/derivative use the exact represented t−window rather than a rounded intermediate endpoint. Zero/nonpositive/invalid windows and malformed coefficients remain guarded. True final overflow raises ValueError; final underflow0 is allowed. No signed-zero or arbitrary-degree/bit-size resource guarantee is added.

Independent references use closed-form constant/linear/quadratic identities and exact represented binary64 inputs. In particular, balance1e16 plus integral−1e16+1/2 must report1/2; a unit rolling window at1e16 retains length1; the linear rolling derivative is its exact window length. Numeric checks use rtol5e-14/atol0; exception/zero outcomes exact. No source primitive outputs are used to manufacture expected cancellation results.

Each corrected scoped run executes complete CLI, strengthened checker and compilation (three commands). Eleven regressions extend the existing native checker. The prior polynomial review's27 predicates and ordinary CLI fields pass (three commands), and the chapter support runner passes its earlier33 predicates, compiles/verifiesall21 Chapter10 Python files and executes11 checkers/10CLI labs (22 commands). Support runners deliberately keep their original baseline pins. Candidate Git blob SHA/SHA256 identities are recorded; the baseline pin does not contain these changes.

The source still excludes interest-on-balance, discounting, costs and contractual discontinuities. Endpoint rates are caller-supplied derivatives in compatible time units. Rolling windows must lie in the modeled polynomial domain; exact internal endpoints can differ from what an intermediate binary64 subtraction would represent. No external callback is sampled by these polynomial composition routines. Exact arithmetic may increase resource use.

**Section10.3 remains in progress.** `centered_derivative` is unchanged: its full stencil representation, preflight/callback, complete quotient, cancellation/rounding and reporting contracts remain next, followed by full pinned runtime refresh before10.4. Ordinary finite-difference examples do not close those obligations. Earlier fourteen exercise/six lab units remain distinct from new predicates. Latest full run is V230 at278fe361a26394ce4d2c5d1e1955d804994e150a; fresh inventory642/429/643,641 of643 required blobs match, only10.3 source/checker differ. No new full-book execution is claimed.

All38 selected COV categories remain partial, none closed. Broader numerical/resource/provenance/model/supported-platform/release/independent/canonical acceptance remains open. Book1 has separate trackers.
