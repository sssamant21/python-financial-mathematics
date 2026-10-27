# Book 02 — Initial inventory and runtime check

**Status:** Initial automated pass; failures unresolved. Independent mathematical and editorial review pending.

- Source revision: `a20484672beae64e7c61037af0b11baba2fd7e54`.
- Environment: Python 3.12.14, Linux runtime.
- Inventory: 215 numbered manuscript files across 21 chapters (15 in Chapter 01; 10 in each remaining chapter); 427 Python files.
- Compilation: 427/427 Python files compiled.
- Runtime: 210/216 files named check* or test* exited successfully; six exited nonzero. One chapter-level check invokes section checks, so these counts are script executions, not independent tests or section certification.
- Each script was invoked with the current Python executable from its own directory, with a 15-second timeout. Source files and the Chapter 01 JSON fixture were obtained at the stated revision. The two fixture-dependent checks were rerun after the fixture was included.

## Nonzero checks

| Check | Observed failure | Follow-up |
|---|---|---|
| chapter-08/code/check_section_8_10.py | Centered second derivative 262818.32163112995 versus 262817.77409400605 exceeds stated tolerance | Assess finite-difference truncation and threshold against the analytic result. |
| chapter-10/code/check_section_10_07.py | Boolean interval count raises ValueError; check expects TypeError | Reconcile public contract, implementation and check. |
| chapter-11/code/check_section_11_05.py | Angle for positively rescaled vector is about 1.2074e-6 degrees rather than zero within test tolerance | Assess angle calculation and justified absolute tolerance. |
| chapter-16/code/check_section_16_07.py | Not every run meets the expected gradient-tolerance status | Inspect optimization traces, stopping criterion and iteration budget. |
| chapter-18/code/check_section_18_02.py | Assertion expects naive sum to equal zero in this runtime | Examine Python-version summation behavior and choose an explicitly specified summation method. |
| chapter-20/code/check_section_20_05.py | Two sum-rule boundary checks fail | Investigate rounding in the scaled comparison; preserve the stated comparison contract. |

These observations do not identify root causes definitively. No fixes or tolerance changes are claimed in this pass. Exit code zero alone does not prove a script exercised adequate assertions, and compilation does not establish correctness.

## Pending

- Investigate and resolve failures with independent expected results, then rerun affected checks and integration checks.
- Audit test coverage, dependencies, manuscript links, formulas, companion solutions and index consistency.
- Complete independent mathematical, editorial, source and copyright review.
- Record final book-wide validation against the resulting exact revision.

No canonical or production approval is implied.
