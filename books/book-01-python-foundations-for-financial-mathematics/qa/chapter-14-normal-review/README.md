# Section 14.13 — scoped normal distribution review

Reviewed [Normal Distribution](../../chapter-14/14.13-normal-distribution.md) at `fbd9451298eae7b84169dc25af84e1491ac189c9`. Run `python -B review.py`. The [baseline](baseline.json) retains seven failures; the [rerun](results.json) records exact commands, hashes and comparisons. The standard-library listing ran verbatim with all twelve existing methods, compiled, and imported in isolation. All three command checks and 36 additional predicates passed. No historical unique methods were added. An initial QA sampling probe used only ten draws and did not reach an overflowing draw; the retained baseline and rerun both use the same 100-draw probe.

| Answers | Independent review |
|---|---|
| 1–8 | Integrating the density gives a half at zero by symmetry and the stated one-sided and central masses at one, two and three standard deviations. The origin density is 1/√(2π). |
| 9–16 | Subtract 10 and divide by 2; the stated 8 and 12 cutoffs are ±1. Symmetry gives median 10 and variance 4. Numerically integrating and inverting the standard density gives ±1.644854. |
| 17–22 | Symmetry reflects both tails; the affine map gives mean 31 and SD 6. Independent normal variances 1 and 4 add to 5. Loss reverses the return tail, so 100000×(.02×1.64485362695−.01)=2289.7073. A sufficiently positive mean makes the unfloored quantile negative. A singleton has zero probability. |
| 23–24 | Jumps and clustering can invalidate the normal and constant-volatility assumptions. These are model considerations, not predictions. |

The ten-step project uses hypothetical one-period decimal returns and an unfloored dollar loss. Supplemental Simpson integration supplies the analytic reference and checks both central and extreme cases without the source's error-function implementation. At seed 42, a separate Box–Muller replay agrees with all 20,000 source draws within floating tolerance; the observed mean .00992388, sample SD .01997872 and nearest-rank 5th percentile −.02325365 are within four estimated standard errors of their targets. No market calibration or independent acceptance was performed.

**F122.** CDF subtraction erased far-right interval mass, normalizing extreme inputs could overflow, and the old quantile bracket clipped lower tails or overflowed under rescaling. The corrected listing uses the appropriate tail, bisects standardized probabilities, and delays conversion until after scaling. The quantile solver has an explicit tail cutoff; arbitrarily narrow intervals, arbitrarily small tails and production-grade extreme-tail accuracy are outside scope. F28 and F32 remain open.
