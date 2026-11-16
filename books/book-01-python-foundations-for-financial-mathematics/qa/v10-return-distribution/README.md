# V10 — Section18.5 return-distribution and estimator assumptions

Source `4251353f502d823654eb7920618e545903f37f7e`. [Runnable review](review.py), [first run](first.json), [replay](replay.json), [prior listing identity](source-identity.json), [six assumption records](assumption-crosswalk.json). No source implementation change or defect found. Prior [F177 failures/corrections,78predicates andcentral-CDF evidence](../chapter-18-returns-review/README.md) remain at their original scope;the exact listing hash matches.

**56 predicates pass in each run**:eight source log-return fields,eight terminal fields,20summary fields,four normal-expectation API fields,four observer contracts,four supplemental pair means,four caller geometric means andfour distribution-assumption comparisons. Each run executes the exact demonstration/ten existing methods andcompileall:four formal commands/20method invocations total. No new historical methods,answers orworkflow totals are added.

The controlled standard draws[-1,+1]define an equally weighted two-point law with mean0 andvariance1. They are intentionally not normal draws. Source transforms for four(m,s)cases are compared with independently derived displayed-decimal/rational inputs and120-digit exponential references. Relative5e-14/absolute1e-12 comparisons apply toselected log-return,currency anddimensionless quantities. References share Decimal.exp with source,not an independent transcendental implementation.

For this controlled law,E[V]=100exp(m)cosh(s),whereas the documented normal model gives100exp(m+s²/2). Their log means andvariances match,buttheir higher moments andexpected terminal values differ:

| Mean log | Log SD | Two-point expected terminal | Normal expected terminal |
|---:|---:|---:|---:|
| 0.0 | 0.2 | 102.0066755619 | 102.0201340027 |
| 0.04 | 0.2 | 106.1696469644 | 106.1836546545 |
| 0.04 | 0.4 | 112.5191772291 | 112.7496851579 |
| 0.04 | 0.0 | 104.0810774192 | 104.0810774192 |

The source `expected_terminal` formula remains appropriate for its documented normal assumption. Applying it to an arbitrary law based only on mean/variance would be model misuse,not a source defect. The geometric center100exp(m)is a caller composition;it is not presented as a unique median for the two-point law.

Source summary arithmetic is checked conditional on the supplied terminal observations. This deterministic paired quadrature is not an IID sample,so its reported IID-style SE must not be treated as valid uncertainty for this construction. No normal-generator quality,tail probability,coverage,market measure orfinancial suitability is certified. F165's general CDF/tail gap remains unresolved.

V10 remains IN PROGRESS. Next:Section18.6path/horizon/discretization anddependence crosswalk. F28/F32/F209/F165/F185 andbroaderplatform/model/release/independent/canonicalacceptance remain open. Book2 is independently tracked.
