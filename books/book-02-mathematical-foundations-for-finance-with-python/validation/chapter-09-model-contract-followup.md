# V-158 — Section9.2 constant/linear/income model contracts

Based on `059e25f0f2b1bf376bad2a973e9703d5f6efe749`. [Checker](../chapter-09/code/check_section_02_model_contracts.py),[observer](chapter-09-model-contract-observer.txt),[scope runner](chapter-09-model-contract-runner.txt),[actual scope results](chapter-09-model-contract-results.json).

```sh
python books/book-02-mathematical-foundations-for-finance-with-python/validation/chapter-09-model-contract-observer.txt . baseline
python books/book-02-mathematical-foundations-for-finance-with-python/validation/chapter-09-model-contract-observer.txt . corrected
python books/book-02-mathematical-foundations-for-finance-with-python/validation/chapter-09-model-contract-runner.txt .
```

[Baseline](chapter-09-model-contract-baseline.json):55 passes/39 failed predicates,actual child exit1;[actual replay](chapter-09-model-contract-baseline-replay.json) is identical. [Corrected](chapter-09-model-contract-corrected.json):94/94 pass/exit0. Observer exit0 records actual child output,not a numerical pass by itself. Predicate failures are not unique defect counts.

Independent1800/2400-digit Decimal direct powers and complete polynomial/rational calculations cover27 constant-model and50 linear-model field calls. Seven income expectations follow the independently derived analytic identity I*Q′/Q=e for positive income/scale;they do not claim execution of unreported astronomically large model levels. Ten invalid/priority controls complete94. Relative5e−14/zero absolute slack;explicit signed-zero policy remains distinct from mathematics. Includes power/derivative rescues,positive exact quantity lost to rounded cancellation,quantity underflow with finite analytic normalization,whole-report revenue overflow,zero/negative true quantity rejection and scalar income elasticity despite unreported-level range.

Constant demand validates in its original price/scale/exponent order before using reviewed Section9.1 demand_sensitivity;linear uses complete Fraction expressions before domain/reporting;income returns the model exponent after strict input validation. Literal-zero supplied-baseline point API remains unchanged. Six files compiled,five top-level commands passed (demo+four checkers),six hashes verified before-after. Existing Section9.2,point/arc/rate and Section9.1 demand/portfolio checkers pass unchanged. Fresh611 Python files/398 check-test scripts/612 required source-fixture blobs is inventory,not itself a full run;full pinned refresh records execution separately.

Three[original numeric probes](chapter-09-model-helper-resume-initial.json),[actual before-fix replay](chapter-09-model-helper-resume-before-fix-replay.json) are retained. [Explicit dispositions](chapter-09-model-helper-resume-disposition.json) resolve the three selected numerical contracts only. The fourth centered callback/preflight observation remains OPEN;its constant output0 is not a claimed wrong derivative. [Source scope comparison](chapter-09-model-contract-scope-comparison.json) preserves point/arc/rate/centered function text.

[Lab contract review](chapter-09-model-lab-contract-review.json) repairs eight escaped backticks around the actual commands and documents the new sibling helper dependency;both commands executed. Runtime checkbox is qualified as scoped,not independent approval. Introducing that dependency exposed a separate[QA loader import failure](chapter-09-model-loader-initial-failure.json),not a numerical failure. Two historical spec loaders now add the code directory only inside the QA process,default to replay instead of overwriting initial records,and no longer assert an unverified executable pin for current-tree diagnostics. Actual[model-loader](chapter-09-model-helper-resume-loader-compatibility-check.json) and[point-loader](chapter-09-elasticity-resume-loader-compatibility-check.json) executions completed;those diagnostics are not extra acceptance predicates. Historical initial JSON records remain unchanged.

All36 selected COV categories remain partial,none closed. Broad conditioning/resources/financial/model/platform/independent mathematical/editorial/release/canonical acceptance pending. Next:Section9.2 centered-elasticity finite-perturbation preflight,complete sampled report and callback/error-consumption contracts,resuming the retained observation. Book1 tracked independently.

Executable source/checker bytes verified against candidate `2b64f1adaeae6e143e76d7f5570b5d50fecd3dba`;see [source manifest](chapter-09-model-contract-publication-verification.json).
