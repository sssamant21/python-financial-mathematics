# V-140 — Full pinned candidate Linux runtime refresh

Executable source revision `c0afbc3ae3367b263bc0aacef202bb4a80495f50`. All **600 Python files compiled**,all **387 check/test scripts passed**,and all **601 required source/fixture blobs matched before and after execution**. Python3.12.14,Linux-6.18.57-x86_64-with-glibc2.41;assertions enabled,60-second per-script timeout. Counts derive from this pinned tree.

[Per-file results and exact manifest](runtime-refresh-2026-11-14-r2.json) · [Runnable exact-source staging runner](runtime-refresh-2026-11-14-r2-runner.txt).

```sh
python books/book-02-mathematical-foundations-for-finance-with-python/validation/runtime-refresh-2026-11-14-r2-runner.txt . c0afbc3ae3367b263bc0aacef202bb4a80495f50 books/book-02-mathematical-foundations-for-finance-with-python/validation
```

The runner stages exact Git source/fixture blobs into a temporary tree,verifies them,compiles each Python file,runs every check_/test_ script separately from its directory with assertions enabled,and verifies all input hashes again. The non-Python required fixture is chapter-01/data/section-1.14-cases.json. Results retain actual exits,per-script timings,successful stdout digests and stderr;failed stdout would be retained if present. No failures occurred in this full run. Elapsed time352.1seconds.

This refresh includes V-137 noise diagnostics,V-138 bounded sweep checker and V-139 comparator complete-quotient/exact-tolerance changes. [Initial comparator failures,replays and scoped results](chapter-08-comparator-followup.md) remain separate;V-137's10 nominal accuracy exceedances are not converted to passes by this runtime run. V-136's597/384/598 remains historical full evidence at its earlier revision. Final publication verifies these601 input blobs against the published tree;metadata/report updates do not change executable inputs.

This is one candidate Linux execution,not independent mathematical/editorial review,supported-platform validation,release acceptance or canonical approval. Thirty-five selected COV categories remain partially addressed;none closed. Book1 workflow/answer evidence and counts remain separate.

Next substantive item:Section8.9 financial model-factory complete-range/domain and report serialization/input-resource contracts. Broader branch/conditioning/noise and independent acceptance obligations remain open.
