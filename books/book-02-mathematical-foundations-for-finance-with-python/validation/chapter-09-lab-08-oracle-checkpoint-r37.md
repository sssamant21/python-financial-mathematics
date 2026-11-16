# V-220 — Section9.8 complete CLI oracle: partial checkpoint

Source pin `ecd8f947c1aaa69a905e220d86f8f5a2c55d9edd`; source implementation unchanged. This batch completes an independent default-output reference and optional-tolerance fixtures while **Python source execution remains blocked by the unavailable executor**. It does not close §9.8,V219,any COV category or Book2.

## Actual independent evaluation and retained observer failure

[Corrected runnable oracle](chapter-09-lab-08-cli-oracle-r37.js.txt) was evaluated twice in JavaScript with identical [174 passing checks](chapter-09-lab-08-cli-oracle-r37.json):151 cross-precision leaf comparisons,18 parallel sign/expm1 diagnostics,one nonparallel expm1 diagnostic andfour optional-tolerance controls. These are supplemental reference checks,not Python or source-checker passes.

[Initial oracle](chapter-09-lab-08-cli-oracle-initial-r37.js.txt) and[initial143pass/27fail receipt](chapter-09-lab-08-cli-oracle-initial-r37.json) retain a QA conversion problem:converting a large fixed-point integer andits scale separately to Number before division introduced double rounding. The observer now constructs a signed decimal string andconverts once. The original170 comparisons then agree;four new tolerance controls are separately added. No source numerical failure or implementation defect inferred from that observer error.

The independent arithmetic uses BigInt fixed point at80 and100 decimal places,160 exponential Taylor terms,andIEEE754 represented input rates andconverted bp shocks. It forms complete baseline/endpoints/changes/errors before report conversion. This avoids sharing the source's Decimal.exp backend. Cross-precision agreement andselected JavaScript Math.expm1 diagnostics are useful checks,not a certified global error bound,all-range arbitrary-precision guarantee or supported-platform validation. The saved expected JSON is a numerical oracle,not captured Python stdout.

## Default CLI contract now reference-complete

| Component | Independently prepared fields |
|---|---|
|Parallel baseline|V,V′,V″,D,K,model/rate/flows/currency-tolerance metadata. V≈1111.5069249405317.|
|Nine parallel rows|−100,−50,−25,−10,0,10,25,50,100bp;exact/linear/quadratic changes andvalues,signed/absolute errors,shock bp/decimal andtwo tolerance flags.|
|Nonparallel|Consumed spots.035/.04,shocks10/−20bp,positive baseline,complete exact/linear/quadratic changes/errors andmodel. No native market-key-rate orparallel-value fields inferred.|
|Optional tolerance|None omits flags;zero accepts onlyzero-shock for this selected grid;.05 rejects linear errors at±50/±100bp whilequadratic passes;.25 makesbothflags true throughout defaultgrid.|

All default.25flags being true would be a weak sole tolerance test;the additional.05/zero/None controls make the pending comparison substantive. Tolerances refer to reported absolute currency-error floats,not latent mathematical bounds orfractions ofbaseline/exactchange. Exact zero controls are preserved as exact comparisons. Fields/models/schema are taken from explicit static contracts,not fabricated as source output.

## Source replay checkpoint

[Prepared full CLI/tolerance runner](chapter-09-lab-08-cli-resume-r37.txt) is **unexecuted,including syntax/compile**. Once Python is restored,run it twice with distinct output labels. It extracts the exact pinned source/checker,records actual CLI/checker/compile output,compares complete default schemas/leaves anddirectly calls optional-tolerance reports. Nonzero numbers use rtol5e-14/atol1e-12;zero,booleans,text andschemas useexact predicates. Preserve initial source failures andreruns beforefixing. Also run the earlier[Exercise6/7 fixture runner](chapter-09-lab-08-resume-r36.txt);it remains independently pending. Prepared runners are not counted as execution.

[Fresh runtime identity delta](chapter-09-lab-08-runtime-delta-r37.json):642Pythonfiles/429check-test scripts/643requiredblobs;642still match V212 andonlyearlier V216check9.05differs. NoPythoncode added/modified;latest full remains V212 at `2ee81822af67357087e2af6193348f2b3c5dbdf8`. Existing V219 static exercise crosswalk/markup repair andhistorical source validations remain at original scope,not recounted.

Next remains §9.8 native runtime/complete lab crosswalk,then9.9.38selectedCOVcategories partial,noneclosed;notdefectcounts orcompletion percentages. Broader resource,provenance,model,platform,release,independent/canonical acceptance remain open;Book1 separate.
