# V-146 — Assessment rational/log helper contracts

Based on `815dc77f8f5accf0166b6e4c107f5d861a86f8c2`. [Checker](../chapter-08/code/check_section_10_rational_log_range.py), [observer](chapter-08-assessment-rational-log-observer.txt), [scope runner](chapter-08-assessment-rational-log-runner.txt), [actual scope results](chapter-08-assessment-rational-log-results.json).

```sh
python books/book-02-mathematical-foundations-for-finance-with-python/validation/chapter-08-assessment-rational-log-observer.txt . baseline
python books/book-02-mathematical-foundations-for-finance-with-python/validation/chapter-08-assessment-rational-log-observer.txt . corrected
python books/book-02-mathematical-foundations-for-finance-with-python/validation/chapter-08-assessment-rational-log-runner.txt .
```

[Initial output](chapter-08-assessment-rational-log-baseline.json) retains40 passes/25 failures;[replay](chapter-08-assessment-rational-log-baseline-replay.json) has identical predicates and actual exit1. Observer exits zero because it records the child failure;child stdout/stderr/returncode are retained. [Corrected output](chapter-08-assessment-rational-log-corrected.json) passes65 predicates/exit0.

Twenty-five positive-price pairs include near-unity,nextafter,normal/subnormal,maximum/subnormal,zero-log and15 seeded wide-exponent pairs. Independent Decimal ln(end/start) references at120/180 digits agree at report precision. Relative tolerance4e-15 with zero absolute slack tests nonzero values;zero sign is explicit. Scaled logs avoid ratio/difference overflow while log1p retains near-unity accuracy.

Eight bond vectors test yield and inverse derivative;seven break-even vectors test quantity and derivative. Independent1600/2200-digit Decimal references agree at report precision for complete (C−P)/P,−C/P²,K/(P−C),−K/(P−C)². Complete Fraction arithmetic fixes premature quotient/subtraction/product overflow,cancellation and derivative double rounding. True final overflow consistently raises ValueError;finite underflow signed zero is allowed. Ten controls retain domain/type/validation-order checks. Signed cost/price fixtures exercise the stated arithmetic domain rather than asserting economic suitability.

Eight selected files compiled;four Python commands passed (source demo plus three checker invocations),eight input blobs verified before/after. Existing assessment and alignment checkers passed unchanged. Fresh inventory604 Python files/391 check-test scripts/605 required Python-fixture blobs is not itself full execution;the pending pinned refresh records actual full results separately.

COV-51 remains partial and35 selected categories remain partially addressed;none closed. PV/derivative/shock overflow/underflow and centered-helper perturbation/report copies are the next substantive scope. Broader conditioning,resource,model,platform,independent review,release and canonical approval remain pending. Book1 has independent evidence/trackers.
