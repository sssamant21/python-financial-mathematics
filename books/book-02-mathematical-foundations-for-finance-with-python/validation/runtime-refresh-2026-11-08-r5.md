# V-124 — Pinned full Book 2 candidate Linux runtime

Executable source revision: `a02160a18fcb320ffb537ea5b5cf7bce8e64a3d3`.

589/589 Python sources compiled and 376/376 independently launched check/test scripts exited zero with assertions enabled. All 590 required Python/fixture Git blob hashes matched before and after execution. Python 3.12.14, Linux; elapsed 190.44 seconds. The counts derive from the pinned tree, including V-122/V-123 additions; they do not count this report runner, which is retained as text to keep the tested Python inventory unchanged.

[Raw per-file results and manifest](runtime-refresh-2026-11-08-r5.json) · [Exact runner](runtime-refresh-2026-11-08-r5-runner.txt).

Reproduce from a Git checkout containing the pinned commit:

```bash
python books/book-02-mathematical-foundations-for-finance-with-python/validation/runtime-refresh-2026-11-08-r5-runner.txt . a02160a18fcb320ffb537ea5b5cf7bce8e64a3d3 /tmp/book2-v124
```

The runner stages exact pinned blobs into an isolated temporary tree, compiles all Python sources, launches check_/test_ scripts from their own directories with a 60-second per-script timeout, and verifies input hashes afterward. It retains successful stdout digests, stderr, and full failed stdout if encountered. No failures occurred in this full run. Earlier numerical failures and corrected reruns remain in their scoped records, including [V-123](chapter-08-cash-flow-derivatives-followup.md).

This establishes execution on one candidate Linux runtime. It does not establish mathematical/editorial completeness, supported-platform coverage, independent reviewer sign-off, release acceptance or canonical approval. Thirty-five selected COV categories remain partially addressed; none closed. Next: Section 8.6 polynomial/derivative-coefficient complete-expression range/output contracts with independent exact references, then sampled-second differences. Book 1 retains its independent tracker and open findings.
