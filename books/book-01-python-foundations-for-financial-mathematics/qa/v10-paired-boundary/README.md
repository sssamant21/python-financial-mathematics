# V10 — Section18.15 paired uncertainty and zero-event boundary

Source pin: `3a9dddb78f225bef1cd59241f28ea8d5e0a87744`. [Runnable review](review.py), [first run](first.json), [replay](replay.json).

```bash
python books/book-01-python-foundations-for-financial-mathematics/qa/v10-paired-boundary/review.py first
python books/book-01-python-foundations-for-financial-mathematics/qa/v10-paired-boundary/review.py replay
```

Both runs pass **980 predicates** with identical rows: 960 native summary fields across80 finite paths, fifteen exact/weighted joint-law checks, and five zero-event/boundary checks. Three selected common-draw joint models have the same A/B marginals90/110 with equal probability. Three independent pair-units per sample produce8 positive-pair paths,8 negative-pair paths and64 independent-pair paths, with their exact product probabilities. These are deterministic enumerations, not Monte Carlo replications.

| Pair law | Cov(A,B) | Var(A−B) | Var(mean(A−B)), n=3 | Naive independent variance |
|---|---:|---:|---:|---:|
| Identical signs | 100 | 0 | 0 | 200/3 |
| Opposite signs | −100 | 400 | 400/3 | 200/3 |
| Independent signs | 0 | 200 | 200/3 | 200/3 |

Caller code forms each paired difference. The native18.8 `estimate_mean` runs on A,B and A−B; its count, mean, SD and SE are checked against exact rational centered moments. Weighted expected native squared paired SE equals the exact model variance of the paired mean in each law. Summing component SE squares incorrectly assumes zero covariance, and can overstate or understate uncertainty. Pairing alone does not guarantee variance reduction. Independent units here are the modeled pairs, not the two correlated observations within a pair. Arithmetic tolerance is rtol5e-14/atol1e-12. Normal interval coverage and optional stopping are not tested.

For Exercise49, source18.10 Wilson interval with zero events in100 trials has lower0 and upper z²/(100+z²), z=1.96 (about.036995). The plug-in Bernoulli SE is zero, but an interval under the stated binomial assumptions remains nontrivial. Exact (1−p)^100 is positive for selected p=.01,.05,.25; these are model likelihoods of the zero-event observation, not posterior probabilities or proof that any p is the real market probability.

Exercise50 is a conceptual decision review: replay and a narrow sampling interval do not establish input volatility, dependence, model suitability, independent sign-off or release acceptance. No native acceptance flag/API exists here, and no synthetic flag assertion is counted as a test. The stated conclusion aligns with the question; external review remains required where applicable.

Each run executes two complete verbatim demos/test suites (18.8 and18.10) and compiles both extracted listings. Across both runs: six command records,48 invocations of24 existing methods (twelve per suite). No new historical unique methods, workflow/answer/step totals or source changes are claimed. Initial evidence serialization needed Fraction-to-string handling; this was a harness serialization issue before the saved runs, not a source/numerical failed predicate. No saved source failure is omitted.

This advances the partial18.15 V10 assumption review for46/49 and conceptual50. Earlier Exercise45 is not repeated. Next: reconcile the remaining chapter-wide exercise/lab assumption matrix (including31–44/47–48) against prior scoped records and V10 evidence before considering a Chapter18 progression decision. V10/Book1, F28/F32/F209/F165/F185 and broader model, resource, platform, release, independent and canonical acceptance remain open.
