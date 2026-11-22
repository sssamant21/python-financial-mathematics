# V-240 — Section10.5 exponential/constant/growing kernel; partial lab crosswalk

Baseline source: `199352a9f3398bb2bdd2b2fe3eee5ec42e605a76`. [Runnable review](review.txt), [baseline](baseline.json), [baseline replay](baseline-replay.json), [corrected first](first.json), [corrected replay](replay.json), [chapter runner](chapter-support.txt), [chapter support](chapter-support.json), [fresh inventory](inventory.json).

```bash
python books/book-02-mathematical-foundations-for-finance-with-python/validation/ch10-payment-kernel-2026-11-21/review.txt baseline --baseline
python books/book-02-mathematical-foundations-for-finance-with-python/validation/ch10-payment-kernel-2026-11-21/review.txt first
python books/book-02-mathematical-foundations-for-finance-with-python/validation/ch10-payment-kernel-2026-11-21/review.txt replay
python books/book-02-mathematical-foundations-for-finance-with-python/validation/ch10-payment-kernel-2026-11-21/chapter-support.txt
```

Baseline20 passes/eleven failed predicates reproduce identically. Corrected31 predicates pass twice:26 selected kernel/input/final-result cases and five ordinary assessment PV fields. Failed predicates are observations, not eleven separately classified defects. The baseline manifest is the exact old source/checker; corrected manifests identify candidate blobs (the older pin does not contain fixes). Source selection is explicit. All actual command outputs and exception types are retained. Each scoped run invokes the native CLI/checker and compilation (three commands). Chapter support stages all21 Python files, compiles them and runs eleven checkers/ten lab CLIs (22 commands); hashes are unchanged after. Eight native regression assertions are added, separate from31 supplemental predicates.

The independent oracle uses800-digit halving/Taylor/squaring exponential evaluation and exact represented-input fractions, not the source Decimal.exp implementation or midpoint agreement. Relative tolerance3e-15, absolute0 avoids concealing tiny/subnormal failures. The selected exact difference (growth1,discount−1e−16,horizon700,scale1e−300) is retained before exponentiation; rounding the difference to1 loses about7e−14 relatively. Ordinary five report PVs are checked, but report schema, quadrature, curve value and derivative coverage are deferred.

Corrections retain exact scale/time/exponent arithmetic before reporting: zero scale/horizon after validation; exact constant multiplication; anchored800-digit exponential with scale integrated before float conversion; exact growing-rate difference even when ordinary subtraction overflows. Examples include c1e308,k−1,T2→8.6466471676e307; c1e−300,k1,T1000→1.9700711140e134; c1,g−1e308,r1e308,T1→5e−309. Raw `OverflowError` for final exponential overflow becomes declared `ValueError`. Report underflow0 is allowed. These selected finite-range support extensions and validation policies are explicit, not universal all-finite-input correctness claims.

For nonzero validated floats |c|≥2^-1074 and |k|≤2^1025 (growing difference included). Thus |c/k|≥2^-2099, and e^10000 makes a positive-exponent integral unreportable even at that smallest prefactor; the10000 growth cutoff cannot discard a finite selected result. For gap>10000, replacing1−e^-gap by1 has negligible relative error, well below binary reporting. Tiny nonzero products can be as small as2^-2148;800 digits leave guard digits for the selected cancellation. Decimal precision is finite, not a correctly-rounded guarantee; exact arithmetic and high precision carry resource costs and no arbitrary workload/time guarantee. Finite conversion retains the prior float-input semantics (large ints converted to finite float).

|Lab/project review unit|Current disposition|
|---|---|
|Prerequisites/units and deterministic curve conventions|Conceptual crosswalk: currency/year payment rate, year horizon, continuous inverse-year rates; no stochastic-short-rate/calibration claim|
|Constant/growing stream kernels and r=g|Selected independent source predicates and ordinary PV benchmarks pass; boundary/range policies above|
|Linear stream / J moment|Ordinary native checker runs; substantive range/composition review remains next|
|Midpoint quadrature|Ordinary CLI/checker runs; grid/callback/complete-sum contracts pending|
|Variable deterministic curve and rate sensitivity|Ordinary native runs only; complete-expression/range/oracle review pending|
|Report/project acceptance and reproducibility|Five exact PV fields reviewed; remaining report fields/schema/flags/provenance/meaningful resolution/error claims pending|

Fourteen existing exercises are reconciled as dispositions, not new test counts:1/2/3/5/6 map to ordinary constant/growing checks;4 units,8 deterministic curve formula,9/10 nonnegative-flow inequalities,13 bp conversion and14 model-versus-numerics are conceptual;7 linear PV and11/12 derivative integrals await substantive source contracts. The applied project is partially reviewed, not completed. Ten escaped backticks repaired so existing lab commands render as runnable fences. Runtime checklist now distinguishes scoped execution from the remaining full-runtime gate.

Fresh candidate inventory:642 Python files,429 check/test scripts,643 required Python/fixture blobs;641/643 match V239, only10.5 source/checker differ. This is not a new full runtime. Retain V239's pinned642/429/643 pass. Next:10.5 time-weighted moment and complete linear-PV contracts, then midpoint/variable-curve/sensitivity/full-report obligations; fresh full runtime after coherent accumulated code changes and before10.6. All38 selected COV categories remain partially addressed, none closed; these are not defect counts or percentages. Broader numerical/resource/provenance/model/platform/release/independent/canonical gates remain open. Book1 evidence/trackers remain separate.
