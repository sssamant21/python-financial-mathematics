# V10 — Section15.9 power, effect hurdles and post-selection assumptions

Executed source pin: `199352a9f3398bb2bdd2b2fe3eee5ec42e605a76`. [Runnable review](review.py), [first](first.json), [replay](replay.json), [F218 wording/identity record](F218-assumption-clarification.json).

```bash
python books/book-01-python-foundations-for-financial-mathematics/qa/v10-power-selection/review.py first
python books/book-01-python-foundations-for-financial-mathematics/qa/v10-power-selection/review.py replay
```

**1,267 predicates pass twice with identical rows:** 960 native sign-test rejection-region checks over every n6–9 ordered ±1 path; 36 exact alternative-law mass/rejection/miss checks at positive-sign probabilities 1/4,1/2,3/4; four magnitude/effect checks; 256 caller-selected-tail decisions and three attained-size aggregates; eight statistic/effect/reference-model checks. All finite probabilities are exact rational arithmetic. The selected native dyadic p-values are exact, not Monte Carlo. Numeric statistic expectations use decimal moments and a 100-digit square root (rtol5e-14,atol1e-15). The three p=.5 laws are null attained-size calculations, not alternative power or Type II error claims.

|n|Power at positive-sign p=.25 or .75|Miss probability under either alternative|Null attained size at p=.5|
|---|---:|---:|---:|
|6|365/2048|1683/2048|1/32|
|7|547/4096|3549/4096|1/64|
|8|3281/32768|29487/32768|1/128|
|9|9845/32768|22923/32768|5/128|

Native decisions are weighted over the exact IID-path laws and compared to a separate closed binomial critical-region sum. The discrete rejection boundary explains why power need not increase with every one-observation increment. These examples are not real-data power estimates or a sample-size design recommendation. Independence, no ties, specified sign probabilities and predeclared tests are assumptions. A sign/median hypothesis is distinct from a mean-return target: eight +1 values plus -1 or -100 have the same significant sign p-value, but means7/9 and−92/9.

For n8 fair IID signs, a predeclared positive one-sided binomial-tail test has size9/256. Choosing the favorable tail after inspection and feeding native two-sided p/2 to the source decision helper has size9/128=.0703125; the actual native two-sided test has size1/128. One-sided probabilities and selection are **caller calculations**, not a source one-sided API. This is an exact counterexample to nominal validity after selection, not calibration for arbitrary multiple testing or dependent returns.

For [.01,.02,.03], the hypothetical cost hurdle0/.005 gives mean excess.02/.015 and t=2√3/1.5√3. The documented **supplemental df2 reference** p=1−|t|/√(t²+2) gives.0741799002/.1216899343 (both do not reject at.05). The separate source normal-tail function gives.0005320055/.0093747685 (both reject). These different reference models must not be mixed; the listing has no general t CDF. Positive estimated excess is not evidence of a positive population mean after costs. Costs are hypothetical per-period return assumptions, not measured execution data; model suitability remains unaccepted.

F218 qualifies the remaining Section11 expected-false-count paragraph, paralleling F217's earlier Exercise22 correction: equality1 requires actual marginal rejection probability.05; upper levels imply at most1. Original/corrected text and the prior n6 counterexample5/8 are preserved. This is a prose assumption correction, not a new implementation bug/numeric failed predicate. The baseline whole-source matches F217's candidate identity; the executable fence is unchanged before/after. Prior F135 nine failures/observer correction/35 predicates and F217's earlier2,888 checks retain their scope, not recounted.

Each run executes the complete verbatim demo/twelve existing unit methods and compilation: four command records/24 invocations of twelve existing methods in total. No new workflow, lab-step, answer or historical-method totals. Selected15.9 assumption crosswalk recorded; next V10 Section15.10 regression residual/design/selection assumptions, preserving earlier exact-source arithmetic evidence. V10/Book1 remain IN PROGRESS; F28/F32/F209/F165/F185 and broader numerical/resource/data/model/platform/release/independent/canonical gates remain open. F218 is resolved only at the stated paragraph scope.
