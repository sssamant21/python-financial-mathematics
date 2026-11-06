# Section 14.12 — scoped distribution survey review

Reviewed [Common Probability Distributions](../../chapter-14/14.12-common-probability-distributions.md) at `c6aa18bb662a2ee15a3c3c531759ebb52c7fdfbe`. Run `python -B review.py`. The [baseline](baseline.json) retains five failures and the [rerun](results.json) records exact commands, source hashes and independent expectations. Three command checks, twelve existing methods and 39 additional predicates passed. Execution used the exact standard-library listing, compile and isolated import; no historical unique methods were added.

| Answers | Independent review |
|---|---|
| 1–4 | Bernoulli outcomes have mass .02 and .98; the first and second moments are both .02, so the variance is .0196. |
| 5–10 | Ten survivals give .9¹⁰; choose which one defaults for the next mass. Six ways to choose two successes in four trials give .2109375. The ten indicators add to mean 1 and variance .9. The zero-count complement gives .65132156. |
| 11–18 | Poisson zero mass is exp(−2), and the next mass doubles it. The first and second factorial moments are 2 and 4, implying variance 2. Uniform density is .1; length 3 gives .3, midpoint 5, and integrating the centered square gives 100/12. |
| 19–24 | Exponential scaling gives mean 2 and survival exp(−1) at two hours. Standard normal symmetry splits mass in half and relates opposite tails. Dependence invalidates simple binomial assumptions, and overdispersion calls for testing the Poisson model. |

For the ten project steps, supplemental enumeration of 1,024 weighted default paths verifies all 11 binomial masses and both moments. Poisson masses are compared by a separate forward recurrence. The exact source's 20,000 simulated counts match a seeded uniform replay, with mean 1.0017. Poisson(1) assigns .36787944 to zero vs .34867844 for Binomial(10,.1) and has larger variance and unbounded support. The common-shock stress is conceptual with an explicit arithmetic example; no calibration, operational decision or independent acceptance was performed.

**F121.** Float conversion could overflow binomial coefficients or CDF intermediates, and the original normal CDF erased a representable left tail. The corrected code scales before conversion and uses the complementary error function; an independent Simpson integration of the normal density on [10,14] checks the −10 CDF. Poisson extreme-rate accuracy and arbitrarily rare simulation tails remain outside this scope. F28 and F32 remain open.
