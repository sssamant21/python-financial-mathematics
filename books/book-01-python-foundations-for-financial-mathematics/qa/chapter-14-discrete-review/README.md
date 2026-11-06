# Section 14.7 — scoped discrete random variables review

Reviewed [Discrete Random Variables](../../chapter-14/14.07-discrete-random-variables.md) at `8de70ceafbb6903c9f462a5fcc7c907a60446563`. Run `python -B review.py` here. The [baseline](baseline.json) retains seven failures and the [rerun](results.json) records exact command output, hashes, expectations, and counts. The standard-library fence was copied verbatim, run with twelve existing methods, compiled and imported in isolation. Three command checks and 48 additional predicates passed. No historical unique methods were added.

| Answers | Independent review |
|---|---|
| 1–9 | The valid and invalid mass sums are 1 and 1.2. The Bernoulli indicator has first and second moment .3, hence variance .21 and SD .4583. Only the zero outcome lies at or below 0; outside the support the CDF is zero or one, and the strict upper tail at 0 is .3. |
| 10–14 | The three-state moment sums give 5 and 337.5, hence variance 312.5. Inclusive CDF at 5 includes the first two values; strict thresholds at zero and five include just −20. |
| 15–21 | Two trials enumerate as .81, .09, .09 and .01; grouping gives .18 for one success. Independent indicators add to mean 1 and variance .9. Five survivals give .8⁵; the complementary event is .67232. Four trials give six ways to choose two, each with mass .25²×.75². The fixed default loss gives 4000×.02=80. |
| 22–24 | Under the stated Poisson assumption the zero-count mass is exp(−2)≈.1353. Dependent loans do not satisfy the binomial assumptions, and reproducibility does not establish calibration. |

For the ten project steps, the supplemental oracle enumerates all 1,024 binary paths using integer tenths (weight 9 for survival and 1 for default). All 11 source masses agree, as do the moments and event tails. The replay of uniform draws by explicit CDF boundaries matched both source sequences: the 20,000-draw means are 1.00525 and .99995, with theoretical standard error about .00671. Invalid input controls ran. A perfect common shock is a design stress: it preserves the marginal .1 and mean 1 but makes all ten defaults .1 rather than 10⁻¹⁰ and changes variance from .9 to 9. The figures are for synthetic one-year scenarios, not a calibrated default forecast.

**F116.** The original code lost small dispersion at large integer offsets, overflowed before weighting, accepted unnormalized near-unit mass, and could overflow constructing a binomial PMF before the small factors were applied. Exact fractions now carry these intermediates and explicit range checks govern reported floats. The simulation still uses floating weights, and full-support construction and rare-tail sampling were not evaluated at production scale. F28, F32 and independent acceptance remain open.
