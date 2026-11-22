# V10 — Section15.8 stochastic bootstrap replicate variability

Pin: `cdf2679391b0060db8465c0de08c09c632d658e6`. [Runnable review](review.py), [first](first.json), [replay](replay.json), [source identity](source-identity.json), [replicate sensitivity](sensitivity.json).

```bash
python books/book-01-python-foundations-for-financial-mathematics/qa/v10-bootstrap-variability/review.py first
python books/book-01-python-foundations-for-financial-mathematics/qa/v10-bootstrap-variability/review.py replay
```

Both runs pass **2,311 predicates** identically. There are384 native bootstrap calls per run: eight ordered n3 {0,2} samples×32 seeds atB27, plus two canonical nonconstant samples×32 seeds atB54/B216. They request24192 source bootstrap replicates per run. Independent histogram/rank arithmetic checks768 endpoint values,384 replay counts and1152 mean-target membership decisions. Seven separate exact-law checks verify multinomial mass, a binomial boundary identity and reflection. These are predicates, not new methods, workflows or answer records.

The exact conditional B27 oracle enumerates all4060 four-category count vectors for each of two empirical laws. For an original sample with one success out of three, resampled three-index means0,2/3,4/3,2 have probabilities[8,12,6,1]/27; the reflected sample has[1,6,12,8]/27. Exact multinomial integer weights and type7 rank counts determine conditional interval coverage. For target.2, coverage also equals P(2≤Z≤26), Z~Binomial(27,q0), independently checked as1−(1−q0)^27−27q0(1−q0)^26−q0^27.

| Original p | Exact IID-resampling B27 coverage |32-seed descriptive weighted average | Earlier controlled exhaustive27/type7 |
|---|---:|---:|---:|
|.1|.24990558776264937|.25228125|.243|
|.5|.7479341874743703|.75|.75|
|.9|.24990558776264937|.25228125|.243|

The first column of coverage results is an exact **hypothetical IID-resampling law**, combined with the finite original IID Bernoulli sample law. It does not validate the real PRNG. The second is a deterministic selected-seed diagnostic, not independent statistical replications, a calibrated coverage estimate or an acceptance band. The third belongs to a different controlled exhaustive design and is not relabeled as ordinary random B27. Rare conditional count events explain why a small seed grid need not expose the exact-law difference.

Actual source endpoints are checked against a separate Random(seed) **index** replay summarized into four bins; the histogram oracle selects order-statistic categories and interpolates exact rational ranks. This shares Python's Random/choices algorithm and is not an independent RNG-distribution oracle. Per-case data, B, seed, category counts, index-replay hash and exact oracle endpoints are retained. Endpoint tolerance is rtol5e-14/atol1e-12; model identities and membership decisions exact.

Sensitivity records show the actual endpoint spread acrossB27/54/216 for the two canonical samples. The original sample size remains3. IncreasingB changes Monte Carlo quantile variability, not original market information; a particular interval need not improve monotonically. Exact empirical inverse-CDF population quantiles and finite-B type7 interpolation remain distinct. Prediction intervals, selection-biased sampling, serial dependence, block/HAC methods and population/frame suitability are not implemented or accepted by this experiment.

Each run executes the complete source demo/twelve existing methods and compilation: four command records and24 invocations of twelve existing methods across both runs. Whole-source/listing identity matches F134. Its eleven baseline failures, critical-value observer correction,43 arithmetic predicates and2000-replay evidence retain their original scope; they are not recounted here. No source failure/change or new historical methods occurred.

The selected15.8 finite-model/replicate crosswalk is recorded; V10/Book1 remain in progress. Next:15.9 finite-null rejection rates/multiple-comparison dependence and post-selection assumptions, preserving priorF135/35-predicate evidence. F28/F32/F209/F165/F185 and broader numerical/resource/data/model/platform/release/independent/canonical acceptance stay open.
