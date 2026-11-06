# Section 14.15 — scoped random generation review

Reviewed [Random Number Generation and Reproducibility](../../chapter-14/14.15-random-number-generation-and-reproducibility.md) at `44c6a0bcd5d5e8e6ab8ac84e9691c89610d3ed3e`. Run `python -B review.py`. The [baseline](baseline.json) preserves five failures and the [rerun](results.json) records both fence hashes, exact commands and observed values. The verbatim lab ran twelve existing methods, compiled and imported in isolation. Its separate uniform illustration also ran verbatim. Three command checks and 32 additional predicates passed; no historical unique methods were added.

| Answers | Independent review |
|---|---|
| 1–8 | Replay depends on the algorithm, state and call sequence. Uniform cutoff .02 gives the ideal Bernoulli probability; exponential scaling gives mean 2; affine normal scaling gives mean .01 and SD .02. The weight ratio 1:2:1 gives mean (−20+10+30)/4=5. |
| 9–16 | 10/√100=1, a fourfold sample halves SE, and ±1.96 gives the stated interval. A local generator isolates state but does not guarantee statistical independence. Positive pairing covariance can reduce variance; a constant .02 shift gives .02 for every difference. |
| 17–24 | Seed changes are not an independence proof. 20,000×10=200,000 evaluations; the quantile convention is part of reproducibility. Manifest hashes identify bytes, not validation. The embedded token test verifies byte count only. Model bias and duplicate parallel state remain distinct from sampling error. |

For the ten-step project, direct moment sums give mean 5 and variance 312.5. Supplemental inverse-CDF classification reproduces all four source runs; integer sums give the means and sample standard errors. Reusing each seed for its stressed fixture yields an exact paired $2 shift on every draw. A separate canonical JSON string reproduces the SHA-256 digest of each source manifest; the supplemental audit supplies payoff, stress, runtime, and source metadata omitted by that narrow manifest. Parallel stream design, cryptographic security review, calibration and independent acceptance were not executed.

**F124.** Large weight sums and samples could overflow before scaling, tiny paired shifts were lost, and normal draws could silently be infinite. The corrected lab shares weight validation, scales before sampling, preserves paired differences, and rejects nonfinite draws. Rare-tail weights and cross-runtime sequences remain outside scope. F28 and F32 remain open.
