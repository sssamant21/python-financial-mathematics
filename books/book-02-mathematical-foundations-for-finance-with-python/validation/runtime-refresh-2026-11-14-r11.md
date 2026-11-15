# V-163 — Full pinned candidate Linux refresh

Executable source revision: `067c4205c8339341e1f76352f60fdf4fd2615b78`. [Actual per-file outcomes and614-input manifest](runtime-refresh-2026-11-14-r11.json),[runnable staging/execution runner](runtime-refresh-2026-11-14-r11-runner.txt).

```sh
python books/book-02-mathematical-foundations-for-finance-with-python/validation/runtime-refresh-2026-11-14-r11-runner.txt . 067c4205c8339341e1f76352f60fdf4fd2615b78 books/book-02-mathematical-foundations-for-finance-with-python/validation
```

613/613 Python files compiled;400/400 check/test scripts exited zero. All614 required Python/fixture Git blob hashes verified during staging and after execution. Assertions enabled;60-second per-script timeout. Python3.12.14,Linux-6.18.57-x86_64-with-glibc2.41;elapsed249.8s. Counts derive from the pinned tree.

Includes V-162 complete affine/generic-report source/checker changes. [39 initial failed predicates/replay,one first-correction signed-zero failure/replay and125 final corrected predicates](chapter-09-affine-report-followup.md) remain separate from this full script pass. Exact first-correction source and later two-probe scoped dispositions retained;historical initial/replay records unchanged.

[Actual post-affine diagnostics](chapter-09-taylor-after-affine-replay.json),[runner](chapter-09-taylor-after-affine-probes.txt) confirm affine rescue−1e308 and callback-preflight rejection;the discounted-value rescue still raises OverflowError despite finite independent expectation2.233994766161711. That case remains OPEN;it is not settled by a full exit-zero script run. Discounted/shock/ladder/revenue functions were unchanged by this batch. No claim of analytic Taylor error bounds,domain discovery,smoothness or callback side-effect safety.

All36 selected COV categories remain partial,none closed. One candidate Linux runtime;independent mathematical/editorial/platform/release/canonical acceptance pending. Next:Section9.3 discounted value/shock/error-report numerical contracts,resuming the saved finite-value rescue failure,then ladder/revenue contracts. Book1 uses independent trackers;F28/F32/F209 and broader limits remain open.
