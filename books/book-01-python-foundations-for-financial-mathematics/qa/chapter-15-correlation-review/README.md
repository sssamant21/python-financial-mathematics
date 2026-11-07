# Section 15.6 — scoped correlation lab and worked-answer review

Baseline source revision: `d59583f1bbda71866dd6997d38da184015bd6619`. One core workflow, 24 local answers and one ten-task mini-project reviewed. Counts of workflows, exercises, predicates and historical unique methods remain distinct.

Run from repository root:

```bash
python books/book-01-python-foundations-for-financial-mathematics/qa/chapter-15-correlation-review/review.py
```

The observer extracts the exact single source fence, runs the printed demonstration and twelve existing unittest methods, verifies silent import and runs the printed compilation command in isolation. Three command checks pass. It imports the same source for 50 supplemental predicates, all passing. No historical unique methods added. Raw output, runtime/platform, hashes and expected values/tolerances are in `results.json`. `baseline.json` retains seven failed predicates against the baseline revision above, reproducible with the same observer and that source; all twelve existing methods passed even before correction.

F132 corrects integer precision lost in both Pearson and Spearman pairing, overflowing/underflowing Pearson denominator products, extreme centering/mean overflow, and finite decimal constants erroneously receiving a numeric correlation. Exact rational centering preserves integer precision; float inputs follow the declared displayed-decimal convention. The squared correlation ratio cancels scale before an 80-digit Decimal square root; no clipping hides faulty intermediate results. Underflow of a nonzero reported result is an explicit error. These educational numerical conventions do not claim binary-float compatibility or performance suitability.

## Independent derivation and answer alignment

The independent oracle forms pairwise differences: cross=Σ(i<j)(xi−xj)(yi−yj), xx=Σ(i<j)(xi−xj)² and yy similarly. Pearson=cross/√(xx yy); rational squares and Decimal roots provide numerical expectations independently of source centered sums. Tied-rank expectations are assigned manually before this oracle. The six-return project has Pearson=Spearman=29/35≈.8285714286. Three-period windows all give √(3/7)≈.6546536707; four-period windows give .6, √(49/65)≈.8682431421, .6.

| Prompts | Reviewed answer and evidence |
|---|---|
| 1–4 | Perfect positive/negative correlation, nonlinear zero and unit invariance executed. Zero linear association in the deterministic quadratic example does not imply independence. |
| 5–9 | Means 2.5 and 5 for four-point fixture; three-point centered cross sum 4 and square sums 2/8 give ratio 1. Means/sums are independent manual derivations, not source report fields. |
| 10–13 | Translation, reflection and symmetry checked. All project matrix values stay in [−1,1]; this finite probe is not a proof over all possible inputs. |
| 14 | Integer and decimal constant series both rejected; source baseline incorrectly returned a number for [.05,.05,.05]. |
| 15–18 | Quadratic monotonic example Spearman=1 while Pearson<1; inverse Spearman=−1. Average ranks [3.5,2,3.5,1] checked; tied Spearman compared to manually assigned ranks of both series, not the no-ties shortcut. |
| 19 | Six observations give four windows of length 3; all four and all three windows of length 4 checked numerically against independent oracle. |
| 20–21 | Holding positive weights/SD fixed, lower correlation reduces variance: mathematical/design review. Two-asset matrix diagonal, symmetry and this fixture's nonnegative determinant checked. No general PSD certification claimed. |
| 22 | Symmetric X² fixture returns exactly zero Pearson despite deterministic dependence. |
| 23–24 | Trending prices, small samples, instability, causality and forecast limits reviewed conceptually. No market data, stationarity test or causal inference performed. |

## Mini-project steps and prerequisites

| Task | Result and boundary |
|---|---|
| 1 | Manuscript now fixes A=[.01,.02,.03,.04,.05,.06], B=[.02,.01,.04,.03,.06,.05]. Synthetic daily simple returns, period labels 1–6; dates unspecified. |
| 2 | Source Pearson 29/35 compared with the independent covariance/SD-equivalent pairwise ratio. No reliance on another manuscript module's implementation. |
| 3 | Source Spearman 29/35; this fixture has no ties and both orderings have the same linear rank relation. Ties separately tested. |
| 4 | Source separate [1,2,3,4]→squares diagnostics recorded; monotonic transformation preserves ranks, not linear Pearson correlation. Transformation fixture is numeric, not a newly defined financial return. |
| 5 | Separate symmetric [−2,−1,0,1,2]→squares diagnostic recorded; Pearson zero. |
| 6 | Manuscript now specifies windows 3 and 4; all seven source outputs and counts retained. Constant-window source rejection separately tested; no invented fallback value. |
| 7 | Source 2×2 matrix checked entrywise; nonconstant variables and common observation table are prerequisites. |
| 8 | In Var(P)=wA²σA²+wB²σB²+2wAwBρσAσB, project ρ=29/35 enters the cross term. Formula integration reviewed conceptually; no portfolio module/runtime invoked or accepted. |
| 9 | Units, synthetic labels, missing/nonfinite rejection, windows and estimators recorded. Length checks cannot verify real timestamp alignment; actual calendar joins remain upstream. |
| 10 | Inputs unchanged, fixture hash, runtime, source/listing hashes, generated outputs and original failures retained. Corrected revision is the containing commit. |

The lab is a task list, not a complete report-generator listing; the observer's assembly is supplemental. Source commands, ranks, rolling functions and matrix calls are exact-source execution. Pairwise rational benchmarks and metadata are supplemental. Causal claims, real-data cleaning, stationarity, production suitability and forecast validity are conceptual/unexecuted. Prerequisites are Python functions/sequences, the covariance section, decimal-return units and upstream alignment; standard library only.

## Remaining scope and checkpoint

Scoped Linux CPython only; no external platform/notebook execution, independent reviewer acceptance, exhaustive branch proof, real-data integration or certification. F28 notebook/platform and F32 shared-input integration, plus any other unresolved findings, remain open. Chapter 15 now records six workflows and 144 local answers reviewed. Next formal review: Section 15.7 — Sampling and Estimation.
