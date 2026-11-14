# V-142 — Full pinned candidate Linux runtime refresh

Executable source revision `a847812cb63d75354199723e5489cd84a579988d`. All **601 Python files compiled**,all **388 check/test scripts passed**,and all **602 required source/fixture blobs matched before and after execution**. Python3.12.14,Linux-6.18.57-x86_64-with-glibc2.41;assertions enabled,60-second per-script timeout. Counts derive from this pinned tree.

[Per-file results and exact manifest](runtime-refresh-2026-11-14-r3.json) · [Runnable exact-source staging runner](runtime-refresh-2026-11-14-r3-runner.txt).

```sh
python books/book-02-mathematical-foundations-for-finance-with-python/validation/runtime-refresh-2026-11-14-r3-runner.txt . a847812cb63d75354199723e5489cd84a579988d books/book-02-mathematical-foundations-for-finance-with-python/validation
```

The runner stages every required Git source/fixture blob into an isolated temporary tree,verifies it,compiles Python sources,runs each check_/test_ script separately from its directory with assertions enabled,and verifies input hashes again. The required non-Python fixture is chapter-01/data/section-1.14-cases.json. Actual exits,per-script timings,successful stdout digests and stderr are retained;failed stdout would be retained if present. No failures occurred in this full run. Elapsed time218.7seconds.

Includes V-141's complete financial factory/input/domain changes and new independent factory checker,with V-139 report and legacy checks retained. [Initial factory mismatches and exact replay](chapter-08-factory-followup.md) remain separate from corrected runtime results. V-140 at its earlier revision remains historical600/387/601 evidence. Final publication verifies all602 tested inputs against the resulting tree;metadata/report pins do not alter executable inputs. Book1's pipeline source/fixtures/lab/answer evidence has separate counts and limits.

One candidate Linux run does not establish independent mathematical/editorial review,supported-platform validation,release acceptance or canonical approval. Thirty-five selected COV categories remain partial;none closed. Next:Section8.9 step-ladder/report resource and late-input-failure contracts,then Chapter8 assessment alignment. Broader branch/conditioning/noise and independent acceptance remain open.
