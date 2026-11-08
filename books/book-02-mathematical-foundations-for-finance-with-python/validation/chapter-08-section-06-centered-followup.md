# V-126 — Section 8.6 complete sampled second difference

Candidate based on `79b2bd3053d0099d7d1f8af7d8fb9c52d13781a3`; exact corrected source/check Git blobs in the [scope manifest](chapter-08-section-06-centered-scope.json). [Baseline](chapter-08-section-06-centered-baseline.json) has54 passed/16 mismatches; [baseline replay](chapter-08-section-06-centered-baseline-replay.json) reproduces all70 observations identically. [Corrected](chapter-08-section-06-centered-corrected.json):70 passed/0 failed. Mismatches are predicates, not distinct defect or COV counts.

Independent signed weighted sums of exact represented callback values and exact h² check complete sampled quotients. This differs from the source's explicit numerator expression but shares Fraction; it is an independent algebraic expectation, not arithmetic-library certification or external reviewer acceptance. Named fixtures cover constant huge samples, finite overflowing numerators, true final overflow, underflowed/overflowed float h², exact zero, negative step and signed underflow;50 seeded fixtures expand represented magnitudes. Callback traces check default/signed steps, order, count, validation priority, early invalid-return termination and exception propagation.

Source now evaluates the complete rational quotient before one final float conversion. Two explicit policy changes are separate from promise violations: finite results formerly rejected solely because float h² was zero/nonfinite are now accepted; true nonfinite final results raise ValueError instead of returning infinity. Callback controls/default/order remain. Already rounded sample values and represented perturbations define the quotient; no claim that it equals a derivative. The existing tiny-step quadratic cancellation example remains valid and passes.

```bash
python books/book-02-mathematical-foundations-for-finance-with-python/chapter-08/code/check_section_06_centered_range.py
python books/book-02-mathematical-foundations-for-finance-with-python/validation/chapter-08-section-06-centered-observer.txt . baseline 79b2bd3053d0099d7d1f8af7d8fb9c52d13781a3
python books/book-02-mathematical-foundations-for-finance-with-python/validation/chapter-08-section-06-centered-observer.txt . baseline-replay 79b2bd3053d0099d7d1f8af7d8fb9c52d13781a3
python books/book-02-mathematical-foundations-for-finance-with-python/validation/chapter-08-section-06-centered-observer.txt . corrected
python books/book-02-mathematical-foundations-for-finance-with-python/validation/chapter-08-section-06-centered-scope-runner.txt .
```

## Initial observer and legacy-regression failures retained

An initial mode named baseline-replay incorrectly selected the current source because the observer recognized only exact mode baseline. [Mis-selected observation](chapter-08-section-06-centered-observer-initial-replay.json) is not baseline evidence. The selector now recognizes baseline-prefixed modes; the corrected baseline replay has identical70 observations.

The first scope run stopped at check_difference_denominators.py: two Section8.6 assertions required rejection of zero/infinite rounded h². [Actual failed checker rerun](chapter-08-section-06-centered-legacy-initial.json) retains stdout/stderr, exit1 and original checker/corrected source hashes. After explicit policy reconciliation, only the Section8.6 assertions now expect its exact sampled quotient (zero for the underflowed callback quadratic and huge-step constant). Other Section8.8/8.10/helper rejection assertions remain. Five historical unittest methods unchanged in count; no invented pass for the initial run. Final scope runner retains all script results before asserting aggregate success.

Final scoped run:49 Chapter8 Python files compiled and39 check/test scripts passed; exact49 source/check blobs matched before/after. Fresh inventory591 Python/378 scripts/592 required Python-fixture blobs is not a full pass. V-124 remains latest full candidate Linux run until a fresh pinned refresh executes. Thirty-five selected COV categories remain partially addressed; none closed. Independent mathematical/editorial review, platform, resource, release and canonical acceptance remain open.

Next substantive item: Section8.7 implicit helper circle/break-even numerical range and output/input contracts, followed by bond/exposure/centered-copy obligations. Broader COV-49 noisy/wrong-reference/resource cases remain open; do not repeat completed Section8.6 scaling examples.

Corrected executable publication pin: `1c7aa7fb7d3fd229f77ef9d0a03584d010e9f9f2`; all31 publication blobs verified, including the tested49-file Chapter8 scope. Concurrent unrelated main work preserved with expected-head lease.
