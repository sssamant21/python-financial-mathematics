# Section 20.3 quadratic-form and feasibility range

Date: 2026-11-05. Baseline: `5f5ab519941f85d7e6b062c227757bc3793f8fcf`. Corrected executable pin: `c8110de2a09da05fca5591c5a70c0d9278f51df4`.

Section 20.3 evaluates the complete quadratic form in rational arithmetic after converting valid inputs to their represented float values. Rounding occurs once, at the final scalar. Finite results survive cancellation or scaling even when a separate term or coefficient sum would overflow. Exact zero is valid; nonzero results rounding to zero and final overflow raise ValueError. This evaluates a raw form, with no symmetry or PSD test.

Portfolio feasibility compares the exact represented weight sum with one and the represented tolerance. The long-only lower bound is unchanged. A large sum outside the permitted interval returns false, without requiring the sum to fit in a float. At zero tolerance, decimal-looking weights need not add to one as represented floats. The tolerance applies to both the individual lower bounds and the budget gap; it is not an economic allocation approval.

The quadratic oracle uses 4,000-digit Decimal row products, then a dot product, for the selected fixtures. The feasibility oracle puts represented weights and tolerance on a common integer scale and checks an integer interval. Cases include signed/nonsymmetric matrices, cancellation, intermediate overflow with a finite result, final range rejection, subnormal and adjacent tolerance boundaries, and large gross weights. The checker also verifies two actual assessment fields and observes both helper calls.

The initial run failed 12 of 36 cases; the corrected run passed all 36. Chapter scope: 28 files compiled and 17 scripts passed, with all source hashes matching before and after.

[Raw failures, reruns and scoped hashes](chapter-20-invariant-matrix-range-followup.json) · [Runnable checker](../chapter-20/code/check_invariant_matrix_range.py).

Replay from Book 02's chapter-20/code directory at the corrected pin with python check_invariant_matrix_range.py, assertions enabled. For the initial run save the checker externally, check out the baseline and overlay only that checker. For chapter scope compile each .py with py_compile.compile(path,doraise=True), then execute each check_/test_ script in its parent directory in a fresh Python process with a 60-second timeout. Compare Git blob SHA-1 values before and after; successful stdout is omitted from the scoped summary.

COV-87 remains partially addressed; 32 selected COV categories remain partial and none closed. Case failures are not a defect total or completion percentage. Selected assistant-run numerical and runtime evidence only; no independent review, supported-platform validation, release acceptance or canonical approval.
