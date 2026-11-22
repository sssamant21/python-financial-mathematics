# V10 — Partial Section15.12 rolling distributions and caller selection

Executed source pin: `e29f14d85ecbdf6bde690da001b06d61fa191865`. [Runnable review](review.py), [first](first.json), [replay](replay.json).

```bash
python books/book-01-python-foundations-for-financial-mathematics/qa/v10-rolling-distributions/review.py first
python books/book-01-python-foundations-for-financial-mathematics/qa/v10-rolling-distributions/review.py replay
```

**585 predicates pass twice with identical rows:**64 native SD/compounded-window fields across16 four-observation paths;512 native correlation fields over256 independently paired x/y paths and two windows; nine weighted variance/covariance/undefined/selection expectations. Exact rational gross products/pairwise identities and100-digit roots provide independent expectations. Numeric comparisons rtol5e-14,atol1e-15; exact None positions/probability identities stay exact. Rounded native SDs are squared/weighted then compared with arithmetic tolerance, not falsely treated as bit-exact variances.

For four IID fair signs±1 with trailing windows of length3, sample variance is0 for constant windows and4/3 otherwise. Each window's expected native SD² is1, but adjacent sample-variance covariance is1/9:both are nonconstant with probability5/8, giving E[product]=10/9. The caller chooses the smaller of the two same-path window variances; its expectation5/6 is below the predeclared window mean1. This is a finite selection effect, not discovery that the underlying IID variance decreased or a recommended risk-selection rule.

For two independent four-sign x/y series, each three-point source correlation is undefined if either window is constant. Exact probability=1−(3/4)²=7/16; source returns **None**, not0. Every defined source value is checked against a pairwise-cross-difference oracle independent of centered products. The256 paths are an exact hypothetical joint law, not256 independent real observations or calibrated short-window correlation inference. No t/p-value/effective-sample-size API is introduced.

A separate compounding interpretation scales the signs to returns±.1 (positive gross wealth). Every native three-period compound value matches the exact gross product. Both expected rolling returns are0, while adjacent compounded-return covariance is(1+.1²)²−1=201/10000 because two gross factors are shared. This is not covariance of additive means or a universal scaling rule. SD/correlation fixtures use signs±1 as generic measurements, while the compounding fixture uses±.1 as simple returns; the conventions are kept separate.

The manuscript's overlap/short-window-noise/undefined-correlation and window-selection warnings align with these controlled laws. Source functions execute the metrics; exact-law weighting, covariance and choosing a window are caller supplemental calculations. Earlier24 answers/ten project tasks are not new records. Each run executes the full verbatim demo/twelve existing methods and compilation:four command records/24 invocations of twelve existing methods total. Whole-source/fence identity matches F138 corrected evidence. Its initial None-comparison observer crash,twelve baseline failures and54 arithmetic predicates plus the earlier89 mean-overlap predicates retain scope, not recounted. No source change/defect or new workflow/answer/step/historical-method totals.

Section15.12 remains partial. Next:local-window compounded wealth/bankruptcy versus global-account semantics, window-policy/expanding/EWMA/project and supplied-data/timing assumptions before15.13. V10/Book1,F28/F32/F209/F165/F185 and broad numerical/resource/data/model/platform/release/independent/canonical gates stay open. No real-data, supported-platform or independent acceptance.
