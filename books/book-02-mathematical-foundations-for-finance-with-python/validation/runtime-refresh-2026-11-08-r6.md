# V-127 — Full pinned Book2 candidate Linux refresh

Executable source revision `1c7aa7fb7d3fd229f77ef9d0a03584d010e9f9f2`. All591 Python sources compiled; all378 check/test scripts exited zero; all592 required Python/fixture blob hashes matched before and after execution. Python3.12.14/Linux, assertions enabled,60-second per-script timeout. These counts derive from the pinned tree, including V-125/V-126 changes/checkers and updated legacy Section8.6 domain predicates. Actual per-file records, source manifest,stderr and successful stdout digests are in [raw evidence](runtime-refresh-2026-11-08-r6.json); failure stdout would be retained, but none occurred in this full run.

```bash
python books/book-02-mathematical-foundations-for-finance-with-python/validation/runtime-refresh-2026-11-08-r6-runner.txt . 1c7aa7fb7d3fd229f77ef9d0a03584d010e9f9f2 /tmp/book2-v127
```

[Exact runner](runtime-refresh-2026-11-08-r6-runner.txt) stages pinned blobs into a temporary tree, compiles all Python files and separately launches check_/test_ files from their own directories with assertions enabled, then rechecks source/fixture hashes. The observer is retained as text, outside the tested Python inventory. Earlier [V-126 baseline/observer/legacy-regression failures and corrected reruns](chapter-08-section-06-centered-followup.md) remain separate; the full pass does not erase them.

This is one candidate Linux runtime, not a mathematical/editorial completeness claim, supported-platform validation, independent reviewer sign-off, release acceptance or canonical approval. Thirty-five selected COV categories remain partially addressed; none closed. Next: [Section8.7 eight-probe circle/break-even screen](chapter-08-section-07-circle-break-even-baseline.md) with five retained mismatches; reconcile and correct its numerical/input/output contracts, then bond/exposure/centered-copy obligations. Book1 independently advances to Chapter19 Section19.1 after its scoped Chapter18 assessment record.
