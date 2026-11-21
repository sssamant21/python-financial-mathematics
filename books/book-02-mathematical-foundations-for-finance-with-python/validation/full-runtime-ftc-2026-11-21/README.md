# V-234 — Full pinned Book2 runtime after FTC corrections

Executable source pin: `7e98df4194191241042e19c5dba66873a8b4a852`. [Runnable review](review.txt), [actual execution](runtime.json), [verification](verification.json).

```bash
python books/book-02-mathematical-foundations-for-finance-with-python/validation/full-runtime-ftc-2026-11-21/review.txt /absolute/repository/path 7e98df4194191241042e19c5dba66873a8b4a852 /absolute/evidence/output
```

Fresh inventory: **642 Python files compile, 429 check/test scripts pass, 643 required source/fixture blobs verify before and after execution**. The single non-Python fixture is chapter-01/data/section-1.14-cases.json. Exact Git blob manifest, actual stdout/stderr, exit statuses and per-script timings are retained. Assertions are enabled; each checker has a60-second timeout. The runner extracts required pinned blobs into a temporary tree, rather than executing an unpinned working copy. Recorded total runtime: 540.422 seconds.

This includes the accumulated Section10.3 polynomial, balance/endpoint/rolling and centered-stencil corrections. The actual-rounded-span secant policy, selected complete-expression extensions, baseline failures and separate observer corrections retain their documented scopes. Passing scripts do not prove correctly rounded output across all inputs, numerical/resource/model acceptance or independent review. Review .txt files do not add Python/script counts.

Next: **10.4 substitution/integration-by-parts lab/source crosswalk**. The selected10.3 runtime progression gate is met; independent mathematical/editorial, supported-platform, provenance/model/resource, release and canonical gates remain open. All38 selected COV categories remain partial, none closed; they are not defect counts or completion percentages. Book2 remains in progress. Book1 has separate trackers.
