# Project contracts and scoped review records

These records are separate from eight local exercises, sixteen existing methods and eighteen QA predicates. They are a manual trace of responsibilities, not independent acceptance.

| Architecture responsibility | Scoped verification |
|---|---|
| validate_grid | Original tests cover uniqueness, hourly incompatibility, ordering, baseline and 24-hour expected schedule; grid supplied independently. |
| load_prices | Exact CSV bytes hashed; original parser/domain tests executed; extra identical-duplicate and row-reversal probes retained. |
| analyze | Every aligned value and adjacent ratio reconciled independently; all linked values and endpoint-only summaries checked; input-copy tests executed. |
| build_dashboard | Exact artist data and histogram counts checked; PNG inspected for gaps, sample counts, units and pair selection. |
| run | Fresh output directory, six output hashes and evidence-last behavior checked. Simulated export failure and existing-directory rejection exercised. |

| Deliverable | Scoped result and limit |
|---|---|
| dashboard.png | Generated and inspected; its hash belongs to that exact run. Regeneration can change image bytes. |
| dashboard.svg | Generated and hashed; original suite parses SVG. No separate SVG visual inspection. |
| aligned_prices.csv | Retained; eleven observed values over twelve slots. |
| adjacent_returns.csv | Retained; baseline undefined, ALPHA gaps preserved, final zero genuine. |
| strict_linked_returns.csv | Retained; ALPHA does not restart, BETA completes. |
| complete_return_pairs.csv | Retained; Jan 2, Jan 3 and Jan 6 only. |
| evidence.json | Retained; source/code hashes, versions, coverage, outputs and null withheld result checked. No authenticity guarantee. |

The seven stated learning objectives are covered through input validation, independent grid alignment, no-fill arithmetic, shared-result artists, numerical audit reconciliation, exact hash checks and the written separation of automated, visual and financial-data scope. Remaining real-data, accessibility, platform/notebook and independent review obligations are not credited as passed.
