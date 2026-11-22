# V10 — Section 15.7 finite sampling-design assumptions

Pin: `0e5b5fc323732073c2164acbad2e30507e13a883`. [Runner](review.py), [first](results.json), [replay](replay.json).

```bash
python books/book-01-python-foundations-for-financial-mathematics/qa/v10-sampling-design/review.py results
python books/book-01-python-foundations-for-financial-mathematics/qa/v10-sampling-design/review.py replay
```

**416 predicates pass twice**, identical rows. Four exact-fence demonstration/compilation commands pass across the final pair, including 24 invocations of twelve existing unittest methods. No source failure or source change. [F133 prior review](../chapter-15-sampling-estimation-review/README.md) source/listing identities match; nine initial failed predicates, 34 corrected predicates, 24 local answers and ten project tasks retain their scopes. No new historical methods, workflows, answers or steps are counted.

| Predicates | Native execution and independent design expectation |
|---|---|
|73|All six unordered size-two samples without replacement and all sixteen ordered pairs with replacement from [0,1,2,3]. Source means, variances and SEs checked with exact pairwise-distance formulas and 100-digit square roots. External uniform design laws give mean 3/2 and sampling-mean variances 5/12 versus 5/8. Expected corrected variance is 5/12 in the first design; uncorrected variance expectation is 5/8 in the second. Incorrectly applying FPC to replacement samples yields 5/16. Unbiased estimated variance does not imply unbiased estimated SE.|
|4|Finite population variances with N and N−1 denominators are 5/4 and 5/3. Source FPC sqrt(1/2) multiplies sample-s/sqrt(n); the distinct known N-denominator SD convention gives exact design SE sqrt(5/12).|
|5|Native census returns every unit, mean 3/2 and FPC/corrected SE zero despite positive uncorrected SE. This concerns the finite frame only, not measurement error or future uncertainty.|
|4|Census of the caller-selected frame [2,3] has local FPC zero but full-frame target bias 1 and MSE 1. FPC cannot repair a wrong sampling frame.|
|66|32 native seeded draws from labelled units versus duplicate values [1,1,2,2] preserve selected unit identity and value mapping. Duplicate values occur; their ideal six-subset design probability is 1/3. PRNG uniformity is not proved by seed replay.|
|256|Every size-four resample of four labelled empirical observations is externally enumerated and evaluated by native sample_mean. This is exhaustive arithmetic under a declared empirical law, not execution of the native PRNG bootstrap for all possible seeds.|
|3|That conditional empirical bootstrap has mean 3/2 and variance 5/16, distinct from the original n−1 variance estimate 5/12.|
|3|Actual bootstrap_means with B=128/seed=11: count and exact repeatability; native bootstrap_standard_error agrees with independent pairwise variance of those reported means. No population calibration or coverage claim.|
|2|Prior whole-source/listing identities.|

Sections 2–8 assumptions are crosswalked to the declared finite designs above. Sections 9 and project tasks retain conceptual requirements for eligibility/as-of boundaries, missingness, delistings, serial/cluster dependence, nonstationarity, weighting, provenance and real inclusion probabilities; these synthetic fixtures do not satisfy those operational requirements. Block bootstrap and stratified/cluster estimators are described, not implemented by this lab. The ordinary bootstrap resamples the observed empirical frame and does not identify an unobserved population or repair selection bias.

Next: reconcile the remaining V10 scope and evidence obligations against the current tracker before choosing the next unfinished substantive item. Selected 15.1–15.15 assumption crosswalks do not establish whole-book acceptance or close V10. F28 notebook/platform, F32 shared-input integration, F209/F165/F185 and broader numerical/resource/data/model/platform/release/independent/canonical gates remain open. Local Linux CPython only.
