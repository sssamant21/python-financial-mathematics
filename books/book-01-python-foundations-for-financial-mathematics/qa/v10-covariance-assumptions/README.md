# V10 — Section14.11 covariance/correlation model assumptions

Pinned manuscript: `f0af8925838af1a123848be1b3774c45c009bb29`. Run `python -B review.py results` and `python -B review.py replay`. [Results](results.json) and [replay](replay.json) each record **119 predicates passed,zero failed**, exact source/listing SHA256, Python/platform and captured native commands. No initial financial or observer failure occurred. No manuscript/source correction was required.

| Selected contract | Independent expectation and scope |
|---|---|
| Paired observations and scaling | Six pairings with unchanged three-value marginals compare source covariance to pairwise products of differences. Six signed scale pairs per pairing check covariance scaling,shift invariance and correlation sign. Marginals or length checks do not establish correct timestamp alignment. |
| Sample estimator | Exhaustive IID draws of paired vectors at sizes2/3 check sample covariance unbiasedness and descriptive covariance factor(n−1)/n for independent/shared/opposed within-pair laws. IID is required across draws;the two coordinates need not be independent. Perfectly shared observations across time instead give sample covariance0. |
| Linear versus joint downside dependence | Two stipulated finite laws both have Pearson correlation0 while joint negative-event probabilities are1/4 and0. This is a synthetic model comparison,not empirical tail calibration or a same-marginal claim. |
| Matrix feasibility | Each of three two-asset matrices with variance1/covariance−.9 passes the lab's pairwise bound. Their proposed three-asset matrix gives negative quadratic form−2.4 on the all-ones vector,proving non-PSD. This supplemental algebra is not a source three-asset validator. |
| Portfolio weights | Nine combinations of signed/leveraged weights and feasible covariances compare with exact rational quadratic forms. Lower correlation reduces the cross term only when the weight product is positive. |

The exact Python fence is imported in isolation;native main and compilation run once per final execution. **Four commands/24 invocations of twelve existing methods** across both runs. Supplemental finite-law,estimator and matrix reasoning is labelled in the records;these do not add manuscript methods,workflows,answers or project steps.

Exact source/listing identities match [the prior formal review](../chapter-14-covariance-review/README.md):F120,eight initial failures,29 predicates,24 answers and ten-step project remain retained within their original scope. Actual date alignment,nonstationary market estimation and matrix calibration are not performed.

Next: §14.12 common-distribution assumptions,then14.13–14.17 and other marked V10 interfaces. V10/Book1,F28/F32/F209/F165/F185 and broader acceptance remain open. No independent reviewer,platform,release or canonical acceptance.
