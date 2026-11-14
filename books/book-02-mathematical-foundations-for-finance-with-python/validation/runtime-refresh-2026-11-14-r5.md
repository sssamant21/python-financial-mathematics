# V-150 — Full pinned candidate Linux refresh

Executable source revision:`23d3517e5720e8e7ef541f420cf24412c19c5d8b`. [Actual per-file outcomes and607-input manifest](runtime-refresh-2026-11-14-r5.json),[runnable staging/execution runner](runtime-refresh-2026-11-14-r5-runner.txt).

```sh
python books/book-02-mathematical-foundations-for-finance-with-python/validation/runtime-refresh-2026-11-14-r5-runner.txt . 23d3517e5720e8e7ef541f420cf24412c19c5d8b books/book-02-mathematical-foundations-for-finance-with-python/validation
```

606/606 Python files compiled;393/393 check/test scripts exited zero. All607 required Python/fixture Git blob hashes verified at staging and after execution. Assertions enabled;60-second per-script timeout. Python3.12.14,Linux-6.18.57-x86_64-with-glibc2.41;elapsed260.5s. Counts derive from this pinned tree.

The [initial full attempt](runtime-refresh-2026-11-14-r5-initial.json) at2ee70e207d55c70306860378c29bc0bf331ea834 compiled606 files,passed392/393 scripts and verified607 hashes before/after. Its one failed checker had two assertions requiring rejection of an unrepresentable float h². The complete sampled quotients are exactly0 for those fixtures;[retained initial/corrected method output and rationale](chapter-08-assessment-centered-followup.md) document the precise expectation reconciliation without tolerance relaxation. The same five historical methods pass after correction. A separate staging-harness missing dependency was corrected and is not counted as a source defect.

Includes V-148 complete PV/shock facade and V-149 centered-copy source/checker changes. Earlier initial failures/replays,oracle corrections and scoped numerical expectations remain distinct. A full exit-zero run is not every mathematical/model/coverage contract or supported-platform acceptance. Thirty-five selected COV categories remain partial,none closed. Independent mathematical/editorial review,release and canonical approval remain pending.

Next:Section8.10 chapter-report full field/serialization/validation-order coverage against the existing assessment mapping. Book1 uses independent trackers.
