# Section 21.5 — Capstone replication range follow-up

- Baseline: `4c9d4825d2debbc4f3bebf74232d901f5486471b`; the new checker alone was overlaid. 14 cases, 5 mismatches, exit 1.
- Corrected executable revision: `bc29b0d67dfd61b3d522d36d956b768101fee0ab`; 14 cases passed, exit 0.
- [Runnable checker](../chapter-21/code/check_capstone_replication_range.py) · [Corrected lab](../chapter-21/code/section_21_05.py) · [Recorded expectations, observations, exits, initial failure and blob manifests](chapter-21-capstone-replication-range-followup.json) · [Full run V-77](runtime-refresh-2026-11-05-r19.md)

Baseline mismatches: `screen_rounded_zero`, `near_dependence`, `large_canceling_products`, `exact_rounded_residual`, `scaled_target_overflow`.

The reference uses exact pivoted elimination on the represented coefficients, then evaluates dot products on the returned rounded holdings. The lab uses a two-by-two direct formula. The exact normalized determinant determines the inclusive screening boundary; its rounded display can be zero even when the zero-threshold screen accepts. The checker distinguishes threshold rejection, exact singularity, and genuine holding overflow. It also checks finite residuals whose intermediate float products overflow.

The checker exercises the actual `build_report()` replication field, verifies the linked callable, and confirms the synthetic report's validation, independent review and approval placeholders are unchanged. Replay from the book root with `python chapter-21/code/check_capstone_replication_range.py` and assertions enabled. To replay baseline, use a clean checkout of the baseline and copy only that checker from the corrected revision into the indicated path. The logs include a hash-verified replay of the initial result.

This is selected binary64 evidence for the teaching interface and partial COV-90. It does not establish a general solver guarantee, independent mathematical review, supported-platform acceptance or release approval.
