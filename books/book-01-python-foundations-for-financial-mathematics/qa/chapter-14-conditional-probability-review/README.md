# Section 14.4 — scoped conditional probability review

Reviewed [Conditional Probability](../../chapter-14/14.04-conditional-probability.md) at `b64bb51b940a20bc11928a3f433713d218e1007a`. Run `python -B review.py` here. The [baseline](baseline.json) retains six failures and the [rerun](results.json) records the exact command output, source hashes, and expectations. The source fence was copied verbatim to the prescribed script, executed with all twelve existing methods, compiled, and imported in isolation. Three command checks and 33 additional predicates passed. No historical unique methods were added.

| Answers | Independent review |
|---|---|
| 1–8 | Direct ratios .06/.20 and .06/.15 differ because the conditioning event changes. The four credit atoms yield .05/.20, .08/.80, .05+.08 and .05/.13. The stress survival complement is .75 and .20×.25 reconstructs the .05 joint probability. |
| 9–12 | The weighted default branches give .05+.08. In 10,000 modeled alerts, 100 borrowers default, giving 90 true flags; the other 9,900 produce 990 false flags, hence 90/1080. Removing the false flags gives posterior one if any flags remain; zero flags leave no denominator. |
| 13–18 | Independence with positive conditioning mass preserves .30. Joint .20 over .40 gives .50, different from .30. Disjoint events have zero conditional mass; self-conditioning is one if defined. The second regime model gives .040+.018=.058, with posterior .04/.058=20/29. |
| 19–24 | Sensitivity and posterior are reversed conditions; specificity is the false-positive complement. Predictive value needs a prior and likelihoods; changing time horizons or prior can change the result. Weighted loss .6×.1+.4×.3 is .18. |

The ten-task project uses direct integer atoms 72, 8, 15 and 5. It verifies both directions of the multiplication rule, .13 reconstructed by total probability, and stress and default dependence because .05 differs from .20×.13. The source computed the conditional results and the alert posterior. The supplemental audit record in the JSON lists denominators, the source fixture, tolerance and observed results. No dashboard UI, production calibration, or independent acceptance was performed.

**F113.** Invalid numerator labels could disappear on intersection. Near-unit accepted weights could yield a probability above one, single-pass regimes were consumed before weighting, and positive evidence could round to zero before Bayes division. The correction validates both events, normalizes mass, consumes regimes once and computes the ratio with exact fractions. F28 and F32 remain open.
