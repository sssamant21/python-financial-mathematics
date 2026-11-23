# V10 — Section14.10 variance and SD model assumptions

Pinned source: `47f7f67f22be55b31fa5164f2774e3d324060610`. Run `python -B review.py results` and `python -B review.py replay`. [Results](results.json) and [replay](replay.json) each record **53 passed, zero failed predicates**, exact manuscript/listing SHA256, Python/platform and captured command output. No initial numerical failure or financial-source edit occurred in this batch.

| Contract | Independent expectation and scope |
|---|---|
| Transformations/units | Exact centered rational law gives variance312.5; nine signed/zero affine cases square the multiplier for variance and take its absolute value for SD. Unit conversions square variance units. |
| Covariance | Independent/shared/opposed sign sums give variances2/4/0, also checked with pairwise squared differences. For dependent X∈{−1,0,1},Y=X², covariance0 and sum variance8/9 coexist with a nonfactorizing joint event. |
| Sampling denominator | Exhaustive IID ±1 samples of sizes2,3,4 give expected sample variance1 and descriptive variance(n−1)/n. Shared samples give sample variance0 despite generating variance1: Bessel correction needs its sampling contract. |
| Default counts | Three IID and three shared indicators have identical marginal probability.5 and mean1.5 but count variances.75 and2.25. |
| Horizon scaling | Two-period additive sign sums give variances2/4/0 under zero/positive/negative covariance. This illustrates zero-cross-covariance requirements; it does not validate empirical252-day scaling or compounded wealth. |

The exact-source native main and compilation execute in isolation in each final run: **four commands,24 invocations of twelve existing methods** across two runs. Supplemental finite-law reasoning is labelled in records; it does not add manuscript methods or empirical calibration. Exact F119 source/listing hashes match [the prior review](../chapter-14-variance-review/README.md), retaining its nine initial failures,34 predicates,24 answers and ten-step project without duplicating totals.

A combined report-authoring heredoc initially failed to parse because triple-apostrophe prose conflicted with its Python string delimiter. No report writes or financial executions occurred in that failed authoring call; the diagnostic is retained in the paired Book2 evidence folder. Final documentation was written with literal heredocs. This was an authoring error,not a financial-source failure.

Next: §14.11 covariance/correlation assumptions,then14.12–14.17 and other marked V10 interfaces. V10/Book1,F28/F32/F209/F165/F185 and broader acceptance remain open. No independent reviewer/platform/release approval.
