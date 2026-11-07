# Section 15.2 — scoped lab and worked-answer review

Source baseline: `4da843a1e5ea7b025bcd484d45a1d85480a76b07`. Scope: one core workflow, twenty-four local prompt/answer records and one ten-task mini-project. These counts are separate from test predicates and historical unique methods.

Run from the repository root:

```bash
python books/book-01-python-foundations-for-financial-mathematics/qa/chapter-15-quantiles-review/review.py
```

The runner extracts the single Python fence unchanged into an isolated temporary directory, runs the exact demonstration and its twelve existing unittest methods, imports without demonstration side effects, and runs the printed compilation command. Three commands pass. The supplemental observer then imports the same source and evaluates 49 predicates; all pass in `results.json`. No historical unique methods were added. Python/platform, source/listing SHA-256, raw command output, expected values and tolerances are recorded.

`baseline.json` retains the original command output and nine failed numeric predicates. The runner is rerunnable against the baseline manuscript at the commit above; baseline source hashes identify that version. All twelve original methods passed even on the baseline: they did not cover the demonstrated edge cases. No baseline failure was discarded. F128 corrects premature overflow in mean/median/trimmed/weighted calculations, overflowing interpolation, integer precision loss during sorting/rank selection, and `ceil(.14*100)` choosing rank 15 instead of 14. Exact rational intermediate arithmetic follows a declared displayed-decimal interpretation of floats. Averages/interpolations report floats; ranked observations preserve their original values. Unreportable nonzero outputs are explicitly rejected. This is an educational correctness policy, not a performance claim or a promise of binary-float compatibility with other packages.

## Independent numerical derivation and all local answers

References were derived from rational sums/order statistics before comparison with source functions; they are not another implementation of the manuscript routine. Exact finite decimal expectations use `Fraction`; comparisons use recorded tolerances. The source float results are compared to those references, not to their own intermediate results.

| Local prompts | Reviewed contract and evidence |
|---|---|
| 1–3 | Sum 5 percentage points / 5 = 1%; sorted middle 0%; even middle average .5%. |
| 4–8 | Sorted ranks give −4%, 8%, −1%, 2%; IQR 3 pp. |
| 9–11 | Type-7 rank .75 between 0 and 10 gives 7.5; nearest-rank first observation 0; median equivalence at .5. |
| 12–14 | Strict negatives 2/5; outlier sample mean 6.5%, median and one-each-side trimmed mean 2.5%. |
| 15–16 | Weighted sums .75×.02+.25×.08=.035 and (.01+2×.03+.05)/4=.03; pairs stay aligned, zero/negative/mismatched weights rejected. |
| 17–18 | Shift and positive scale laws checked for mean, median and an interpolated quantile; these are metamorphic supplemental predicates, not independent numeric oracles. |
| 19–20 | Replacement increases sum by .20, mean by .04 to .05; middle rank remains zero. |
| 21 | Missing value is rejected by source; conceptual answer permits explicitly disclosed filtering to n=4, not silent zero filling. No missing date/value is invented. |
| 22–23 | h=.2 gives −.034; h=3.8 gives .068. |
| 24 | For L=−100000R, reversed ordered interpolation gives .95 loss quantile 3400. Five observations support only this arithmetic illustration, not forecasting adequacy. |

These are scoped author/agent checks, not independent reviewer acceptance.

## Mini-project step and prerequisite contracts

| Task | Review/result and limit |
|---|---|
| 1 | Exact five-return fixture preserved; missing dates/frequency now explicitly unspecified. Units decimal simple returns, common hypothetical period. |
| 2 | Source mean .01 and median 0 recorded. |
| 3 | Source five requested quantiles recorded: −.034, −.01, 0, .02, .068. |
| 4 | IQR .03 and strict-negative fraction .4 recorded; input remains unchanged. |
| 5 | Nearest-rank Q25 = −.01 for this five-value fixture. It happens to equal type 7 here; the four-value [0,10,20,30] counterexample differs (0 vs 7.5). |
| 6 | Source stress mean .05, median 0 recorded; no mutation of original fixture. |
| 7 | Prompt now supplies both [.02,.08] returns and [.75,.25] weights; weighted source result .035 recorded. No fifth-return/date alignment is implied. |
| 8 | Missing observations rejected, disclosed upstream filtering permitted; quantile convention specified; small-sample tails/regime/dependence limits reviewed conceptually. |
| 9 | Runtime version, fixture hash, source hash and expected values retained. Baseline revision above; corrected revision is the Git commit containing this evidence. |
| 10 | Report and runnable evidence retained here for broader QA. |

The project report is a supplemental assembly of calls to exact-source routines, not an additional published executable lab. The manuscript provides tasks and acceptance numbers rather than a complete report generator. Chapters' Python fundamentals and return-unit conventions are prerequisites; no third-party package or fetched data is needed. Input validation, singleton/endpoints and strict threshold semantics are covered by source/supplemental tests. Financial suitability, feed adjustments, real metadata provenance and model approval remain conceptual and unexecuted.

## Remaining scope and checkpoint

Only local Linux CPython execution is evidenced. F28 notebook/platform and F32 shared-input integration remain open. No Windows/macOS/notebook run, independent acceptance, exhaustive branch proof, performance benchmarking or certification is claimed. Existing unrelated findings remain open. Next pending formal review: Section 15.3, Variance and Standard Deviation. The Chapter 15 tracker now records two workflows and 48 local answers, not 48 unique test methods.
