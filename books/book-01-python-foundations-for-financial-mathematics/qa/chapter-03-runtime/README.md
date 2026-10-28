# Chapter 3 — Reference runtime evidence reconciliation

**Date:** 2026-10-27. **Reviewer / execution owner:** Codex. **Source:** Book 1 baseline `f429fb81b8d8f7d228100333c76019d583200d64`. Chapter 3 manuscript and companion files were unchanged through `dd3b9ea2931a37f0ab541f12fcf31b41eb8af693`; GitHub comparison returned no changed Book 1 Chapter 3 paths. [results.json](results.json) retains per-file SHA-256 values, supporting-module identities, selected block indices, commands and exit codes.

## Scoped result

PASS: 31 unittest methods, 21 doctest examples, nine standalone assertion-based labs, three selected snippet groups, the function-library demonstration and fifteen extracted-directory compilation checks. No skips or execution failures were reported. No manuscript corrections were needed.

| Material | Scope executed | Result |
|---|---|---|
| 3.1 | Python blocks 0 and 3, combined | Executed; existing invariant assertions passed |
| 3.2 | Worked-example and scenario blocks 22 and 23, combined | Executed; output retained |
| 3.3 | Definition and valid-call blocks 0 and 1, combined | Executed; no separate unit-test count |
| 3.4–3.7 | Four complete hands-on labs | Passed their in-script checks |
| 3.8 | Complete documentation lab and doctest run | 5 doctest examples passed; contract checks passed |
| 3.9 | Complete valuation lab and doctest run | 4 doctest examples passed; valuation checks passed |
| 3.10 | Complete rate/factor lab and doctest run | 6 doctest examples passed; rate/factor checks passed |
| 3.11 | Complete composition lab and doctest run | 4 doctest examples passed; composition checks passed |
| 3.12 | Complete reproducibility lab and doctest run | 2 doctest examples passed; numerical-policy checks passed |
| 3.13 | Published reference suite with the Section 3.12 module | 12 unittest methods passed |
| 3.14 | Complete library, acceptance suite and demonstration | 12 unittest methods and demonstration passed |
| 3.15 companion | Published suite with the Section 3.14 library | 7 unittest methods passed |

Block indices are zero-based among Python fences in each source file. Selected fragment groups are recorded as executions, not independently counted unit tests. The standalone documentation labs also invoke their doctests; their examples are counted once using the explicit doctest reports, rather than doubling them for repeated execution. The companion's twenty exercise answers are not equated with twenty automated tests.

## Environment and reproduction

Python 3.12.14 on Linux x86_64 with glibc 2.39, using the standard library.

From the repository root, select a fresh output directory:

```sh
python books/book-01-python-foundations-for-financial-mathematics/qa/chapter-03-runtime/run_reference_checks.py books/book-01-python-foundations-for-financial-mathematics/chapter-03 /tmp/chapter03-repro
```

The [runner](run_reference_checks.py) extracts the complete labs and suites without editing their contents. For the three selected early-section groups it concatenates only the listed Python fences in order. Each source has a separate working directory. Declared dependencies are supplied locally: Section 3.12's module for 3.13, and Section 3.14's library for the companion.

Programs run with `-W error::FutureWarning`. The five documentation labs are additionally checked through `python -m doctest -v FILE`; the three suites use `python -m unittest -v MODULE`. Actual unittest and doctest counts are parsed from their output, and nonzero statuses, skips, absent test counts or failed examples cause the runner to fail. Compilation uses `python -m compileall -q .`. [all-checks.log](all-checks.log) preserves the detailed output.

The project demonstration printed:

```text
Monthly effective rate: 1.00%
Effective annual rate: 12.682503%
Future value: 1126.83
Recovered present value: 1000.00
```

## Reconciliation and limits

The recorded reference suites, doctest counts and complete lab executions were reproduced in this environment. Earlier mypy/static-type claims were not rerun. The intentionally invalid type-checking fixture and unselected illustrative fragments remain outside the runtime scope. Earlier canonical labels describe publication history, not independent acceptance by this tracker.

Passing reference checks does not independently validate all financial derivations, numerical ranges, every worked answer, platform support or source attribution. Windows/macOS instructions and comprehensive mathematical, editorial and acceptance reviews remain pending.

**Next action:** Chapter 2 runtime evidence reconciliation.
