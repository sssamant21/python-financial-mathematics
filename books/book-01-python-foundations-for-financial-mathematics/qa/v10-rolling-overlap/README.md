# V10 — Partial Section15.12 rolling-mean overlap and timing

Executable source pin: `56ed4b707947235643686a472fb6e5b860199cee`. [Runnable review](review.py), [first](first.json), [replay](replay.json).

```bash
python books/book-01-python-foundations-for-financial-mathematics/qa/v10-rolling-overlap/review.py first
python books/book-01-python-foundations-for-financial-mathematics/qa/v10-rolling-overlap/review.py replay
```

**89 predicates pass twice with identical rows:**80 native rolling-mean fields across16 exact four-IID-fair-sign paths (two three-point means and three two-point means per path),five weighted covariance/variance checks and four trailing perturbation/output-map/lag checks. Native rounded means are weighted as exact fractions then compared to independent coefficient-covariance formulas with rtol5e-14,atol1e-15. No PRNG, real return process, or general independence test is used.

For IID variance1 increments, each three-point mean has variance1/3; adjacent three-point windows share two increments, covariance2/9 and caller-derived correlation2/3. Adjacent two-point means have covariance1/4; disjoint two-point means have covariance0 under this specified IID law. Source rolling-mean arithmetic is checked against exact window sums, then its outputs are aggregated under the finite process law. The correlation2/3 is a supplemental covariance ratio, not a native `rolling_correlation` call or universal effective-sample-size rule. Window overlap induces dependence even with independent inputs; no Student-t/forecast calibration follows.

Changing only the last observation1,2,3,4→1,2,3,400 leaves earlier two-point means unchanged and changes the final mean by198. With caller labels[1,2,8,10], native means pair to end labels[(2,1.5),(8,2.5),(10,3.5)]; source `lagged_signal` yields[None,1.5,2.5], one **output position** later. The caller supplies labels; the numeric API does not check clocks, exchange calendars, publication availability, execution delay or costs. This is an arithmetic dependency/map illustration, not point-in-time backtest acceptance. Earlier tasks concerning warm-up/window-end conventions align at this scope, not new lab-step or answer records.

Each run executes the full verbatim demo/twelve existing methods and compilation:four commands/24 invocations of twelve existing methods total. Whole-source/fence identity matches F138 corrected evidence. Its initial observer-only None-comparison crash, twelve baseline predicates and54 corrected arithmetic predicates retain their original evidence/scope, not recounted. No source change/defect or new workflow/answer/step/historical-method totals.

Section15.12 remains partial:next rolling SD/correlation/compounded-window distribution/selection and supplied-project/data-timing boundaries. V10/Book1 and F28/F32/F209/F165/F185 plus broader numerical/resource/data/model/platform/release/independent/canonical gates stay open. Book2 has separate trackers.
