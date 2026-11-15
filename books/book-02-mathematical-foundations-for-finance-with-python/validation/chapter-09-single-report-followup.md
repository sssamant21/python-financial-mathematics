# V-172 — Section9.4 complete single-cash-flow reports

Based on `78b2ddb63e3bef63f54b89e6e879ef2c4ea46f2c`. [Checker](../chapter-09/code/check_section_04_single_reports.py),[observer](chapter-09-single-report-observer.txt),[scope runner](chapter-09-single-report-runner.txt),[scope results](chapter-09-single-report-results.json).

```sh
python books/book-02-mathematical-foundations-for-finance-with-python/validation/chapter-09-single-report-observer.txt . baseline
python books/book-02-mathematical-foundations-for-finance-with-python/validation/chapter-09-single-report-observer.txt . corrected
python books/book-02-mathematical-foundations-for-finance-with-python/validation/chapter-09-single-report-runner.txt .
```

[Corrected-oracle baseline](chapter-09-single-report-baseline.json):89 passes/29 failed field/control predicates,actual child exit1;[actual replay](chapter-09-single-report-baseline-replay.json) identical. [Final corrected](chapter-09-single-report-corrected.json):118/118 predicates/exit0. Whole-report rejection affects multiple field predicates;29 failures are not29 unique implementation defects,and include the explicit finite whole-report policy adoption.

[Initial oracle correction](chapter-09-single-report-oracle-correction.json) retains31-failure[initial baseline](chapter-09-single-report-baseline-initial-oracle.json),[initial replay](chapter-09-single-report-baseline-replay-initial-oracle.json) and two-failure[first corrected run](chapter-09-single-report-first-correction.json). Decimal zero arithmetic did not encode the retained−t*0 first-derivative sign. Expected zero sign now comes explicitly from the input-time sign;all nonzero references/tolerances and production source remain unchanged for that repair. [Initial checker](chapter-09-single-report-initial-oracle-checker.txt),[exact first-correction source](chapter-09-single-report-first-correction-source.txt),[actual two-failure replay](chapter-09-single-report-first-oracle-replay.json) are runnable with observer mode first-oracle-replay. This QA issue is separate from source numerical fixes.

Twenty five-field vectors use independent1800/2400-digit direct complete value/first/second/duration/convexity references. Log-amplitude guards1000/−2000 avoid claiming enormous unbounded exponent execution;production coefficient/exponent bounds use±10000. Relative5e−14/zero absolute slack. Fourteen original input/domain/priority controls and four private-context/unchanged-parent controls complete118.

Positive reported value remains required;value underflow to0 still rejects. Complete represented coefficients/exponent precede float reporting;second derivative can remain nonzero when reported convexity underflows. First zero sign retains−t*0;duration retains supplied time sign. Every field must be finite;final derivative/normalized overflow raises ValueError. Private1300-digit context isolates ambient precision/exponent/traps. Selected reference agreement is not universal correctly-rounded transcendental certification.

Four files compiled,four commands/three checkers pass,four hashes verified before-after;original section and prior quadratic56 checkers unchanged. Only single_cash_flow text changes with two private helpers ([comparison](chapter-09-single-report-scope-comparison.json));portfolio/shock integrations remain pending despite transitive behavior changes. Fresh618 Python/405 check-test/619 required-blob inventory is not full execution;full pinned refresh records execution separately.

[Later saved-case dispositions](chapter-09-single-report-resume-disposition.json) resolve two numerical cases and adopt whole finite-report policy;historical original/prior records unchanged. All36 selected COV categories partial,none closed. Next:Section9.4 portfolio aggregation/normalization and single/portfolio shock complete-report contracts. Broader conditioning,resources,financial/model/independent mathematical/editorial/platform/release/canonical acceptance pending. Book1 tracked independently.

Executed source/checker bytes verified against `248b67271091d210fa62d3fb68cdbfb09a5c6793`;[source manifest](chapter-09-single-report-publication-verification.json).

[Next portfolio/shock checkpoint](chapter-09-portfolio-shock-resume-initial.json),[actual replay](chapter-09-portfolio-shock-resume-replay.json),[runner](chapter-09-portfolio-shock-resume-probes.txt) retain two OPEN numerical/integration cases and one separate eligibility-policy observation;not part of the118 passing predicates.
