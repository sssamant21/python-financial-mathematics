# Section 14.5 — scoped independence review

Reviewed [Independence](../../chapter-14/14.05-independence.md) at `fdbb400eb865981a68ba00c11cb6b1e30472e247`. Run `python -B review.py` here. The [baseline](baseline.json) retains six failures; the [corrected evidence](results.json) records exact outputs, hashes, expectations and observed values. The verbatim standard-library listing ran with twelve existing methods, compiled and imported in isolation. Three command checks and 41 additional predicates passed after correction. No historical unique methods were added.

| Answers | Review and independent derivations |
|---|---|
| 1–6 | .20×.30=.06 and .20+.30−.06=.44. The two-loan baseline partitions 10,000 probability points into 9506 neither, 194 only A, 294 only B and 6 both; either is 494 and exactly one is 488. |
| 7–12 | Conditioning on a positive-mass independent event leaves the marginal unchanged. .05 differs from .20×.13, so the stress pair is dependent. Positive disjoint events fail the product identity; zero- and unit-mass events satisfy it with every event. |
| 13–18 | In even parity, each pair occurs jointly with probability 1/4 but all three cannot occur. Given C=1, the two remaining outcomes have one of A or B each, so conditional independence fails. The three-loan survival product is .941094. Zero covariance alone does not establish independence; independence implies zero covariance when moments exist. |
| 19–24 | Common shocks and volatility clustering undermine an untested independence assumption. The intersection lower bound is .8+.7−1=.5 and upper bound min(.8,.7)=.7. .06 equals the product of .20 and .30. Stress dependence can reduce diversification. |

The eight-step project checks both joint tables against integer probability points. At the same 2% and 3% marginals, the stressed joint mass is 1% vs 0.06% (50/3 times baseline), while the any-default probability is 4% vs 4.94%. Both distributions, all requested event probabilities and the independence classification were exercised. The runner's supplemental JSON audit contains the scenario inputs and outcomes. Common-factor calibration, portfolio loss severity, operational decisions, and independent acceptance were reviewed as scope limits.

**F114.** Binary subtraction erased small union probabilities, default tolerance hid rare dependence, conditional intersection could drop undeclared event members, and near-unit mass was not normalized. Exact arithmetic preserves the product model and normalizes input; invalid operands and tolerances reject explicitly. Exercise 16 now provides a concrete conditioning counterexample. F28 notebook/platform coverage and F32 shared-input integration remain open.
