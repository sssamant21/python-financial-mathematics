# V10 — Section15.8 finite-law interval coverage/dependence

Pin: `31f4962bb9efee1a6e09d65c72a59187f0ce14c4`. [Runnable review](review.py), [first](first.json), [replay](replay.json), [prior source identity](source-identity.json).

```bash
python books/book-01-python-foundations-for-financial-mathematics/qa/v10-confidence-coverage/review.py first
python books/book-01-python-foundations-for-financial-mathematics/qa/v10-confidence-coverage/review.py replay
```

Both runs pass **149 predicates** identically:48 native interval endpoints, eight controlled resample counts,72 native membership versus exact score/rank decisions, three law-mass checks, nine weighted coverage checks and nine dependent-law coverage checks. The complete exact source demo/twelve existing methods and compilation execute per run: four command records/24 invocations of twelve existing methods across both runs. No new historical unique methods, workflow, answer or project totals are added.

The finite model is X∈{0,2}, P(X=2)=p, n=3, target mean2p. All eight ordered IID samples are enumerated with exact p^k(1−p)^(3−k) weights. Mean/SE² derive from exact centered moments. Selected normal z=1.96 (explicitly supplied, not the function's slightly different default) and supplied df2 t critical4.30265273 give the native intervals. Independent exact membership tests use (mean−2p)²≤critical² SE², avoiding interval-endpoint arithmetic as the decision oracle. Endpoint arithmetic tolerance is rtol5e-14/atol1e-12; membership decisions exact.

| p | Normal interval coverage | Supplied-t interval coverage | Controlled exhaustive27/type7 coverage |
|---|---:|---:|---:|
|.1|.27|.27|.243|
|.5|.75|.75|.75|
|.9|.27|.27|.243|

These small discrete models do not satisfy the normal-sampling conditions for exact Student-t coverage and do not establish a95% normal approximation. All-identical samples have estimated SE0 and collapsed intervals excluding the interior model mean. The results are assumption counterexamples, not new implementation defects or a claim that nominal95% was promised for n3 Bernoulli samples.

For the bootstrap column, the actual source receives a controlled Random dependency that enumerates all27 ordered triples of the three **indices**, preserving repeated equal-valued units. It is restored in finally. This is a deterministic exhaustive27-replicate experiment, **not** the ordinary IID random B27 bootstrap procedure, the prior native B2000 seeded run, or a large-B limit. Independent rank-count arithmetic gives bounds[0,47/30] when k=1 and[13/30,2] when k=2. Type7 uses h=26p for these27 equally represented replicates; it differs from inverse-CDF quantiles of the exact empirical bootstrap population. No actual PRNG distribution/independence or ordinary stochastic-bootstrap coverage is certified.

A second sampling design repeats one Bernoulli draw three times, preserving each row's marginal law. Only all-zero/all-two samples occur, so all three interval procedures cover the interior target with probability0. This illustrates the independence-unit assumption; no HAC/block-bootstrap method is implemented or accepted.

Whole-source/listing hashes match [earlier F134 evidence](../chapter-15-confidence-review/README.md). Its eleven baseline failures, initial critical-value observer tolerance correction,43 arithmetic predicates,2000-replay record and24 answers/mini-project remain at original scope, not rerun/recounted here. No financial source changed and no new source failure was found.

Next:15.8 actual finite-replicate stochastic-bootstrap variability versus the exhaustive type7 control, with percentile/prediction/selection limitations explicit. Broader dependence-aware methods, population/frame/model suitability and independent acceptance remain open. V10/Book1 and F28/F32/F209/F165/F185/resource/platform/release/canonical gates remain IN PROGRESS/open.
