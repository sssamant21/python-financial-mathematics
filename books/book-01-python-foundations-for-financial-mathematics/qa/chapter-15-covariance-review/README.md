# Section 15.5 — scoped covariance lab and worked-answer review

Baseline revision: `8504bfb195f55bc723b1d997da0bb59dbc115258`. Scope: one core workflow, 24 local prompt/answer records and one ten-task mini-project. These are distinct from predicates and historical unique methods.

Run from repository root:

```bash
python books/book-01-python-foundations-for-financial-mathematics/qa/chapter-15-covariance-review/review.py
```

The observer extracts the single Python fence unchanged into an isolated directory, runs the exact printed demonstration and twelve existing unittest methods, imports silently, and runs the printed compilation command. All three command checks pass. It then imports the same exact source and evaluates 44 supplemental predicates, all passing. No historical unique methods added. Runtime/platform, hashes, command outputs, expected values and tolerances are in `results.json`.

`baseline.json` retains eight failed predicates against the baseline source revision above. The same observer reproduces those failures against that manuscript. The original twelve methods and three commands already passed. F131 corrects integer precision lost before centering, overflow/underflow in correlation's variance product, overflow when averaging large constants, overflow/cancellation in portfolio expansion, and raw OverflowError instead of deliberate ValueError for unreportable covariance. Rational intermediate moments preserve integer precision and use the declared displayed-decimal interpretation of float inputs. Correlation cancels scale before taking an 80-digit Decimal square root, without clipping invalid intermediates. Portfolio weights may be signed, with total weight one. Outputs must be finite floats and may not silently erase nonzero values through underflow. Individual covariance/variance reporting may fail while scale-free correlation remains computable. These are documented educational conventions, not performance or binary-float compatibility claims.

## Independent numeric expectations and all local answers

The oracle uses the pairwise identity Cov = Σ(i<j)(xi−xj)(yi−yj)/[n(n−ddof)], with rational inputs, independently of the source's centered-product algorithm. Synthetic sample covariance is 1/5000, population covariance 1/7500. Means are 1/50 and 1/25; variances 1/10000 and 1/2500. Pairwise checks also include a mixed unsorted fixture and zero covariance despite nonlinear dependence.

| Prompts | Answer alignment and evidence |
|---|---|
| 1–4 | Independent means .02/.04; deviations −.01,0,.01 and −.02,0,.02; cross-products .0002,0,.0002, sum .0004. Means/deviations are supplemental derivation, not numeric fields exposed by the reference API. |
| 5–10 | Source sample/population covariance, both variances, correlation 1 and reflected covariance −.0002 checked against rational expectations. |
| 11–13 | Symmetry, +.05 shift and ×3 scaling checked; covariance remains .0002 or triples to .0006 as applicable. |
| 14–15 | Constant covariance zero; constant-series correlation rejected. |
| 16–17 | Portfolio variance 9/40000, SD 3/200; source variance and supplemental square root executed. |
| 18–20 | All four matrix entries checked; rational determinant zero and Cauchy–Schwarz equality verified. Nine signed quadratic-form probes are nonnegative. This is scoped evidence, not a general matrix-certification algorithm. |
| 21 | Holding marginal variances fixed, lower covariance lowers positive-weight portfolio variance. Mathematical/design review; no real diversification forecast. |
| 22 | Equal lengths do not prove alignment. Timestamp joins/calendar/missing-data policy remain upstream contracts. Synthetic period labels only; no real-data adapter executed. |
| 23 | Singleton population covariance zero and sample covariance rejected. |
| 24 | Percent-unit source covariance 2, versus decimal .0002: scale factor 10000. |

## Project step and prerequisite contracts

| Task | Evidence and scoped limit |
|---|---|
| 1 | Original paired arrays preserved, period labels 1–3 synthetic. No real dates/frequency invented. |
| 2 | Numeric equal-length checks and unequal-length rejection executed. Matching synthetic labels reviewed; API cannot inspect timestamps. Manuscript now states this boundary explicitly. |
| 3 | Supplemental rational means plus source sample variances/covariance recorded in matrix/report. |
| 4 | Source population covariance 1/7500 recorded. |
| 5 | Source symmetric matrix recorded and every entry checked; singular because B=2A. |
| 6 | Source correlation 1 follows B=2A with positive nonzero variation. |
| 7 | Source equal-weight portfolio variance .000225, supplemental SD .015. |
| 8 | Source reflected covariance −.0002 recorded; source tests also cover reflected correlation −1. |
| 9 | Explicit shift/scale predicates above; transformed series do not mutate originals. |
| 10 | Input fixture hash, Python version, source/listing SHA-256 and output retained. Baseline revision above; corrected code revision is the containing commit. |

Prerequisites: Python sequences/functions, previous mean/variance sections, decimal-return units, and upstream pairing. Standard-library source only. The lab is a task list rather than a standalone report generator: this observer assembles the project report supplementally. Positional pairing is executed, while calendar alignment, corporate actions and actual source provenance are design review. Missing/nonfinite/boolean values, bad ddof, invalid weights, singleton sample and unequal lengths are rejected in recorded probes. Source execution, rational expectations, report assembly and conceptual review are distinct.

## Limits and resume checkpoint

Local Linux CPython only; no Windows/macOS/notebook execution, real-data integration, exhaustive branch coverage, independent human acceptance or certification. F28 notebook/platform and F32 shared-input integration remain open, as do other unresolved findings. Chapter 15 now has five reviewed workflows and 120 local answer records. Next pending formal review: Section 15.6 — Correlation.
