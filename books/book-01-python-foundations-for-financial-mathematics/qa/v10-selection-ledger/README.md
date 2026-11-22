# V10/F219 — Partial Section15.13 selection and declared test ledger

Executed source pin: `aad482ca16bd3c011c402f4ce92ff216170123e4`. [Runnable review](review.py), [first](first.json), [replay](replay.json), [F219 original/corrected prose and identities](F219-assumption-clarification.json).

```bash
python books/book-01-python-foundations-for-financial-mathematics/qa/v10-selection-ledger/review.py first
python books/book-01-python-foundations-for-financial-mathematics/qa/v10-selection-ledger/review.py replay
```

**170 predicates pass twice with identical rows:**32 source full/retained-mean or all-excluded-policy checks over16 fair±.1 four-observation paths;four exact selection-law aggregates;128 native n6 sign p/decision fields and two attained-size/expected-count checks;four native threshold/caller ledger decisions. Exact probabilities/ratios and exception policy remain exact; reported mean comparisons use rtol5e-14,atol1e-15. The n6 fair-sign diagnostic is reused deliberately to crosswalk this section's expected-count wording, not recounted as a new historical method or independent model validation.

Across the unconditional16-path law, full-universe expected mean is0. Retaining only positive observations is defined on15/16 of paths and gives conditional selected mean.1. Full-universe mean **conditional on that nonempty selection event** is1/150, distinct from both0 and.1. The all-excluded path is rejected by the source rather than silently omitted; its probability is recorded. This distinguishes estimands and conditioning instead of asserting that selected and full universes estimate the same population. Retention flags are caller inputs, not native historical-membership reconstruction or a proven missingness mechanism.

The pinned Section15.9 sign-test source is executed independently of the pitfall helper. Direct enumeration of absolute-sign-sum null tails gives two rejection paths out of64, attained size1/32 at nominal.05. Native p-values and decisions match. Thus20 true-null tests of this form have expected false count5/8 by linearity, irrespective of across-test independence. This is an explicit model counterexample to unqualified equality1; it does not certify p-values for real strategies or any financial null.

F219 qualifies the remaining Section4/Exercise13 wording: equality1 needs actual marginal false-rejection probability.05; valid upper levels imply at most1 and can be conservative. Original/corrected passages, the exact native counterexample and whole/fence identities are retained. This is a scoped mathematical/editorial assumption correction, not a new source-code defect or numerical failed predicate. Executed source prose is from the older pin; corrected candidate prose is separate and its executable fence is unchanged. Earlier F217/F218 corrections keep their original scopes.

Native Bonferroni thresholds are.0025 for the complete declared20-test ledger and.005 if only10 are supplied. A caller's hypothetical p=.003 is rejected under the latter and not the former. These values are diagnostic inputs, not calibrated research results. The threshold helper cannot discover hidden trials; valid individual p-values and complete family definition remain prerequisites. No real experiment ledger, FDR or selection-aware inference implementation is claimed.

Each run executes both verbatim demos/twelve-method suites and compiles the two source files:three commands per run,six total;48 invocations of24 existing methods across both runs. Pitfall F139 whole-source/fence identity and hypothesis F218 fence identity verified. Prior F139 fifteen baseline failures/42 predicates and F135 nine failures/35 predicates remain retained, not recounted. No new workflow/answer/step/historical-method totals.

Section15.13 remains partial. Next:availability/clock/revision timing and ACF/volatility/missingness/outlier/cost/project assumption crosswalks. Source timing/selection helpers do not establish authentic data, complete searches or independent acceptance. V10/Book1,F28/F32/F209/F165/F185 and broader numerical/resource/data/model/platform/release/independent/canonical gates remain open. F219 is resolved only at the stated wording scope.
