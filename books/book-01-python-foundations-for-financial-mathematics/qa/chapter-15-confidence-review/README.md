# Section 15.8 — scoped confidence-interval lab and answer review

Baseline source: `76324a64e73b57826100c043ae18dfb34ff094e2`. Scope: one core workflow, 24 local answer records and one ten-task mini-project, distinct from predicate and historical method counts.

Run from repository root:

```bash
python books/book-01-python-foundations-for-financial-mathematics/qa/chapter-15-confidence-review/review.py
```

The observer extracts the single source fence unchanged, executes the printed demonstration and twelve existing unittest methods, verifies silent import, and runs the printed compilation command in isolation. Three commands and 43 supplemental predicates pass in `results.json`. No historical unique methods added. Runtime/platform, raw outputs, hashes, numerical expectations and tolerances are retained. `baseline.json` retains eleven failed predicates against the baseline source, reproducible with this observer and that revision; the original twelve methods already passed.

`observer-initial.json` separately retains a QA tolerance error. The independent df=2 critical-value benchmark initially demanded relative tolerance 1e-12 of an approximate supplied t critical. Solving F₂(t)=1/2+t/(2√(t²+2))=.975 gives approximately 4.302652729749464; the supplied 4.302652729911275 differs by about 1.6e-10 and is consistent with the manuscript's stated 4.30265273 precision. The benchmark now uses absolute tolerance 5e-9 and zero relative tolerance. The corrected observer was rerun against unchanged baseline source before rerunning corrected source. This observer tolerance issue is not counted as a manuscript defect.

F134 corrects integer spread lost before centering, constant-series residual SE, intermediate mean/square overflow or underflow, unstable extreme quantile interpolation and bootstrap averaging, invalid extreme Wilson arithmetic, overflowing interval endpoints and positive-width mean intervals collapsing to one reported float. Rational means/variance/quantiles and Wilson coefficients interpret floats by displayed decimal values; roots and mean endpoint arithmetic use an 80-digit Decimal context. The Wilson lower quadratic root is rationalized to avoid subtraction cancellation. Outputs must be finite floats without silently rounding nonzero values to zero; collapsed positive-width mean intervals are explicitly rejected. These are educational numerical policies, not performance or binary-float compatibility guarantees.

## Independent numerical expectations and all local answers

The variance oracle uses the pairwise identity Σ(i<j)(xi−xj)²/[n(n−1)] rather than source centered squares. For [.01,.02,.03], SE=√(1/30000). Interval endpoints are independently evaluated with Decimal and the declared critical values: normal [.008684142659238283,.03131585734076172], t [−.004841377118437528,.044841377118437525]. The df=2 critical check uses the closed-form CDF above, independently of source tests. Wilson expectations independently solve the score-inequality quadratic n(p_hat−p)²≤z²p(1−p), rather than the source baseline's center/half-width formula. For zero of ten, [0,.2775327998628892].

| Prompts | Answer review and scope |
|---|---|
| 1–5 | Mean .02, SD .01, SE √(1/30000), normal half-width and both endpoints agree with rational/Decimal expectations. SD is an independent derivation; source returns mean/SE. |
| 6–10 | n−1=2, supplied critical precision checked independently, both t endpoints checked; t width exceeds normal width. |
| 11–12 | Long-run coverage interpretation reviewed conceptually. No simulation of repeated-sample coverage and no probability assigned to the fixed parameter in a realized CI. |
| 13–15 | Alpha .05 gives tails .025; normal 99% critical about 2.575829 gives greater width; fourfold sample-size scaling is conditional on stable variance/critical. Critical convention and scaling reviewed mathematically, not a forecast/data adequacy claim. |
| 16–17 | All 2000 seeded size-three with-replacement draws replayed for exact rational mean/quantile expectations. Source percentile endpoints .01/.03 match; type-7 median 2 and nonintegral-rank interpolation 7.5 checked. |
| 18–19 | Wilson roots checked for 0,3,10 successes out of 10; zero-success upper positive and full-success lower below one. Extreme-z behavior tested separately. |
| 20–22 | Dependence, heavy tails and selection bias can invalidate textbook coverage; conceptual review. No HAC, block bootstrap, real sampling frame or robust-coverage acceptance executed. |
| 23–24 | CI for mean differs from next-observation prediction interval. Seed, B, quantile convention and data revision are required for reproducibility. No prediction model implemented. |

PRNG replay shares Python's Random/choices algorithm and is a reproducibility check, not independent PRNG validation. Bootstrap means are summed with Fraction and type-7 endpoint interpolation is independently rational. The actual bootstrap interval is .01 to .03 for the declared fixture/seed; it need not resemble the normal or t interval in a three-point empirical distribution.

## Project step and prerequisite contracts

| Task | Evidence and limitation |
|---|---|
| 1 | Synthetic daily simple returns and labels 1–3 now specified; real dates/calendar unavailable. Hypothetical iid population mean is the target. |
| 2 | Source mean and SE retained; sample SD .01 derived independently. |
| 3 | Source normal endpoints retained; n=3 example is arithmetic illustration, not justification of a large-sample approximation. |
| 4 | Source t endpoints retained, df=2 and supplied t critical checked within stated precision; exact coverage requires iid normal observations. |
| 5 | Manuscript now specifies B=2000, alpha=.05, seed=42 and type-7 endpoints. Source output checked against full replay. |
| 6 | Normal width≈.0226317, t width≈.0496828, bootstrap width=.02. Method/assumptions differ; this comparison does not establish relative coverage quality. |
| 7 | Zero-of-ten source Wilson result retained and independently checked by score inversion; independent Bernoulli assumption explicit. |
| 8 | Autocorrelation invalidates naive iid SE/coverage assumptions; justified HAC or block bootstrap proposed conceptually. Neither alternative implemented here. |
| 9 | Target is a population mean, not next-return variability; interpretation reviewed without claiming prediction coverage. |
| 10 | Inputs, fixture hash, source/listing hashes, runtime, critical values, B, alpha, seed and results retained. Corrected revision is the containing commit. |

The reference listing supplies functions and a demonstration; the project report assembly is supplemental. Exact commands/source tests, rational/Decimal expectations, PRNG replay and conceptual coverage/dependence review remain separate. Prerequisites: Python sequences/functions, prior sample variance/SE, quantile convention and return units. Standard library only; no real market data, Student-t quantile library or external platform invoked.

## Limits and resume checkpoint

Local Linux CPython scoped review only. F28 notebook/platform, F32 shared-input integration and other unresolved findings remain open. No exhaustive branch proof, independent reviewer acceptance, actual model coverage certification, real-data integration or Windows/macOS/notebook run. Chapter 15 now records eight workflows and 192 local answers reviewed. Next: Section 15.9 — Hypothesis Testing Foundations.
