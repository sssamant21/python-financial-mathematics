# V-245 — Section10.5 full fixed report and reference/provenance crosswalk

Executed source pin: `56ed4b707947235643686a472fb6e5b860199cee`. [Runnable review](review.txt), [first](first.json), [replay](replay.json).

```bash
python books/book-02-mathematical-foundations-for-finance-with-python/validation/ch10-payment-report-2026-11-22/review.txt first
python books/book-02-mathematical-foundations-for-finance-with-python/validation/ch10-payment-report-2026-11-22/review.txt replay
```

**38 predicates pass twice; complete reports and semantic expectations agree.** Four global schema/count/flag checks,25 ordered scenario schema/numeric fields,three derivative/sign/conceptual-second-derivative checks,three curve reference/error-bound checks,two model invariants and one complete CLI/function agreement. Schema-set diagnostic strings may print in a different order; their sets/verdicts agree. This is not a numeric failure or observer correction. Each run imports the exact source and invokes native CLI/checker/compilation (three commands); actual outputs/environment/blob SHA/SHA256 and references retained. No source defect/change was found or required by this scoped report review.

The five fixed rates−.01,0,.02,.05,.08, C1000,g.02,T4,n2000 are checked. Independent120-digit exponential power series integrated termwise gives continuous growing PV and the first/second rate moments. An independent geometric-grid recurrence gives ideal midpoint sums; the callback's separately rounded binary g−r is explicitly distinguished from the exact difference used by native analytic PV. Native numerical fields use rtol5e-14,atol0. Source callback/sample rounding is empirically small at these ordinary fixtures, not a universal correct-rounding proof. Every `absolute_difference` is checked as the exact subtraction of the two **reported float fields**, not as a rigorous bound.

For the fixed variable curve, independently integrate exp(A t+B t²) via Taylor coefficients j a_j=A a_(j−1)+2B a_(j−2), and independently sum the ideal2000-midpoint grid via two exponential recurrences. Here A=g−.03<0 and B=−.005/2<0. The ideal midpoint theorem gives error≤T³/(24n²)×1000[(|A|+2|B|T)²+2|B|]≈3.9333333e−6 because exp(A t+B t²)≤1. The ideal reference satisfies this bound. Native curve output is checked against that continuous reference with a separately declared1e−9 floating margin; this is a diagnostic for the selected fixture, **not** a fully rigorous floating-point error budget or a new native error-bound API.

The parallel-shift derivative is negative for this positive stream. Supplemental second derivative1000∫t²exp[(g−r)t]dt is positive, explaining the manuscript's convexity statement under bounded-horizon differentiation assumptions. No native second-derivative routine or numeric implementation is invented. Raw manuscript Exercises11–12 retain analytical/conceptual obligations beyond the first-derivative API. The source flags `runtime_certified` and `independent_review_completed` remainFalse; assistant checks/full runtime do not change them.

|Fixed-report/project contract|Recorded disposition|
|---|---|
|Payment model and units|Deterministic1000 exp(.02t),currency/year; time in years, continuous annual rates; currency label and real valuation date unspecified|
|Scenarios/resolution|Five ordered flat rates; n2000 for midpoint and variable curve; source and manifest pinned|
|Analytic versus numerical fields|Every row field checked; discrepancy is reported-float difference, numerical/model errors remain distinct|
|Parallel shift and curve|First derivative source checked; second derivative conceptual reference; deterministic q(t)=.03+.005t, no stochastic-short-rate calibration|
|Provenance and reproducibility|QA evidence records these fixed assumptions and exact blobs externally; native report has no generalized valuation-date/units/provenance input/output API|
|Acceptance|Selected source/report/lab crosswalk recorded; full pinned runtime refresh V246 must pass before10.6; financial/independent/release acceptance remain open|

The existing report is a fixed illustrative assessment. Its numeric payload does not contain all metadata in the table; reproduction relies on the pinned source and this external QA record. This is not portrayed as a self-contained production valuation report or user-supplied curve provenance system. Existing six lab units/fourteen exercise dispositions are reconciled without new workflow/exercise/step counts. No general parameter ranges or arbitrary continuous-integral coverage are inferred. Prior V240–244 baseline failures, corrected reruns, policies and limitations (including conservative exponent guard and non-identical near-cancellation precision) remain open at their documented scopes.

Next:finish the pinned full runtime refresh (V246), verify executable identities unchanged by report/manuscript updates, then10.6 improper-integral lab/source crosswalk if its progression gate passes. All38 selected COV categories remain partial, none closed; categories are not defects/percentages. Broader numerical/resource/provenance/model/platform/release/independent/canonical acceptance stays open. Book1 separate.
