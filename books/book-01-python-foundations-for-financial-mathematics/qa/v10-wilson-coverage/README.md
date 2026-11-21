# V10 — Section18.10 fixed-N Wilson coverage assumptions

Source pin `51991b60a598dd4167a26cfcc245821655fd8621`,reviewed2026-11-21. [Runnable review](review.py),[first](first.json),[replay](replay.json),[prior identity](identity.json). Run from repository root:

```bash
python books/book-01-python-foundations-for-financial-mathematics/qa/v10-wilson-coverage/review.py first
python books/book-01-python-foundations-for-financial-mathematics/qa/v10-wilson-coverage/review.py replay
```

378supplemental checks pass twice withidenticalrows:64nativeWilsonendpoints,288nativeinterval/exactscore-containment decisions,18exactbinomial-mass checks andeightcomplement-coverage identities. Thereare32nativewilson_interval calls:events0..N atN10andN20. Cachedreturnedintervals arethencomparedacrossnineselectedtrueprobabilities perN;this isnot288newsourcecalls. Theentireverbatimreferencedemo/twelveexistingmethods andcompile passperrun(fourcommandrecords/24invocationsofthe same12methods acrosstworeplays). No newanswers/workflows/labsteps/historicalmethod totals. PriorF182/88predicateevidence and19originalfailures/observertransitions retainedat originalscope;listingidentitymatches. No sourcechange ornewimplementationdefect found.

## Independent algebra and exact finite-model diagnostic

Callerz=1.96=49/25 isexplicit;no sourceconfidence-level orquantile lookup isinferred. Invert thescorequadratic A*p²−B*p+C≤0 with A=N(N+z²),B=N(2k+z²),C=k². Independent160-digit Decimalrootsexpectations checkthe two sourceendpoints foreachk,N. Sourceandobserver shareDecimal.sqrt,not independentarithmetic-librarycertification.

For truep∈[0,1],theexactscoredecision is N(p−k/N)²≤z²p(1−p). Itagreeswithnativefloatingintervalcontainment inallselected cases. Exactbinomialmasseschoose(N,k)p^k(1−p)^(N−k) sumto1;sumtheacceptedmasses toobtaincoverage. Selectedpvalues are0,.01,.1,.25,.5,.75,.9,.99,1,with noMonteCarlosamplingorstreamqualityclaim.

| N | truep | Exact-model coverage (decimal display) |
|---:|---:|---:|
|10|.01|.9043820750088045|
|10|.5|.978515625|
|20|.01|.9831406623643483|
|20|.5|.9586105346679688|

Fullrationalcoveragefractions andaccepted eventcountsareinJSON. AtN10,p.01,onlyk0covers;coverageequals(.99)^10. AtN20,p.01,k0andk1cover. Thesearefixed-NIIDBernoulli-model results,not empiricalcoverageestimates,universalnominal95%guarantees ordefectsintheexplicitlyapproximateWilsoncontract. Zeroobservedevents occurwithpositiveprobabilityanddonotprovep0;sourceclosedboundaryintervalsretainpositiveupperbounds.

## Assumption/step contracts

| Contract | Scoped disposition |
|---|---|
|Samplingdesign|IndependentBernoullitrials withfixedprespecifiedNintheexactreference model;sourcecounts cannotauthenticate independence.|
|Criticalvalue|Caller-supplied1.96,notanexact95%quantileimplementationorStudent-tmethod.|
|Interpretation|Frequentistcoverage acrossrepeatedcounts atfixedtruep;observedinterval containsornot,themodelparameterisnotre-randomized.|
|Boundarybehavior|Zero/allcountformulasandcomplementcases checked;not evidenceofabsenceofeventrisk.|
|Otheruncertainty|Parameter/model/discretization/market risk notquantifiedbythissamplinginterval.|
|Stopping/planning|No confidence-sequence orsequentialstoppingcoverageapproved;plannedcountsremainformulaoutputs,notexecutedsimulations.|

Oldfortyanswer/twelvesteplabrecords andmean/planning/rangeguards remaininthepriorformalreview,notrecounted. Arithmeticrtol5e-14/atol1e-12 isnotastatisticalacceptanceband. Next18.11portfolio-simulationassumptions. V10/Book1remaininprogress;F28/F32/F209/F165/F185 andbroaderintegration/resource/model/platform/release/independent/canonicalacceptanceopen.
