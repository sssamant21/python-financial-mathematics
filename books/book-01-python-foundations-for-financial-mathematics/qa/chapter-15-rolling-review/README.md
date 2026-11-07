# Section 15.12 — scoped rolling lab and worked-answer review

Baseline manuscript: `3b9e31148c9d11091190d3fee2ded4b381f595e0`. One core workflow, 24 local answers and one ten-task project reviewed. These counts are separate from predicates, per-window values and historical unique methods.

Run from repository root:

```bash
python books/book-01-python-foundations-for-financial-mathematics/qa/chapter-15-rolling-review/review.py
```

The observer extracts the single Python fence unchanged, executes the printed demonstration and twelve existing unittest methods, checks silent import, and runs the printed compilation command in isolation. Three commands and 54 supplemental predicates pass in `results.json`; no historical unique methods added. Runtime/platform, raw outputs, source/listing hashes, expected values and tolerances are retained. The project predicates compare arrays, covering 232 core metric values over 58 window-ending positions, plus 58 supplemental annualized SD values and expanding/lag/timing checks. Per-window values are not counted as additional unique tests or workflows.

`observer-initial.py` and `observer-initial.json` retain an observer-only crash: the source unexpectedly returned None for a numeric integer-offset correlation probe, and the scalar comparison helper did not handle None. The observer was corrected to record a failed predicate instead. Before changing the manuscript, it reran unchanged source and retained twelve failed predicates in `baseline.json`. The same runner against the baseline revision reproduces them. All twelve original methods already passed. This observer error is distinct from the manuscript's lost integer precision.

F138 corrects integer coercion, mean/SD/correlation overflow or underflow, nonzero residual variance for decimal constants, false −100% compounded losses, unreportable compound output and an empty lag helper inventing a one-element result. Exact rational intermediate arithmetic follows integer/displayed-decimal float inputs; roots use 80-digit Decimal after scale cancellation. Nonzero unreportable results are errors, and positive wealth that would round to total loss is rejected. Constant correlations remain None, rather than zero. An empty lag input now stays empty. These educational conventions are not performance or binary-float compatibility guarantees.

## Independent derivation and local answers

Mean and gross compounding expectations use exact rational sums/products. Independent sample variance uses pairwise squared differences divided by w(w−1), rather than source centered squares. Correlation uses pairwise cross differences and square sums, independently of source window centering. Zero-variance windows are detected exactly in the oracle. All source arrays are compared to recorded rational/Decimal values with zero absolute and 1e-12 relative tolerances, except exact None positions.

| Prompts | Alignment and evidence |
|---|---|
| 1–3 | Source [1.5,2.5,3.5] and full-window [2] checked; n−w+1 gives 7 for n=10,w=4. All project array counts are also checked by elementwise observer. |
| 4 | Rolling sums [6,9] by direct arithmetic; no rolling-sum function exists in the listing, so this is a supplemental derivation. |
| 5–9 | Sample SD 1, constant SD zero, correlations ±1 and constant-window None checked. Decimal constants and integer-offset cases supplement source's original tests. |
| 10–11 | Compound .1/−.1 gives −.01; windows with bankruptcy give −1. A later window excluding that loss is a fresh local-window wealth calculation, not resurrection of a global account. |
| 12–13 | Annual SD scaling is supplemental multiplication by √252 with independent root(var×252) checks; n=20,w=5 gives 16 outputs. No exported annualization helper claimed. |
| 14–18 | Trailing end labels, prior-period lag map, future-data exclusion, warm-up and trading-date-versus-calendar-date interpretation reviewed. Source means are invariant to changes after cutoff 20 for outputs ending by 20. This is scoped timing evidence, not a venue execution audit. |
| 19 | Missing/nonfinite observations rejected by source. No silent omission, forward fill or imputation executed. |
| 20 | EWMA .94v+.06r² follows the displayed recursion and timing convention; conceptual arithmetic only, no EWMA implementation supplied or executed. |
| 21–22 | Explicit synthetic amplitude change and overlapping windows reviewed; no structural-break test or independence claim about rolling outputs. |
| 23–24 | Slicing can be optimized but stability needs review; lag alignment must respect actual availability. No streaming performance benchmark, order execution or production backtest claimed. |

## Fully specified project and step contracts

| Task | Executed result and limit |
|---|---|
| 1 | 30 synthetic daily labels. A=[.01]×10+[.01,−.01]×5+[.04,−.04]×5, B=[.005,−.005]×5+[.02,−.02]×10. Real dates unspecified. Positional length validation does not prove calendar alignment. |
| 2 | Source means for w=5,10,20 checked at all 26,21,11 endings respectively. |
| 3 | All 58 source sample SDs checked; 58 supplemental annualized SDs checked under 252-period stationary uncorrelated-increment convention. Actual financial dependence/forecast quality unvalidated. |
| 4 | All 58 source correlations checked. A is constant at labels 1–10: w=5 has None at ends 5–10; w=10 has None at end 10; w=20 has no all-constant A window. |
| 5 | All 58 source compounded returns checked against exact rational products. |
| 6 | Warm-up labels explicitly retained (1 through w−1). API rejects an invalid w>n instead of returning partial windows. Undefined correlations are distinct from warm-up and numeric zero. |
| 7 | Expanding means assembled through full-prefix source mean calls and independently checked. This is supplemental workflow, not an exported expanding API. |
| 8 | A's amplitude increases at label 21. Five-observation windows fully contain new-regime data by label 25; 20-observation windows still mix old and new at label 30. This deterministic diagnostic is not a fitted regime model or confirmed break. |
| 9 | Lagged means mapped to the same ending labels: first output None, subsequent values use the previous ending label. Future-perturbation checks at cutoff 20 pass. Real observation availability, execution latency/costs and actual orders remain unavailable. |
| 10 | Fixture hash, units, window sizes, source/listing hashes, raw arrays, lag maps, ending/warm-up labels, runtime and baseline failures retained. Corrected revision is the containing commit. |

Exact printed commands and source rolling functions are execution evidence. Dataset assembly, array oracle, annualized SDs, expanding-prefix assembly and synthetic label maps are supplemental. Actual market calendars, quote quality, dependence-aware inference, execution feasibility and model suitability remain conceptual/unexecuted. Prerequisites are Python sequences/functions, sample moments, Pearson correlation, compounding and upstream chronological alignment. Standard library only.

## Limits and resume checkpoint

Scoped Linux CPython only. F28 notebook/platform and F32 broader shared-input integration remain open, alongside other unresolved findings. No Windows/macOS/notebook run, independent acceptance, exhaustive branch proof, performance benchmark or certification. Chapter 15 now records twelve workflows and 288 local answer records reviewed. Next: Section 15.13 — Statistical Pitfalls in Financial Data.
