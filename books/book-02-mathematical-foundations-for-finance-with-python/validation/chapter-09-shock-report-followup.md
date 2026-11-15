# V-166 — Section9.3 complete discounted-shock/error reports

Based on `5ada3da82c869410cdc54311b187fe51e695fdcf`. [Checker](../chapter-09/code/check_section_03_shock_reports.py),[observer](chapter-09-shock-report-observer.txt),[scope runner](chapter-09-shock-report-runner.txt),[scope outcomes](chapter-09-shock-report-results.json).

```sh
python books/book-02-mathematical-foundations-for-finance-with-python/validation/chapter-09-shock-report-observer.txt . baseline
python books/book-02-mathematical-foundations-for-finance-with-python/validation/chapter-09-shock-report-observer.txt . corrected
python books/book-02-mathematical-foundations-for-finance-with-python/validation/chapter-09-shock-report-runner.txt .
```

[Baseline](chapter-09-shock-report-baseline.json):106 passes/52 failed field/control predicates,actual child exit1;[actual replay](chapter-09-shock-report-baseline-replay.json) identical. [Corrected](chapter-09-shock-report-corrected.json):158/158 predicates/exit0. Observer exit0 records a child result,not a numerical pass. Whole-dictionary rejection affects multiple field predicates;52 failures are not52 unique defects.

Twenty seven-field vectors use independent1800/2400-digit direct endpoint values,differences,first-order terms and errors;140 field predicates plus14 input/domain controls and four ambient-context/unchanged-parent controls give158. Extreme endpoints below exponent−20000 are treated as zero only in selected cases whose normalized reference remains defined and whose ignored terms cannot affect binary64 reports;no claim that unbounded exponential execution occurred. Oracle overflow guards use log amplitude1000;production uses bounded factors/complete exponents with cutoffs10000. Relative5e−14/zero absolute slack;explicit zero-sign policy.

For B=C*exp(−t*r),z=−t*h,complete reports are D=B*expm1(z),L=B*z,linear level B*(1+z),error B*(expm1(z)−z). Production uses bounded positive/negative z factors and private1700-digit Decimal arithmetic,not rounded baseline/field subtraction. Relative error cancels the latent positive B and remains defined for nonzero z even if amount fields underflow. Zero z returns signed-zero changes,positive-zero errors and relative None. Every dictionary field must be finite or raises ValueError. Context/flags unaffected.

Five files compiled,five commands/four checkers pass,five hashes verified before-after;prior section,affine125 and value34 checkers unchanged. Only discount_shock text changes ([comparison](chapter-09-shock-report-scope-comparison.json));ladder calls it transitively,so unchanged ladder text is not a full behavior guarantee. Fresh615 Python/402 check-test/616 required-blob inventory is not itself full execution;full pinned refresh records execution separately.

[Later three-probe disposition](chapter-09-shock-report-resume-disposition.json) resolves finite-change recovery,tiny relative-error cancellation and zero-shock nonfinite output only in mapped scope. Original zero expectation0 magnitude is fulfilled by signed−0 under the declared sign policy;historical initial/replay records unchanged. All36 selected COV categories partial,none closed. Next:Section9.3 step-ladder collection/model/input-consumption and revenue numerical/report contracts. Broader conditioning,resources,financial/model/independent mathematical/editorial/platform/release/canonical acceptance pending. Book1 tracked independently.
