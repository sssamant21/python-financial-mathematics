# V-132 — Section8.8 complete sampled quotients/Richardson

Candidate based on `dea228397b36589d91f7b325b48a8165a5c43a4e`. [Original7-probe screen](chapter-08-section-08-complete-quotient-baseline.md) retained. [Expanded baseline](chapter-08-section-08-complete-quotient-baseline-expanded.json):161passed/18mismatches of179;[baseline replay](chapter-08-section-08-complete-quotient-baseline-expanded-replay.json) reproduces all179 observations identically. [Corrected](chapter-08-section-08-complete-quotient-corrected.json):179passed/0failed. Predicate mismatches are not distinct defect/COV counts.

Independent exact weighted sample sums over represented values derive all4 finite differences andcomplete(4fine-coarse)/3 extrapolation. Named and30seeded3-sample vectors,3Richardson cases andactual callback traces check numerator/denominator range,signed pair zeros,canonical second/Richardson cancellation,nonzero underflow,true final overflow,controls-first priority,strict positive h,symmetric preflight andsample order. Richardson includes a finite zero final result despite an unreportable coarse quotient andan overflowing fine-coarse correction case. Shared Fraction arithmetic is explicit;this is sampled quotient verification,not arithmetic-library certification or an analytical derivative oracle.

Source rationally combines sampled expressions before final reports. Accepting exact h²/2h beyond prior rounded-denominator guards,complete unrounded coarse/fine composition andcanonical cancellation zeros are explicit policy reconciliation,not all prior promise violations. Coarse callbacks still occur before half-step validation;invalid half-step retains exactly2coarse calls. Even one-sided helpers retain the existing symmetric control gate. No callable-first reordering was introduced.

```bash
python books/book-02-mathematical-foundations-for-finance-with-python/chapter-08/code/check_section_08_complete_quotients.py
python books/book-02-mathematical-foundations-for-finance-with-python/validation/chapter-08-section-08-complete-quotient-observer.txt . baseline-expanded dea228397b36589d91f7b325b48a8165a5c43a4e
python books/book-02-mathematical-foundations-for-finance-with-python/validation/chapter-08-section-08-complete-quotient-observer.txt . baseline-expanded-replay dea228397b36589d91f7b325b48a8165a5c43a4e
python books/book-02-mathematical-foundations-for-finance-with-python/validation/chapter-08-section-08-complete-quotient-observer.txt . corrected
python books/book-02-mathematical-foundations-for-finance-with-python/validation/chapter-08-section-08-complete-quotient-scope-runner.txt .
```

[Initial legacy-check failures](chapter-08-section-08-complete-quotient-legacy-initial.json) retain actual failed runs of check_section_8_08.py andcheck_difference_denominators.py,with original checker/corrected-source hashes andstdout/stderr. Only Section8.8 assertions affected by explicit complete-quotient policies were reconciled:finite centered output,h²/2h domain extensions,actual callback counts. Other helper rejection assertions remain. True final-overflow andinvalid-sample rejection remains tested;callback-overflow is distinguished from a preflight failure. Five historical denominator unittest methods remain five;no new historical methods claimed. Scoped final reruns pass;no observer correction needed.

Final Chapter8 scope:53Python files compiled/43scripts passed,53candidate blobs verified before/after in [scope evidence](chapter-08-section-08-complete-quotient-scope.json),actual outputs/versions retained. Fresh inventory595Python/382scripts/596required Python-fixture blobs is not a full pass. V-130 remains latest full candidate Linux evidence pending accumulated V-131/V-132 refresh. Thirty-five selected categories partial;none closed.

Next:Section8.8 discounted-price/normalized-rate-sensitivity complete numerical/input/output contracts andindependent suggested-step expectations;do not repeat completed guard-only examples. Conditioning/noise/resource,independent mathematical/editorial/platform/release/canonical acceptance remain open. Book1 has separate progress.

Corrected executable publication revision:`30fe802218e5ad9978031287330cd887ebbcf1dc`;all31publication blobs and53tested Chapter8 inputs verified. Next financial probes retain unchanged helper functions at this source identity.
