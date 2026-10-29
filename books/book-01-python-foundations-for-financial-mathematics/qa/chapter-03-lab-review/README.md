# V06 — Chapter 3 lab-step review

Date: 2026-10-29. Source baseline: `61e4e27d1d05d7aa60e8b2ca0cdba853d1e67cd3`.

**PASS (scoped): ten lab records reviewed; 34 verification records passed, zero unexpected failures.** These comprise nine standalone labs in Sections3.4–3.12 and Section3.13's testing lab. Expected negative fixtures are retained as negative results; they are not evidence that defective copies passed.

| Evidence | Scope |
|---|---|
| [Step review](STEPS.md), [register](step-register.json) | Prerequisites, exact source files, contracts, commands, expected output and interpretation for ten labs |
| [Runner](review.py), [actual results](results.json) | 25 command outcomes and nine exact stdout comparisons; source/file/code hashes and complete outputs |

All ten source lab commands passed. All nine standalone programs matched their documented direct stdout exactly. The five explicit doctest commands passed (5/4/6/4/2 examples, 21 distinct source examples counted once). Section3.13's 12-method suite passed, and its known-value method passed alone. Existing methods/examples are reruns; no historical reference-test count is increased.

The prescribed deliberate exercises were performed in temporary copies: changing a docstring Boolean expectation caused doctest failure; restoring it passed. Adding an unsupported beginning-contribution prose claim left doctests passing, illustrating why contract review must compare prose with interface and code. Replacing the Section3.12 PV division with multiplication caused the published suite's independent known-value test to fail; restoring exact source passed. The complete failure stdout/stderr is retained alongside successful restoration outputs. No defective copy was published as canonical source.

Mypy2.4.0 was installed in a separate venv. The exact typed lab passed --strict; the exact bad-call fixture returned exit1 and three expected incompatible-argument diagnostics. It was never run as a financial program. The Section3.12/3.13 implementation/test pair also passed --strict. Checker version and diagnostics are in results.json; wording/counts may change with other checker versions.

Reproduce using Python3.10+ and an isolated mypy environment: set CH3_MYPY_PYTHON to that environment's interpreter, then run `python books/book-01-python-foundations-for-financial-mathematics/qa/chapter-03-lab-review/review.py` from repository root. Actual run: CPython3.12.14, Linux x86_64. Source commands are invoked through that exact interpreter for reliable identity; Windows launcher/PowerShell and macOS commands were reviewed but not executed. No -O/-OO is used. Bytecode writing is disabled for child executions so rapid temporary mutation/restoration cannot reuse stale bytecode.

All 34 verification records passed on the first run. The instruction/contract review remains scoped: selected assertions and examples do not establish exhaustive numerical, input-domain, branch or platform coverage, financial suitability or independent reviewer acceptance. Ambient-context policy in earlier labs differs intentionally from Section3.12's fixed policy. No source correction was needed; every manuscript chapter file remains byte-identical.

Next: earlier Chapter3 section exercises and the complete Section3.14 project/definition/call/contract checklists. All 20 Section3.15 chapter-wide answers retain separate evidence. Book1 F28 notebook/platform and F32 external-input integration gaps remain open.
