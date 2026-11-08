# V-131 — Section8.7 implicit ratios and centered copy

Candidate based on `2e211d5f6b7c0d1875a7f84000083ddaca425554`. [Original9-probe screen](chapter-08-section-07-exposure-centered-baseline.md) retained. [Expanded baseline](chapter-08-section-07-slopes-centered-baseline-expanded.json):117 passed/34 mismatches of151;[baseline replay](chapter-08-section-07-slopes-centered-baseline-expanded-replay.json) reproduces all151 observations identically. [Corrected](chapter-08-section-07-slopes-centered-corrected.json):151 passed/0 failed. Predicate mismatches are not distinct defect/COV totals.

Independent exact rational complete ratios derive-x/y and-a*x/(b*y);the source likewise uses complete rational arithmetic,so algebra/backend sharing is explicit andnot library certification. Seven named plus40seeded input tuples exercise numerator/denominator range,signed outputs,underflow,true final overflow andzero identities. Centered references derive the sampled numerator/2h from represented outputs;seven named plus35seeded cases andactual callback traces check output range,zero signs,negative/default steps,preflight,callback order,early invalid-return termination andexception propagation. These are sampled quotient expectations,not proof of an analytical derivative or optimal step size.

Source now avoids intermediate products/quotients andreports only final floats. True nonfinite-output ValueError andpre-callback rejection of collapsed/nonfinite perturbations are explicit policy reconciliation,not assumed prior promises. Exact ratio zeros preserve-x/y;centered exact zeros preserve represented numerator-zero andstep signs. Existing domains,finite/type/input order anddefault/signed step remain. No narrowing to positive y or exclusion of valid signed x was introduced.

```bash
python books/book-02-mathematical-foundations-for-finance-with-python/chapter-08/code/check_section_07_slopes_centered.py
python books/book-02-mathematical-foundations-for-finance-with-python/validation/chapter-08-section-07-slopes-centered-observer.txt . baseline-expanded 2e211d5f6b7c0d1875a7f84000083ddaca425554
python books/book-02-mathematical-foundations-for-finance-with-python/validation/chapter-08-section-07-slopes-centered-observer.txt . baseline-expanded-replay 2e211d5f6b7c0d1875a7f84000083ddaca425554
python books/book-02-mathematical-foundations-for-finance-with-python/validation/chapter-08-section-07-slopes-centered-observer.txt . corrected
python books/book-02-mathematical-foundations-for-finance-with-python/validation/chapter-08-section-07-slopes-centered-scope-runner.txt .
```

Final Chapter8 scope52compiled/42scripts passed;52exact candidate input blobs verified before/after in [scope evidence](chapter-08-section-07-slopes-centered-scope.json),with actual stdout/stderr andPython/platform. Fresh inventory594Python/381scripts/595required Python-fixture blobs is not a full runtime. [V-130](runtime-refresh-2026-11-08-r7.md) remains latest full candidate Linux evidence at its earlier pin(593/380/594). No observer correction needed.

Thirty-five selected categories remain partially addressed;none closed. Broader implicit-function branch/conditioning/noise/resource,independent mathematical/editorial review,supported-platform,release andcanonical acceptance remain open. Next:Section8.8 remaining complete sampled-quotient/Richardson range contracts andfinancial-helper obligations,without repeating completed guard-only checks. Book1 progress remains independent.

Corrected executable/source revision:`9079c61bf30d0223278e740c0fbbb617f8c4b35d`. [Publication verification](chapter-08-section-07-slopes-centered-publication-verification.json) pins tested input identities andverified source tree;the following metadata commit does not change these executed sources.
