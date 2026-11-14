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

Source wrappers now preserve callable-first validation and delegate to reviewed Section8.8 routines. Ten selected files compiled,six commands passed (assessment demo+five checker invocations),ten source/checker hashes verified before-after. Existing assessment/alignment/rational-log/PV-shock checkers passed unchanged. Fresh606 Python files/393 check-test scripts/607 required source-fixture blobs is an inventory,not itself a full pass;the planned full pinned refresh records execution separately.

COV-51 remains partial;35 selected categories partial,none closed. Conditioning,analytic error budgets,broader callback/resource/report interfaces,independent mathematical/editorial review,supported platforms,release and canonical approval remain pending. Next:Section8.10 chapter-report serialization/field/validation-order coverage against existing assessment mapping,then next substantive tracker obligation. Book1 tracked independently.
