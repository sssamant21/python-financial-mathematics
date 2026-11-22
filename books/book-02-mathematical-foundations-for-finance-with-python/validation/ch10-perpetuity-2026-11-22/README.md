# V-247 — Section10.6 perpetuity convergence and complete quotient; partial lab

Baseline source: `e29f14d85ecbdf6bde690da001b06d61fa191865`. [Runnable review](review.txt), [baseline](baseline.json), [baseline replay](baseline-replay.json), [corrected first](first.json), [corrected replay](replay.json), [chapter runner](chapter-support.txt)/[results](chapter-support.json), [fresh inventory](inventory.json), [documentation guard correction](documentation-correction.json).

```bash
python books/book-02-mathematical-foundations-for-finance-with-python/validation/ch10-perpetuity-2026-11-22/review.txt baseline --baseline
python books/book-02-mathematical-foundations-for-finance-with-python/validation/ch10-perpetuity-2026-11-22/review.txt first
python books/book-02-mathematical-foundations-for-finance-with-python/validation/ch10-perpetuity-2026-11-22/review.txt replay
python books/book-02-mathematical-foundations-for-finance-with-python/validation/ch10-perpetuity-2026-11-22/chapter-support.txt
```

Baseline18 passes/seven failed predicates reproduce identically. Corrected25 predicates pass twice:16 finite/exact-report cases and nine convergence/type/domain/final-overflow checks. Each run stages exact source/checker blobs and invokes native CLI/checker/compilation (three commands); actual outputs/exception types/environment and Git blob/SHA256 identities retained. Candidate fixes are not falsely attributed to baseline pin. Seven added native regressions are separate from25 supplemental predicates. Chapter support compiles21 Python files and executes eleven checkers/ten lab CLIs (22 commands), staged identities unchanged after. Predicate failures are observations, not seven independently classified defects or new COV categories.

The oracle uses1800-digit Decimal arithmetic from exact binary-float conversions, independently of source Fraction subtraction/division. It retains the complete difference before quotient/reporting; selected outputs compare **exactly as floats** to expose last-bit rate-rounding loss rather than hide it with loose tolerance. E.g. C1,g−1e−16,r1 gives.9999999999999999 instead of1; C1e308 with the same rates gives9.999999999999998e307. Exact symbolic identities support overflowed-difference cases:C1e308,g−1e308,r1e308→.5; negative C→−.5; C1→5e−309. Near-equality positive decay and minimum-subnormal rate cases are included. The oracle precision is far beyond selected finite-input cancellation scales; no general arbitrary-precision API or decimal market-rate interpretation is asserted.

Correction is scoped to **perpetuity_pv**. Validate all finite-float inputs before zero payment; c0 is identically zero for any finite g/r, including rate differences outside float range. For nonzero positive or negative c, classify exact represented d=r−g>0 before evaluating c/d. Zero/negative d diverges and raises ValueError. Convert the exact ratio to float once; true final overflow raises ValueError and underflow0 is allowed. Exact intermediate rationals carry workload costs with no arbitrary runtime/memory guarantee. Existing `inputs` still supplies rounded float decay to finite-horizon/tail/target helpers; those are explicitly unfinished, not silently certified by this correction.

|Lab/project review unit|Disposition|
|---|---|
|Prerequisites and units|Finite rates/payment inputs; currency/year and continuous inverse-year rates; actual real valuation date/currency unspecified|
|Infinite-horizon convergence/zero/signed streams|Selected native convergence/quotient checks and independent exact-input expectations recorded|
|Finite-horizon stream|Ordinary native execution only; complete-expression/range contracts next|
|Tail decomposition and target horizon|Ordinary native checks only; tail/target numerical contracts next|
|p-integrals, endpoint singularities and comparison tests|Manuscript analytic examples reviewed conceptually; substantive p-helper contracts and proof crosswalk remain pending; no singular-integration API invented|
|Fixed assessment/report/model risk|Native CLI/checker runs support only; full independent report/provenance crosswalk and fresh full runtime remain pending|

Fourteen exercises are dispositions, not new tests:2/5 native worked perpetuity cases execute;3/4 are convergence conditions;1/6/7/8 are limit/tail formulas awaiting full source crosswalk;9/10 await p-helper contracts;11/12 one-sided singularity derivations are conceptual;13 derivative−C/(r−g)² is analytic, no new derivative API claimed;14 separates finite truncation from convergence/model suitability. Real payer survival/default/regimes and infinite extrapolation are not validated by finite arithmetic. The report builder initially expected ten escaped backticks, observed twelve and stopped before Book2 mutation; the separate documentation guard record retains that correction. Twelve escaped backticks repaired so existing learner commands render as code; runtime checklist distinguishes scoped execution from remaining progression gates.

Fresh inventory642 Python/429 check-test/643 required blobs;641/643 V246 blobs match, only10.6 source/checker differ. This is not a new full run; V246 retains its own pinned642/429/643 pass. Next:10.6 finite-horizon complete-expression and tail-value contracts, then target-horizon/p-integral/report/proof/navigation obligations; fresh pinned full runtime before10.7. All38 selected COV categories remain partial, none closed, distinct from defects/percentages. Broader numerical/resource/provenance/model/platform/release/independent/canonical gates stay open. Book1 separate.
