# V-149 — Assessment centered-copy preflight and complete quotients

Based on `fb5b9d7482605ae671893f70a2af6649db9ae9da`. [Checker](../chapter-08/code/check_section_10_centered_contracts.py),[observer](chapter-08-assessment-centered-observer.txt),[scope runner](chapter-08-assessment-centered-runner.txt),[actual scope results](chapter-08-assessment-centered-results.json).

```sh
python books/book-02-mathematical-foundations-for-finance-with-python/validation/chapter-08-assessment-centered-observer.txt . baseline
python books/book-02-mathematical-foundations-for-finance-with-python/validation/chapter-08-assessment-centered-observer.txt . corrected
python books/book-02-mathematical-foundations-for-finance-with-python/validation/chapter-08-assessment-centered-runner.txt .
```

[Baseline](chapter-08-assessment-centered-baseline.json):53 passes/15 failed predicates,actual child exit1;[actual replay](chapter-08-assessment-centered-baseline-replay.json) has identical predicates. [Corrected](chapter-08-assessment-centered-corrected.json):68/68 passed/exit0. Observer exit0 means the failing child outcome was recorded,not that source checks passed. Predicate failures include both numerical/preflight outcomes and callback-order consequences;they are not15 distinct defects.

Independent2200/2600-digit Decimal sample sums and quotients agree at float reporting precision. Nine first-order pairs and nine second-order triples use exact represented callback floats,then divide by exact high-precision2h orh². Range-rescue numerator/denominator cases,subnormal estimates,underflow-to-zero,true final overflow,cancellation and normal polynomial samples checked at relative4e−15/zero absolute slack. Zero signs are separate declared reporting-policy checks. These oracles judge the actual sampled stencil,not a claim that rounded x±h has exact analytic spacing or that every derivative is accurate.

Eighteen numeric cases each retain the exact expected callback order (36 predicates). Six invalid perturbation/step cases each verify ValueError and zero callback consumption (12 predicates). Twenty further callable/type/sample-invalid/first-failure/second-failure propagation predicates retain strict priority and no extra calls. The first helper no longer invokes callbacks at infinity. The second no longer rejects a finite complete estimate merely because float h² overflows/underflows;both avoid premature numerator and denominator rounding.

Source wrappers now preserve callable-first validation and delegate to reviewed Section8.8 routines. Eleven selected files compiled,seven commands passed (assessment demo+six checker invocations),eleven source/checker hashes verified before-after. Existing assessment/alignment/rational-log/PV-shock checkers passed unchanged. Fresh606 Python files/393 check-test scripts/607 required source-fixture blobs is an inventory,not itself a full pass;the planned full pinned refresh records execution separately.

COV-51 remains partial;35 selected categories partial,none closed. Conditioning,analytic error budgets,broader callback/resource/report interfaces,independent mathematical/editorial review,supported platforms,release and canonical approval remain pending. Next:Section8.10 chapter-report serialization/field/validation-order coverage against existing assessment mapping,then next substantive tracker obligation. Book1 tracked independently.

Executable source/checker revision:`23d3517e5720e8e7ef541f420cf24412c19c5d8b`. [Pinned eleven-input manifest](chapter-08-assessment-centered-publication-verification.json).


### Historical denominator expectations and initial full-run failure

The first full refresh at2ee70e207d55c70306860378c29bc0bf331ea834 exposed two failed assertions in one existing checker:[actual two-failure replay](chapter-08-denominator-contract-initial.json). Those assertions required Section8.10 to reject an unrepresentable float h² even though reviewed Section8.6/8.8 already returned the complete sampled quotient. They now require the exact sampled result0,without changing tolerances. At h1e−200,the callback x*x itself rounds both side samples to0;the resulting sampled estimate0 is NOT the analytic second derivative2. At h1e200,the constant callback gives exact zero numerator,so the estimate0 is valid.

[Corrected checker output](chapter-08-denominator-contract-corrected.json) passes the same five existing methods;no new historical methods. [Replay/staging runner](chapter-08-denominator-contract-replay.txt) retains the original checker from the failed candidate. A separate[first staging-harness failure](chapter-08-denominator-contract-harness-failure.json) was a missing Section8.9 dependency,not a numerical-source defect;the runner dependency list was corrected and both actual initial/corrected checker outcomes rerun. Full initial failure and corrected full rerun are recorded separately under V-150.

[Candidate comparison](chapter-08-denominator-contract-comparison.json) verifies the historical checker is the only changed Python file between full-run candidates and the same five test-method names remain;no new historical unique methods.
