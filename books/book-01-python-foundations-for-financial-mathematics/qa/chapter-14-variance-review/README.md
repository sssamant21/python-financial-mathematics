# Section 14.10 — scoped variance review

Reviewed [Variance and Standard Deviation](../../chapter-14/14.10-variance-and-standard-deviation.md) at `510524cb0b22e96a0c8748383afbbf11bf2aed95`. Run `python -B review.py`. The [baseline](baseline.json) retains nine failures. The [rerun](results.json) records source hashes, commands and predicates: three command checks, twelve existing methods, and 34 additional predicates passed. Execution uses the exact standard-library listing, compile check and isolated import. No historical unique methods were added.

| Answers | Independent review |
|---|---|
| 1–10 | Weights 1:2:1 yield mean 5 and raw second moment 337.5, giving variance 312.5 and SD 17.6777. A constant has no spread; shifting changes neither variance nor SD. Multiplying outcomes by two or minus one squares the factor for variance and uses its absolute value for SD. |
| 11–18 | Binary second moment equals p, giving .16 at .2; ten independent .1 indicators add to .9. For 1,2,3, pairwise squared differences total 6, giving population 6/9 and sample 6/6. Five observations give four sample degrees of freedom. SD restores original units. Outcomes 0 and 10 yield mean 5 and variance 25. |
| 19–24 | Greater SD means greater dispersion, not necessarily worse downside. Covariance 2 adds 4 to 4+9; independence omits that cross term. Perfect opposing values cancel. Fat tails require more than an SD summary, and total mass 1.2 is invalid. |

The ten-step project checks the theoretical PMF, affine transform, Bernoulli variance .0196 and sample/population denominators. The supplemental eight-state sign enumeration constructs the covariance fixture and confirms covariance 2 independently; exact-source PMF variances for X, Y, X+Y and X−Y are 4, 9, 17 and 9. No production model calibration or independent acceptance was performed.

**F119.** Unnormalized near-unit mass, lost integer spread, and intermediate variance overflow or underflow caused inaccurate or unreportable results. The corrected lab uses exact centered calculations and takes the square root before float conversion. F28 and F32 remain open.
