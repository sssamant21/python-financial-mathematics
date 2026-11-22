# V10 — Section15.11 supplied return basis and project provenance

Executed source pin: `56ed4b707947235643686a472fb6e5b860199cee`. [Runnable review](review.py), [first](first.json), [replay](replay.json).

```bash
python books/book-01-python-foundations-for-financial-mathematics/qa/v10-return-basis/review.py first
python books/book-01-python-foundations-for-financial-mathematics/qa/v10-return-basis/review.py replay
```

**58 predicates pass twice with identical rows:**44 native simple-return/compound-endpoint/log-endpoint fields over13 supplied price paths, plus14 supplemental transformation/dispersion/alignment/snapshot/project checks. Simple returns use independent rational price-difference ratios; log totals use a100-digit endpoint logarithm; observed sample variance uses pairwise squared differences of displayed native returns. Numeric tolerance rtol5e-14,atol1e-15; fixture/hash/Boolean identities exact. Labels and basis descriptions are supplied observer metadata, not inputs inspected by the source API.

|Synthetic basis example|Executed numerical behavior|Responsibility remaining outside source|
|---|---|---|
|Hypothetical2-for-1 split, raw100→50 versus adjusted100→100|Price returns−.5 versus0; two ending shares preserve total value|Corporate-action/reinvestment convention and authenticity|
|Ex-dividend100→99 with separately specified dividend1; total index100→100|Price-only−.01 versus total-index0; supplemental(99+1)/100−1=0|Cash-flow processing; no native dividend adapter|
|Local100→110, FX2→1 base per local; base value200→110|Local+.1 versus base−.45; exact gross FX identity checked|Currency, FX timestamps/units and conversion provenance|
|100→100→110 versus100→105→110|Different sample SD despite same endpoint wealth|Neither path is verified latent truth or freshness; staleness need not move estimated SD in one universal direction|
|Asset labels1,2,4 versus1,3,4|Both numeric APIs produce two returns|Equal lengths cannot establish identical observation intervals/calendar joins|
|Reorder prices to labels1,4,2|Accepted positive sequence produces different returns|Chronology/as-of feature and price validation|
|100→110 versus revised100→105|Different returns and content hashes|Availability time/authenticity/latest-eligible revision policy|

These controlled inputs show arithmetic dependence on an explicit basis. They do not execute a corporate-action, FX, calendar, stale-quote, point-in-time or revision-selection pipeline. The source receives positive positional numeric prices and cannot infer those controls. No real feed or market audit was supplied; F32 shared-input integration remains open. No claim that a raw/adjusted or original/revised input is universally correct is made.

The prescribed project hash matches earlier evidence. Prices[100,110,99] (fictional USD,labels0–2,no cash flows) and the separate six-return risk fixture[−.04,−.01,0,.02,.08,.01] intentionally have different lengths; the latter is not derived from the price path. Hypothetical same-period risk-free.001 gives native mean of caller excess differences.009 and caller per-period Sharpe.225. There is no source Sharpe, date-alignment or benchmark-calibration API. Metadata records252 periods/year and absent real dates; scaling validity remains conditional as reviewed earlier. Prior24 exercise/ten project-task records are not recounted. Prerequisites and source/project basis contracts align at the scoped synthetic level; broader shared-input/data-model acceptance is not resolved.

Each run executes the complete verbatim demo/twelve existing methods and compilation:four command records/24 invocations of twelve existing methods total. Whole-source/fence identities match F137 corrected evidence; twelve original failures/46 arithmetic predicates and168 scaling/267 tail-selection predicates retain their scopes. No source change/defect or new workflow/answer/step/historical-method totals. Selected15.11 V10 assumption crosswalk recorded; next15.12 rolling statistics/window/order/dependence assumptions. V10/Book1,F28/F32/F209/F165/F185 and broader numerical/resource/data/model/platform/release/independent/canonical gates remain open; no independent/platform/certification claim.
