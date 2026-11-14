# V-148 — Assessment PV/shock complete-expression facade

Based on `9392004a95ed37258177ee1cf1018d9170cbb3b3`. [Checker](../chapter-08/code/check_section_10_pv_shock_range.py), [observer](chapter-08-assessment-pv-shock-observer.txt), [scope runner](chapter-08-assessment-pv-shock-runner.txt), [scope results](chapter-08-assessment-pv-shock-results.json).

```sh
python books/book-02-mathematical-foundations-for-finance-with-python/validation/chapter-08-assessment-pv-shock-observer.txt . baseline
python books/book-02-mathematical-foundations-for-finance-with-python/validation/chapter-08-assessment-pv-shock-observer.txt . corrected
python books/book-02-mathematical-foundations-for-finance-with-python/validation/chapter-08-assessment-pv-shock-runner.txt .
```

[Final baseline](chapter-08-assessment-pv-shock-baseline.json):40 passes/29 failures,actual child exit1;[replay](chapter-08-assessment-pv-shock-baseline-replay.json) has identical predicates. [Corrected](chapter-08-assessment-pv-shock-corrected.json):69/69 pass,exit0. The observer exits zero when it successfully records a failing child;actual returncode/stdout/stderr remain explicit.

Independent1300/1800-digit Decimal references agree at float reporting precision for complete C*exp(−rT),−T*C*exp(−rT),T²*C*exp(−rT),linear/quadratic Taylor shocks and the difference of independently computed exponential levels. Nine PV/derivative tuples (36 field calls),nine shock reports (27 field calls),six invalid-input/priority controls. Relative tolerance5e−14 and zero absolute slack;zero signs checked separately as reporting conventions,not mathematical uniqueness claims. Normal,large/small amount,underflow-rescue,overflow-rescue,large/small horizon,small-shock-rescue,quadratic cancellation,zero identities and true final overflow cases executed. Tuple/dict rejection applies to the whole report if any field cannot be represented.

The assessment now delegates to reviewed Section8.6 routines. This avoids rounding a PV/derivative before multiplying by a rescuing horizon/shock and keeps input order/strict types. Existing assessment,alignment and rational/log checkers passed unchanged. Nine source/checker files compiled,five commands passed (source demo+four checker invocations);nine hashes verified before-after.

Oracle history is retained rather than counted as defects: [first oracle observation](chapter-08-assessment-pv-shock-initial-oracle-observation.json) had31 failures;[intermediate baseline](chapter-08-assessment-pv-shock-intermediate-oracle-baseline.json) had30;[first corrected-source observation](chapter-08-assessment-pv-shock-first-corrected-observation.json) had two mismatches. These exposed Decimal expression zero-sign choices that differed from the declared reporting policy. Final references explicitly encode negative first-order zero and positive quadratic-sum zero;29 final baseline failures are the scoped source mismatches. No independently accepted oracle is claimed.

Fresh inventory605 Python files/392 check-test scripts/606 required source-fixture blobs is not full execution. V-147 at489c46b92214906f22e642b199a8829909a64f00 remains latest full604/391/605 result;next full refresh should follow the remaining centered-copy changes. COV-51 remains partial;35 selected categories partial,none closed. Next:Section8.10 centered-copy perturbation/preflight,callback and complete quotient/report contracts. Broader conditioning/resource/platform/independent mathematical/editorial/release/canonical acceptance remains pending. Book1 tracked independently.

Executable source/checker revision:`cebfd7261943c3ab9e4411554a15af73f6dda60f`. [Pinned nine-input manifest](chapter-08-assessment-pv-shock-publication-verification.json).
