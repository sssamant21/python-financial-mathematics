# Section 14.3 — scoped probability rules review

Reviewed [Probability Rules](../../chapter-14/14.03-probability-rules.md) at `b8d9ad694136393a36aca2c06d9c0798062cb21c`. Run `python -B review.py` here. [Original results](baseline.json) retain nine failures; [corrected results](results.json) record all output, hashes, numeric expectations, and observed values. The extracted standard-library lab was run as named, compiled, and imported in isolation. Three command checks, twelve existing test methods and 40 additional predicates passed on rerun. No historical unique methods were added.

| Answers | Independent derivation and alignment |
|---|---|
| 1–5 | A valid event mass is between zero and one. All atoms sum to one; the empty set sums to zero. Complement of .04 is .96; disjoint masses .20 and .30 add to .50. |
| 6–10 | For .40 and .30 marginals with .10 overlap, the exclusive masses are .30 and .20, giving .60 union and .50 exactly-one. Marginals .50 and .40 and union .70 imply .20 overlap. Adding atoms preserves subset monotonicity; complement of .45 is .55. |
| 11–17 | Independent .60 and .50 events intersect in .30 and their union is .80. Direct ratios 5/20 and 5/13 give the two conditional probabilities. The joint mass .05 exceeds .20×.13=.026. Total probability adds .05 and .08; multiplying the reversed conditional by .13 reconstructs .05. |
| 18–24 | The survival masses multiply to .9506, with .0494 complement. The sample weight sums are 1 and 1.1. Conditioning on zero mass is undefined here; disjoint positive-mass events cannot satisfy the product identity. Inclusion–exclusion prevents overlap from being counted twice. |

For the ten-step project, the independent oracle assigns integer weights 72, 8, 15 and 5 to the four states. It enumerates all 256 ordered pairs of events and compares the joint and union masses to the source. Project calculations also verify 25% default given stress, 10% default given normal, and 5/13 stress given default. The results file contains the supplemental reconciliation table, scenario version and hypothetical input weights. Production calibration, provenance collection outside the synthetic fixture and risk decisions remain design scope.

**F112.** Invalid operands could disappear in intersection or complement; accepted near-unit mass could return a probability above one. The default absolute tolerance mislabeled very rare dependent events, and invalid tolerances were accepted. All operands are now validated before set operations, accepted mass is normalized, and exact independence is the default with opt-in absolute tolerance. This is scoped Linux CPython evidence; F28, F32 and independent acceptance remain open.
