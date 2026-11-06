# Section 14.8 — scoped continuous random variables review

Reviewed [Continuous Random Variables](../../chapter-14/14.08-continuous-random-variables.md) at `afda7a09f82b9067a77e89a29cd1a3c6af77b003`. Run `python -B review.py` here. The [baseline](baseline.json) preserves six failures and the [rerun](results.json) records exact command output, hashes and independent expectations. The standard-library fence was copied verbatim, run with all twelve existing methods, compiled and imported in isolation. Three command checks and 31 additional predicates passed. No historical unique methods were added.

| Answers | Independent review |
|---|---|
| 1–8 | Integrating the exponential density from zero gives the CDF; integrating from the threshold to infinity gives survival. At rate .5, the one-hour density is half the survival, and the (1,2] interval has mass exp(−.5)−exp(−1). Negative times are outside the support. |
| 9–13 | By the change of variable u=.5x, the exponential's first two raw moments are 2 and 8, so variance is 4. Solving survival .5 and .1 gives the median and 90th percentile. |
| 14–20 | An integral over a singleton is zero; a density has inverse-time units. CDF is monotone and the survival complement uses the same threshold. Converting 2 hours gives 120 minutes. Rate 2 gives mean .5, and the quantile is a cutoff rather than a mean. |
| 21–24 | Uniform probability is length ratio 3/10 and symmetry gives midpoint 5. Lognormal support is positive by construction, and time-varying intensity violates the constant-rate model. |

The ten project requirements use rate .5/hour. A high-precision Decimal calculation checks the density, CDF, survival, interval and quantiles. Independent inverse-CDF replay with the same underlying uniform generator matches the 20,000 source draws to floating-point tolerance. The mean is 2.005217655 hours, and the nearest-rank 90th percentile is 4.607543410 hours. Both lie within four standard errors of the analytic targets, using the asymptotic quantile standard error. The supplemental audit record documents the synthetic parameters and units. Queue behavior and operational hazard calibration were reviewed as design issues, not executed against production observations.

**F117.** Direct CDF subtraction erased a positive far-tail interval; density evaluation could underflow before applying the rate. Boolean time values and unreportable quantiles or draws were not rejected. The corrected listing factors interval mass by survival, evaluates extreme density in the log domain, and validates numeric inputs and finite reported times. Extremely small probabilities can still round to zero at float output. This is scoped Linux CPython evidence; F28, F32 and independent acceptance remain open.
