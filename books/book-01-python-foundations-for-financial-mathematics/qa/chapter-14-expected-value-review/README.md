# Section 14.9 — scoped expected value review

Reviewed [Expected Value](../../chapter-14/14.09-expected-value.md) at `28f70b6ff1510516a24644b167adb70f68e0e56e`. Run `python -B review.py` here. The [baseline](baseline.json) retains nine failures; the [rerun](results.json) records exact command output, source hashes and expectations. The exact standard-library fence ran as named with all twelve existing methods, compiled, and imported in isolation. Three command checks and 37 additional predicates passed. No historical unique methods were added.

| Answers | Independent review |
|---|---|
| 1–7 | Weights 1:2:1 give (−20+10+30)/4=5. The constant and indicator expectations are 7 and .02. Fixed loss on default is 4000; weighting by .02 gives 80. Zero or unit PD give the stated bounds; −8+2=−6. |
| 8–13 | Affine maps give 2×5+1 and 5−3; direct second moment is (400+50+900)/4=337.5, distinct from 25. Discounting 110 by 1.10 gives 100 with either certain cash or the specified expected cash and deterministic rate. |
| 14–20 | A 5% chance of 1000 gives expected claim 50 at the same date; this excludes expenses and risk loading. The three-scenario sum is −20+10+24=14; opposing return endpoints average .05. Expectation adds without independence, the weighted portfolio gives .07, and an indicator averages to its probability. |
| 21–24 | Conditional weights give .4×100=40; squaring outcomes before averaging gives 2 instead of 1. Equal expectation need not imply equal downside. Inconsistent weights invalidate an authoritative expectation. |

The ten project requirements use a one-period synthetic dollar payoff table and one-year credit assumptions. Direct integer sums yield 5, 337.5 and 11; multiplying loss on default (4000) by .01, .02 and .05 yields 40, 80 and 200. The exact lab agrees and discounts 110 at 10% to 100. Dependent variables were used in the linearity control. No independence assumption is needed for addition or deterministic discounting; multiplying separate expectations of stochastic factors would require additional justification. The supplemental JSON audit retains the scenario horizon and outputs. No empirical credit calibration, market pricing validation or independent acceptance was performed.

**F118.** Accepted near-unit mass was not normalized, large opposing payoffs could erase a representable difference, and an intermediate discount factor could overflow even when the PV fit in a float. All expectation paths now share validation and retain fractions through calculation; unreportable final results raise an explicit error. F28 and F32 remain open.
