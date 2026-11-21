# V10 — Installed price validation and caller model boundary

Pin: `c13faeefbb83044100436a01e6190c3439018743`. [Offline review](review.py), [isolated probe](probe.py), [first](first.json), [replay](replay.json), [commands](commands.json), [source/artifact manifest](artifact-manifest.json).

```bash
python books/book-01-python-foundations-for-financial-mathematics/qa/v10-validation-model-boundary/review.py
```

Seven new offline commands build the exact scaffold through21.13, install a wheel into a clean consumer and run two isolated probes outside hidden source with `-I`. Installed validation/simulation/statistics hashes match exact source fences and selected prior corrected validation scaffold hashes. Build tooling uses preprovisioned system packages; consumer is clean. No index/dependency download, global install, financial source change or binary artifact publication occurs. Source/wheel/member hashes retained; no reproducible-byte or release approval.

Both probes pass **22 predicates** identically: nine native price-validation/ownership/guard checks, twelve native-model-parameter/observed-statistic fields across two explicit caller choices, and one caller model-mean distinction. Arithmetic comparisons use rtol5e-13/atol0; strings and decisions exact. Independent summary expectations use actual observed75/125 counts and exact centered squares, not the source summary outputs.

The fictional price pair100→125 is one day apart and eligible by the supplied decision cutoff, with matching instrument/currency but different source labels (permitted by the published contract). Its realized return is.25. Changing only the source label leaves the numerical return eligible; labels are not authenticated. Future availability or instrument/currency mismatch is rejected. Caller dictionaries remain unchanged.

The same eligible data is retained alongside hypothetical one-period models with returns+.25/−.25 and caller-chosen p=.25 or.75. Exact model means are87.5 and112.5. Native sampled values/summary are checked against their realized counts, not required to equal those model means. This does not infer one-period predictive returns, horizon, measure or independence from the one-day observation. There is **no native price-to-probability/return calibration adapter**; no adapter is invented or claimed tested. The choices are clearly labeled hypothetical, not a market or risk-neutral model.

Two separate conceptual dispositions are retained: price eligibility does not authenticate source/adjustment/revision/model suitability, and ScenarioResult does not durably carry instrument/currency/source/decision-cutoff/horizon/measure provenance. The external evidence JSON retains that fictional context; it is not a new native durable-audit feature or accepted calibration. These dispositions are not additional executable predicates.

No source failure occurred in this new batch. Earlier F214 failures/corrected reruns,401 installed predicates,122 methods,40 answers and12 lab records retain their original scope and are not rerun/recounted. This checkpoint executes no unittest suite. Prior grid/small-value SD/SE limitations remain open.

Next:21.13 revision-history, adjustment/source-basis and freshness boundaries, keeping any caller scenario conversion distinct from native validation and model approval. V10/Book1, F28/F32/F209/F165/F185 and broader numerical/resource/data/model/platform/release/independent/canonical acceptance remain open.
