# Book 02 — Chapter 1 Foundation Boundary Review

**Date:** 2026-10-28  
**Status:** Focused source review and runtime pass complete; independent review pending.

## Scope and snapshot

Reviewed the 15 Chapter 1 implementation modules, with attention to representation contracts, cash-flow schedules, exact policy boundaries and batch validation. Runtime used the 31 chapter Python files and the Section 1.14 JSON fixture from repository revision `bed04cb7f8896b6ef09074d560f1fbfe6eef68d0`, plus the new [foundation boundary checks](../chapter-01/code/check_foundation_boundaries.py). No implementation change was needed for the cases examined.

## Added checks

Five unittest methods cover minor-unit conservation and allocation spread, one-shot signed repeated-date schedules and mismatched iterator lengths, the zero-transfer fee exemption versus positive-transfer fixed fees, mixed PASS/FAIL/INVALID batch isolation and preservation of submitted input, and rejection of duplicate JSON keys, nonstandard constants and duplicate case IDs.

The initial new cash-flow test incorrectly expected exact zero using decimal-rate binary float arithmetic; it produced approximately -7.1e-15. The test was changed to exactly representable binary inputs (rate 0.25) so its exact assertion isolates schedule handling rather than float rounding. This was a test-oracle correction, not a production defect.

## Runtime evidence

Python 3.12.14 on Linux. All 32 Python files compiled using `py_compile.compile(path, doraise=True)`. Each `check*.py` script ran individually from its code directory, with captured output and a 15-second timeout.

All 17 scripts exited zero: 15 numbered section checks, the chapter aggregate check and the new boundary suite. The aggregate invokes section checks again; 17 script exits do not mean 17 independent suites. All five new unittest methods passed. The Section 1.14 checks included the pinned JSON fixture and CLI scenarios.

## Remaining work

This focused pass does not certify all derivations, exercises, attribution or editorial quality. Review numerical-range policies, input-type consistency and the pedagogical distinction between exact arithmetic and approximate comparisons independently. Final-revision validation must pin the complete agreed book snapshot and rerun the appropriate suite on supported platforms.

The reverse-order focused chapter pass has reached Chapter 1. This is a workflow milestone, not canonical approval. Broader substantive coverage, independent mathematical/editorial review and final-revision validation remain pending.
