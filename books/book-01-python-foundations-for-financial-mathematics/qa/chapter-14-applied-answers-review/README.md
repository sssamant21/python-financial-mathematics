# Section 14.17 — scoped Chapter 14 assessment review

Resumed the unfinished baseline from parent `c6246704bbdb1d9095cfef6d2edc0be630c39909` on fresh main `8d1be9d0249aa6fed2256c7e9b27120754df176b`; intervening changes were confined to Book 2. The assessed [manuscript](../../chapter-14/14.17-exercises-and-applied-problems.md) was unchanged. Run `python -B review.py`. The [baseline](baseline.json) retains eleven failures, and the [rerun](results.json) records source hashes, command output and independent numeric expectations. The verbatim standard-library lab ran twelve existing methods, compiled and imported in isolation. Three command checks and 49 additional predicates passed. No historical unique methods were added.

| Chapter-wide answers | Independent review |
|---|---|
| 1–6 | Two ordered fair flips give four equally likely states. Inclusion–exclusion gives .6, complement gives .98, conditioning gives .12/.3=.4, and independence is the stated .4×.3=.12. The positive predictive value is 18 true flags per 67 flags. |
| 7–12 | A binary indicator has first and second moment .02, so variance .0196. Independent counts add means and variances to 1 and .9. Ten survivals give .9¹⁰; the complementary event gives .65132156. |
| 13–18 | The trial-count geometric mean is 1/.2=5. Poisson has zero mass exp(−2), mean and variance 2. The uniform interval is length 3/10, exponential survival exp(−1), and the normal z score is (12−10)/2=1. |
| 19–24 | Normal integration gives .841345 and .682689. The weighted payoff moments are 5 and 337.5, giving variance 312.5 and SE √312.5/100. Replaying bootstrap draws does not remove sampling uncertainty. |

Applied A: supplemental enumeration of 1,024 weighted binary paths checks all 11 local binomial masses. A separate Bernoulli-loop simulation (not part of the manuscript API) produces the retained 20,000-count histogram and mean 1.0017. Independence and homogeneous default probabilities remain assumptions.

Applied B: the exact source's weighted samples match independent uniform classification at n=1,000 and 20,000. Integer moments check their means, sample SDs and SEs; percentiles follow the declared interpolation. A supplemental index replay reproduces all 500 bootstrap means. Shifted source draws retain the +$2 pairing. The supplemental JSON audit records the seeds, inputs, summaries, source hash and runtime; the local listing has no manifest or stress exporter.

Applied C: independent Simpson integration and bisection give the 5th return percentile −.02289707254 and unfloored loss quantile $2289.70725. The source CDF agrees at that independently derived quantile. No model calibration, market forecast, operational runbook execution or independent acceptance was performed.

**F126.** The assessment inherited binomial and moment range failures, lost integer spread, used unnormalized mass, overflowed interpolation or averages, and consumed one-pass simulation inputs before use. Exact arithmetic and stable summaries now preserve the tested values and reject unreportable outputs. The twelve capstone checklist items remain a rubric, not twelve approvals. F28 and F32 remain open.
