# V-219 — Section9.8 lab/exercise crosswalk: partial static checkpoint

Pinned current source `17a15f56db324709638d7fe5b7cc1500f9d0b2fa`. [Manuscript](../chapter-09/9.08-sensitivity-reports-and-scenario-revaluation.md), source blob `ca30add057669c6c1f93b7efac8a11aab893026d`. No Python execution environment was available: **“No usable execution environment is available.”** No Python source/checker/compile ran here. Prior runtime evidence remains historical at its recorded pins, not a fresh pass. This partial batch does not finish §9.8 or Book2.

## Actual checks and repair

[Supplemental integer-scaled observer](chapter-09-lab-08-algebra-r36.js.txt) evaluated twice with identical [seven passing algebra checks](chapter-09-lab-08-algebra-r36.json). It independently derives Exercise6 linear−80, Exercise7 convexity correction+.45 andquadratic−79.55, and verifies that duration4/convexity18 can arise from positive-payment weights1/3 at2years and2/3 at5years. A runnable integer-flow fixture uses8000 at2years plus16000 at5years,r0:V24000,D4,K18,25bp linear−240,quadratic−238.65. Divide currency outputs by3 to match the exercise's V8000; this division is caller work, not an exported report option. These are mathematical references, **not Python source outputs**.

To replay algebra with Node: `node -p 'JSON.stringify(eval(require("fs").readFileSync("books/book-02-mathematical-foundations-for-finance-with-python/validation/chapter-09-lab-08-algebra-r36.js.txt","utf8")),null,2)'`. No Node/platform acceptance claim; the actual evaluation in this batch used JavaScript BigInt.

[Markup evidence](chapter-09-lab-08-markup-r36.json) retains the original static predicate failure:ten escaped backticks(two around inline expm1,eight around command path/fence). Removed those escapes;the same no-escaped-backtick predicate then passes. Source and reference-checker Python unchanged. This verifies the literal markup repair, not a rendered-page/browser or source-runtime test.

## Six lab contracts reviewed statically

| Unit | Contract and pending evidence |
|---|---|
|Inputs|Positive fixed cash flows,times≥0,decimal annual continuous rates;flows100/1100 at1/2years,r.04. No market valuation data or curve calibration.|
|CLI|Two top-level reports:parallel nine signed bp shocks andnonparallel[10,−20]bp using spots .035/.04. Complete leaf/schema/source execution remains to be checked;static reading is not output validation.|
|Baseline|Native parallel baseline includes V,V′,V″,D,K,consumed flows/model/rate/tolerance metadata;normalization before report conversion. No as-of/model-version/reviewer sign-off fields supplied.|
|Scenarios|Parallel rows have exact/linear/quadratic changes,values,errors andoptional currency-tolerance booleans. Spot report has change/error fields andconsumed rate/shock metadata;no native market-key-rate construction or all-parallel-baseline fields.|
|Errors|Exact-minus-approximation sign;absolute currency-tolerance booleans compare rounded reported errors. Relative ratios discussed in manuscript are caller calculations,not returned fields;small scenario error is not a uniform mathematical bound.|
|Eligibility|Parallel complete-baseline gate,spot strictly positive finite baseline,finite-output/exponent/precision policies retained. Existing broader numerical/resource/model/platform acceptance remains open.|

## Twelve exercise alignment dispositions

| Exercise | Scoped disposition |
|---|---|
|1|Baseline/model/convention/units/duration prerequisite reviewed conceptually.|
|2|25bp=1/400 and−50bp=−1/200;integer-scaled unit algebra,not source execution.|
|3|Taylor formula V′h+V″h²/2 follows flat continuous-rate derivatives;conceptual derivation.|
|4|Sum discounted amounts×expm1(−th) is mathematical stable-change identity. Current high-precision source computes endpoint-minus-baseline before final float conversion;no literal math.expm1 implementation claim.|
|5|Zero-shock required;prepared fixture control still unexecuted.|
|6|−8000×4×.0025=−80,exact scaled arithmetic.|
|7|8000×18×.0025²/2=.45;quadratic−79.55;positive-flow moment feasibility checked above.|
|8|E2=exact−quadratic:reviewed report sign convention,source outputs pending.|
|9|Relative error undefined atzero/unstable nearzero;not a native relative-error field.|
|10|Independent spot linear response−ΣtCexp(−zt)h follows component differentiation;runtime spot fields pending.|
|11|Market key rates need interpolation/bump/repricing contract absent from independent cash-flow spot model.|
|12|Cap/floor crossing requires piecewise repricing;this positive fixed-flow model cannot claim that feature.|

These are six review units/twelve dispositions,notnew test-method orcompletion totals. No independent reviewer sign-off. [Runtime delta](chapter-09-lab-08-runtime-delta-r36.json):current tree642Pythonfiles/429check-test scripts/643required blobs;642match V212,onlyearlier V216check9.05differs. Latest full execution remains V212 at `2ee81822af67357087e2af6193348f2b3c5dbdf8`,notthispin.

## Exact resume checkpoint

[Prepared source runner](chapter-09-lab-08-resume-r36.txt) is unexecuted andnot syntax/runtime verified. It checks the positive-flow Exercise6/7 fixture,zero-shock,selected independent math.expm1 exact value,then exact CLI/checker/compile commands from the pin. Run twice when Python is restored;retain failures before fixes. Complete the defaultCLI leaf/schema oracle andoptional reported-tolerance/nonparallel alignment before closing this crosswalk. No need to re-derive the saved exercise/dependence fixtures. Next remains §9.8 runtime/complete lab crosswalk,then §9.9;do not skip ahead as thoughthispartial item passed.38selectedCOVcategories partial,noneclosed;broader provenance/resource/model/platform/release/independent/canonical gates open. Book1 separatelytracked.
