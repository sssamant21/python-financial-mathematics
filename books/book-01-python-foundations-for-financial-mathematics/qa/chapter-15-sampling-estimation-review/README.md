# Section 15.7 — scoped sampling lab and worked-answer review

Baseline source revision: `8507eee5e60a46c613b61976b161e3a928eb0efe`. Scope: one core workflow, 24 local prompt/answer records and one ten-task project. Predicate, workflow, exercise and historical unique method counts remain separate.

Run from repository root:

```bash
python books/book-01-python-foundations-for-financial-mathematics/qa/chapter-15-sampling-estimation-review/review.py
```

The observer extracts the single Python fence unchanged, executes the printed demonstration and twelve existing unittest methods, imports silently and runs the printed compilation command in an isolated directory. Three command checks pass. It imports the same source and evaluates 34 supplemental predicates, all passing. No historical unique methods added. Raw command output, hashes, Python/platform and tolerances are in `results.json`, alongside all 1000 bootstrap means.

`baseline.json` retains nine failed predicates against the baseline source at the revision above, reproducible with this observer and that manuscript. All twelve original methods passed on baseline. F133 corrects loss of integer identity/spread, premature sum/square overflow, squared underflow before the SE square root, constant-series residual variance, and unreportable variance raising raw OverflowError. More substantially, finite-population correction now matches the n−1 sample-SD convention used in the section. The twelfth-method count is unchanged: the existing FPC expected value was corrected together with its formula, not treated as an independent numerical oracle.

Intermediate means/variance use exact fractions of integers or displayed decimal float values. Square roots use 80-digit Decimal before float reporting; nonzero unreportable outputs deliberately raise ValueError. Standard error can remain reportable even if variance is too small to report as a float. Bootstrap SE requires at least two replicates and summarizes the returned float replicate means. Sampling without replacement preserves selected original integer values. Different population units may have the same numeric return; repeated values are not evidence of replacement. These educational conventions are not performance or binary-float compatibility claims.

## Independent numerical derivation and FPC convention

Sample-variance benchmarks use Σ(i<j)(xi−xj)²/[n(n−1)], independently of the source's centered-square implementation. For [.01,.02,.03], mean=.02, sample variance=.0001 and iid SE=√(1/30000)≈.0057735027.

For finite population [0,2,4,6], all six size-two subsets have means [1,2,3,3,4,5]. Their exact design variance is 5/3 around population mean 3. Average n−1 sample variance over these subsets is 20/3. Therefore E[(s²/n)(1−n/N)]=(20/3)/2×1/2=5/3, matching the design variance. The original multiplier squared (N−n)/(N−1)=2/3 instead gives 20/9. The corrected sample-SD multiplier is √((N−n)/N). This validates an unbiased estimated design variance, not an unbiased estimated SE. If one starts instead with known finite-population SD using denominator N, the alternative √((N−n)/(N−1)) is appropriate; the manuscript now distinguishes these conventions. For n=10,N=100, the sample-SD multiplier is √.9≈.9486833.

The RNG replay uses the same standard-library PRNG and choices algorithm, so it is a sequence/reproducibility check, not independent RNG acceptance. Every seeded draw's mean is independently summed with Fraction; all 1000 source means match within recorded tolerance. The source bootstrap SE .0046472067 matches the pairwise rational variance of those seeded replicate means. The exact empirical-bootstrap population SE is √(1/45000)≈.0047140452; Monte Carlo replicate SD need not equal it. The analytical s/√n and empirical-bootstrap SE also need not coincide for n=3, because the empirical bootstrap's generating variance uses denominator n.

## All local prompt/answer records

