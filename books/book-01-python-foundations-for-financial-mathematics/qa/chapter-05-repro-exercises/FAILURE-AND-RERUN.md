# F34 — QA input/output name collision, resolved

Severity: low, QA executor owned. Affected new runner against main `015fa852cf678fe91948643c03d7570d9b46b69e`; manuscript/source unaffected.

Initial runner selected whitespace.json for both its copied input and output. Original research.py correctly raised FileExistsError through exclusive creation. The supplemental completion validator correctly rejected the nonzero process status with ValueError; the runner stopped before writing its final results. This was a QA orchestration defect, not an aggregation or exclusive-create source defect.

[Initial runner snapshot](initial-review.py) and [reproduced initial exception](initial-failure.json) are retained. [Failure observer](reproduce_failure.py) invokes that unchanged snapshot and records original subprocess return codes/stdout/stderr plus runner traceback in [raw reproduction](failure-reproduction.json). It observes the child FileExistsError and validator rejection; it does not alter source files or launch semantics. Initial original-suite reruns overlap the final nine methods and are not added to historical unique totals.

```bash
python3 -B books/book-01-python-foundations-for-financial-mathematics/qa/chapter-05-repro-exercises/reproduce_failure.py
python3 -B books/book-01-python-foundations-for-financial-mathematics/qa/chapter-05-repro-exercises/review.py
```

Correction: choose label-report.json for every generated report and update existing-output probe accordingly. The failed/reproduced attempt retained the source input by correctly refusing overwrite. Corrected runner checks four original files unchanged and existing result bytes preserved. Final rerun:7 satisfied command expectations,54 passing predicates and9 existing methods. Broader platform/input/independent acceptance remain open.
