# V10 — Section18.11 correlation, moments and joint-tail assumptions

Source pin `ad0f11b8eb295b0c062256a47d869044b874aa77`. [Runnable review](review.py),[first](first.json),[replay](replay.json),[prior identity](identity.json). Run from repository root:

```bash
python books/book-01-python-foundations-for-financial-mathematics/qa/v10-portfolio-moments-tails/review.py first
python books/book-01-python-foundations-for-financial-mathematics/qa/v10-portfolio-moments-tails/review.py replay
```

32checks pass twice:two analyticalsourcefields,14source-summaryfields,14exactfinite-modelmoments andtwocaller severelossindicators. Twonative summarize calls use64equallyweighted expandedrows each. Entireverbatimreference demo/twelveexistingmethods andcompile passperrun;fourformalcommands/24invocationsof12existingmethodsacrosstwo runs. PriorF183/90predicate numerical/input/samplerreview and15originalfailures remainat originalscope;listingSHA256matches. No sourcechange/newdefect/newanswers/workflows/historicalmethod totals.

## Controlled joint laws

Bothassetreturnmarginals take−.4,0,.4 withprobabilities1/8,3/4,1/8. Eachhasmean0,variance.04,SD.2. Bothjointlaws havecovariance0;withweights.5/.5,theanalyticalportfolio mean0/variance.02areidentical. Thesearenon-Gaussian callerfixtures;theyare**notdrawsfromthesourceGaussian simulator** anddonotcontradicttheindependencepropertyofaspecifiedjointGaussianmodel.

| Law | Construction | E[R1²R2²] | P(Rp<0) | P(Rp<−.3) |
|---|---|---:|---:|---:|
|Independent|8atomsmarginal×8atoms,64rows|.0016|13/64|1/64|
|Dependent,sameabsolutevalue|48zero/zerorowsplusfourcopiesofeach(±.4,±.4)|.0064|1/16|1/16|

Thefirsttwomoments andcorrelation agree,butdependenceandjointlossbehavior differ. Severe-lossprobability isfourtimeslargerinthisspecificdependentlaw;thisisnotamarket-tailprediction,generalstressboundorcomparisonofcalibratedmodels. Rationalmoments/weightedcountsareexact. Sourceanalyticalmean/varianceandsummarymean/count/SD/terminalmean/SE/lossfrequency/below−1countmatchindependently derivednumbers. ReturnSDusesthesampleN−1denominator;theoreticalpopulationvariance.02isnotconfusedwiththeobservedenumeration’ssamplevariance. Decimalrootsareindependentalgebrausingthesamearithmeticbackend,notindependentlibrarycertification.

The64rowsaredeterministicexpandedfinite-statequadrature,not64IIDMonteCarlopaths. NativeSEarithmetic ischecked,butitdoesnotestablishsamplinguncertaintyforthisenumerationorvalidateanIIDdesign. CallerthresholdRp<−.3isaseparateindicator;native summarize onlyexportsstrictlossRp<0. Allselectedassetreturns≥−.4;zerobelow−1countdoesnotcertifytheunboundednormalmodeltail. No clipping/resampling introduced.

## Contracts and remaining scope

| Contract | Scoped disposition |
|---|---|
|Positions/units|Oneperiod,longonlyfullyinvested.5/.5,initial100fictionalcommoncurrency;noactualhorizonlength/marketdate/data/calibration supplied.|
|Jointmodel|Correlationaloneisnotajointlaw;normalconstructor assumptionsandalternatefinitecallerrowsaredistinct.|
|Riskfields|Samevariance/nativeheaderdoesnotvalidatelosstails,modelmeasureorreal-worldrisk. No CDF/tailAPI/F165resolutionclaimed.|
|Sharedinputs|Summarytrustsprovidedthirdfieldportfolio returns;weights/horizon/currencyreconciliationremainexternalF32integrationobligations.|
|Multi-period|No buy-and-hold/rebalancing/costs/fundingextensionorvalidationperformed.|
|Progression|This18.11V10assumptions batchcompletesatselectedscope;next18.12risksimulation.|

Arithmeticrtol5e-14/atol1e-12 isnotastatisticalacceptanceband. V10/Book1remaininprogress;F28/F32/F209/F165/F185 andbroaderresource/model/platform/release/independent/canonicalacceptanceopen.
