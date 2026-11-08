# V-125 — Section 8.6 complete polynomial/derivative output

Candidate based on `5ad0dc3066bfcca85a3c50d1aac8a538c6459851`. Exact corrected source/check blobs are recorded in the [48-file scope manifest](chapter-08-section-06-polynomial-scope.json); publication commit provides their executable revision. [Initial nine-probe screen](chapter-08-section-06-polynomial-baseline.md) retained unchanged.

[Expanded baseline](chapter-08-section-06-polynomial-baseline-expanded.json):122 passed/5 failed out of127 executed predicates. [Pinned baseline replay](chapter-08-section-06-polynomial-baseline-replay.json) reproduces all127 observations identically. The excessive-order probe is explicitly omitted on the old source to avoid an unbounded loop; no old-source timeout pass/failure is invented. [Corrected observations](chapter-08-section-06-polynomial-corrected-expanded.json) and [corrected replay](chapter-08-section-06-polynomial-corrected-replay.json):128 passed/0 failed including that guard.

Failures are predicate mismatches, not distinct defect or COV-category counts. They include the two explicitly proposed finite-output/error policies from the earlier screen. The manuscript now adopts complete represented-input evaluation rounded only at the output, finite-output ValueError, signed underflow, exact-positive-zero, derivative-order and input-consumption conventions. Rational Horner fixes recoverable intermediate overflow/subnormal loss. Direct exact coefficient scaling avoids intermediate derivative overflow; order above degree exits immediately. Independent oracle uses monomial sums and direct falling-factorial references rather than Horner/repeated differentiation; Fraction backend is shared and is not independently certified.

```bash
python books/book-02-mathematical-foundations-for-finance-with-python/chapter-08/code/check_section_06_polynomial_range.py
python books/book-02-mathematical-foundations-for-finance-with-python/validation/chapter-08-section-06-polynomial-observer.txt . baseline 5ad0dc3066bfcca85a3c50d1aac8a538c6459851
python books/book-02-mathematical-foundations-for-finance-with-python/validation/chapter-08-section-06-polynomial-observer.txt . corrected
python books/book-02-mathematical-foundations-for-finance-with-python/validation/chapter-08-section-06-polynomial-scope-runner.txt .
```

Observer correction retained: an initial manual replay invocation supplied an invalid expanded revision ID and failed during git-show before any numerical probe ran. The supplied ID was replaced by the actual `git rev-parse HEAD` result above; subsequent baseline observations match identically. This invocation error is separate from numerical failures and corrected reruns.

All48 Chapter8 Python files compiled; all38 check/test scripts passed, with48 exact candidate blobs verified before/after. Actual per-script stdout/stderr and Python/platform retained. Fresh tree inventory590 Python files/377 scripts/591 required Python-fixture blobs is not a full runtime pass. [V-124](runtime-refresh-2026-11-08-r5.md),589/376/590 at its earlier pinned revision, remains the latest full candidate Linux run.

Limits: arbitrary coefficient count/degree resource growth, broader numerical/editorial coverage, independent review, supported platforms, release/canonical approval remain open. Thirty-five selected COV categories remain partially addressed; none closed. Next: Section8.6 sampled-second-difference numerator/denominator/output range and callback contracts with independently derived rational expectations. Do not repeat completed polynomial/PV/cash-flow examples.

Navigation correction: the previous checkpoint reused the Section8.2 polynomial baseline filename. Its original Section8.2 baseline Markdown is restored from `a02160a18fcb320ffb537ea5b5cf7bce8e64a3d3`; this Section8.6 screen is preserved under the distinct section-06 namespace. The existing Section8.2 follow-up/JSON evidence is unchanged. Earlier Section8.6 JSON/probe paths remain available as historical artifacts.
