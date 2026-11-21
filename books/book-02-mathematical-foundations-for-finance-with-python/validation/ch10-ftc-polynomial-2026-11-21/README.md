# V-231 — Section10.3 polynomial value/accumulation, partial checkpoint

Baseline pin: `3a9dddb78f225bef1cd59241f28ea8d5e0a87744`. [Runnable review](review.txt), [baseline](baseline.json), [baseline replay](baseline-replay.json), [corrected run](first.json), [corrected replay](replay.json), [Chapter10 support](chapter-support.json), [support runner](chapter-support.txt), [full-runtime delta](runtime-delta.json).

```bash
python books/book-02-mathematical-foundations-for-finance-with-python/validation/ch10-ftc-polynomial-2026-11-21/review.txt baseline --baseline
python books/book-02-mathematical-foundations-for-finance-with-python/validation/ch10-ftc-polynomial-2026-11-21/review.txt first
python books/book-02-mathematical-foundations-for-finance-with-python/validation/ch10-ftc-polynomial-2026-11-21/review.txt replay
python books/book-02-mathematical-foundations-for-finance-with-python/validation/ch10-ftc-polynomial-2026-11-21/chapter-support.txt chapter-support --chapter
```

Baseline/replay preserve **19 passes/eight failed predicates**. Selected tiny-coefficient/large-power values, zero coefficients with overflowing powers, complete signed product cancellation, zero-width primitive handling and final-overflow normalization fail. These predicates are not eight independent financial-model defects. Four cases are explicitly finite-result range extensions. Both corrected runs pass **27 predicates** identically: twenty polynomial/input/report contracts plus all seven ordinary CLI numeric fields. The numerical derivative CLI field uses rtol/atol1e-8 for finite-difference error; other comparisons use rtol5e-14/atol0, exceptions/zero identities exact.

The source now converts finite binary64 inputs once, consumes coefficients once and uses exact Fraction products, powers and endpoint differences before one final float report. Zero coefficients are skipped; zero-width amounts still validate nonempty finite coefficients. True final overflow raises ValueError, final underflow0 is allowed. No signed-zero rule or arbitrary-degree/length/bit-size resource guarantee is added. Exact constant/linear references and rational complete expressions are independent of the source outputs. This represented-input policy is distinct from Book1's displayed-decimal risk policy.

Each scoped run executes the complete source CLI, strengthened native checker and compilation (three commands). Nine regressions extend the existing checker. The separate support runner passes the earlier33 polynomial/ordinary10.2 predicates, compiles/verifiesall21 Chapter10 Python files and executeseleven checkers/ten CLI labs (22 commands). Copied support runner deliberately retains its original10.2 baseline pin. All candidate source/checker Git blob SHA/SHA256 identities are recorded; the baseline commit does not contain fixes.

The runbook's eight escaped backticks are repaired and its status/checklist now names the partial scope. Earlier conceptual/lab alignment is reviewed as six units: FTC continuity/interior-domain prerequisites; signed/oriented accumulation and units; initial-balance composition; variable endpoint chain factors/sign; rolling-window removal; and finite-difference/discontinuity limits. These are review units, not six executable tests.

Fourteen exercise dispositions stay separate:1/2 FTC linear derivative/amount,3 quadratic primitive difference16,4 caller balance400,5 variable upper endpoint chain rule,6 rolling quadratic derivative2t+1,7 nonpolynomial exponential chain expression (conceptual, not a symbolic API),8/9 amount2025/balance3025,10 signed net0,11 units,12 one-sided jump slopes0/2,13 antiderivative additivity,14 rolling removal term. Ordinary applicable CLI/checker cases execute; no universal endpoint, discontinuity or symbolic integration acceptance follows.

**Section10.3 remains unfinished.** `balance`, `endpoint_derivative`, rolling helpers and `centered_derivative` are unchanged. Next review their complete-expression, one-pass collection, interval/step preflight, callback and reporting contracts, then refresh the full runtime before10.4. No completion is inferred from ordinary examples. Latest full run remains V230 at278fe361a26394ce4d2c5d1e1955d804994e150a. Fresh inventory642/429/643;641 of643 required blobs match, only10.3 source/checker differ. No new full-book run is claimed.

All38 selected COV categories remain partial, none closed. Broader numerical/resource/provenance/model/supported-platform/release/independent/canonical acceptance remains open; Book2 is not complete. Book1 has separate trackers.
