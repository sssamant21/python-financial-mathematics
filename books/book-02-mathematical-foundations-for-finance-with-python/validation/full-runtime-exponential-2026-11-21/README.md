# V-230 — Full pinned Book2 runtime refresh

Executable source pin: `278fe361a26394ce4d2c5d1e1955d804994e150a`. [Runnable review](review.txt), [actual execution](runtime.json), [verification](verification.json).

```bash
python books/book-02-mathematical-foundations-for-finance-with-python/validation/full-runtime-exponential-2026-11-21/review.txt /absolute/repository/path 278fe361a26394ce4d2c5d1e1955d804994e150a /absolute/evidence/output
```

Fresh inventory from the pinned tree: **642 Python files compile, 429 check/test scripts pass, 643 required Python/fixture blobs verify before and after execution**. The fixture is chapter-01/data/section-1.14-cases.json. Assertions are enabled. Per-script exit status, stdout, stderr, timings and exact Git blob identities are retained. The runner extracts only the required pinned blobs into a temporary tree; it does not execute an unpinned working copy. Total recorded runtime is 451.299 seconds.

This refresh includes the accumulated Section10.2 polynomial, midpoint and exponential source/checker corrections. Earlier baseline failures, explicit support extensions, grid policies and observer corrections remain retained at their original scopes. A passing checker is not an independent mathematical reviewer or a guarantee of every numerical/resource contract. The review .txt artifacts do not add Python files or check/test-script counts.

Next: **10.3 fundamental theorem of calculus lab/source crosswalk**. The scoped10.2 runtime progression gate is met; independent mathematical/editorial, supported-platform, model, resource, release and canonical acceptance remain open. All38 selected COV categories remain partial, none closed; these are not defect counts or completion percentages. Book2 is not complete. Book1 has separate trackers and next18.15.
