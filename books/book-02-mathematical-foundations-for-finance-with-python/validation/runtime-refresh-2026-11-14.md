# V-136 — Full pinned candidate Linux runtime refresh

Executable source revision `3db1be648a9acba29d706e2dba0138540adacc7f`. All **597 Python files compiled**, all **384 check/test scripts passed**, and all **598 required Python/fixture blobs matched before and after execution**. Python 3.12.14, Linux-6.18.57-x86_64-with-glibc2.41; assertions enabled,60-second per-script timeout. Counts derive from the pinned tree, not an old inventory. The required non-Python fixture is Chapter1's section-1.14-cases.json.

[Per-file execution and exact source manifest](runtime-refresh-2026-11-14.json) · [Runnable exact-source staging runner](runtime-refresh-2026-11-14-runner.txt).

```sh
python books/book-02-mathematical-foundations-for-finance-with-python/validation/runtime-refresh-2026-11-14-runner.txt . 3db1be648a9acba29d706e2dba0138540adacc7f books/book-02-mathematical-foundations-for-finance-with-python/validation
```

The runner stages all required source/fixture blobs from Git into an isolated temporary tree, verifies input hashes, compiles each Python file, launches every check_/test_ script separately from its directory with assertions enabled, then verifies all hashes again. Results retain per-script timing, exit status, successful stdout digests and actual stderr; failed stdout would be retained if present. No failures occurred in this full run. Runtime was 202.4 seconds.

This refresh includes V-134's complete discounted-price and normalized-sensitivity source/legacy contract changes, its financial range checker, and V-135's independent suggested-step checker. Earlier [financial baselines and legacy failure](chapter-08-section-08-financial-followup.md), [suggested-step observer corrections](chapter-08-suggested-step-followup.md), and prior full V-133 evidence remain intact. [Changed metadata formatting check and rerun](chapter-08-suggested-step-format-check.json) is separate from numerical test failures.

Publication metadata and reports do not alter these executable inputs; final publication verifies this manifest against its resulting tree. Book1 source/lab/answer review has independent evidence and counts. This is one candidate Linux runtime, not independent mathematical/editorial review, supported-platform validation, release acceptance or canonical approval. Thirty-five selected COV categories remain partially addressed; none closed.

Next substantive item: COV-51 conditioning/noise limits for suggested steps and finite-difference derivative estimates with independently known noisy/quantized callbacks. Other resource and independent acceptance obligations remain open.
