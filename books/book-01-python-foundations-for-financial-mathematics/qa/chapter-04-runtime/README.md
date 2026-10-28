# Chapter 4 — Reference runtime evidence reconciliation

**Date:** 2026-10-27. **Reviewer / execution owner:** Codex. **Source:** Book 1 baseline `f429fb81b8d8f7d228100333c76019d583200d64`. Chapter 4 manuscript and companion files were unchanged through `0e4ec168f56e155bd1c6bdcd2531b5b40890c3df`; GitHub comparison returned no changed Book 1 Chapter 4 paths. Per-file SHA-256 values are retained in [results.json](results.json).

## Scoped result

PASS: 101 reference unittest methods across fourteen suites, with no skips, failures or errors. The holdings-manager demonstration and all fourteen extracted-directory compilation checks also passed. No manuscript corrections were required.

| Material | Passing methods |
|---|---:|
| Sections 4.1–4.6 | 6 each, 36 total |
| Sections 4.7–4.12 | 7 each, 42 total |
| Section 4.13 project | 10 |
| Section 4.14 companion | 13 |
| **Total** | **101** |

The companion contains answers to twenty exercises and thirteen executable reference test methods. Conceptual answers are not counted as automatically graded by those methods. The chapter's canonical labels remain publication-history claims rather than independent acceptance under the validation tracker.

## Environment and reproduction

Python 3.12.14 on Linux x86_64 with glibc 2.39. The extracted reference code uses the Python standard library.

From the repository root, choose a new output directory:

```sh
python books/book-01-python-foundations-for-financial-mathematics/qa/chapter-04-runtime/run_reference_checks.py books/book-01-python-foundations-for-financial-mathematics/chapter-04 /tmp/chapter04-repro
```

The [runner](run_reference_checks.py) extracts complete unittest blocks without modifying them and places each in a separate directory. It supplies the complete Section 4.13 project module to the companion as documented. Each suite runs via `python -W error::FutureWarning -m unittest -v MODULE`; the actual count must match the test methods found in that complete listing, the unittest report must say OK, and skips are rejected. The project demonstration runs separately and compilation uses `python -m compileall -q .`. Detailed commands, exit codes, counts, source hashes and supporting-module identity are retained in [results.json](results.json); [all-checks.log](all-checks.log) contains the complete test, demonstration and compilation output.

The holdings-manager demonstration reported:

```text
PASS: active report contains SEC-A and SEC-C; S0 baseline preserved
```

The demonstration's assertions completed successfully. This reproduces the documented synthetic scenario; it does not establish persistent transaction safety or live portfolio correctness.

## Historical claims and remaining scope

The current runs reproduce the reference suite and project demonstration counts recorded in the manuscripts. Earlier mypy 2.4.0 strict-check claims were not reproduced: mypy is not installed in the current interpreter. That historical static-analysis claim remains separate from this runtime and compilation pass.

Short illustrative fragments, every optional exercise, conceptual answers, Windows/macOS commands, numerical range guarantees, independent financial derivations and broader editorial/source review were not validated by this run. Comprehensive acceptance remains pending.

**Next action:** Chapter 3 runtime evidence reconciliation.
