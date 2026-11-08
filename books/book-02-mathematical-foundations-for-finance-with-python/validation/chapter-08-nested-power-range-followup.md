# Section 8.4 nested-power derivative follow-up

Baseline `768cafb968d261c3c801f8e8d5af71d7f2c5feca`, original Section 8.4 blob `269a5196af7f37d5bd998a717c5baddaba04db8a`. Corrected executable tree `76208b8f944cf6ab706ae75f94cc0329d1f3dbfe`. [Exact dependencies, full observations and replay](chapter-08-nested-power-range-followup.json).

**45 checks pass**, with seventeen baseline mismatches and a byte-identical baseline replay. Six mismatches returned signed infinities at unrepresentable outputs; eleven are finite rounding differences reconciled under the now explicit complete-expression contract. They are not seventeen distinct defects or claims that a prior one-final-rounding specification existed.

The independent oracle expands 24x(3x²+2)³ into 648x⁷+1296x⁵+864x³+192x and evaluates each monomial exactly as a Fraction before output rounding. Production instead retains the factored rational expression. This avoids reproducing the implementation's intermediate calculation order.

Positive polynomial coefficients make the function strictly increasing for nonnegative x. An oracle-only binary search of ordered positive binary64 bit patterns finds last finite input **4.3125521996301313e43** and first overflow input **4.312552199630132e43**, exactly one bit-pattern step apart. Neither boundary was selected by inspecting production output. The corpus tests these and the preceding float on both signs, twelve seeded magnitude-varied values, ordinary/large inputs, signed zeros, minimum subnormals, minimum normals and six invalid-input observations.

The source normalizes input as before, preserves signed zero, evaluates the complete factored expression exactly and rounds once. Unrepresentable final output raises OverflowError consistently with the pre-existing large-power error convention; infinity is not returned. Since the polynomial degree and normalized binary64 input size are fixed, this helper does not introduce the unbounded-degree resource question of a general polynomial evaluator.

Run `python check_nested_power_range.py` from `chapter-08/code`. For baseline replay retrieve the original Section 8.4 source at the baseline revision into a separate directory and pass that directory as the corrected checker's sole argument. Requested source existence is enforced; Section 8.1 remains the unchanged pinned dependency. Original source hash verified. Baseline/replay exit 1 with byte-identical JSON; corrected run, existing Section 8.4 checks and the 78-case large-count suite exit 0. No checker correction was needed in this batch.

[V-110 full runtime](runtime-refresh-2026-11-07-r16.md). Next: [price/log-growth baseline](chapter-08-price-log-growth-baseline.md). COV-51 remains partial; thirty-five selected categories remain partial, none closed. Independent reviewer, supported-platform, release and canonical approval remain pending.
