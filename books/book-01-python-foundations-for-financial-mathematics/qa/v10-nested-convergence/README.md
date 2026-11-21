# V10 — Section18.9 nested-prefix covariance and convergence assumptions

Pinned source `63984650b354db8b361106303bc5d2317a314e71`, reviewed2026-11-21. [Runnable review](review.py),[first](first.json),[replay](replay.json),[identity](identity.json). Run from repository root:

```bash
python books/book-01-python-foundations-for-financial-mathematics/qa/v10-nested-convergence/review.py first
python books/book-01-python-foundations-for-financial-mathematics/qa/v10-nested-convergence/review.py replay
```

738predicates pass twice withidenticalrows:648native summary fields,81source/exact error-worsening decisions andnineexactfinite-model aggregates.81native prefix_study calls eachreturntwo summaries(N2,N4);source summaryfields arecount,mean,estimatedSE,absoluteerror. Entireverbatimreference demo/twelve existingmethods andcompile passperrun;fourformalcommands/24invocationsof12existingmethodsacross tworuns. No newhistorical unique methods,answers,labsteps orworkflowtotals. PriorF181/88predicate review and12originalfailures remainat originalscope;listingidentity verified. No sourcechange/newdefect found;initial and replay areboth passingactual runs.

## Exact joint-prefix reference

IIDmodel X=80,100,120 withprobabilities1/4,1/2,1/4 hasmean100 andvariance200. We enumerateall81ordered four-observationsequences withproductweights,not81equallylikelysamples. The same four-observation sequence suppliesitsfirst2 andfirst4 values,so the native table isexplicitly nested. Rationalprefixmeans/samplevariances and120-digit Decimal square-rootreferences independentlycheck all648reportedfields. Decimal.sqrtbackendisshared;this isnotindependentarithmetic-librarycertification. No RNGdrawquality/streamindependence test orstatistical acceptancetolerance.

For this specified IIDmodel:

| Quantity | Exact value |
|---|---:|
|E(mean2−100),E(mean4−100)|0,0|
|Var(mean2),Var(mean4)|100,50|
|Cov(mean2,mean4)|50|
|Var(mean4−mean2)|50|
|Naive variance sum ignoring prefix covariance|150|
|E(sampleVariance2/2),E(sampleVariance4/4)|100,50|
|P(error atN4 exceeds error atN2)|17/64|

The correct variance ofthechange is100+50−2×50=50. Treatingtheprefix estimates as independent wouldgive150,three times larger. These areexact modelaggregates,notanative covariance estimator. AnordinarySEfield describes itsown samplemean;itdoesnot automatically supplyuncertainty for adifference ofdependentprefix means. Pair ormodelthedependence explicitlywhencomparing estimates.

The81sourceerror-worsening decisionsagree withrationalreferences;theirweightedprobability17/64quantifies thisparticular smallIIDexample. Itdoesnot estimateanunknownreal-worldprobabilityorprove anasymptotic theorem. LowerMSE atN4doesnot mean every realized errorimproves. The listedprobabilities andIIDassumption define thereference law;sourceplainobservationscannotauthenticate thoseassumptions.

## Scope and prerequisite review

| Contract | Disposition |
|---|---|
|Target/units|Fictionalcommoncurrency payoffmean100,onecommonperiod,explicitthree-state model. No marketmeasure/calibration approval.|
|Prefix design|N2andN4shareobservations;notindependentreplications andnotaveragedasanindependentpair.|
|Samplingrate|Var(mean)=200/N holdsunderthisIIDfinite-variance model;notguaranteedpathwiseerrorhalving.|
|Convergence|Finiteenumeration isnotanLLN/CLTprooforcoverage/stoppingrulevalidation.|
|Implementation/prerequisites|NativeprefixAPIvalidatesrequestedprefixobservations/sizes,notindependence,metadataorunusedtails. Priorinput/rangecontracts preserved.|
|Othererrors|Morepathsdo notfixmodelbias,wrongprobabilities,discretization,monitoringorimplementationerrors. No confidence-sequence/bridge/streamingAPI added.|

Arithmetic rtol5e-14/atol1e-12 isnotastatisticalacceptanceband. No sourceconfidenceinterval orsampleSDreport isclaimed;thisAPIexportsestimatedSEonly. Next18.10confidence/simulation-errorassumptions. V10/Book1remaininprogress;F28/F32/F209/F165/F185 andbroaderintegration/resource/model/platform/release/independent/canonicalacceptanceopen.
