# V10 — Section18.3 reproducibility and partition/draw-order crosswalk

Source `1ba1206bc29ac02dbdbc0576fd41cc953463bc52`. [Runnable exact-source review](review.py), [first run](first.json), [replay](replay.json), [prior source identity](source-identity.json), [eight assumption records](assumption-crosswalk.json). No executable source change or defect invented. All four prior listing hashes match;[F175 failures/corrections and63predicates](../chapter-18-reproducibility-review/README.md),NumPy/state/encoding observations and40answer/12lab records remain at their original scope.

**66 predicates pass in each run**:11source count checks,11independent count-to-mean arithmetic checks,11observer-restoration checks,one source-signature boundary,15draw-order observations,five caller aggregate comparisons,ten supplemental state-continuation comparisons andtwo selected interpretation checks. Each run executes the exact final demonstration/tenexistingmethods andcompileall:four formal commands/20method invocations total;no new historical methods,answers orworkflow totals.

Actual source calls are traced without changing their generator algorithm;the temporary constructor wrapper records draws and is restored in `finally`. For source `run(42,8,.6)`,up_count4 andmean100 are observed. Five chunk partitions restart the same seed for both pieces. Each chunk uses a prefix of the full sequence,and the concatenated draw mapping differs in all five designs. **4+4 reports a caller-aggregated mean105 instead of100**;2+6 and6+2 happen to match mean100 despite incorrect draw assignment. Exact Fraction90+20k/N verifies report arithmetic;this is not an independent generator-quality oracle.


| Chunk sizes | Restarted mean | Same aggregate mean? | Same draw mapping? |
|---|---:|---|---|
| 2 + 6 | 100.0 | Yes | No |
| 3 + 5 | 102.5 | No | No |
| 4 + 4 | 105.0 | No | No |
| 5 + 3 | 102.5 | No | No |
| 6 + 2 | 100.0 | Yes | No |

A separate trusted in-memory `getstate`/`setstate` caller workflow resumes at each split and reproduces the full trace/count. The native API always starts a fresh local seed and accepts no state/offset argument;the external continuation is not advertised as a source checkpoint or parallel API. State digests identify selected in-memory representations,not a portable/trusted serialization protocol. No actual parallel deployment is exercised.

The native manifest/digest and child metadata are retained. Their hash covers encoded manifest fields;it does not capture arbitrary code/data,offset/state,financial provenance or approval. Prior encoding/tolerance controls remain separate. A matching mean or seed alone does not establish replay;matching draw identities still do not prove IID or model suitability. The model expectation102 is separate from selected finite-sample mean100.

V10 remainsINPROGRESS. Next:Section18.4outcomes/model/measure andestimator-assumption crosswalk. F28/F32/F209/F165/F185 andbroaderplatform/model/release/independent/canonicalacceptance remainOPEN. Book1 notcomplete;Book2 separatelytracked.
