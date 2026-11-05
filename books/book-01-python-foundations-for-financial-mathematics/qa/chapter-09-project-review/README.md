# Section 9.16 — Project review checkpoint

**Date:** 2026-11-05. **Baseline:** `6a393b6bb977938709ec0bd555c305b0d9d54414`. **Source Git blob:** `7e70580b8b7ad7b3bac06b9192c31be961e1d32d`. Source: [9.16 project](../../chapter-09/9.16-chapter-project-time-value-of-money-engine.md).

**Status: STATIC REVIEW SCOPED; PYTHON EXECUTION BLOCKED.** The execution service returned “No usable execution environment is available. Wait for an environment to become available before using this tool.” No shell command, Python test, compilation or platform check ran in this checkpoint. Historical Chapter 9 runtime evidence is separate and does not execute this new runner.

Completed: eight local prompt/answer alignment records, twelve acceptance-gate mappings, project prerequisite/evidence contracts, and supplemental exact-rational JavaScript benchmarks. Seven JavaScript benchmark predicates passed in the code orchestration runtime. These checks do not execute, translate or certify the Python engine. The manuscript is unchanged. Fifteen previously completed Chapter 9 workflows and eighty earlier local prompts retain their recorded scope; this adds eight **static** local records, not an executed sixteenth workflow.

- [Answer review](ANSWERS.md)
- [Contracts and candidate defects](CONTRACTS.md)
- [Executed supplemental rational benchmarks](benchmarks.json), with [reproducible JavaScript](benchmarks.js)
- [Prepared Python runner](review.py) — not executed or Python-compiled here
- [Machine-readable checkpoint](checkpoint.json)

The source has one complete Python listing and twelve named unittest methods, established by source-text inspection only. The runnable minimum needs only tvm_engine.py and a standard-library Python interpreter; the example CSV file is optional because the demonstration parses an inline string. There is no implemented --input/--output CLI. The illustrated evidence directory is not created by the source. The PowerShell redirection combines test diagnostics and JSON, so acceptance-output.txt is a transcript rather than a standalone JSON document.

## Resume without duplication

1. Restore an available Python execution environment; refresh main and reread both trackers before making changes.
2. Run the prepared review.py against the unchanged baseline source first. Its output goes to a new runs/<UTC>-<uuid>/ directory so failures and subsequent corrected reruns remain separate. It executes both documented POSIX-compatible commands, records raw stdout/stderr, checks the twelve existing methods, and probes the source functions against independent rational/Decimal expectations.
3. Inspect any failures, including runner errors. Candidate issues below are not runtime-confirmed; do not count their proposed assertions as passing evidence. Fix substantiated defects, add regression cases within existing source methods where appropriate, and rerun into another retained directory.
4. Record actual environment, source/listing hashes, commands, predicate totals and disposition. Publish an atomic expected-head update after comparing fresh main. Only then advance the completed workflow count or runtime queue to Section 9.17.
5. Preserve this checkpoint, all initial failures and F28/F32/platform/independent-acceptance gaps. Do not repeat the static eight-answer review unless the source changes.

From repository root:

```bash
python3 -B books/book-01-python-foundations-for-financial-mathematics/qa/chapter-09-project-review/review.py
```

The runner's --source option accepts an explicit baseline manuscript path. It never fetches code or edits the manuscript. Generated JSON is event-level local synthetic evidence, not independent financial acceptance. Source changes require affected checks to be rerun. Notebook, Windows/PowerShell, fresh-install, resource-limit, day-count and production/security acceptance remain outside this checkpoint.
