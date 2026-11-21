# V10 — Section18.8 paired-estimator and covariance assumptions

Pinned source `e3ea11cfbfcd0563d2306de43b97c4ab2a0ef9b5`, reviewed2026-11-21. [Runnable review](review.py),[first](first.json),[replay](replay.json),[source identity](source-identity.json),[prior identity](prior-identity.json). Run from repository root:

```bash
python books/book-01-python-foundations-for-financial-mathematics/qa/v10-paired-estimation/review.py first
python books/book-01-python-foundations-for-financial-mathematics/qa/v10-paired-estimation/review.py replay
```

Both corrected runs pass545supplemental predicates with identical rows:486source numeric fields,27caller exact covariance comparisons,27source-interval/exact-decision comparisons andfive exact model aggregates. Eachrun executes the entire unmodified reference demo/twelve existing methods andcompiles it;four commandrecords/24invocations of12existing methods across tworeplays. No newhistorical unique methods,fortyanswer,twelvelabstep orworkflow totals. PriorF180/104predicate review and13original failures are retained at original scope;listing SHA256matches. No financial implementation change ornew source defect found.

## Independent pair model

The independent unit is an IID *pair* (X,Y),where P(X=80,100,120)=(1/4,1/2,1/4) andY=X/2+50. Two strategies sharethe same underlying X;Y is not an independently sampled position. Paired difference D=Y−X=50−X/2 has outcomes10,0,−10 andmean0. Source estimate_mean iscalled separately onX,Y,D for each of27ordered three-pair outcome sequences,weighted byproduct probabilities. The27sequences are not equally likely. No Monte Carlo joint sampler orrandom-stream independence test isimplemented bythis observer.

Exact moments:Var(X)=200,Var(Y)=50,Cov(X,Y)=100,soVar(D)=200+50−2(100)=50. With three IIDpairs,Var(meanD)=50/3. Ignoring covariance instead gives(200+50)/3=250/3,five times larger. Exact reference expectations also give E(sampleVarianceD/3)=50/3 andE((sampleVarianceX+sampleVarianceY)/3)=250/3;these areexpectations ofvariance estimators,not squares ofexpectedreported SEs.

Fraction sample means/variances andseparate120-digit Decimal square-root/interval references check every native summary field:count,mean,SD,SE,two endpoints. Native functions compute no cross-strategy covariance;pair construction andthe naive-independent comparison arecaller analyses. Count/mean/SD/SE/report fields arevalidated numerically,not silently relabeled as anative paired-comparison API. Source andobserver share Decimal.sqrt butnot the arithmetic implementation;no independent arithmetic-library certification.

## Exact coverage diagnostic

For each weighted sequence,an exact rational decision tests meanD²≤(49/25)² sampleVarianceD/3. It agrees withwhether thenative reported normal interval contains0. Summing those probabilities gives25/32coverage for this particular N3discrete model,not95%. This is an exhaustive counterexample to universal nominal coverage,not a statistical failure ofthe documented teaching interface. No source guarantee was violated;the manuscript explicitly warns about small/discrete/dependent samples. IncreasingN,antithetic/control-variate construction,sequential orbinomial intervals andreal-world model acceptance remain outside this batch.

## Contracts and provenance

| Contract | Disposition |
|---|---|
|Estimand/units|Mean strategy difference infictionalcommoncurrency overonecommonperiod;fixed in-model probabilities,notmarket likelihoods/pricing approval.|
|Independent unit|Three IIDpairs inthereference model;withinpair covariance explicit. The supplied numbers donot establish actual RNG independence.|
|Prerequisites|Source accepts plain finite observations andcannot authenticate pairing/stream/model metadata. Caller mustconstructaligned differences beforeestimating their uncertainty.|
|Approximation|Native fixed-Nnormalinterval isonly a teaching approximation;25/32 isfixture-specific.|
|Old formal scope|Fortyanswers/twelvesteps,seed/sampler/range guards andsupplementalNumPystreams remaininprior review,not repeatedorclosedhere.|
|Progression|This scoped18.8V10assumptions batch iscomplete;next18.9convergence assumptions. V10/Book1 remaininprogress.|

[Initial observer](initial-observer.txt) and[actual serialization failure](initial-serialization-failure.json) retain aFraction JSON-writing error. Corrected serialization converts exact non-JSON observer values tostring;source numeric checks unchanged. This is aQA serialization issue,not a manuscript defect. Corrected first/replay receipts arefinal. Arithmetic comparisons rtol5e-14/atol1e-12 are not statistical acceptance bands. F28/F32/F209/F165/F185 andbroaderintegration/resource/model/platform/release/independent/canonicalacceptance remainopen.
