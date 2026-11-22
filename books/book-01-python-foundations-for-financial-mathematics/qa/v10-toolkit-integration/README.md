# V10 — Partial Section 15.14 shared-fixture integration

Source pin: `4d32cafb9c9d97c9d3d3b4b81d3ef387bfd71ec4`. [Runner](review.py), [first run](first.json), [replay](replay.json). Run from any location:

```bash
python books/book-01-python-foundations-for-financial-mathematics/qa/v10-toolkit-integration/review.py first
python books/book-01-python-foundations-for-financial-mathematics/qa/v10-toolkit-integration/review.py replay
```

**108 predicates pass twice**, identical rows and source report. Exact Sections 15.11–15.14 first Python fences execute; toolkit CSV and helper fences execute unchanged. Each run has six command records: four demonstrations (48 invocations of 48 existing reference methods), exact CSV helper and compilation. Across two runs: twelve commands / 96 existing-method invocations. No new historical unique methods, workflows, exercise/answer/step totals. This observer is an external orchestrator; the four manuscripts are not a native combined package.

The exact five-row CSV is 2026-01-05 through 2026-01-09, asset [100,101,103,102,105], benchmark [100,102,104,103,106]. Hashes, actual outputs, environment, dates, prices and report are retained in JSON. [Initial observer](observer-initial.py) and [initial result](observer-initial.json) retain 107 passes / one failed expected-date predicate: the observer incorrectly expected a January 2 start. The source fixture already started January 5. Only the observer expectation changed; this is not a manuscript defect. Prior F140 observer failure, nineteen source baseline failures, 62 corrected predicates and complete 24-answer/32-step records remain in [prior evidence](../chapter-15-toolkit-review/README.md); both prior source/listing identities match.

| Contract | Verified scope |
|---|---|
| CSV to four sections | Both source return implementations match rational price ratios. The same returned float vectors feed mean, sample volatility, cumulative return, rolling statistics and pitfall overlap routines. |
| Independent report fields | Pairwise-difference variance, expanded raw-product covariance, beta/alpha and SSE=(n−1)(var(asset)−cov²/var(benchmark)), explained-variance R², exact gross product, sorted tail ranks and a separately supplied normal critical literal. Relative tolerance 5e−14 / absolute 1e−15 where float reporting intervenes. |
| Windows | All native means for w=1,2,3,4; sample SD for w>=2, full-window count and gross products; pitfall overlaps agree on shared inputs. No calendar duration implied by row counts. |
| Unit scaling | Three positive integer asset/benchmark scale combinations preserve the whole report. No corporate-action or FX adapter asserted. |
| Tails | Four selected tail probabilities share rank/ES outputs across 15.11/15.14; signed thresholds remain unfloored. No tail-model adequacy or rare-event coverage claim. |
| Metadata/alignment boundary | A cyclically mispaired benchmark of equal length is accepted numerically and changes correlation. Native report has no date field. Actual timestamp joins and availability provenance remain caller obligations. |
| Undefined outputs | Rolling constant correlation yields None; standalone toolkit Pearson raises ValueError; constant-return combined report fails. These documented contracts require an adapter; no partial-report API invented. |

Selected shared-fixture arithmetic is source execution; rational/Decimal benchmarks, metadata register and cross-module orchestration are supplemental. IID/normal/OLS/causal/market-risk acceptance is conceptual and unverified. Dates are fictional labels, not proof of exchange sessions, quote freshness or availability.

**Checkpoint:** Section 15.14/V10 remains partial. Next: remaining toolkit data/inference/tail/model-report/readiness assumption crosswalk and project-deliverable disposition, preserving earlier arithmetic/lab evidence. F32 remains OPEN: this four-section fixture does not establish book-wide shared-input integration, upstream parsing/context/time alignment or installed consumer contracts. F28 notebook/platform, F209/F165/F185, resource/model/data/platform/release/independent/canonical acceptance remain open. No production/data/reviewer acceptance.
