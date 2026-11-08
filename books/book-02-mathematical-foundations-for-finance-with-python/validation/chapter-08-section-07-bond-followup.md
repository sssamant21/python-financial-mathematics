# V-129 — Section8.7 complete bond price/derivative/reciprocal

Candidate based on `72aa53dd47dcb91d838e9ece800a1626486e3992`. [Original12-probe screen](chapter-08-section-07-bond-baseline.md) remains unchanged. [Expanded baseline](chapter-08-section-07-bond-baseline-expanded.json):115 passed/62 mismatches out of177;[baseline replay](chapter-08-section-07-bond-baseline-expanded-replay.json) reproduces all177 observations identically. [Corrected](chapter-08-section-07-bond-corrected.json):177 passed/0 failed. Mismatches are predicate observations,not distinct defects or COV totals.

The oracle directly sums complete discounted monomials using exact represented payments and the existing represented float1+y base. It derives the derivative directly and takes its exact reciprocal before reporting. Source uses Horner in reciprocal discount,with weighted original flows for the derivative. Separate algebra,shared Fraction backend;not arithmetic-library or external mathematical certification. Eight named vectors plus40seeded vectors cover ordinary/base controls,large positive sums,extreme positive/negative yields,weighted-payment/power range,subnormal reports,true output overflow and finite reciprocal sensitivity despite unreportable derivative. Domain/type/validation priority,unconsumed generators on invalid yield and one-shot iteration are actual checks for all3APIs.

The implementation validates once,forms exact complete expressions and converts only the final requested output. True nonfinite output ValueError and complete represented-base rounding are explicit policy adoption;some baseline mismatches are ordinary prior rounding differences,not prior promise violations. Positive-flow exact derivative never vanishes;the reciprocal API does not require its rounded report. Signed underflow is retained. No nonpositive flows are silently accepted or dropped.

```bash
python books/book-02-mathematical-foundations-for-finance-with-python/chapter-08/code/check_section_07_bond_range.py
python books/book-02-mathematical-foundations-for-finance-with-python/validation/chapter-08-section-07-bond-observer.txt . baseline-expanded 72aa53dd47dcb91d838e9ece800a1626486e3992
python books/book-02-mathematical-foundations-for-finance-with-python/validation/chapter-08-section-07-bond-observer.txt . baseline-expanded-replay 72aa53dd47dcb91d838e9ece800a1626486e3992
python books/book-02-mathematical-foundations-for-finance-with-python/validation/chapter-08-section-07-bond-observer.txt . corrected
python books/book-02-mathematical-foundations-for-finance-with-python/validation/chapter-08-section-07-bond-scope-runner.txt .
```

Final Chapter8 scope:51 Python files compiled and41 scripts passed,51 exact source/check blobs verified before/after in [scope evidence](chapter-08-section-07-bond-scope.json). Per-script stdout/stderr and Python/platform retained. Fresh inventory593 Python/380 scripts/594 required Python-fixture blobs is not a full run. V-127 remains latest full candidate Linux runtime pending accumulated-change refresh. No observer correction needed in this batch.

Thirty-five selected categories remain partially addressed;none closed. Independent review,supported platforms,resource/conditioning/release/canonical approval remain open. Next: Section8.7 exposure/circle-slope and centered-copy numerical/input/output contracts;broader implicit-function branch/model review remains separate. Book1 has independent progress.
