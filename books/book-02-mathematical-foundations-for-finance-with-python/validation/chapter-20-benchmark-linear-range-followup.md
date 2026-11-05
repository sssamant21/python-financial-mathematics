# Section 20.2 two-by-two benchmark range

Date: 2026-11-05. Baseline: `c8110de2a09da05fca5591c5a70c0d9278f51df4`. Corrected executable pin: `5988dee92cf70f48f718bf8b96e0ae465d22ee42`.

The Section 20.2 2×2 benchmark forms determinants and Cramer numerators exactly over the represented float inputs, then rounds each solution component once. The determinant need not be representable as a float. Exactly singular systems reject; nonzero solution components rounding to zero and overflowing final components raise ValueError. This is a small-system reference calculation, not a conditioning assessment, general solver or recommendation to use Cramer's rule in production.

An independent exact pivoted elimination oracle checks both equations before rounding. Cases include large and subnormal diagonal systems, overflowing cross-products with a finite determinant, nearly dependent represented rows whose float products coincide, zero pivot row swaps, signed outputs, singular cases, genuine final range rejection and ordinary controls. The actual assessment solution is checked and one observed helper call verifies report integration.

The initial run failed seven of 19 cases; the corrected run passed all 19. Chapter scope: 29 files compiled and 18 scripts passed, with all source hashes matching before and after.

[Raw failures, reruns and scoped hashes](chapter-20-benchmark-linear-range-followup.json) · [Runnable checker](../chapter-20/code/check_benchmark_linear_range.py).

Replay from Book 02's chapter-20/code directory at the corrected pin with python check_benchmark_linear_range.py, assertions enabled. For the initial run save the checker externally, check out the baseline and overlay only that checker. For chapter scope compile each .py with py_compile.compile(path,doraise=True), then execute each check_/test_ script in its parent directory in a fresh Python process with a 60-second timeout. Compare Git blob SHA-1 values before and after; successful stdout is omitted from the scoped summary.

COV-87 remains partially addressed; 32 selected COV categories remain partial and none closed. Case failures are not a defect total or completion percentage. Selected assistant-run numerical and runtime evidence only; no independent review, supported-platform validation, release acceptance or canonical approval.
