# Section 14.11 — scoped covariance and correlation review

Reviewed [Covariance and Correlation](../../chapter-14/14.11-covariance-and-correlation.md) at `92cc74261632fef18658f1df523275d2284b0cc6`. Run `python -B review.py`. The [baseline](baseline.json) retains eight failures and the [rerun](results.json) records source hashes, command output and independent expectations. The exact standard-library listing ran all twelve existing methods, compiled, and imported in isolation. All three command checks and 29 additional predicates passed. No historical unique methods were added.

| Answers | Independent review |
|---|---|
| 1–8 | Pairwise products of differences total 12; dividing by 9 or 6 gives 4/3 or 2. Positive/negative proportional centered vectors give ±1. Pairwise products are symmetric, and self-products give variance 2/3. The symmetric X and its square have zero cross-moment but are dependent. |
| 9–14 | Covariance multiplies the units; correlation cancels them. Adding/subtracting a covariance of 2 changes the base variance 13 by ±4. Portfolio arithmetic gives .0325 and .03456, the latter with SD .185903. |
| 15–21 | The product of volatilities is .06, giving .012 at ρ=.2 and ±.06 at the extremes. .08 breaches the bound. Scaling the series by 3 and −2 multiplies covariance by −6; shifts leave it unchanged. Normalizing .012 by .06 gives .2. |
| 22–24 | With strictly positive weights and volatilities the covariance cross term increases with ρ. Missing dates need alignment before pairing. Pearson correlation does not establish low joint tail risk. |

For the ten-step project, both weighted volatilities equal .12, giving the independent simplification .0288(1+ρ). Source results match .01440, .02880, .03456 and .05184 at the four supplied stresses. The exact lab also checks the paired estimator, symmetry, self-covariance and invalid inputs. The supplemental JSON records the synthetic pairs and stress values. Actual timestamp alignment, risk calibration and independent acceptance remain outside this run.

**F120.** Covariance could erase integer spread and reuse an already-consumed iterator. Correlation could overflow or underflow its normalizer, and an absolute covariance tolerance or overflowing variance product could admit an impossible matrix. The corrected listing keeps exact intermediates and checks the squared covariance bound before evaluating portfolio variance. F28 and F32 remain open.
