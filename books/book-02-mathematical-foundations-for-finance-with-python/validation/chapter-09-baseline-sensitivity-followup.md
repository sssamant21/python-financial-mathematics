# V-184 — Section9.6 complete baseline sensitivity reports

Baseline da68056d0ed2d80f4aeb8abbf11ea0a760ae8ce3. [Scope](chapter-09-baseline-sensitivity-scope.json):onlyportfolio_sensitivity plusprivatefloatguard/importschange;validators/parallel/spotfunctiontextunchanged. [Independentchecker](../chapter-09/code/check_section_06_baseline_reports.py) computes Cexp(-rT),-TCexp(-rT),T²Cexp(-rT),duration,convexity,per-cashderivatives andweights at1800/2400digits;referencesmustagree. Relative5e-14,absolute0;zero signs numeric only. Eighteenvectors*7reportfields (listfieldselementwise) plus11input/priority and4ownership/iterator/weight/context controls =141sourcepredicates,notindividualelements oruniquemethods.

[Initial110pass/31failed](chapter-09-baseline-sensitivity-baseline.json),[identicalreplay](chapter-09-baseline-sensitivity-baseline-replay.json),[actualbaselinecommand](chapter-09-baseline-sensitivity-baseline-run.json),[replaycommand](chapter-09-baseline-sensitivity-baseline-replay-run.json). Fourteenfailedfieldsarewhole-reportValueError/range-categoryalignment (truecash-derivative andaggregatevalueoverflow);17arecompletenumerical/reportdifferences:secondderivative1,tinynormalizedsecond1,finiteaggregate7,discountfactor-underflowrescue5,latentweights/normalization3. Not31uniquedefects;range/listpolicyisexplicit,notindependentfinancialapproval.

[Corrected141/141](chapter-09-baseline-sensitivity-corrected.json),[actualcorrectedcommand](chapter-09-baseline-sensitivity-corrected-run.json),[three-file/three-commandscopedrun](chapter-09-baseline-sensitivity-results.json). [Observer](chapter-09-baseline-sensitivity-observer.txt):`python books/book-02-mathematical-foundations-for-finance-with-python/validation/chapter-09-baseline-sensitivity-observer.txt . baseline-replay` stagesoriginalsourcewithnewchecker;correctedstagesworkingtree. [Scopedrunner](chapter-09-baseline-sensitivity-runner.txt) compilesmodule/original/newchecker,runsdemo+twocheckers. Fresh624Python/411check-test/625requiredblobsisinventoryuntilseparatepinnedfullruntime.

## Contract and remaining scope

Allscalar/listfieldsfinite,positive roundedtotal. Per-cashderivative exp(-rT)mustfit independently oftotal;this mayrejecta rescuedamountwhenits requiredderivativeisunrepresentable. Private1500-digit latent amounts/derivatives avoid prematurefactor/productrounding;normalizebeforeconversion. Extremelynegativeexponenttermsbelow-10000cannotbe rescuedbyfinite C,T²or divisionbypositivefloatbaseline exceptunboundedcollection/resourcesnotproved. Positiveexponentsover10000areineligible. Selectedreferenceagreementdoesnotproveuniversaltranscendentalrounding orarbitrarycollectionbounds.

Savedbaselinesecond-derivativeobservationisscopedresolved. Historicalinitial/replayrecordsunchanged. Parallel/spotexpm1overflowfindingsremainOPEN;theirparentbaselinepolicy mayalso imposestricter unusedfieldrequirements thatneedseparatereview. Next:parallel_shock completeexact/linear/quadratic/error fields andprerequisites,then spotcurve/spotshockcontracts. All37selectedCOVcategoriespartial,noneclosed. Independentmathematical/editorial/model/platform/release/canonicalapprovalnotgranted;Book1independent.


### Section9.6 parallel/spot resume — OPEN

[Freshinitialobservations](chapter-09-parallel-resume-r11-initial.json),[actualidenticalreplay](chapter-09-parallel-resume-r11-replay.json),[runner](chapter-09-parallel-resume-r11-probes.txt) at70da93bc07c55a0c0b5eb1a48b7f80bb0614289c. Parallel/spotfiniteexactchangesstillraiseexpm1OverflowError (twoOPENnumericalcases). Parallelzero-shockwithunrepresentableunusedper-cashbaseline-derivativeisrejected (separateOPENparent-prerequisitepolicyquestion). Notpassing141baselinepredicatesorcompletedwrapperreview. Nextparallel_shockcompletefields/prerequisites,then spotcurve/shock;historicalrecordsretained.

Candidate/executedsourcepin`70da93bc07c55a0c0b5eb1a48b7f80bb0614289c`;[hashverification](chapter-09-baseline-sensitivity-publication-verification.json).
