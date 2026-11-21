# V-229 — Section 10.2 exponential complete-expression contracts

Baseline: `ce38a04197aef40afd31e54adbb8d0bdadc588a3`. [Runnable review](review.txt), [baseline](baseline.json), [baseline replay](baseline-replay.json), [corrected run](first.json), [corrected replay](replay.json), [initial checker failure](initial-checker-failure.json), [Chapter10 support](chapter-support.json), [midpoint support](midpoint-support.json).

```bash
python books/book-02-mathematical-foundations-for-finance-with-python/validation/ch10-exponential-2026-11-21/review.txt baseline --baseline
python books/book-02-mathematical-foundations-for-finance-with-python/validation/ch10-exponential-2026-11-21/review.txt first
python books/book-02-mathematical-foundations-for-finance-with-python/validation/ch10-exponential-2026-11-21/review.txt replay
python books/book-02-mathematical-foundations-for-finance-with-python/validation/ch10-exponential-2026-11-21/polynomial-support.txt chapter-support --chapter
python books/book-02-mathematical-foundations-for-finance-with-python/validation/ch10-exponential-2026-11-21/midpoint-support.txt midpoint-support
```

Baseline runs retain **12 passes/ten failed predicates**, identically repeated. Failures span zero-scale/width identities, constant complete endpoint differences, selected scaled finite-result range extensions and true overflow/underflow reporting. These are predicates, not ten independent financial-model defects. Both corrected runs pass **22 predicates** identically. The initially typed native-checker constant for a scaled growing case was wrong: its command failure, stdout/stderr, manifest and already-passing independent22 predicates are retained. The independent oracle supplied the corrected constant3.3851373959875596e134. This observer/checker correction is separate from source failures.

The independent oracle uses exact represented-float Fraction inputs, 800-digit arithmetic, argument halving, a converged Taylor sum and repeated squaring. It never calls Decimal.exp or the source exponential helper. Source instead uses Decimal.exp with anchored endpoints and the stable positive gap factor. Independent constant/zero identities and the very-wide decaying limit complete the selected cases. Relative tolerance5e-14 with zero absolute tolerance prevents tiny expected results from silently passing as zero. Input/exception/zero checks are exact.

The source validates all inputs, short-circuits zero scale/width, combines exact constant products, and evaluates nonzero-growth magnitude in a fresh800-digit context before one float report. The manuscript derives conservative ±10000 exponent/gap guards from binary64 input bounds; this avoids enormous Decimal exponential arguments. Complete finite results such as scale1e-300 over [1000,1001] or scale1e300 over [-1000,-999] now survive intermediate exponent overflow/underflow. True final overflow raises ValueError; final underflow0 is permitted. No correctly-rounded-transcendental theorem, arbitrary precision/resource acceptance or signed-zero convention is claimed.

Each review executes source CLI, strengthened checker and compilation: three command records per run. The separate Chapter10 support run passes the earlier33 polynomial/ordinary predicates, compiles/verifies21 Python files and passes11 checkers/10CLIs (22 commands). Midpoint support repeats its22 predicates and three commands successfully. Copied support runners preserve their original baseline pins deliberately. Exact candidate blob SHA/SHA256 identities are retained; the new source is not in the baseline commit.

Next: publish the coherent polynomial/midpoint/exponential source/checker batch, then refresh full pinned Book2 runtime before advancing to10.3. Latest full runtime remains V226 until that refresh. All38 selected COV categories remain partial, none closed. Fourteen earlier exercise/six lab-review dispositions remain distinct from new predicates. Book2 and broader resource, provenance, model, supported-platform, release, independent and canonical acceptance remain open. Book1 has separate trackers.
