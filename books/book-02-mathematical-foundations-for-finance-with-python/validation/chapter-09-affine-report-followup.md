# V-162 — Section9.3 affine updates and generic change/error reports

Based on `c7d5060fc6bf7a8f01f7a91dd6651b7bccb25e1c`. [Checker](../chapter-09/code/check_section_03_affine_reports.py),[observer](chapter-09-affine-report-observer.txt),[scope runner](chapter-09-affine-report-runner.txt),[scope results](chapter-09-affine-report-results.json).

```sh
python books/book-02-mathematical-foundations-for-finance-with-python/validation/chapter-09-affine-report-observer.txt . baseline
python books/book-02-mathematical-foundations-for-finance-with-python/validation/chapter-09-affine-report-observer.txt . corrected
python books/book-02-mathematical-foundations-for-finance-with-python/validation/chapter-09-affine-report-runner.txt .
```

[Baseline](chapter-09-affine-report-baseline.json):86 passes/39 failed predicates,actual child exit1;[actual replay](chapter-09-affine-report-baseline-replay.json) identical. [First correction](chapter-09-affine-report-first-correction.json) retained one signed-zero failure;[exact first-correction source](chapter-09-affine-report-first-correction-source.txt) hashes to its recorded source blob and can be staged with observer mode first-correction-replay. [Final corrected](chapter-09-affine-report-corrected.json):125/125 predicates/exit0. Observer exit0 records a child result,not a numerical pass. Predicate failures are not unique defect counts.

Eight independent1800/2400-digit Decimal complete-affine references and eleven seven-field sampled-report vectors cover complete affine rescue,cancellation lost in rounded products,underflowed product/error normalization,whole-report field/relative overflow,zero sampled change,collided shocked point and negative zero. Complete expressions are formed before float reporting. A whole dictionary requires every field reportable;standalone affine rescue can be valid even when a generic report's separate linear_change overflows. Relative error is None only for equal supplied sample values. Relative5e−14/zero absolute slack;standalone exact-zero sum preserves original arithmetic zero sign;generic exact rational zeros report positive zero except retained baseline_value.

Ten preflight controls,21 callback/sample-stage controls,one zero-shock consumption control,two callable-priority controls and six affine-input controls complete125 predicates. Rounded shocked point must be finite before any callback. Order remains function(baseline),function(shocked),derivative(baseline);invalid outputs/raised errors stop later calls. Zero shock still invokes both function evaluations. Collided points are allowed;reports use supplied samples and nominal h,not an exact analytic f(x+h) oracle or error bound. No retry/rollback/domain discovery/side-effect certification.

Three files compiled,three commands/two checkers pass,three hashes verified before-after;original checker and all discounted/revenue/ladder function text unchanged ([comparison](chapter-09-affine-report-scope-comparison.json)). Fresh613 Python/400 check-test/614 required-blob inventory is not itself full execution;full pinned refresh records execution separately. Ten escaped manuscript backticks repaired around code/path/fences;both printed lab commands actually execute.

[Later disposition](chapter-09-taylor-affine-resume-disposition.json) resolves the saved affine case and callback-preflight observation only. The saved discounted-value rescue case remains OPEN;historical initial/replay records unchanged. All36 selected COV categories partial,none closed. Next:Section9.3 discounted value/shock/error-report numerical contracts,resuming the retained finite-value rescue failure,then step-ladder/revenue contracts. Broader conditioning,financial/resources/independent mathematical/editorial/platform/release/canonical acceptance pending. Book1 tracked independently.

Executable source/checker bytes verified against `067c4205c8339341e1f76352f60fdf4fd2615b78`;[source manifest](chapter-09-affine-report-publication-verification.json).

[Actual post-affine replay](chapter-09-taylor-after-affine-replay.json),[runner](chapter-09-taylor-after-affine-probes.txt) confirm the scalar rescue now returns−1e308 and nonfinite point rejects before callbacks;discount_value still raises OverflowError. These diagnostics are separate from the125 acceptance predicates.
