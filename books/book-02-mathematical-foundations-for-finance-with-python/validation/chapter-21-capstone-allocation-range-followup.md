# Section 21.6 — Capstone allocation range follow-up

- Baseline: `4c9d4825d2debbc4f3bebf74232d901f5486471b`; the new checker alone was overlaid. 20 cases, 7 mismatches, exit 1.
- Corrected executable revision: `bc29b0d67dfd61b3d522d36d956b768101fee0ab`; 20 cases passed, exit 0.
- [Runnable checker](../chapter-21/code/check_capstone_allocation_range.py) · [Corrected lab](../chapter-21/code/section_21_06.py) · [Recorded expectations, observations, exits, initial failure and blob manifests](chapter-21-capstone-allocation-range-followup.json) · [Full run V-77](runtime-refresh-2026-11-05-r19.md)

Baseline mismatches: `equal_large`, `equal_negative_large`, `small_second_weight`, `sum_recovers_subnormal`, `positive_tolerance_rounding`, `negative_tolerance_rounding`, `integrated_allocation`.

The reference projects onto the budget line by shifting both coordinates equally in a 2,500-digit Decimal context, then selects the nearest endpoint when needed. The lab clips an exact rational stationary point and rounds each weight separately. The checker evaluates the complete objective and tests feasibility on the represented weights, including a diagnostic rounded to the tolerance that still fails the exact comparison. It also checks a positive subnormal objective recovered only when the squares are summed before rounding.

The checker exercises the actual `build_report()` allocation field, verifies the linked callable, and confirms the synthetic report's validation, independent review and approval placeholders are unchanged. Replay from the book root with `python chapter-21/code/check_capstone_allocation_range.py` and assertions enabled. To replay baseline, use a clean checkout of the baseline and copy only that checker from the corrected revision into the indicated path. The logs include a hash-verified replay of the initial result.

This is selected binary64 evidence for the teaching interface and partial COV-90. It does not establish a general solver guarantee, independent mathematical review, supported-platform acceptance or release approval.
