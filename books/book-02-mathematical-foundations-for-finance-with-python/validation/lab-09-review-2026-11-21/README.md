# V-223 — Section9.9 project lab/export/acceptance crosswalk

Pinned executable source `e3ea11cfbfcd0563d2306de43b97c4ab2a0ef9b5`,reviewed2026-11-21. [Runnable review](review.txt),[baseline296/1](baseline.json),[baseline replay](baseline-replay.json),[corrected297/0](first.json),[corrected replay](replay.json),[source identity](source-identity.json),[runtime delta](runtime-delta.json).

Run from repository root:

```bash
python books/book-02-mathematical-foundations-for-finance-with-python/validation/lab-09-review-2026-11-21/review.txt first
python books/book-02-mathematical-foundations-for-finance-with-python/validation/lab-09-review-2026-11-21/review.txt replay
```

Append --baseline toreadthepinnedoriginalmanuscript;itsliteral acceptance-method mismatch intentionallyfails. Both baseline runs preserve296passes/onefailure;all numerical/CSV predicates pass. Requirement5 demandedmath.expm1 whiletheactual implementation deliberately formscompletehigh-precisionendpoints/errors beforefloatconversion. The wording nowdescribes thatmethod andkeeps expm1asamathematical identity/independentreference. No numericalPythonalgorithmchanged;the existing precision/exponent/report-range policies remainexplicitlylimited.

Corrected297predicates pass twice withidenticalrows:167completeCLI checks(18schemas,122numeric,27boolean/text),129callerCSVchecks andone manuscriptcontractpredicate. Eachrun compiles twoexactPythonfiles andpassesthreecommands:exactCLI,referencechecker,compile. Timestamps/environment/sourcehashes/actualstdout-stderr retained. Currency/rate fieldscompare rtol5e-14/atol1e-12;zeros/booleans/strings/schemas exact. Prior290projectreport predicates andbaseline/scenario historicalfailures remainat originalscope,notrerun/recountedasnewunique methods.

Independent140-digit references buildexp from120Taylor terms ratherthancalling sourcehelpers orDecimal.exp. Theyderiveoriginal-input discounted amounts,moments,endpointchanges,errors andinterval derivative bounds for allnine shocks. Represented binary64 rate/converted-shock inputs areconverted withFraction;bound interval usesexact R+H. Same Decimalarithmeticbackend isshared,whilethe exponential algorithm isindependent. These small-fixture numeric references are not a universal truncation/rounding certification orindependent-review signoff.

## Twelve acceptance requirements

| Requirement | Review/execution disposition |
|---|---|
|1 Inputvalidation|Exactsource referencechecker runs;broaderinvalid/range tests retained inprior baseline/scenario/report scopes.|
|2 Convention|CLI decimalannualcontinuous convention/modelmetadata checked.|
|3 Basispoints|Allnine signed bp/decimal fields checked againstconverted inputs.|
|4 Baseline|V,V′,V″,D,K independently derived/compared.|
|5 Exactchanges|Allnine completeendpoint changes compared;literalalgorithm wordingreconciled.|
|6 Approximations/errors|Alllinear/quadratic,signed/absoluteerror fields checked.|
|7 Intervalbounds|M2/M3atlowestexactintervalrate derived;bothboundfields compared. Proof assumptions positivefixedflows/times remainconceptual,notplatformcertification.|
|8 Boundflags|Reportederror vsreportedbound+documentedbaselineallowance checked;notlatent/roundingproof.|
|9 Grid|Defaulttwo-sidednine-shockladder/zeroidentity checked.|
|10 Machine-readable|CompleteCLI/schema plusstrictJSON andcallerCSVroundtrip;nativeJSONunchanged.|
|11 Independentchecks|Actualreferencecheckerruns;newindependentseriesoracles. Broadernumericaldomainacceptance pending.|
|12 Evidence/approval|Executiontimestamps/platform/pinhashes retainedexternally;native runtime_certified/independent_review_completed stayfalse.|

## Twelve exercise dispositions

1/2 differentiateexponentials;thirdderivative magnitude entersremainder.3 −75bp=−.0075 (conceptualunitreference,separatefromdefaultgrid).4singlepayment t3 impliesD3/K9 (retainedpriorfixture).5K−D²isPV-weightedtimevariance,not a samplingclaim.6+25bp exactchangeand7−50bpquadraticchange runinthedefaultCLI.8lowestintervalrate M2and9entire-intervalboundpremise reviewed.10zero-shock executes.11modelbiasversusapproximationerror remainsconceptual.12runtime/sourcechecks do notsupplyindependentreviewapproval. These12alignmentrecords arenotnewtestpredicates.

## Five extension contracts

| Extension | Scoped result |
|---|---|
|Nonparallel|Notnative section9.9;section9.8hasseparatelyreviewed cash-flowspot engine. No market-key-rate APIadded.|
|Threshold/kink|Notnativeprojectfeature;requirespiecewise cash-flowmodel andone-sided analysis.|
|CSV|Actualcallerexport [first](first-caller-export.csv) /[replay](replay-caller-export.csv),nine scenario rows/all14fields;126fieldcomparisons+rowcount,columnorder,unchangedJSON. Thisdoesnotadd anativeCSV API.|
|Currencytolerance|Notnativeprojectfeature;reportedmathematicalboundflags aredifferent fromauserchosen errorbudget. Section9.8tolerance isseparate.|
|Externaltestharness|Thisrunnable observer recordsPython/platform/actualUTCexecutiontimestamps,pinnedhashes andstdout/stderr. Not anapproval/data-lineage authority.|

[Caller exportmetadata](first-caller-export-metadata.json) carriesmodel/rateconvention/baseline/fictionalcurrency/sourcepin andunchangedfalsecertification flags;notfinancialdata provenance. CSVroundtrip comparisons usethe statednumeric tolerance;JSONcanonicalcontent isexactlyunchanged. Sourceas-of/model-version/reviewer lineage remainsabsentfromnativeeducationalreport.

Fresh642Python/429check-test scripts/643requiredblobs;642matchV212 andonlypriorV216check9.05differs. Latestfull remains `2ee81822af67357087e2af6193348f2b3c5dbdf8`;this batch addsonlyvalidation.txt/CSV/JSON/Markdown andchangesnoPython/requiredfixtureblobs. Next9.10cumulativelab/extension/acceptancecrosswalk.38selectedCOVcategoriespartial,noneclosed;broaderresource/provenance/model/platform/release/independent/canonicalacceptanceopen.Book1separate.
