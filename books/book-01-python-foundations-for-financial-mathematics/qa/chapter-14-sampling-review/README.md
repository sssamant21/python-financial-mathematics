# Section 14.14 — scoped sampling review

Reviewed [Sampling with Python](../../chapter-14/14.14-sampling-with-python.md) at `ac68976ded8e30972a0a911683938cd2eb476cf7`. Run `python -B review.py`. The [baseline](baseline.json) retains four failures; the [rerun](results.json) records both Python fence hashes, exact commands and checks. The exact standard-library lab ran with twelve existing methods, compiled and imported in isolation. The separate replacement illustration ran verbatim. Three command checks and 33 additional predicates passed; no historical unique methods were added.

| Answers | Independent review |
|---|---|
| 1–6 | The sum is 6 and the centered square sum is 2. Dividing by 2 or 3 gives the sample or population variance; taking a square root and dividing by √3 gives SE. Decimal-return average is .10/4. |
| 7–12 | Two defaults per 100 give .02, and summing 100 expectations gives 2 without needing independence for the mean. Normalizing 1:2:1 gives quarters and half. The weighted payoff is (−20+10+30)/4=5. SE scales with inverse square root; .2/20=.01. |
| 13–18 | The interpolated ranks give 2.5, 1 and 3. A margin .0196 gives [.0304,.0696]. The illustrative resample sums to 10 and ordinary resamples retain the original size. |
| 19–24 | Replacement allows repeats; no replacement selects distinct records. A fixed algorithm, seed, inputs and runtime reproduce the stream. .1/100=.001; survivorship and autocorrelation can invalidate the interpretation. |

The ten project tasks use the stated synthetic payoff distribution. Rational raw moments give mean 5 and variance 312.5. Supplemental uniform draws classified by the three CDF bands reproduce both exact-source sequences; integer sums and raw moments independently check sample estimates. For bootstrap, separate uniform-index replay from the 1,000-draw sample reproduces all 2,000 means and yields SD .55370 versus SE .55629. Both weighted samples have interpolated tails −20 and 30. No empirical calibration, dependence-aware bootstrap or independent acceptance was performed.

**F123.** Floating sums or endpoint differences could overflow before computing a finite statistic, and the interval could silently emit infinity. The corrected lab scales relative weights, uses a stable mean and interpolation, and rejects unreportable interval endpoints. Extremely small sampling weights and other runtimes were not validated. F28 and F32 remain open.
