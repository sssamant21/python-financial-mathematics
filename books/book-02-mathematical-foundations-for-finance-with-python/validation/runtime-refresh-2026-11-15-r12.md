# V-187 — Full pinned Book 2 candidate Linux runtime

Source revision: `39ebd9690c5c5b3d946ffd6141b7165b0b8e9388`. The inventory comes from that exact Git tree. All **625 Python files compiled**, all **412 check/test scripts exited zero**, and all **626 required Python/fixture blobs matched before and after execution**. Assertions were enabled, with a 60-second timeout per checker. Python 3.12.14; platform `Linux-6.18.57-x86_64-with-glibc2.41`. Elapsed time: 412.9 seconds.

The [staging runner](runtime-refresh-2026-11-15-r12-runner.txt) and [full manifest with per-file results](runtime-refresh-2026-11-15-r12.json) are retained. Run from the repository root:

```bash
python books/book-02-mathematical-foundations-for-finance-with-python/validation/runtime-refresh-2026-11-15-r12-runner.txt . 39ebd9690c5c5b3d946ffd6141b7165b0b8e9388 books/book-02-mathematical-foundations-for-finance-with-python/validation
```

This stages pinned Git blobs rather than working files. It includes the [V-186 parallel-report scope](chapter-09-parallel-report-followup.md): 112 passing source predicates, with 17 initial predicate failures and actual replay retained. Twelve failed fields came from two rejected reports; five concerned latent error fields. These are not 17 unique defects.

The existing full-baseline prerequisite remains a documented design/range restriction, including eligibility of unused per-cash derivative fields. Only the parallel function changed; spot functions did not. The [three fresh spot diagnostics](chapter-09-spot-resume-r12-initial.json) remain open and are not passing parallel predicates. Passing the full existing script set does not resolve those unasserted contracts.

Next: complete spot-curve contracts, then spot-shock reports and prerequisites. All 37 selected COV categories remain partial, none closed. This is one candidate Linux run, not universal numerical/resource correctness, supported-platform validation, model/release acceptance or independent mathematical/editorial/canonical approval. Book 1 is tracked separately.
