# V10 — Section15.9 finite-null sign decisions and multiplicity

Executed source pin: `7108ac9f0776faa84bb1b024276023900e20b66f`. [Runnable review](review.py), [first](first.json), [replay](replay.json), [F217 original/corrected assumption record](F217-assumption-clarification.json).

```bash
python books/book-01-python-foundations-for-financial-mathematics/qa/v10-sign-null-multiplicity/review.py first
python books/book-01-python-foundations-for-financial-mathematics/qa/v10-sign-null-multiplicity/review.py replay
```

Both runs pass **2,888 predicates** identically:960 fair-sign paths over n6–9 each check the native two-sided p, decision at.05 and decision at a separately chosen caller threshold.05/20; eight weighted rejection-region checks complete the count. Null p-values use direct enumeration of absolute-sign-sum tails, not the source's binomial-tail sum. Fractions of reported p-values and all decisions are exact here. No random simulation or PRNG assumption is used.

|n|Actual fair-IID null size at.05|20 independent tests: any false rejection|20 perfectly dependent tests: any false rejection|Expected false count, either family law|
|---|---:|---:|---:|---:|
|6|1/32|.4700507153|1/32|5/8|
|7|1/64|.2701871440|1/64|5/16|
|8|1/128|.1451793082|1/128|5/32|
|9|5/128|.5492841448|5/128|25/32|

The exact sign test is discrete and conservative under these predeclared fair independent-sign null models. Attained size need not equal nominal alpha or increase monotonically with n. There are no ties in these fixtures; dropping ties or using dependent/selected observations requires separate assumptions. These results are not calibration for financial return signs or general power/t-test acceptance.

Family probabilities are **caller mathematical models**, not a native family-wise correction API: independent-family P(any false)=1−(1−q)^20; perfectly dependent-family P(any false)=q. Both have expected false count20q. Applying a caller Bonferroni threshold.0025 via the native decision helper gives zero rejection in the selected n6–9 models; no universal power/optimality or real-data dependence assumption follows.

F217 clarifies Exercise22's unqualified expected count1 for20 tests at nominal.05. The n6 native counterexample has q=1/32 and expectation5/8, so exact equality1 needs **actual** marginal false-rejection probability.05, not merely an upper level. Original and corrected prose, exact counterexample and source hashes are retained. The corrected answer also states the at-most1 bound when the marginal probabilities are only bounded by.05. This is a scoped mathematical/editorial assumption clarification, not a new implementation bug or numeric failed predicate. The executed fence is byte-identical before/after; the candidate prose correction is not falsely attributed to the older execution pin.

Each run executes the full verbatim source demo/twelve existing methods and compilation: four command records/24 invocations of twelve existing methods across both runs. F135 whole-source/listing baseline identities match earlier evidence before the prose clarification; its nine baseline failures, observer correction,35 predicates and earlier five-sign enumeration remain retained, not recounted. No new historical method, answer, project or workflow totals are added.

Next:15.9 alternative-sign power, cost/effect hurdle and post-selection/reference-distribution assumptions, keeping normal tails separate from a small-sample Student-t model. V10/Book1, F28/F32/F209/F165/F185 and broader numerical/resource/data/model/platform/release/independent/canonical acceptance remain open. F217 is resolved only at the recorded worked-answer wording scope.