| Prompts | Review and evidence |
|---|---|
| 1–3 | Defined population N=100, sample n=10 and fraction 1/10; population/sampling-frame interpretation reviewed conceptually. |
| 4–7 | Source mean .02, variance .0001 and SE √(1/30000) checked; SD .01 obtained by supplemental square root. |
| 8 | Conditional s/√n scaling halves SE at 4n only for stable variance. Separate larger synthetic sample executed; it does not assert identical realized variance or information gained by duplicating rows. |
| 9–10 | FPC convention corrected and independently verified by exhaustive finite-population subsets; census multiplier zero, including singleton census helper convention. n=1 sample variance remains undefined. |
| 11–12 | Seeded without-replacement replay and full census IDs checked. Reproduction is scoped to recorded runtime/algorithm, not an across-version sequence promise. |
| 13–14 | With-replacement duplicates observed; exactly 1000 replicate means retained and checked. |
| 15 | Replicate values [1,2,3] have sample variance 1 and SD 1 by direct arithmetic; this conceptual statistic example is not a call to a bootstrap input series [1,2,3] that would generate different replicate estimates. |
| 16–18 | Survivorship, look-ahead and convenience-sample biases reviewed. Random resampling cannot restore omitted units or repair unavailable as-of information; no real feed/frame audited. |
| 19–20 | Persistence fixture and iid-resampling limitations reviewed; dependence-aware SE and block bootstrap not implemented or accepted here. |
| 21–22 | Historical mean is a point estimate; sampling distribution varies the estimator across hypothetical repeated samples. Neither is a future guarantee. |
| 23 | None observation rejected by source. Missingness, closures and stale prices require an explicit upstream policy, not silent zero insertion. |
| 24 | MSE=variance+bias² follows expanding (estimate−target)² around estimator expectation, with zero cross term; finite second moments required. Mathematical review, not a market-data calibration claim. |

## Project step contracts and prerequisites

| Task | Executed result or explicit limit |
|---|---|
| 1 | Manuscript now fixes synthetic [.01,.02,.03], daily units and period labels 1–3. Real dates/calendar unspecified; target is a hypothetical iid population mean. |
| 2 | Source mean/variance/iid SE recorded and independently checked. |
| 3 | Seed 42, 1000 returned source bootstrap means retained; with-replacement size-three samples replayed. |
| 4 | Source SE .0046472067 versus analytical .0057735027; finite empirical generating variance and Monte Carlo variability explain the difference. No bootstrap consistency claim from three observations. |
| 5 | Supplemental `random.Random(31).choices([.01,.02,.03],k=12)` fixture generated and recorded, source SE checked with rational benchmark. Stable-variance square-root-n rule is conditional, not guaranteed by these small realized samples. |
| 6 | Missing-value rejection executed; filtering/imputation decisions and implications remain upstream design work. |
| 7 | Supplemental [.01,.01,.01,.01,.03,.03,.03,.03] persistence fixture retained; lag-one sample correlation .75 by paired centering. Source descriptive mean executed. This deterministic fixture is not a fitted AR model, and no dependence-aware bootstrap executed. |
| 8 | Survivorship and look-ahead limitations documented conceptually; no actual market universe or timestamped data provided. |
| 9 | Inputs, fixture hash, runtime, seed and source/listing hashes retained. Baseline revision above; corrected revision is the containing commit. |
| 10 | Estimates describe a tiny synthetic sample. No stationarity, sampling-frame validity, tail adequacy or future-performance certification. |

Prerequisites: Python functions/sequences, return units and sample variance/SE definitions. Standard-library source only. The task-list project is assembled supplementally by the observer, not a second published complete lab program. Exact source execution, rational/design enumeration, PRNG replay, synthetic fixture creation and conceptual bias/dependence review are separate evidence scopes.

## Limits and resume checkpoint

Local Linux CPython only. F28 notebook/platform and F32 shared-input integration remain open, as do other unresolved findings. No external platform tests, real-data integration, block bootstrap, independent reviewer acceptance, exhaustive branch proof or certification. Chapter 15 now records seven workflows and 168 local answers reviewed. Next pending formal review: Section 15.8 — Confidence Intervals.
