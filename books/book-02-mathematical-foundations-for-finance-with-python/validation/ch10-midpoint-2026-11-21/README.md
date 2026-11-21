# V-228 — Section 10.2 midpoint contracts, partial checkpoint

Baseline pin: `477083a59f74be60e5e5766f4cd9ec5c8b1656b9`. [Runnable midpoint review](review.txt), [baseline](baseline.json), [baseline replay](baseline-replay.json), [corrected run](first.json), [corrected replay](replay.json), [initial observer](initial-observer.json), [Chapter 10 support](chapter-support.json), [support runner](polynomial-regression.txt), [full-runtime delta](runtime-delta.json).

Run from the repository root:

```bash
python books/book-02-mathematical-foundations-for-finance-with-python/validation/ch10-midpoint-2026-11-21/review.txt baseline --baseline
python books/book-02-mathematical-foundations-for-finance-with-python/validation/ch10-midpoint-2026-11-21/review.txt first
python books/book-02-mathematical-foundations-for-finance-with-python/validation/ch10-midpoint-2026-11-21/review.txt replay
python books/book-02-mathematical-foundations-for-finance-with-python/validation/ch10-midpoint-2026-11-21/polynomial-regression.txt chapter-support --chapter
```

Both baseline runs retain **16 passes and six failures**. These are failed predicates, not six independent defects: unreportable sum exception normalization, two selected finite-result range extensions (overflowing products that cancel, and an overflowing interval difference), and three explicit grid-policy/side-effect predicates. The initial observer expected a nonzero result for a subnormal interval with no representable interior sample. That expectation was replaced by the documented grid-rejection policy before baseline replay and source correction; the original observer is retained, not counted as another source defect.

Both corrected midpoint runs pass **22 predicates** with identical rows. Native ordinary linear/reversed amounts, five quadratic convergence references, zero-width no-callback behavior, type/nonfinite inputs, caller exception propagation, selected range/report cases and sample positions are checked. The independent quadratic formula is 1/3−1/(12n²), derived from finite sums of integer powers. Large-width references use exact represented endpoint differences; they do not subtract the source's computed primitives. Comparisons use rtol 5e-14 and zero absolute tolerance; exception types, lists and zero checks are exact.

The source constructs each midpoint with rational endpoint arithmetic, converts the sample once, and requires it to lie strictly inside its exact subinterval. All points preflight before any callback. Invalid fine grids now raise ValueError instead of silently sampling endpoints or duplicates. Complete callback-value × signed-width products and their sum are exact before one final float report; true overflow becomes ValueError. Finite underflow to zero remains allowed. The callback's own exception propagates; callback side effects during later evaluation are not rolled back. O(n) preflight storage and Fraction costs are explicit new tradeoffs, not resource acceptance.

Each midpoint review runs the exact source CLI, strengthened native checker and compilation: three actual commands per run. The separate support runner repeats the earlier 33 polynomial/ordinary-lab predicates successfully and compiles/verifies all 21 Chapter 10 Python files, executes eleven checkers and ten CLI labs (22 command records). It records candidate blob SHA/SHA256 and manuscript identity; the baseline pin itself does not contain the fixes. The support runner retains its original polynomial baseline pin by design. No full-book runtime is claimed for this candidate.

Inventory remains 642 Python files, 429 check/test scripts and 643 required source/fixture blobs. Only Section 10.2 source and checker differ from V226 (641/643 match). Latest full execution remains pinned to V226 at ad0f11b8eb295b0c062256a47d869044b874aa77. Refresh after the remaining coherent exponential batch before advancing to 10.3.

**Next remains Section 10.2 exponential integration:** complete-expression/range, zero-width, cancellation, rounding and reporting contracts. Its implementation is unchanged and not accepted by ordinary CLI examples. The section, lab and book are not declared complete. Earlier fourteen exercise/six lab-review dispositions remain distinct from these predicates. All 38 selected COV categories remain partial, none closed; broader resource, provenance, model, supported-platform, release, independent and canonical acceptance stays open. Book 1 has separate trackers.
