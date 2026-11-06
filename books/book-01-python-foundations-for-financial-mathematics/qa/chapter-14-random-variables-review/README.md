# Section 14.6 — scoped random variables review

Reviewed [Random Variables](../../chapter-14/14.06-random-variables.md) at `67cd50135e7ff7087a045d259d0499c57270cecf`. Run `python -B review.py` here. [Baseline](baseline.json) preserves six failures; [rerun](results.json) records exact command output, source hashes and numeric expectations. The standard-library listing was extracted verbatim, run with all twelve existing methods, compiled and imported in isolation. Three command checks and 30 additional predicates passed on rerun. No historical unique methods were added.

| Answers | Independent review |
|---|---|
| 1–7 | Three outcome labels map to distinct payoffs. Integer weights 1:2:1 give mean 5 and second moment 337.5, hence variance 312.5 and SD about 17.6777. The negative state carries one quarter and the positive states three quarters. |
| 8–13 | Scaling by 2 doubles the centered differences and multiplies variance by 4; adding 1 shifts the mean to 11. A constant payoff has variance zero. Duplicate zero payoffs have aggregate mass .5. Bernoulli moments follow by counting the default state, and 4000 × .02 = 80. |
| 14–18 | Price gains are (90−100)/100 and (120−100)/100. A .05 simple return raises 100 to 105. At 5, inclusive CDF includes bear and base; the strict event includes only bear; the upper inclusive event includes base and bull. |
| 19–24 | Continuous density models have no point masses. The variable is a function on states. A 100 loss with probability .1 gives mean 10; an indicator averages to its event's probability. Sample averages and hypothetical weights do not imply calibrated future outcomes. |

The twelve project requirements were reviewed using the stated three-state fixture. Direct counts, the second-moment identity, and cumulative mass sums independently reproduce the analytic outputs. A supplemental inverse-CDF replay assigns each seeded uniform draw to one of the three intervals; it matches all 10,000 exact-source draws and the observed mean $4.95. The rerun records the counts, theoretical standard error, invalid-input results and tests. No continuous sampler, model calibration, or independent acceptance was performed.

**F115.** Conversion of integer labels to floats could merge distinct payoffs, moments could overflow before applying probability weights, and near-unit accepted weights were not normalized. The fix preserves payoff labels, normalizes accepted mass and computes moments before float conversion. Simulation still uses floating sampling weights; rare-tail sampling and cross-platform behavior are outside scope. F28 and F32 remain open.
