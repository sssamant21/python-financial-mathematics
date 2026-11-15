# V-165 — Full pinned candidate Linux refresh

Executable source revision: `9a00097d0669af492c85f0468cd93c2bd447100c`. [Actual per-file outcomes and615-input manifest](runtime-refresh-2026-11-15-r1.json),[runnable staging/execution runner](runtime-refresh-2026-11-15-r1-runner.txt).

```sh
python books/book-02-mathematical-foundations-for-finance-with-python/validation/runtime-refresh-2026-11-15-r1-runner.txt . 9a00097d0669af492c85f0468cd93c2bd447100c books/book-02-mathematical-foundations-for-finance-with-python/validation
```

614/614 Python files compiled;401/401 check/test scripts exited zero. All615 required Python/fixture Git blob hashes verified during staging and after execution. Assertions enabled;60-second per-script timeout. Python3.12.14,Linux-6.18.57-x86_64-with-glibc2.41;elapsed257.6s. Counts derive from the pinned tree.

Includes V-164 standalone discounted-value source/checker changes. [Eight initial failed predicates/replay and34 corrected predicates](chapter-09-discount-value-followup.md) remain separate from this full script pass. The saved standalone rescue is scoped resolved through an explicit later disposition;historical initial/replay/prior OPEN records unchanged.

[Next discounted-shock diagnostics](chapter-09-discount-shock-resume-initial.json),[identical replay](chapter-09-discount-shock-resume-replay.json),[runner](chapter-09-discount-shock-resume-probes.txt) retain three OPEN report cases:finite exact-change recovery raises OverflowError,tiny-shock relative error reports0 rather than independent1e−308,and validated zero shock produces nonfinite linear_change rather than0. These are diagnostic observations,not passing script evidence and not settled by this full exit-zero run. discount_shock text unchanged but receives the corrected baseline through discount_value. Whole shock/error/ladder/revenue numerical review remains pending.

All36 selected COV categories remain partial,none closed. One candidate Linux runtime;independent mathematical/editorial/platform/release/canonical acceptance pending. Next:Section9.3 complete discounted shock/error-report contracts,resuming the three saved cases,then step-ladder/revenue. Book1 uses independent trackers;static checker/configuration,F28/F32/F209 and broader limits remain open.
