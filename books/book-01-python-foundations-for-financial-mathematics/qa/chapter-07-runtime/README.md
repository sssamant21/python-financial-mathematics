# Chapter 7 — Reference runtime evidence reconciliation

**Date:** 2026-10-27. **Reviewer:** Codex. **Source:** Book 1 manuscript baseline `f429fb81b8d8f7d228100333c76019d583200d64`. The Chapter 7 manuscript files were unchanged through `b2bad41b584a483077fcd6a34b0644c7fb6e14eb`; GitHub comparison returned no changed Book 1 Chapter 7 paths. Per-file SHA-256 values are recorded in [results.json](results.json).

## Scoped result

PASS: 156 unittest methods across 18 suites, with no skips, failures or errors. Sections 7.1–7.17 each ran eight tests; the Section 7.18 companion solutions ran twenty tests. All 17 standalone demonstrations exited zero and all 18 extracted lab directories passed compilation. No manuscript corrections were required.

The manuscript records earlier Linux test, demonstration and compilation passes. This run reproduces those execution claims for the extracted complete listings and supplied synthetic CSV fixtures. The chapter's earlier canonical labels are publication-history claims and are not an independent acceptance decision in this tracker.

## Environment and reproduction

Python 3.12.14, Linux x86_64 with glibc 2.39, NumPy 2.3.5 and pandas 2.2.3. Tests and demonstrations ran with `-W error::FutureWarning`.

From the repository root:

```sh
python books/book-01-python-foundations-for-financial-mathematics/qa/chapter-07-runtime/run_reference_suites.py books/book-01-python-foundations-for-financial-mathematics/chapter-07 /tmp/chapter07-repro
```

The runner extracts each complete implementation and reference suite into its own lab directory, supplies the published CSV fixtures in Sections 7.5 and 7.17, and includes the project's own panel component. It does not rewrite source listings. Each suite runs via `python -W error::FutureWarning -m unittest -v test_reference`; each implementation demonstration runs in a separate process; each extracted directory is checked with `python -m compileall -q .`. The companion solution listing is executed as its unittest suite and has no separate demonstration. Detailed output is retained in [all-tests.log](all-tests.log); the JSON records each exit status.

The project demonstration reported ALPHA's complete path with linked and endpoint returns of -0.01, and BETA's incomplete path with a 0.10 endpoint return but unknown linked return. It reported zero complete aligned intervals and five source records. This matches the supplied missing-observation fixture and does not use an external market feed.

## Limits and next work

Execution of existing reference checks is not independent verification of every financial formula, worked answer, numerical limit or data contract. Short illustrative fragments, Windows setup commands, live feeds and alternative dependency versions were not tested. Comprehensive mathematical, source, platform and acceptance reviews remain pending. Continue with Chapter 6 runtime evidence reconciliation.
